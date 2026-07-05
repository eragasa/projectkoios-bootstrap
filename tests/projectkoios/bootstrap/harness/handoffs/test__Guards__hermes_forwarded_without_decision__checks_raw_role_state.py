from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.handoff import KoiosHandoff
from projectkoios.bootstrap.harness.data.marking import HandoffMarking, PetriNetMarking
from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.guards import (
    check_hermes_forwarded_without_decision,
)


def _token(
    tag: str = "token",
    kind: str = "user-request",
    sender: str = "Athena",
    recipient: str = "Vulcan",
) -> KoiosHandoff:
    """Create a Koios handoff fixture for Hermes forwarding guard tests."""
    return KoiosHandoff(
        path=Path(f"/fake/{tag}.md"),
        kind=kind,
        origin=sender,
        sender=sender,
        recipient=recipient,
    )


def test__Guards__hermes_forwarded_without_decision__allows_user_request() -> None:
    """Validate raw user requests in the pi inbox are allowed."""
    # Token is the raw user-request fixture under guard evaluation.
    token: KoiosHandoff = _token(
        "role-state",
        kind="user-request",
        sender="user",
        recipient="pi",
    )
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_hermes_forwarded_without_decision(marking)
    assert len(violations) == 0


def test__Guards__hermes_forwarded_without_decision__user_request_is_not_violation() -> None:
    """Validate user-request artifacts are not forwarding violations."""
    # Token is the user-request fixture under guard evaluation.
    token: KoiosHandoff = _token(
        "user-request-1",
        kind="user-request",
        sender="user",
        recipient="pi",
    )
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_hermes_forwarded_without_decision(marking)
    assert len(violations) == 0


def test__Guards__hermes_forwarded_without_decision__routing_decision_is_not_violation() -> None:
    """Validate Hermes routing decisions are not forwarding violations."""
    # Token is the routing-decision fixture under guard evaluation.
    token: KoiosHandoff = _token(
        "routing-1",
        kind="routing-decision",
        sender="Hermes",
        recipient="Athena",
    )
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_hermes_forwarded_without_decision(marking)
    assert len(violations) == 0


def test__Guards__hermes_forwarded_without_decision__unknown_kind_in_pi_place_is_violation() -> None:
    """Validate unknown Hermes artifacts in pi inbox are forwarding violations."""
    # Token is the unknown Hermes-authored fixture under guard evaluation.
    token: KoiosHandoff = _token(
        "unknown-artifact",
        kind="random-note",
        sender="Hermes",
        recipient="Athena",
    )
    # PetriNetMarking places the fixture token into the handoff net.
    marking: HandoffMarking = PetriNetMarking(tokens_by_place={"pi_inbox": [token]})
    # Violations are the emitted guard failures under assertion.
    violations: list[Violation] = check_hermes_forwarded_without_decision(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.HERMES_FORWARDED_WITHOUT_DECISION
