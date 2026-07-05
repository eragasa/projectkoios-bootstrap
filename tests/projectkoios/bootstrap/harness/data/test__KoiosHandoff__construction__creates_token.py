from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.handoff import KoiosHandoff


def test__KoiosHandoff__construction__creates_token() -> None:
    """Validate KoiosHandoff stores required construction fields."""
    # Token represents a minimal implementation-brief Koios handoff.
    token: KoiosHandoff = KoiosHandoff(
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


def test__KoiosHandoff__construction__accepts_optional_fields() -> None:
    """Validate KoiosHandoff stores optional provenance fields."""
    # Token includes optional acting_as and delegated_operator provenance fields.
    token: KoiosHandoff = KoiosHandoff(
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


def test__KoiosHandoff__provenance_has_codex__detects_codex_in_delegated_operator() -> None:
    """Validate provenance_has_codex detects Codex delegated operators."""
    # Token records Codex as the delegated operator provenance source.
    token: KoiosHandoff = KoiosHandoff(
        path=Path("/fake/handoff.md"),
        kind="implementation-report",
        origin="Vulcan",
        sender="Vulcan",
        recipient="Hermes",
        delegated_operator="Codex",
    )

    assert token.provenance_has_codex() is True


def test__KoiosHandoff__provenance_has_codex__returns_false_when_no_codex() -> None:
    """Validate provenance_has_codex is false when Codex is absent."""
    # Token contains only non-Codex provenance fields.
    token: KoiosHandoff = KoiosHandoff(
        path=Path("/fake/handoff.md"),
        kind="implementation-brief",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )

    assert token.provenance_has_codex() is False


def test__KoiosHandoff__provenance_has_codex__detects_codex_in_provenance_list() -> None:
    """Validate provenance_has_codex detects Codex list provenance."""
    # Token records Codex in the explicit provenance list.
    token: KoiosHandoff = KoiosHandoff(
        path=Path("/fake/handoff.md"),
        kind="routing-decision",
        origin="Codex",
        sender="Codex",
        recipient="Hermes",
        provenance=["Codex", "projectkoios-bootstrap"],
    )

    assert token.provenance_has_codex() is True
