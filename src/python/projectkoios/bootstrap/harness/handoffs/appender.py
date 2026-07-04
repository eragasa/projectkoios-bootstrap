from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation


VIOLATIONS_HEADING: str = "## Violations"
"""Markdown heading that separates violations from original handoff content."""


def append_violations(path: Path, violations: list[Violation]) -> None:
    """Append one or more violations to a handoff file."""
    if not violations:
        return

    # Content is the original handoff Markdown that will receive violation notes.
    content: str = path.read_text(encoding="utf-8")
    # Block is the rendered Markdown fragment for the new violations.
    block: str = build_block(violations)
    # New content is either inserted below the existing heading or appended at EOF.
    new_content: str = insert_or_append(content, block)
    path.write_text(new_content, encoding="utf-8")


def build_block(violations: list[Violation]) -> str:
    """Render a list of violations into a Markdown string for insertion."""
    # Lines accumulates pre-rendered violation blocks with leading separators.
    lines: list[str] = []
    violation: Violation
    for violation in violations:
        lines.append("")
        lines.append(violation.to_markdown_block())
    return "".join(lines)


def insert_or_append(content: str, block: str) -> str:
    """Insert *block* under an existing violations heading, or append at EOF."""
    # Heading position determines whether to insert into or create the section.
    heading_pos: int = content.find(VIOLATIONS_HEADING)
    if heading_pos != -1:
        # After-heading index preserves existing section content after inserted violations.
        after_heading: int = heading_pos + len(VIOLATIONS_HEADING)
        return content[:after_heading] + "\n" + block.lstrip("\n") + content[after_heading:]
    return content.rstrip("\n") + "\n\n" + VIOLATIONS_HEADING + "\n" + block.lstrip("\n")
