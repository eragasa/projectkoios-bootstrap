from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import ArtifactToken
from projectkoios.bootstrap.harness.data.marking import Marking
from projectkoios.bootstrap.harness.actions.guards import (
    check_codex_as_pi_identity_collapse,
)


def test__Guards__codex_as_pi_identity_collapse__codex_claiming_pi_origin_is_violation() -> None:
    token = ArtifactToken(
        id="codex-pi",
        path=Path("/fake/codex-pi.md"),
        kind="routing-decision",
        origin="pi",
        sender="Codex",
        recipient="Athena",
        delegated_operator="Codex",
    )
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_codex_as_pi_identity_collapse(marking)
    assert len(violations) == 1
    assert violations[0].code == "codex-as-pi-identity-collapse"


def test__Guards__codex_as_pi_identity_collapse__codex_without_pi_claim_is_not_violation() -> None:
    token = ArtifactToken(
        id="codex-no-pi",
        path=Path("/fake/codex-no-pi.md"),
        kind="routing-decision",
        origin="Codex",
        sender="Codex",
        recipient="Athena",
        delegated_operator="Codex",
    )
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_codex_as_pi_identity_collapse(marking)
    assert len(violations) == 0


def test__Guards__codex_as_pi_identity_collapse__pi_actor_without_codex_is_not_violation() -> None:
    token = ArtifactToken(
        id="real-pi",
        path=Path("/fake/real-pi.md"),
        kind="routing-decision",
        origin="pi",
        sender="Hermes",
        recipient="Athena",
    )
    marking = Marking(tokens_by_place={"pi_inbox": [token]})
    violations = check_codex_as_pi_identity_collapse(marking)
    assert len(violations) == 0
