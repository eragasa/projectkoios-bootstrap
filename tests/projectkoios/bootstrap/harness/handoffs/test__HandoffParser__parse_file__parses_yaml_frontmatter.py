from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.harness.data.artifact import HandoffArtifact
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

Architecture specification for read-only evaluator.
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
    """Validate parser converts a complete handoff file into an artifact."""
    # File path is the handoff fixture parsed by the parser.
    file_path: Path = tmp_path / "handoff.md"
    file_path.write_text(VALID_HANDOFF, encoding="utf-8")

    # Parser is the unit under test for handoff artifact extraction.
    parser: HandoffParser = HandoffParser()
    # Token is the parsed artifact returned from the handoff file.
    token: HandoffArtifact | None = parser.parse_file(file_path)

    assert token is not None
    assert token.origin == "Athena"
    assert token.sender == "Athena"
    assert token.recipient == "Vulcan"
    assert token.kind == "architecture-spec"


def test__HandoffParser__parse_file__returns_none_for_no_frontmatter(tmp_path: Path) -> None:
    """Validate parser returns none when no handoff headers exist."""
    # File path is the handoff fixture parsed by the parser.
    file_path: Path = tmp_path / "handoff.md"
    file_path.write_text(MISSING_FIELDS, encoding="utf-8")

    # Parser is the unit under test for handoff artifact extraction.
    parser: HandoffParser = HandoffParser()
    # Token is absent because the fixture has no handoff headers.
    token: HandoffArtifact | None = parser.parse_file(file_path)

    assert token is None


def test__HandoffParser__parse_file__parses_partial_headers(tmp_path: Path) -> None:
    """Validate parser preserves partial handoff headers with blank fields."""
    # File path is the handoff fixture parsed by the parser.
    file_path: Path = tmp_path / "partial.md"
    file_path.write_text(PARTIAL_HEADERS, encoding="utf-8")

    # Parser is the unit under test for handoff artifact extraction.
    parser: HandoffParser = HandoffParser()
    # Token is the parsed artifact returned from partial handoff headers.
    token: HandoffArtifact | None = parser.parse_file(file_path)

    assert token is not None
    assert token.origin == "Hermes"
    assert token.sender == "Hermes"
    assert token.recipient == ""


def test__HandoffParser__parse_file__nonexistent_file(tmp_path: Path) -> None:
    """Validate parser returns none for missing handoff files."""
    # Parser is the unit under test for handoff artifact extraction.
    parser: HandoffParser = HandoffParser()
    # Token is absent because the target file does not exist.
    token: HandoffArtifact | None = parser.parse_file(tmp_path / "nonexistent.md")
    assert token is None


def test__HandoffParser__parse_file__parses_any_file_regardless_of_extension(tmp_path: Path) -> None:
    """Validate parser accepts handoff headers in non-Markdown files."""
    # File path is the non-Markdown handoff fixture parsed by the parser.
    file_path: Path = tmp_path / "notes.txt"
    file_path.write_text("Origin: Athena\nFrom: Athena\nTo: Vulcan", encoding="utf-8")

    # Parser is the unit under test for handoff artifact extraction.
    parser: HandoffParser = HandoffParser()
    # Token is the parsed artifact returned from the handoff file.
    token: HandoffArtifact | None = parser.parse_file(file_path)
    assert token is not None


def test__HandoffParser__parse_directory__aggregates_tokens(tmp_path: Path) -> None:
    """Validate parser aggregates handoff artifacts from a directory."""
    (tmp_path / "a.md").write_text(
        "Origin: Athena\nFrom: Athena\nTo: Vulcan\n\n# Spec\n", encoding="utf-8"
    )
    (tmp_path / "b.md").write_text(
        "Origin: Vulcan\nFrom: Vulcan\nTo: Hermes\n\n# Report\n", encoding="utf-8"
    )

    # Parser is the unit under test for directory artifact extraction.
    parser: HandoffParser = HandoffParser()
    # Tokens are the parsed artifacts returned from the directory.
    tokens: list[HandoffArtifact] = parser.parse_directory(tmp_path)

    assert len(tokens) == 2
    # Kinds provide a concise assertion over inferred artifact types.
    kinds: set[str] = {token.kind for token in tokens}
    assert "implementation-report" in kinds
    assert "architecture-spec" in kinds or "implementation-brief" in kinds
