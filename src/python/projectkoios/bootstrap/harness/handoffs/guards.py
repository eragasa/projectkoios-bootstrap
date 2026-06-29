from __future__ import annotations

from typing import Callable

from projectkoios.bootstrap.harness.data.marking import Marking
from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode


ACCEPTED_DECISION_KINDS = frozenset({
    "routing-decision",
    "revision-request",
    "completion-decision",
    "blockage-report",
})

IMPLEMENTATION_KINDS = frozenset({
    "patch",
    "test-results",
    "implementation-report",
})

HERMES_IDS = frozenset({"pi", "Hermes", "hermes"})
CODEX_IDS = frozenset({"Codex", "codex"})


def check_hermes_forwarded_without_decision(marking: Marking) -> list[Violation]:
    violations: list[Violation] = []
    for place_name in ("pi_inbox",):
        for token in marking.tokens_at(place_name):
            if token.sender not in HERMES_IDS and token.recipient not in HERMES_IDS:
                continue
            if token.kind not in ACCEPTED_DECISION_KINDS and token.kind != "user-request":
                violations.append(Violation(
                    code=ViolationCode.HERMES_FORWARDED_WITHOUT_DECISION,
                    actor=token.sender,
                    path=token.path,
                    reason=(
                        f"Hermes forwarded a {token.kind!r} artifact without producing "
                        f"a routing-decision, revision-request, completion-decision, "
                        f"or blockage-report."
                    ),
                    required_owner="Hermes",
                    suggested_next_action="Issue a routing-decision, revision-request, "
                    "completion-decision, or blockage-report instead of forwarding raw inbox state.",
                ))
    return violations


def check_wrong_implementation_owner(marking: Marking) -> list[Violation]:
    violations: list[Violation] = []
    for token in marking.all_tokens:
        if token.kind not in IMPLEMENTATION_KINDS:
            continue
        owner = token.sender
        expected = "Vulcan"
        if owner and owner.lower() != expected.lower() and owner != "opencode":
            violations.append(Violation(
                code=ViolationCode.WRONG_IMPLEMENTATION_OWNER,
                actor=owner,
                path=token.path,
                reason=(
                    f"Only Vulcan may produce {token.kind!r} artifacts, "
                    f"but the sender is {owner!r}."
                ),
                required_owner=expected,
                suggested_next_action=(
                    f"Route implementation completion to {expected} "
                    f"or issue a revision-request."
                ),
            ))
    return violations


def check_delegated_operator_missing(marking: Marking) -> list[Violation]:
    violations: list[Violation] = []
    for token in marking.all_tokens:
        is_codex_actor = (
            token.sender in CODEX_IDS
            or token.origin in CODEX_IDS
            or (token.acting_as and token.acting_as in CODEX_IDS)
        )
        if is_codex_actor and not token.delegated_operator:
            violations.append(Violation(
                code=ViolationCode.DELEGATED_OPERATOR_MISSING,
                actor=token.sender,
                path=token.path,
                reason=(
                    f"Codex-mediated artifact lacks Delegated-Operator provenance. "
                    f"Sender is {token.sender!r}, origin is {token.origin!r}."
                ),
                required_owner="Codex",
                suggested_next_action=(
                    "Add Delegated-Operator header to the handoff artifact "
                    "or route through a non-mediated channel."
                ),
            ))
    return violations


def check_codex_as_pi_identity_collapse(marking: Marking) -> list[Violation]:
    violations: list[Violation] = []
    for token in marking.all_tokens:
        claims_pi_origin = (
            token.origin in HERMES_IDS
            or token.sender in HERMES_IDS
            or (token.acting_as and token.acting_as in HERMES_IDS)
        )
        is_codex_produced = (
            token.delegated_operator in CODEX_IDS
            or token.provenance_has_codex()
        )
        if claims_pi_origin and is_codex_produced:
            violations.append(Violation(
                code=ViolationCode.CODEX_AS_PI_IDENTITY_COLLAPSE,
                actor=token.sender,
                path=token.path,
                reason=(
                    f"Artifact claims pi/Hermes origin or authority "
                    f"but was produced/mediated by Codex "
                    f"(delegated_operator={token.delegated_operator!r}). "
                    f"Codex must not collapse into the pi role."
                ),
                required_owner="pi",
                suggested_next_action=(
                    "Set a non-pi Origin, preserve Delegated-Operator provenance, "
                    "and avoid claiming pi authority in From/Acting-As."
                ),
            ))
    return violations


ALL_GUARDS: list[Callable[[Marking], list[Violation]]] = [
    check_hermes_forwarded_without_decision,
    check_wrong_implementation_owner,
    check_delegated_operator_missing,
    check_codex_as_pi_identity_collapse,
]
