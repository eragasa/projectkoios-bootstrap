from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from projectkoios.bootstrap.mailbox import (
    InboxEnvelope,
    deliver_inbox_message,
    read_inbox_message,
    read_inbox_status,
)


def test__mailbox_bridge__writes_readable_inbox_envelope_and_notifies_after_write(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path
    inbox = repo_root / "workspaces" / "vulcan" / "inbox"
    outbox = repo_root / "workspaces" / "vulcan" / "outbox"
    inbox.mkdir(parents=True)
    outbox.mkdir(parents=True)

    calls: list[Path] = []

    envelope = InboxEnvelope(
        sender="hermes",
        target="vulcan",
        subject="implementation brief",
        body="Do the smallest bridge slice.",
        provenance="docs/plans/hermes-mailbox-intercom-bridge.md",
        created_at=datetime(2026, 7, 3, 12, 34, 56, tzinfo=timezone.utc),
    )

    def notify(path: Path, delivered: InboxEnvelope) -> None:
        calls.append(path)
        assert_path_exists(path)
        assert delivered.subject == envelope.subject

    delivered_path = deliver_inbox_message(
        repo_root,
        "vulcan",
        envelope,
        notify=notify,
    )

    assert delivered_path.exists()
    assert calls == [delivered_path]
    assert not list(outbox.iterdir())

    content = delivered_path.read_text(encoding="utf-8")
    assert "format: inbox-envelope" in content
    assert "sender: hermes" in content
    assert "target: vulcan" in content
    assert "subject: implementation brief" in content
    assert "provenance: docs/plans/hermes-mailbox-intercom-bridge.md" in content
    assert "Do the smallest bridge slice." in content

    parsed = read_inbox_message(delivered_path)
    assert parsed.sender == envelope.sender
    assert parsed.target == envelope.target
    assert parsed.subject == envelope.subject
    assert parsed.body == envelope.body

    status = read_inbox_status(repo_root, "vulcan")
    assert status.count == 1
    assert status.newest is not None
    assert status.newest.path == delivered_path
    assert status.newest.subject == envelope.subject


def assert_path_exists(path: Path) -> None:
    assert path.exists()
