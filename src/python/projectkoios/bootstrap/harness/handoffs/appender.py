from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation


VIOLATIONS_HEADING = "## Violations"
"""Markdown heading that separates violations from original handoff content."""


def append_violations(path: Path, violations: list[Violation]) -> None:
    """Append one or more violations to a handoff file under a ``## Violations`` heading.

    If the heading already exists, violations are inserted immediately after it
    (before any existing content under that heading). Otherwise the heading and
    violations are appended at the end of the file.

    This is the only mutation point in the evaluator pipeline. Callers should
    provide a ``--dry-run`` option (handled at the CLI level) to skip writing.
    """
    if not violations:
        return

    content = path.read_text(encoding="utf-8")
    block = _build_block(violations)
    new_content = _insert_or_append(content, block)
    path.write_text(new_content, encoding="utf-8")


def _build_block(violations: list[Violation]) -> str:
    """Render a list of violations into a Markdown string for insertion."""
    lines: list[str] = []
    for v in violations:
        lines.append("")
        lines.append(v.to_markdown_block())
    return "".join(lines)


def _insert_or_append(content: str, block: str) -> str:
    """Insert *block* under an existing ``## Violations`` heading, or append at EOF.

    When the heading exists, the block is placed on the line immediately after it,
    pushing any existing content below. When it doesn't exist, the block is appended
    with a new heading.
    """
    heading_pos = content.find(VIOLATIONS_HEADING)
    if heading_pos != -1:
        after_heading = heading_pos + len(VIOLATIONS_HEADING)
        return content[:after_heading] + "\n" + block.lstrip("\n") + content[after_heading:]
    return content.rstrip("\n") + "\n\n" + VIOLATIONS_HEADING + "\n" + block.lstrip("\n")
