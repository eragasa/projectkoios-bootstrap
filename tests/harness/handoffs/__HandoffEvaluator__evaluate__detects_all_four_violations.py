from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.handoffs.evaluator import HandoffEvaluator


def _make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for sub in ("archon/handoffs", "opencode/handoffs", "pi/handoffs", "goose/handoffs"):
        (root / sub).mkdir(parents=True)
    return root


def _write(root: Path, rel: str, content: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test__HandoffEvaluator__build_marking__includes_all_directories(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _write(root, "archon/handoffs/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n# Architecture spec\n")
    _write(root, "opencode/handoffs/report.md",
           "Origin: Vulcan\nFrom: Vulcan\nTo: Hermes\n\n# Implementation report\n")

    evaluator = HandoffEvaluator(repo_root=root)
    marking = evaluator.build_marking()

    assert "archon_inbox" in marking.tokens_by_place
    assert "opencode_inbox" in marking.tokens_by_place


def test__HandoffEvaluator__evaluate__valid_athena_to_vulcan_passes_all_guards(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "archon/handoffs/spec.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\nStatus: active\n\n"
           "# Implementation brief: evaluator\n")

    evaluator = HandoffEvaluator(repo_root=root)
    violations = evaluator.evaluate()

    assert len(violations) == 0


def test__HandoffEvaluator__evaluate__hermes_impl_report_is_wrong_implementation_owner(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "opencode/handoffs/hermes-impl.md",
           "Origin: Hermes\nFrom: Hermes\nTo: Athena\nStatus: active\n\n"
           "# Implementation report: done by Hermes\n")
    _write(root, "archon/handoffs/brief.md",
           "Origin: Athena\nFrom: Athena\nTo: Vulcan\nStatus: active\n\n"
           "# Implementation brief: evaluator\n")

    evaluator = HandoffEvaluator(repo_root=root)
    violations = evaluator.evaluate()

    codes = {v.code for v in violations}
    assert "wrong-implementation-owner" in codes


def test__HandoffEvaluator__evaluate__codex_with_delegated_provenance_passes(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "pi/handoffs/codex-routing.md",
           "Origin: pi\nFrom: Codex\nTo: Athena\nStatus: active\n"
           "Delegated-Operator: Codex\n\n"
           "# Routing decision: mediated\n")

    evaluator = HandoffEvaluator(repo_root=root)
    violations = evaluator.evaluate()

    assert "delegated-operator-missing" not in {v.code for v in violations}


def test__HandoffEvaluator__evaluate__codex_without_delegated_provenance_is_violation(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "pi/handoffs/codex-routing.md",
           "Origin: Codex\nFrom: Codex\nTo: Athena\nStatus: active\n\n"
           "# Routing decision: missing provenance\n")

    evaluator = HandoffEvaluator(repo_root=root)
    violations = evaluator.evaluate()

    codes = {v.code for v in violations}
    assert "delegated-operator-missing" in codes


def test__HandoffEvaluator__evaluate__codex_claiming_pi_is_identity_collapse(
    tmp_path: Path,
) -> None:
    root = _make_repo(tmp_path)
    _write(root, "pi/handoffs/codex-pi.md",
           "Origin: pi\nFrom: Codex\nTo: Vulcan\nStatus: active\n"
           "Delegated-Operator: Codex\n\n"
           "# Implementation brief: from Codex as pi\n")

    evaluator = HandoffEvaluator(repo_root=root)
    violations = evaluator.evaluate()

    codes = {v.code for v in violations}
    assert "codex-as-pi-identity-collapse" in codes
