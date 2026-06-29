from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation
from projectkoios.bootstrap.harness.actions.appender import ViolationAppender


def test__ViolationAppender__append_to_file__adds_violation_section(tmp_path: Path) -> None:
    f = tmp_path / "handoff.md"
    f.write_text("# Test handoff\n\nSome content.\n", encoding="utf-8")

    v = Violation(
        code="wrong-implementation-owner",
        action="CompleteImplementation",
        actor="Hermes",
        token_path=str(f),
        reason="Only Vulcan may produce implementation reports.",
    )
    appender = ViolationAppender()
    appender.append(f, [v])

    content = f.read_text(encoding="utf-8")
    assert "## Violations" in content
    assert "code: wrong-implementation-owner" in content


def test__ViolationAppender__append_to_file__appends_to_existing_violations(tmp_path: Path) -> None:
    f = tmp_path / "handoff.md"
    f.write_text("# Test\n\n## Violations\n\n- old violation\n", encoding="utf-8")

    v = Violation(
        code="delegated-operator-missing",
        action="MediateAccess",
        actor="Codex",
        token_path=str(f),
        reason="Missing delegated operator.",
    )
    appender = ViolationAppender()
    appender.append(f, [v])

    content = f.read_text(encoding="utf-8")
    assert content.count("## Violations") == 1
    assert "delegated-operator-missing" in content


def test__ViolationAppender__append_to_file__does_nothing_for_empty_list(tmp_path: Path) -> None:
    original = "# Test handoff\n\nSome content.\n"
    f = tmp_path / "handoff.md"
    f.write_text(original, encoding="utf-8")

    appender = ViolationAppender()
    appender.append(f, [])

    assert f.read_text(encoding="utf-8") == original


def test__ViolationAppender__dry_run__does_not_modify_file(tmp_path: Path) -> None:
    original = "# Test handoff\n\nSome content.\n"
    f = tmp_path / "handoff.md"
    f.write_text(original, encoding="utf-8")

    v = Violation(
        code="test-code",
        action="TestAction",
        actor="Test",
        token_path=str(f),
        reason="Test reason.",
    )
    appender = ViolationAppender(dry_run=True)
    appender.append(f, [v])

    assert f.read_text(encoding="utf-8") == original
