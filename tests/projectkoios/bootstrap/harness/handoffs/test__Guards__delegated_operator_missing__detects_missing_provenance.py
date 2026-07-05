from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.data.marking import HandoffMarking, Marking
from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.guards import (
    check_delegated_operator_missing,
)


def _codex_token(
    tag: str = "codex",
    delegated_operator: str | None = None,
) -> HandoffArtifact:
    """Create a Codex handoff fixture for delegated-operator guard tests."""
    return HandoffArtifact(
        path=Path(f"/fake/{tag}.md"),
        kind="routing-decision",
        origin="Codex",
        sender="Codex",
        recipient="Hermes",
        delegated_operator=delegated_operator,
    )


def test__Guards__delegated_operator_missing__codex_with_provenance_is_not_violation() -> None:
    """Validate Codex handoffs with delegated-operator provenance pass."""
    # Token is the Codex fixture under guard evaluation.
    token: HandoffArtifact = _codex_token("codex-valid", delegated_operator="Codex")
    # Marking places the fixture token into the handoff net.
    marking: HandoffMarking = Marking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_delegated_operator_missing(marking)
    assert len(violations) == 0


def test__Guards__delegated_operator_missing__codex_without_provenance_is_violation() -> None:
    """Validate Codex handoffs without delegated-operator provenance fail."""
    # Token is the Codex fixture under guard evaluation.
    token: HandoffArtifact = _codex_token("codex-missing", delegated_operator=None)
    # Marking places the fixture token into the handoff net.
    marking: HandoffMarking = Marking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_delegated_operator_missing(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.DELEGATED_OPERATOR_MISSING
    assert violations[0].actor == "Codex"


def test__Guards__delegated_operator_missing__athena_artifact_no_violation() -> None:
    """Validate non-Codex artifacts do not require delegated provenance."""
    # Token is the Athena fixture under guard evaluation.
    token: HandoffArtifact = HandoffArtifact(
        path=Path("/fake/athena.md"),
        kind="architecture-spec",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )
    # Marking places the fixture token into the handoff net.
    marking: HandoffMarking = Marking(tokens_by_place={"archon_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_delegated_operator_missing(marking)
    assert len(violations) == 0
