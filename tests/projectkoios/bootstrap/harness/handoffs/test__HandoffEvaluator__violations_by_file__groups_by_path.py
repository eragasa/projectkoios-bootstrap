from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.evaluator import HandoffEvaluator


def test__HandoffEvaluator__violations_by_file__groups_by_path(tmp_path: Path) -> None:
    """Validate violations_by_file groups violations by resolved path."""
    # Evaluator fixture owns grouping behavior for handoff violations.
    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=tmp_path)

    # First violation fixture targets the first handoff path.
    violation_one: Violation = Violation(
        code=ViolationCode.HERMES_FORWARDED_WITHOUT_DECISION,
        actor="Actor",
        path=tmp_path / "a.md",
        reason="Reason A",
    )
    # Second violation fixture targets the same handoff path as the first.
    violation_two: Violation = Violation(
        code=ViolationCode.WRONG_IMPLEMENTATION_OWNER,
        actor="Actor",
        path=tmp_path / "a.md",
        reason="Reason B",
    )
    # Third violation fixture targets a distinct handoff path.
    violation_three: Violation = Violation(
        code=ViolationCode.DELEGATED_OPERATOR_MISSING,
        actor="Actor",
        path=tmp_path / "b.md",
        reason="Reason C",
    )

    # Mapping under assertion groups all violations by resolved file path.
    by_file: dict[Path, list[Violation]] = evaluator.violations_by_file(
        [violation_one, violation_two, violation_three]
    )

    assert len(by_file) == 2
    # Expected first resolved path receives the first two violations.
    path_a: Path = (tmp_path / "a.md").resolve()
    # Expected second resolved path receives only the third violation.
    path_b: Path = (tmp_path / "b.md").resolve()
    assert len(by_file[path_a]) == 2
    assert len(by_file[path_b]) == 1
