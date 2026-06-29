from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.handoffs.parser import HandoffParser


VALID_HANDOFF = """\
Origin: Athena
Created: 2026-06-29 12:00
From: Athena
To: Vulcan
Status: active
Scope: projectkoios-bootstrap
Repository: /Users/eugene/repos/projectkoios-bootstrap

# Architecture spec: test

Implementation brief for read-only evaluator.
"""

MISSING_FIELDS = """\
# No headers here

Just content.
"""

PARTIAL_HEADERS = """\
Origin: Hermes
From: Hermes

# Routing decision

No To field.
"""


def test__HandoffParser__parse_file__parses_valid_frontmatter(tmp_path: Path) -> None:
    f = tmp_path / "handoff.md"
    f.write_text(VALID_HANDOFF, encoding="utf-8")

    parser = HandoffParser()
    token = parser.parse_file(f)

    assert token is not None
    assert token.origin == "Athena"
    assert token.sender == "Athena"
    assert token.recipient == "Vulcan"
    assert token.status == "active"
    assert token.kind == "architecture-spec"


def test__HandoffParser__parse_file__returns_none_for_no_frontmatter(tmp_path: Path) -> None:
    f = tmp_path / "handoff.md"
    f.write_text(MISSING_FIELDS, encoding="utf-8")

    parser = HandoffParser()
    token = parser.parse_file(f)

    assert token is None


def test__HandoffParser__parse_file__parses_partial_headers(tmp_path: Path) -> None:
    f = tmp_path / "partial.md"
    f.write_text(PARTIAL_HEADERS, encoding="utf-8")

    parser = HandoffParser()
    token = parser.parse_file(f)

    assert token is not None
    assert token.origin == "Hermes"
    assert token.sender == "Hermes"
    assert token.recipient == ""


def test__HandoffParser__parse_file__nonexistent_file(tmp_path: Path) -> None:
    parser = HandoffParser()
    token = parser.parse_file(tmp_path / "nonexistent.md")
    assert token is None


def test__HandoffParser__parse_file__skips_non_markdown_files(tmp_path: Path) -> None:
    f = tmp_path / "notes.txt"
    f.write_text("Origin: Athena\nFrom: Athena\nTo: Vulcan", encoding="utf-8")

    parser = HandoffParser()
    token = parser.parse_file(f)
    assert token is not None


def test__HandoffParser__parse_directory__aggregates_tokens(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text(
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n# Spec\n", encoding="utf-8"
    )
    (tmp_path / "b.md").write_text(
        "Origin: Vulcan\nFrom: Vulcan\nTo: Hermes\n\n# Report\n", encoding="utf-8"
    )

    parser = HandoffParser()
    tokens = parser.parse_directory(tmp_path)

    assert len(tokens) == 2
    kinds = {t.kind for t in tokens}
    assert "implementation-report" in kinds
    assert "architecture-spec" in kinds or "implementation-brief" in kinds
