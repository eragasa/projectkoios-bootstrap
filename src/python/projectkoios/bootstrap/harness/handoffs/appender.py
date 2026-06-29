from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.violation import Violation


VIOLATIONS_HEADING = "## Violations"


def append_violations(path: Path, violations: list[Violation]) -> None:
    if not violations:
        return

    content = path.read_text(encoding="utf-8")
    block = _build_block(violations)
    new_content = _insert_or_append(content, block)
    path.write_text(new_content, encoding="utf-8")


def _build_block(violations: list[Violation]) -> str:
    lines: list[str] = []
    for v in violations:
        lines.append("")
        lines.append(v.to_markdown_block())
    return "".join(lines)


def _insert_or_append(content: str, block: str) -> str:
    if VIOLATIONS_HEADING in content:
        return content + block
    return content.rstrip("\n") + "\n\n" + VIOLATIONS_HEADING + "\n" + block
