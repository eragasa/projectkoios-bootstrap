from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation


VIOLATIONS_HEADING: str = "## Violations"
"""Markdown heading that separates violations from original handoff content."""


def append_violations(path: Path, violations: list[Violation]) -> None:
    """Append one or more violations to a handoff file."""
    if not violations:
        return

    content: str = path.read_text(encoding="utf-8")
    block: str = build_block(violations)
    new_content: str = insert_or_append(content, block)
    path.write_text(new_content, encoding="utf-8")


def build_block(violations: list[Violation]) -> str:
    """Render a list of violations into a Markdown string for insertion."""
    lines: list[str] = []
    violation: Violation
    for violation in violations:
        lines.append("")
        lines.append(violation.to_markdown_block())
    return "".join(lines)


def insert_or_append(content: str, block: str) -> str:
    """Insert *block* under an existing violations heading, or append at EOF."""
    heading_pos: int = content.find(VIOLATIONS_HEADING)
    if heading_pos != -1:
        after_heading: int = heading_pos + len(VIOLATIONS_HEADING)
        return content[:after_heading] + "\n" + block.lstrip("\n") + content[after_heading:]
    return content.rstrip("\n") + "\n\n" + VIOLATIONS_HEADING + "\n" + block.lstrip("\n")
