from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.data.marking import HandoffMarking, Marking
from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.guards import (
    check_codex_as_pi_identity_collapse,
)


def test__Guards__codex_as_pi_identity_collapse__codex_claiming_pi_origin_is_violation() -> None:
    """Validate Codex artifacts claiming pi origin are identity collapses."""
    # Token is the Codex-mediated pi-origin fixture under guard evaluation.
    token: HandoffArtifact = HandoffArtifact(
        path=Path("/fake/codex-pi.md"),
        kind="routing-decision",
        origin="pi",
        sender="Codex",
        recipient="Athena",
        delegated_operator="Codex",
    )
    # Marking places the fixture token into the handoff net.
    marking: HandoffMarking = Marking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_codex_as_pi_identity_collapse(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.CODEX_AS_PI_IDENTITY_COLLAPSE


def test__Guards__codex_as_pi_identity_collapse__codex_without_pi_claim_is_not_violation() -> None:
    """Validate Codex artifacts without pi-origin claims are allowed."""
    # Token is the Codex-origin fixture under guard evaluation.
    token: HandoffArtifact = HandoffArtifact(
        path=Path("/fake/codex-no-pi.md"),
        kind="routing-decision",
        origin="Codex",
        sender="Codex",
        recipient="Athena",
        delegated_operator="Codex",
    )
    # Marking places the fixture token into the handoff net.
    marking: HandoffMarking = Marking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_codex_as_pi_identity_collapse(marking)
    assert len(violations) == 0


def test__Guards__codex_as_pi_identity_collapse__pi_actor_without_codex_is_not_violation() -> None:
    """Validate real pi-origin artifacts without Codex provenance are allowed."""
    # Token is the pi-origin non-Codex fixture under guard evaluation.
    token: HandoffArtifact = HandoffArtifact(
        path=Path("/fake/real-pi.md"),
        kind="routing-decision",
        origin="pi",
        sender="Hermes",
        recipient="Athena",
    )
    # Marking places the fixture token into the handoff net.
    marking: HandoffMarking = Marking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_codex_as_pi_identity_collapse(marking)
    assert len(violations) == 0
