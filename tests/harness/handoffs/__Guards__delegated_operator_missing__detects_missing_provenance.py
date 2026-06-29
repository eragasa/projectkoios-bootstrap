from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
from projectkoios.bootstrap.harness.data.marking import Marking
from projectkoios.bootstrap.harness.data.violation import ViolationCode
from projectkoios.bootstrap.harness.handoffs.guards import (
    check_delegated_operator_missing,
)


def _codex_token(
    tag: str = "codex",
    delegated_operator: str | None = None,
) -> HandoffArtifact:
    return HandoffArtifact(
        path=Path(f"/fake/{tag}.md"),
        kind="routing-decision",
        origin="Codex",
        sender="Codex",
        recipient="Hermes",
        delegated_operator=delegated_operator,
    )


def test__Guards__delegated_operator_missing__codex_with_provenance_is_not_violation() -> None:
    token = _codex_token("codex-valid", delegated_operator="Codex")
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_delegated_operator_missing(marking)
    assert len(violations) == 0


def test__Guards__delegated_operator_missing__codex_without_provenance_is_violation() -> None:
    token = _codex_token("codex-missing", delegated_operator=None)
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_delegated_operator_missing(marking)
    assert len(violations) == 1
    assert violations[0].code == ViolationCode.DELEGATED_OPERATOR_MISSING
    assert violations[0].actor == "Codex"


def test__Guards__delegated_operator_missing__athena_artifact_no_violation() -> None:
    token = HandoffArtifact(
        path=Path("/fake/athena.md"),
        kind="architecture-spec",
        origin="Athena",
        sender="Athena",
        recipient="Vulcan",
    )
    marking = Marking(tokens_by_place={"archon_inbox": [token]})
    violations = check_delegated_operator_missing(marking)
    assert len(violations) == 0
