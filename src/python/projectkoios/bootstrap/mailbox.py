from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from uuid import uuid4
import re


INBOX_DIR_NAME = "inbox"
OUTBOX_DIR_NAME = "outbox"
MAILBOX_FORMAT = "inbox-envelope"


@dataclass(frozen=True, slots=True)
class InboxEnvelope:
    """Durable markdown inbox envelope.

    The on-disk format is a small Markdown document with YAML front matter:

    ---
    format: inbox-envelope
    sender: hermes
    target: vulcan
    timestamp: 2026-07-03T12:34:56Z
    subject: implementation brief
    provenance: docs/plans/hermes-mailbox-intercom-bridge.md
    ---

    Body text goes below the closing fence.
    """

    sender: str
    target: str
    subject: str
    body: str
    provenance: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        object.__setattr__(self, "sender", self.sender.strip())
        object.__setattr__(self, "target", self.target.strip())
        object.__setattr__(self, "subject", self.subject.strip())
        object.__setattr__(self, "provenance", self.provenance.strip())
        if self.created_at.tzinfo is None:
            object.__setattr__(self, "created_at", self.created_at.replace(tzinfo=timezone.utc))

    def timestamp_text(self) -> str:
        return self.created_at.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    def render(self) -> str:
        header: dict[str, str] = {
            "format": MAILBOX_FORMAT,
            "sender": self.sender,
            "target": self.target,
            "timestamp": self.timestamp_text(),
            "subject": self.subject,
        }
        if self.provenance:
            header["provenance"] = self.provenance

        front_matter = "\n".join(f"{key}: {value}" for key, value in header.items())
        body = self.body.rstrip()
        return f"---\n{front_matter}\n---\n\n{body}\n"


@dataclass(frozen=True, slots=True)
class InboxMessageSummary:
    path: Path
    sender: str
    target: str
    subject: str
    provenance: str
    timestamp: datetime


@dataclass(frozen=True, slots=True)
class InboxStatus:
    inbox_dir: Path
    messages: tuple[InboxMessageSummary, ...]

    @property
    def newest(self) -> InboxMessageSummary | None:
        return self.messages[-1] if self.messages else None

    @property
    def count(self) -> int:
        return len(self.messages)


_TIMESTAMP_RE = re.compile(r"Z$")


def workspace_dir(repo_root: Path, target: str) -> Path:
    return repo_root / "workspaces" / target


def inbox_dir(repo_root: Path, target: str) -> Path:
    return workspace_dir(repo_root, target) / INBOX_DIR_NAME


def outbox_dir(repo_root: Path, target: str) -> Path:
    return workspace_dir(repo_root, target) / OUTBOX_DIR_NAME


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "message"


def _timestamp_slug(created_at: datetime) -> str:
    stamp = created_at.astimezone(timezone.utc).strftime("%Y%m%d.%H%M%S.%fZ")
    return stamp


def _parse_timestamp(value: str) -> datetime:
    normalized = _TIMESTAMP_RE.sub("+00:00", value)
    return datetime.fromisoformat(normalized)


def parse_inbox_envelope(text: str) -> InboxEnvelope:
    if not text.startswith("---\n"):
        raise ValueError("inbox envelope must start with YAML front matter")
    try:
        front_matter, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("inbox envelope missing closing front matter fence") from exc

    data: dict[str, str] = {}
    for raw_line in front_matter.splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            raise ValueError("inbox envelope front matter must contain key: value pairs")
        key, value = raw_line.split(":", 1)
        data[key.strip()] = value.strip()

    if data.get("format") != MAILBOX_FORMAT:
        raise ValueError(f"inbox envelope format must be {MAILBOX_FORMAT}")

    for key in ("sender", "target", "timestamp", "subject"):
        if key not in data or not data[key].strip():
            raise ValueError(f"inbox envelope is missing required field: {key}")

    return InboxEnvelope(
        sender=data["sender"],
        target=data["target"],
        subject=data["subject"],
        body=body.lstrip("\n").rstrip("\n"),
        provenance=data.get("provenance", ""),
        created_at=_parse_timestamp(data["timestamp"]),
    )


def read_inbox_message(path: Path) -> InboxEnvelope:
    return parse_inbox_envelope(path.read_text(encoding="utf-8"))


def read_inbox_status(repo_root: Path, target: str) -> InboxStatus:
    inbox = inbox_dir(repo_root, target)
    if not inbox.exists():
        return InboxStatus(inbox_dir=inbox, messages=())

    summaries: list[InboxMessageSummary] = []
    for path in sorted(inbox.glob("*.md")):
        envelope = read_inbox_message(path)
        summaries.append(
            InboxMessageSummary(
                path=path,
                sender=envelope.sender,
                target=envelope.target,
                subject=envelope.subject,
                provenance=envelope.provenance,
                timestamp=envelope.created_at.astimezone(timezone.utc),
            )
        )
    summaries.sort(key=lambda item: (item.timestamp, item.path.name))
    return InboxStatus(inbox_dir=inbox, messages=tuple(summaries))


def deliver_inbox_message(
    repo_root: Path,
    target: str,
    envelope: InboxEnvelope,
    *,
    notify: Callable[[Path, InboxEnvelope], None] | None = None,
) -> Path:
    inbox = inbox_dir(repo_root, target)
    inbox.mkdir(parents=True, exist_ok=True)

    filename = f"{_timestamp_slug(envelope.created_at)}-{_slugify(envelope.subject)}-{uuid4().hex[:8]}.md"
    final_path = inbox / filename
    temp_path = inbox / f".{filename}.tmp"

    temp_path.write_text(envelope.render(), encoding="utf-8")
    temp_path.replace(final_path)

    if notify is not None:
        notify(final_path, envelope)

    return final_path
