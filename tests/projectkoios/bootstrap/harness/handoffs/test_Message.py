from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.handoffs.topics import (
    Message,
    artifact_to_message,
    message_id,
)


def test__Message__construction__builds_message_with_path_derived_id() -> None:
    """Validate message construction derives stable archive-relative IDs."""
    # Artifact is the handoff token converted into a topic message.
    artifact: HandoffArtifact = HandoffArtifact(
        path=Path("/repo/docs/archive/handoffs/archon/spec.md"),
        kind="architecture-spec",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )
    # Message is the topic representation under assertion.
    message: Message = artifact_to_message(
        "docs/archive/handoffs/archon/spec.md", artifact,
    )
    assert message.message_id == "archon/spec.md"
    assert message.source_path == "docs/archive/handoffs/archon/spec.md"
    assert message.place == "archon_inbox"


def test__Message__construction__strips_handoffs_prefix() -> None:
    """Validate message identifiers strip the archive handoff prefix."""
    assert message_id("docs/archive/handoffs/pi/foo.md") == "pi/foo.md"
    assert message_id("docs/archive/handoffs/opencode/bar.md") == "opencode/bar.md"
    assert message_id("docs/archive/handoffs/goose/baz.md") == "goose/baz.md"


def test__Message__construction__copies_artifact_fields() -> None:
    """Validate message construction copies handoff artifact metadata."""
    # Artifact is the handoff token converted into a topic message.
    artifact: HandoffArtifact = HandoffArtifact(
        path=Path("/r/docs/archive/handoffs/pi/out.md"),
        kind="routing-decision",
        origin="pi",
        sender="Hermes",
        recipient="Athena",
        acting_as="Hermes",
        delegated_operator="Codex",
        provenance=["origin: pi", "from: Hermes"],
    )
    # Message is the topic representation under assertion.
    message: Message = artifact_to_message("docs/archive/handoffs/pi/out.md", artifact)
    assert message.kind == "routing-decision"
    assert message.origin == "pi"
    assert message.sender == "Hermes"
    assert message.recipient == "Athena"
    assert message.acting_as == "Hermes"
    assert message.delegated_operator == "Codex"
    assert message.provenance == ["origin: pi", "from: Hermes"]


def test__Message__construction__preserves_optional_fields_when_absent() -> None:
    """Validate absent optional artifact metadata remains absent on messages."""
    # Artifact is the handoff token converted into a topic message.
    artifact: HandoffArtifact = HandoffArtifact(
        path=Path("/r/docs/archive/handoffs/goose/k.md"),
        kind="knowledge-note",
        origin="Koios",
        sender="Koios",
        recipient="Hermes",
    )
    # Message is the topic representation under assertion.
    message: Message = artifact_to_message("docs/archive/handoffs/goose/k.md", artifact)
    assert message.acting_as is None
    assert message.delegated_operator is None
    assert message.provenance is None


def test__Message__construction__maps_place_from_source_path() -> None:
    """Validate message construction maps source paths to topic places."""
    # Cases enumerate source paths and their expected Petri-net places.
    cases: list[tuple[str, str]] = [
        ("docs/archive/handoffs/archon/x.md", "archon_inbox"),
        ("docs/archive/handoffs/opencode/x.md", "opencode_inbox"),
        ("docs/archive/handoffs/pi/x.md", "pi_inbox"),
        ("docs/archive/handoffs/goose/x.md", "goose_inbox"),
        ("some/other/path.md", "unknown"),
    ]
    path: str
    expected_place: str
    for path, expected_place in cases:
        # Artifact is the handoff token converted into a topic message.
        artifact: HandoffArtifact = HandoffArtifact(
            path=Path("/r/" + path),
            kind="user-request",
            origin="user",
            sender="user",
            recipient="Hermes",
        )
        # Message is the topic representation under assertion.
        message: Message = artifact_to_message(path, artifact)
        assert message.place == expected_place, f"{path} → {message.place}"
