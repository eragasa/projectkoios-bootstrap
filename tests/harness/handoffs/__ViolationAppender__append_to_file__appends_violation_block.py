from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.appender import append_violations


def test__ViolationAppender__append_to_file__adds_violation_section(tmp_path: Path) -> None:
    f = tmp_path / "handoff.md"
    f.write_text("# Test handoff\n\nSome content.\n", encoding="utf-8")

    v = Violation(
        code=ViolationCode.WRONG_IMPLEMENTATION_OWNER,
        action="CompleteImplementation",
        actor="Hermes",
        path=f,
        reason="Only Vulcan may produce implementation reports.",
    )
    append_violations(f, [v])

    content = f.read_text(encoding="utf-8")
    assert "## Violations" in content
    assert "code: wrong-implementation-owner" in content


def test__ViolationAppender__append_to_file__appends_to_existing_violations(
    tmp_path: Path,
) -> None:
    f = tmp_path / "handoff.md"
    f.write_text("# Test\n\n## Violations\n\n- old violation\n", encoding="utf-8")

    v = Violation(
        code=ViolationCode.DELEGATED_OPERATOR_MISSING,
        action="MediateAccess",
        actor="Codex",
        path=f,
        reason="Missing delegated operator.",
    )
    append_violations(f, [v])

    content = f.read_text(encoding="utf-8")
    assert content.count("## Violations") == 1
    assert "delegated-operator-missing" in content


def test__ViolationAppender__append_to_file__does_nothing_for_empty_list(
    tmp_path: Path,
) -> None:
    original = "# Test handoff\n\nSome content.\n"
    f = tmp_path / "handoff.md"
    f.write_text(original, encoding="utf-8")

    append_violations(f, [])

    assert f.read_text(encoding="utf-8") == original
