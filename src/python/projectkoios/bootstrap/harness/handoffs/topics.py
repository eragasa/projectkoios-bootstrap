from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.data.violation import Violation
from projectkoios.bootstrap.harness.handoffs.evaluator import (
    HandoffEvaluator,
    PLACE_DIRECTORIES,
)
from projectkoios.bootstrap.harness.handoffs.parser import HandoffParser


HANDOFFS_PREFIX: str = "docs/archive/handoffs/"


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


def message_id(source_path: str) -> str:
    if source_path.startswith(HANDOFFS_PREFIX):
        return source_path[len(HANDOFFS_PREFIX):]
    return source_path


def infer_place(source_path: str) -> str:
    place_name: str
    rel_dir: str
    for place_name, rel_dir in PLACE_DIRECTORIES.items():
        if source_path.startswith(rel_dir):
            return place_name
    return "unknown"


def artifact_to_message(source_path: str, artifact: HandoffArtifact) -> Message:
    return Message(
        message_id=message_id(source_path),
        source_path=source_path,
        place=infer_place(source_path),
        kind=artifact.kind,
        origin=artifact.origin,
        sender=artifact.sender,
        recipient=artifact.recipient,
        acting_as=artifact.acting_as,
        delegated_operator=artifact.delegated_operator,
        provenance=artifact.provenance,
    )


def artifact_to_transition(message_id_value: str, source_path: str) -> Transition:
    return Transition(
        message_id=message_id_value,
        evidence={
            "source_path": source_path,
            "inferred_from": "file_existence_and_headers",
        },
    )


def violation_to_guard_violation(
    violation: Violation,
    path_to_message_id: dict[str, str],
) -> GuardViolation:
    source_path: str = str(violation.path.as_posix())
    return GuardViolation(
        code=violation.code.value,
        reason=violation.reason,
        message_id=path_to_message_id.get(source_path),
        source_path=source_path,
    )


def build_topics_places(messages: list[Message]) -> Topics:
    places: dict[str, list[str]] = {}
    msg: Message
    for msg in messages:
        places.setdefault(msg.place, []).append(msg.message_id)
    return Topics(places=places)


def collect_messages(root: Path, parser: HandoffParser) -> tuple[list[Message], list[Transition], list[SkippedFile], dict[str, str]]:
    messages: list[Message] = []
    transitions: list[Transition] = []
    skipped: list[SkippedFile] = []
    path_to_message_id: dict[str, str] = {}

    place_name: str
    rel_dir: str
    for place_name, rel_dir in PLACE_DIRECTORIES.items():
        dir_path: Path = root / rel_dir
        if not dir_path.exists():
            continue
        file_path: Path
        for file_path in sorted(dir_path.iterdir()):
            if not file_path.is_file() or file_path.suffix != ".md":
                continue
            source_path: str = str(file_path.relative_to(root).as_posix())
            artifact: HandoffArtifact | None = parser.parse_file(file_path)
            if artifact is None:
                skipped.append(SkippedFile(
                    source_path=source_path,
                    reason="no parseable handoff headers",
                ))
                continue
            msg: Message = artifact_to_message(source_path, artifact)
            messages.append(msg)
            transitions.append(artifact_to_transition(msg.message_id, source_path))
            path_to_message_id[source_path] = msg.message_id
    return messages, transitions, skipped, path_to_message_id


def build_topics_view(
    repo_root: Path,
    include_timestamp: bool = False,
) -> TopicsView:
    root: Path = repo_root.resolve()
    parser: HandoffParser = HandoffParser()

    collected: tuple[list[Message], list[Transition], list[SkippedFile], dict[str, str]] = collect_messages(root, parser)
    messages: list[Message] = collected[0]
    transitions: list[Transition] = collected[1]
    skipped: list[SkippedFile] = collected[2]
    path_to_message_id: dict[str, str] = collected[3]

    messages.sort(key=lambda msg: msg.message_id)
    transitions.sort(key=lambda transition: transition.message_id)

    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=root)
    violations: list[Violation] = evaluator.evaluate()
    guard_violations: list[GuardViolation] = [
        violation_to_guard_violation(violation, path_to_message_id)
        for violation in violations
    ]
    guard_violations.sort(key=lambda guard_violation: guard_violation.code)

    generated_at: str | None = datetime.now(timezone.utc).isoformat() if include_timestamp else None
    return TopicsView(
        repo_root=str(root),
        generated_at=generated_at,
        messages=messages,
        transitions=transitions,
        topics=build_topics_places(messages),
        guard_violations=guard_violations,
        skipped=skipped,
    )
