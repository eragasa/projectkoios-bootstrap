from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact


def test__HandoffArtifact__construction__creates_token() -> None:
    token = HandoffArtifact(
        id="test-1",
        path=Path("/fake/handoff.md"),
        kind="implementation-brief",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )
    assert token.id == "test-1"
    assert token.kind == "implementation-brief"
    assert token.origin == "Athena"
    assert token.sender == "Athena"
    assert token.recipient == "Vulcan"
    assert token.status == "active"


def test__HandoffArtifact__construction__accepts_optional_fields() -> None:
    token = HandoffArtifact(
        id="test-2",
        path=Path("/fake/handoff.md"),
        kind="implementation-report",
        origin="Vulcan",
        sender="Vulcan",
        recipient="Hermes",
        acting_as="opencode",
        repository="projectkoios-bootstrap",
        status="active",
        delegated_operator="Codex",
    )
    assert token.acting_as == "opencode"
    assert token.repository == "projectkoios-bootstrap"
    assert token.delegated_operator == "Codex"


def test__HandoffArtifact__construction__defaults_status_to_active() -> None:
    token = HandoffArtifact(
        id="test-3",
        path=Path("/fake/handoff.md"),
        kind="routing-decision",
        origin="Hermes",
        sender="Hermes",
        recipient="Athena",
    )
    assert token.status == "active"


def test__HandoffArtifact__provenance_has_codex__detects_codex_in_delegated_operator() -> None:
    token = HandoffArtifact(
        id="test-4",
        path=Path("/fake/handoff.md"),
        kind="implementation-report",
        origin="Vulcan",
        sender="Vulcan",
        recipient="Hermes",
        delegated_operator="Codex",
    )
    assert token.provenance_has_codex() is True


def test__HandoffArtifact__provenance_has_codex__returns_false_when_no_codex() -> None:
    token = HandoffArtifact(
        id="test-5",
        path=Path("/fake/handoff.md"),
        kind="implementation-brief",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )
    assert token.provenance_has_codex() is False


def test__HandoffArtifact__provenance_has_codex__detects_codex_in_provenance_list() -> None:
    token = HandoffArtifact(
        id="test-6",
        path=Path("/fake/handoff.md"),
        kind="routing-decision",
        origin="Codex",
        sender="Codex",
        recipient="Hermes",
        provenance=["Codex", "projectkoios-bootstrap"],
    )
    assert token.provenance_has_codex() is True
