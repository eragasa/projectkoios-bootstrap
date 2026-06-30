from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.handoffs.topics import (
    _artifact_to_message,
    _message_id,
)


def test__Message__construction__builds_message_with_path_derived_id() -> None:
    artifact = HandoffArtifact(
        path=Path("/repo/docs/archive/handoffs/archon/spec.md"),
        kind="architecture-spec",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )
    msg = _artifact_to_message(
        "docs/archive/handoffs/archon/spec.md", artifact,
    )
    assert msg.message_id == "archon/spec.md"
    assert msg.source_path == "docs/archive/handoffs/archon/spec.md"
    assert msg.place == "archon_inbox"


def test__Message__construction__strips_handoffs_prefix() -> None:
    assert _message_id("docs/archive/handoffs/pi/foo.md") == "pi/foo.md"
    assert _message_id("docs/archive/handoffs/opencode/bar.md") == "opencode/bar.md"
    assert _message_id("docs/archive/handoffs/goose/baz.md") == "goose/baz.md"


def test__Message__construction__copies_artifact_fields() -> None:
    artifact = HandoffArtifact(
        path=Path("/r/docs/archive/handoffs/pi/out.md"),
        kind="routing-decision",
        origin="pi",
        sender="Hermes",
        recipient="Athena",
        acting_as="Hermes",
        delegated_operator="Codex",
        provenance=["origin: pi", "from: Hermes"],
    )
    msg = _artifact_to_message("docs/archive/handoffs/pi/out.md", artifact)
    assert msg.kind == "routing-decision"
    assert msg.origin == "pi"
    assert msg.sender == "Hermes"
    assert msg.recipient == "Athena"
    assert msg.acting_as == "Hermes"
    assert msg.delegated_operator == "Codex"
    assert msg.provenance == ["origin: pi", "from: Hermes"]


def test__Message__construction__preserves_optional_fields_when_absent() -> None:
    artifact = HandoffArtifact(
        path=Path("/r/docs/archive/handoffs/goose/k.md"),
        kind="knowledge-note",
        origin="Koios",
        sender="Koios",
        recipient="Hermes",
    )
    msg = _artifact_to_message("docs/archive/handoffs/goose/k.md", artifact)
    assert msg.acting_as is None
    assert msg.delegated_operator is None
    assert msg.provenance is None


def test__Message__construction__maps_place_from_source_path() -> None:
    cases = [
        ("docs/archive/handoffs/archon/x.md", "archon_inbox"),
        ("docs/archive/handoffs/opencode/x.md", "opencode_inbox"),
        ("docs/archive/handoffs/pi/x.md", "pi_inbox"),
        ("docs/archive/handoffs/goose/x.md", "goose_inbox"),
        ("some/other/path.md", "unknown"),
    ]
    for path, expected_place in cases:
        artifact = HandoffArtifact(
            path=Path("/r/" + path),
            kind="user-request",
            origin="user",
            sender="user",
            recipient="Hermes",
        )
        msg = _artifact_to_message(path, artifact)
        assert msg.place == expected_place, f"{path} → {msg.place}"
