from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.data.marking import Marking
from projectkoios.bootstrap.harness.data.violation import ViolationCode
from projectkoios.bootstrap.harness.handoffs.guards import (
    check_hermes_forwarded_without_decision,
)


def _token(
    tag: str = "token",
    kind: str = "user-request",
    sender: str = "Athena",
    recipient: str = "Vulcan",
) -> HandoffArtifact:
    return HandoffArtifact(
        path=Path(f"/fake/{tag}.md"),
        kind=kind,
        origin=sender,
        sender=sender,
        recipient=recipient,
    )


def test__Guards__hermes_forwarded_without_decision__allows_user_request() -> None:
    token = _token(
        "role-state",
        kind="user-request",
        sender="user",
        recipient="pi",
    )
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_hermes_forwarded_without_decision(marking)
    assert len(violations) == 0


def test__Guards__hermes_forwarded_without_decision__user_request_is_not_violation() -> None:
    token = _token(
        "user-request-1",
        kind="user-request",
        sender="user",
        recipient="pi",
    )
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_hermes_forwarded_without_decision(marking)
    assert len(violations) == 0


def test__Guards__hermes_forwarded_without_decision__routing_decision_is_not_violation() -> None:
    token = _token(
        "routing-1",
        kind="routing-decision",
        sender="Hermes",
        recipient="Athena",
    )
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_hermes_forwarded_without_decision(marking)
    assert len(violations) == 0


def test__Guards__hermes_forwarded_without_decision__unknown_kind_in_pi_place_is_violation() -> None:
    token = _token(
        "unknown-artifact",
        kind="random-note",
        sender="Hermes",
        recipient="Athena",
    )
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_hermes_forwarded_without_decision(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.HERMES_FORWARDED_WITHOUT_DECISION
