from __future__ import annotations

from projectkoios.bootstrap.harness.data.marking import Marking
from projectkoios.bootstrap.harness.data.violation import Violation


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


def check_hermes_forwarded_without_decision(marking: Marking) -> list[Violation]:
    violations: list[Violation] = []
    for place_name in ("hermes_inbox", "pi_inbox"):
        for token in marking.tokens_at(place_name):
            if token.recipient == "pi" or token.recipient == "Hermes" or token.sender == "pi" or token.sender == "Hermes":
                if token.kind not in ACCEPTED_DECISION_KINDS and token.kind != "user-request":
                    violations.append(Violation(
                        code="hermes-forwarded-without-decision",
                        action="ForwardInboxState",
                        actor=token.sender,
                        token_path=str(token.path),
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
    for place_name, tokens in marking.tokens_by_place.items():
        for token in tokens:
            if token.kind in IMPLEMENTATION_KINDS:
                owner = token.sender
                expected = "Vulcan"
                if owner and owner.lower() != expected.lower() and owner != "opencode":
                    violations.append(Violation(
                        code="wrong-implementation-owner",
                        action="CompleteImplementation",
                        actor=owner,
                        token_path=str(token.path),
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
    codex_actors = frozenset({"Codex", "codex"})
    for place_name, tokens in marking.tokens_by_place.items():
        for token in tokens:
            is_codex_actor = (
                token.sender in codex_actors
                or token.origin in codex_actors
                or (token.acting_as and token.acting_as in codex_actors)
            )
            if is_codex_actor and not token.delegated_operator:
                violations.append(Violation(
                    code="delegated-operator-missing",
                    action="MediateAccess",
                    actor=token.sender,
                    token_path=str(token.path),
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
    pi_identifiers = frozenset({"pi", "Hermes", "hermes"})
    codex_actors = frozenset({"Codex", "codex"})
    for place_name, tokens in marking.tokens_by_place.items():
        for token in tokens:
            claims_pi_origin = (
                token.origin in pi_identifiers
                or token.sender in pi_identifiers
                or (token.acting_as and token.acting_as in pi_identifiers)
            )
            is_codex_produced = (
                token.delegated_operator in codex_actors
                or token.provenance_has_codex()
            )
            if claims_pi_origin and is_codex_produced:
                violations.append(Violation(
                    code="codex-as-pi-identity-collapse",
                    action="ClaimPiAuthority",
                    actor=token.sender,
                    token_path=str(token.path),
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


ALL_GUARDS = [
    ("hermes-forwarded-without-decision", check_hermes_forwarded_without_decision),
    ("wrong-implementation-owner", check_wrong_implementation_owner),
    ("delegated-operator-missing", check_delegated_operator_missing),
    ("codex-as-pi-identity-collapse", check_codex_as_pi_identity_collapse),
]


def run_all_guards(marking: Marking) -> list[Violation]:
    violations: list[Violation] = []
    for _name, guard_fn in ALL_GUARDS:
        violations.extend(guard_fn(marking))
    return violations
