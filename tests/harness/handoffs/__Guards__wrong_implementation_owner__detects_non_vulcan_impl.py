from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.data.marking import Marking
from projectkoios.bootstrap.harness.data.violation import ViolationCode
from projectkoios.bootstrap.harness.handoffs.guards import (
    check_wrong_implementation_owner,
)


def _token(
    id: str,
    kind: str = "implementation-report",
    sender: str = "Vulcan",
) -> HandoffArtifact:
    return HandoffArtifact(
        id=id,
        path=Path(f"/fake/{id}.md"),
        kind=kind,
        origin=sender,
        sender=sender,
        recipient="Hermes",
    )


def test__Guards__wrong_implementation_owner__vulcan_impl_is_not_violation() -> None:
    token = _token("valid-impl", kind="implementation-report", sender="Vulcan")
    marking = Marking(tokens_by_place={"vulcan_inbox": [token]})
    violations = check_wrong_implementation_owner(marking)
    assert len(violations) == 0


def test__Guards__wrong_implementation_owner__opencode_impl_is_not_violation() -> None:
    token = _token("valid-impl", kind="implementation-report", sender="opencode")
    marking = Marking(tokens_by_place={"vulcan_inbox": [token]})
    violations = check_wrong_implementation_owner(marking)
    assert len(violations) == 0


def test__Guards__wrong_implementation_owner__hermes_impl_report_is_violation() -> None:
    token = _token("hermes-impl", kind="implementation-report", sender="Hermes")
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_wrong_implementation_owner(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.WRONG_IMPLEMENTATION_OWNER
    assert violations[0].actor == "Hermes"


def test__Guards__wrong_implementation_owner__hermes_patch_is_violation() -> None:
    token = _token("hermes-patch", kind="patch", sender="Hermes")
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_wrong_implementation_owner(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.WRONG_IMPLEMENTATION_OWNER


def test__Guards__wrong_implementation_owner__athena_test_results_is_violation() -> None:
    token = _token("athena-tests", kind="test-results", sender="Athena")
    marking = Marking(tokens_by_place={"archon_inbox": [token]})
    violations = check_wrong_implementation_owner(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.WRONG_IMPLEMENTATION_OWNER
