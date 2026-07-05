from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation, ViolationCode
from projectkoios.bootstrap.harness.handoffs.appender import append_violations


def test__ViolationAppender__append_to_file__adds_violation_section(tmp_path: Path) -> None:
    """Validate append_violations adds a violations section when missing."""
    # Handoff file fixture starts without an existing violations section.
    handoff_file: Path = tmp_path / "handoff.md"
    handoff_file.write_text("# Test handoff\n\nSome content.\n", encoding="utf-8")

    # Violation fixture represents the block appended to the handoff file.
    violation: Violation = Violation(
        code=ViolationCode.WRONG_IMPLEMENTATION_OWNER,
        actor="Hermes",
        path=handoff_file,
        reason="Only Vulcan may produce implementation reports.",
    )
    append_violations(handoff_file, [violation])

    # Content captures the mutated handoff file for section assertions.
    content: str = handoff_file.read_text(encoding="utf-8")
    assert "## Violations" in content
    assert "code: wrong-implementation-owner" in content


def test__ViolationAppender__append_to_file__appends_to_existing_violations(
    tmp_path: Path,
) -> None:
    """Validate append_violations reuses an existing violations section."""
    # Handoff file fixture already contains a violations section.
    handoff_file: Path = tmp_path / "handoff.md"
    handoff_file.write_text("# Test\n\n## Violations\n\n- old violation\n", encoding="utf-8")

    # Violation fixture represents the new violation block being appended.
    violation: Violation = Violation(
        code=ViolationCode.DELEGATED_OPERATOR_MISSING,
        actor="Codex",
        path=handoff_file,
        reason="Missing delegated operator.",
    )
    append_violations(handoff_file, [violation])

    # Content captures the mutated handoff file for duplicate-section assertions.
    content: str = handoff_file.read_text(encoding="utf-8")
    assert content.count("## Violations") == 1
    assert "delegated-operator-missing" in content


def test__ViolationAppender__append_to_file__does_nothing_for_empty_list(
    tmp_path: Path,
) -> None:
    """Validate append_violations leaves files unchanged for empty input."""
    # Original content is the expected stable file content after a no-op append.
    original: str = "# Test handoff\n\nSome content.\n"
    # Handoff file fixture starts with original content and no violations.
    handoff_file: Path = tmp_path / "handoff.md"
    handoff_file.write_text(original, encoding="utf-8")

    append_violations(handoff_file, [])

    assert handoff_file.read_text(encoding="utf-8") == original
