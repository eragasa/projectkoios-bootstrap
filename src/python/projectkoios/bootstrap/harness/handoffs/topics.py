from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation
from projectkoios.bootstrap.harness.handoffs.evaluator import (
    HandoffEvaluator,
    PLACE_DIRECTORIES,
)
from projectkoios.bootstrap.harness.handoffs.parser import HandoffParser


_HANDOFFS_PREFIX = "docs/archive/handoffs/"


@dataclass(frozen=True)
class Message:
    message_id: str
    source_path: str
    place: str
    kind: str
    origin: str
    sender: str
    recipient: str
    acting_as: str | None = None
    delegated_operator: str | None = None
    provenance: list[str] | None = None


@dataclass(frozen=True)
class Transition:
    message_id: str
    kind: str = "created"
    source: str = "inferred"
    evidence: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SkippedFile:
    source_path: str
    reason: str


@dataclass(frozen=True)
class Topics:
    places: dict[str, list[str]]


@dataclass(frozen=True)
class GuardViolation:
    code: str
    reason: str
    message_id: str | None = None
    source_path: str | None = None


@dataclass(frozen=True)
class TopicsView:
    schema_version: str = "1.0"
    repo_root: str = ""
    generated_at: str | None = None
    messages: list[Message] = field(default_factory=list)
    transitions: list[Transition] = field(default_factory=list)
    topics: Topics | None = None
    guard_violations: list[GuardViolation] = field(default_factory=list)
    skipped: list[SkippedFile] = field(default_factory=list)


def _message_id(source_path: str) -> str:
    if source_path.startswith(_HANDOFFS_PREFIX):
        return source_path[len(_HANDOFFS_PREFIX):]
    return source_path


def _infer_place(source_path: str) -> str:
    for place_name, rel_dir in PLACE_DIRECTORIES.items():
        if source_path.startswith(rel_dir):
            return place_name
    return "unknown"


def _artifact_to_message(source_path: str, artifact) -> Message:
    return Message(
        message_id=_message_id(source_path),
        source_path=source_path,
        place=_infer_place(source_path),
        kind=artifact.kind,
        origin=artifact.origin,
        sender=artifact.sender,
        recipient=artifact.recipient,
        acting_as=artifact.acting_as,
        delegated_operator=artifact.delegated_operator,
        provenance=artifact.provenance,
    )


def _artifact_to_transition(message_id: str, source_path: str) -> Transition:
    return Transition(
        message_id=message_id,
        evidence={
            "source_path": source_path,
            "inferred_from": "file_existence_and_headers",
        },
    )


def _violation_to_guard_violation(
    violation: Violation,
    path_to_message_id: dict[str, str],
) -> GuardViolation:
    source_path = str(violation.path.as_posix())
    return GuardViolation(
        code=violation.code.value,
        reason=violation.reason,
        message_id=path_to_message_id.get(source_path),
        source_path=source_path,
    )


def build_topics_view(
    repo_root: Path,
    include_timestamp: bool = False,
) -> TopicsView:
    root = repo_root.resolve()
    parser = HandoffParser()

    messages: list[Message] = []
    transitions: list[Transition] = []
    skipped: list[SkippedFile] = []
    path_to_message_id: dict[str, str] = {}

    for place_name, rel_dir in PLACE_DIRECTORIES.items():
        dir_path = root / rel_dir
        if not dir_path.exists():
            continue
        for f in sorted(dir_path.iterdir()):
            if not f.is_file() or f.suffix != ".md":
                continue
            source_path = str(f.relative_to(root).as_posix())
            artifact = parser.parse_file(f)
            if artifact is None:
                skipped.append(SkippedFile(
                    source_path=source_path,
                    reason="no parseable handoff headers",
                ))
                continue
            msg = _artifact_to_message(source_path, artifact)
            messages.append(msg)
            transitions.append(_artifact_to_transition(msg.message_id, source_path))
            path_to_message_id[source_path] = msg.message_id

    messages.sort(key=lambda m: m.message_id)
    transitions.sort(key=lambda t: t.message_id)

    places: dict[str, list[str]] = {}
    for msg in messages:
        places.setdefault(msg.place, []).append(msg.message_id)
    topics = Topics(places=places)

    evaluator = HandoffEvaluator(repo_root=root)
    violations = evaluator.evaluate()
    guard_violations = [
        _violation_to_guard_violation(v, path_to_message_id)
        for v in violations
    ]
    guard_violations.sort(key=lambda g: g.code)

    return TopicsView(
        repo_root=str(root),
        generated_at=(
            datetime.now(timezone.utc).isoformat() if include_timestamp else None
        ),
        messages=messages,
        transitions=transitions,
        topics=topics,
        guard_violations=guard_violations,
        skipped=skipped,
    )
