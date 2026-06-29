from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact


def test__HandoffArtifact__construction__creates_token() -> None:
    token = HandoffArtifact(
        path=Path("/fake/handoff.md"),
        kind="implementation-brief",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )
    assert token.kind == "implementation-brief"
    assert token.origin == "Athena"
    assert token.sender == "Athena"
    assert token.recipient == "Vulcan"


def test__HandoffArtifact__construction__accepts_optional_fields() -> None:
    token = HandoffArtifact(
        path=Path("/fake/handoff.md"),
        kind="implementation-report",
        origin="Vulcan",
        sender="Vulcan",
        recipient="Hermes",
        acting_as="opencode",
        delegated_operator="Codex",
    )
    assert token.acting_as == "opencode"
    assert token.delegated_operator == "Codex"


def test__HandoffArtifact__provenance_has_codex__detects_codex_in_delegated_operator() -> None:
    token = HandoffArtifact(
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
        path=Path("/fake/handoff.md"),
        kind="implementation-brief",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )
    assert token.provenance_has_codex() is False


def test__HandoffArtifact__provenance_has_codex__detects_codex_in_provenance_list() -> None:
    token = HandoffArtifact(
        path=Path("/fake/handoff.md"),
        kind="routing-decision",
        origin="Codex",
        sender="Codex",
        recipient="Hermes",
        provenance=["Codex", "projectkoios-bootstrap"],
    )
    assert token.provenance_has_codex() is True
