from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.evaluator import HandoffEvaluator


def test__HandoffEvaluator__violations_by_file__groups_by_path(tmp_path: Path) -> None:
    evaluator = HandoffEvaluator(repo_root=tmp_path)

    v1 = Violation(
        code=ViolationCode.HERMES_FORWARDED_WITHOUT_DECISION,
        action="Action",
        actor="Actor",
        path=tmp_path / "a.md",
        reason="Reason A",
    )
    v2 = Violation(
        code=ViolationCode.WRONG_IMPLEMENTATION_OWNER,
        action="Action",
        actor="Actor",
        path=tmp_path / "a.md",
        reason="Reason B",
    )
    v3 = Violation(
        code=ViolationCode.DELEGATED_OPERATOR_MISSING,
        action="Action",
        actor="Actor",
        path=tmp_path / "b.md",
        reason="Reason C",
    )

    by_file = evaluator.violations_by_file([v1, v2, v3])

    assert len(by_file) == 2
    path_a = (tmp_path / "a.md").resolve()
    path_b = (tmp_path / "b.md").resolve()
    assert len(by_file[path_a]) == 2
    assert len(by_file[path_b]) == 1
