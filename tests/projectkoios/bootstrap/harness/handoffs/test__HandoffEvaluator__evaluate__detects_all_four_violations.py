from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.marking import HandoffMarking
from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.evaluator import HandoffEvaluator


def _make_repo(tmp_path: Path) -> Path:
    """Create a repository fixture with archived handoff directories."""
    # Root is the repository fixture evaluated by handoff guards.
    root: Path = tmp_path / "repo"
    # Subdirectory paths represent each archived handoff inbox.
    subdirectory: str
    for subdirectory in (
        "docs/archive/handoffs/archon",
        "docs/archive/handoffs/opencode",
        "docs/archive/handoffs/pi",
        "docs/archive/handoffs/goose",
    ):
        (root / subdirectory).mkdir(parents=True)
    return root


def _write(root: Path, rel: str, content: str) -> None:
    """Write a handoff fixture file relative to the repository root."""
    # Path is the concrete handoff fixture location to write.
    path: Path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test__HandoffEvaluator__build_marking__includes_all_directories(tmp_path: Path) -> None:
    """Validate marking construction includes populated handoff directories."""
    # Root is the repository fixture evaluated by handoff guards.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/spec.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n# Architecture spec\n",
    )
    _write(
        root,
        "docs/archive/handoffs/opencode/report.md",
        "Origin: Vulcan\nFrom: Vulcan\nTo: Hermes\n\n# Implementation report\n",
    )

    # Evaluator builds the Petri-net marking for archived handoffs.
    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=root)
    # Marking captures parsed artifacts grouped by inbox place.
    marking: HandoffMarking = evaluator.build_marking()

    assert "archon_inbox" in marking.tokens_by_place
    assert "opencode_inbox" in marking.tokens_by_place


def test__HandoffEvaluator__evaluate__valid_athena_to_vulcan_passes_all_guards(
    tmp_path: Path,
) -> None:
    """Validate valid Athena-to-Vulcan handoffs pass all guards."""
    # Root is the repository fixture evaluated by handoff guards.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/archon/spec.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\nStatus: active\n\n"
        "# Implementation brief: evaluator\n",
    )

    # Evaluator runs all handoff guard checks.
    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=root)
    # Violations are the guard failures under assertion.
    violations: list[Violation] = evaluator.evaluate()

    assert len(violations) == 0


def test__HandoffEvaluator__evaluate__hermes_impl_report_is_wrong_implementation_owner(
    tmp_path: Path,
) -> None:
    """Validate Hermes implementation reports trigger owner violations."""
    # Root is the repository fixture evaluated by handoff guards.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/opencode/hermes-impl.md",
        "Origin: Hermes\nFrom: Hermes\nTo: Athena\nStatus: active\n\n"
        "# Implementation report: done by Hermes\n",
    )
    _write(
        root,
        "docs/archive/handoffs/archon/brief.md",
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\nStatus: active\n\n"
        "# Implementation brief: evaluator\n",
    )

    # Evaluator runs all handoff guard checks.
    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=root)
    # Violations are the guard failures under assertion.
    violations: list[Violation] = evaluator.evaluate()

    # Codes provide a concise view of emitted violation kinds.
    codes: set[ViolationCode] = {violation.code for violation in violations}
    assert ViolationCode.WRONG_IMPLEMENTATION_OWNER in codes


def test__HandoffEvaluator__evaluate__codex_with_delegated_provenance_passes(
    tmp_path: Path,
) -> None:
    """Validate Codex handoffs with delegated provenance pass that guard."""
    # Root is the repository fixture evaluated by handoff guards.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/pi/codex-routing.md",
        "Origin: pi\nFrom: Codex\nTo: Athena\nStatus: active\n"
        "Delegated-Operator: Codex\n\n"
        "# Routing decision: mediated\n",
    )

    # Evaluator runs all handoff guard checks.
    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=root)
    # Violations are the guard failures under assertion.
    violations: list[Violation] = evaluator.evaluate()

    assert ViolationCode.DELEGATED_OPERATOR_MISSING not in {violation.code for violation in violations}


def test__HandoffEvaluator__evaluate__codex_without_delegated_provenance_is_violation(
    tmp_path: Path,
) -> None:
    """Validate Codex handoffs without delegated provenance are violations."""
    # Root is the repository fixture evaluated by handoff guards.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/pi/codex-routing.md",
        "Origin: Codex\nFrom: Codex\nTo: Athena\nStatus: active\n\n"
        "# Routing decision: missing provenance\n",
    )

    # Evaluator runs all handoff guard checks.
    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=root)
    # Violations are the guard failures under assertion.
    violations: list[Violation] = evaluator.evaluate()

    # Codes provide a concise view of emitted violation kinds.
    codes: set[ViolationCode] = {violation.code for violation in violations}
    assert ViolationCode.DELEGATED_OPERATOR_MISSING in codes


def test__HandoffEvaluator__evaluate__codex_claiming_pi_is_identity_collapse(
    tmp_path: Path,
) -> None:
    """Validate Codex-as-pi claims are identity-collapse violations."""
    # Root is the repository fixture evaluated by handoff guards.
    root: Path = _make_repo(tmp_path)
    _write(
        root,
        "docs/archive/handoffs/pi/codex-pi.md",
        "Origin: pi\nFrom: Codex\nTo: Vulcan\nStatus: active\n"
        "Delegated-Operator: Codex\n\n"
        "# Implementation brief: from Codex as pi\n",
    )

    # Evaluator runs all handoff guard checks.
    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=root)
    # Violations are the guard failures under assertion.
    violations: list[Violation] = evaluator.evaluate()

    # Codes provide a concise view of emitted violation kinds.
    codes: set[ViolationCode] = {violation.code for violation in violations}
    assert ViolationCode.CODEX_AS_PI_IDENTITY_COLLAPSE in codes
