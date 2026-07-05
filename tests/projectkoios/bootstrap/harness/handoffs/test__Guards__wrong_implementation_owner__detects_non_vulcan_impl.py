from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.handoff import KoiosHandoff
from projectkoios.bootstrap.harness.data.marking import HandoffMarking, PetriNetMarking
from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.guards import (
    check_wrong_implementation_owner,
)


def _token(
    tag: str = "token",
    kind: str = "implementation-report",
    sender: str = "Vulcan",
) -> KoiosHandoff:
    """Create a Koios handoff fixture for implementation-owner guard tests."""
    return KoiosHandoff(
        path=Path(f"/fake/{tag}.md"),
        kind=kind,
        origin=sender,
        sender=sender,
        recipient="Hermes",
    )


def test__Guards__wrong_implementation_owner__vulcan_impl_is_not_violation() -> None:
    """Validate Vulcan-owned implementation reports are accepted."""
    # Token is the implementation report fixture under guard evaluation.
    token: KoiosHandoff = _token("valid-impl", kind="implementation-report", sender="Vulcan")
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"vulcan_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_wrong_implementation_owner(marking)
    assert len(violations) == 0


def test__Guards__wrong_implementation_owner__opencode_impl_is_not_violation() -> None:
    """Validate opencode-owned implementation reports are accepted."""
    # Token is the implementation report fixture under guard evaluation.
    token: KoiosHandoff = _token("valid-impl", kind="implementation-report", sender="opencode")
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"vulcan_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_wrong_implementation_owner(marking)
    assert len(violations) == 0


def test__Guards__wrong_implementation_owner__hermes_impl_report_is_violation() -> None:
    """Validate Hermes-authored implementation reports are violations."""
    # Token is the implementation report fixture under guard evaluation.
    token: KoiosHandoff = _token("hermes-impl", kind="implementation-report", sender="Hermes")
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_wrong_implementation_owner(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.WRONG_IMPLEMENTATION_OWNER
    assert violations[0].actor == "Hermes"


def test__Guards__wrong_implementation_owner__hermes_patch_is_violation() -> None:
    """Validate Hermes-authored patches are violations."""
    # Token is the patch fixture under guard evaluation.
    token: KoiosHandoff = _token("hermes-patch", kind="patch", sender="Hermes")
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_wrong_implementation_owner(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.WRONG_IMPLEMENTATION_OWNER


def test__Guards__wrong_implementation_owner__athena_test_results_is_violation() -> None:
    """Validate Athena-authored test results are violations."""
    # Token is the test-results fixture under guard evaluation.
    token: KoiosHandoff = _token("athena-tests", kind="test-results", sender="Athena")
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"archon_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_wrong_implementation_owner(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.WRONG_IMPLEMENTATION_OWNER
