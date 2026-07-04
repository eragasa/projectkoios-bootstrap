from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.validation.harnesses import (
    Severity,
    ValidationResult,
    validate_harnesses,
)


ROOT_AGENTS = """# Root

## Harnesses
archon opencode goose pi
## Meta-harness
## Directions for all harnesses
## Directions for Hermes (pi)
## Directions for Athena (archon)
## Directions for Vulcan (opencode)
## ADR file convention
"""

PI_AGENTS = """# Pi

## Direct capabilities
## Delegation
## Scope
See `opencode/AGENTS.md` and `goose/AGENTS.md`.
## Reference
"""

OPENCODE_AGENTS = """# Opencode

## Workspace layout
Read `../maps/repositories.md` and `../maps/packages.md`.
## Rules
- `rules/build.md`
- `rules/validation.md`
- `rules/specification_gate.md`
- `rules/handoff.md`
- `rules/tool_policy.md`
- `rules/session.md`
## Checklists
- `checklists/multi-repo-execution-readiness.md`
## Setup per repo
## Common commands
## Conventions
"""

GOOSE_AGENTS = """# Goose

## Role identity
## Maps
See `../maps/vault_paths.md`.
## Vault rules
## Handoff support
"""

META_HARNESS = """# Meta

## Purpose
## Skill model
## Anti-patterns
"""

HARNESS_ROUTING = """# Routing

## Harness definitions
Athena Vulcan Koios pi
## Rules
## Output requirement
"""


def write(path: Path, text: str = "x") -> None:
    """Write fixture text to a path, creating parent directories first."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(root: Path) -> None:
    """Create a minimal valid harness repository fixture."""
    write(root / "AGENTS.md", ROOT_AGENTS)
    write(root / "pi/AGENTS.md", PI_AGENTS)
    write(root / "opencode/AGENTS.md", OPENCODE_AGENTS)
    write(root / "goose/AGENTS.md", GOOSE_AGENTS)
    write(root / "docs/meta-harness.md", META_HARNESS)
    write(root / "archon/prompts/harness-routing.md", HARNESS_ROUTING)
    write(root / "archon/skills/.archon/config.yaml")
    write(root / "maps/repositories.md")
    write(root / "maps/packages.md")
    write(root / "maps/vault_paths.md")
    write(root / "src/python/projectkoios/bootstrap/commands/init.py")
    write(root / "src/python/projectkoios/bootstrap/commands/install.py")
    write(root / "src/python/projectkoios/bootstrap/models.py")

    # Rule files satisfy the opencode AGENTS.md references.
    name: str
    for name in (
        "build",
        "validation",
        "specification_gate",
        "handoff",
        "tool_policy",
        "session",
    ):
        write(root / f"opencode/rules/{name}.md")
    write(root / "opencode/checklists/multi-repo-execution-readiness.md")

    # Global harness example configs satisfy bootstrap config assumptions.
    harness: str
    for harness in ("pi", "archon", "opencode", "goose"):
        write(root / f"agents/global/{harness}/config.example")
    write(root / "agents/global/archon/config.yaml.example")

    # Workflow files satisfy required Archon workflow checks.
    workflow: str
    for workflow in (
        "archon-piv-loop",
        "archon-architect",
        "create-adr",
        "design-review",
        "plan-feature",
    ):
        write(root / f"archon/workflows/{workflow}.yaml")


def messages(result: ValidationResult) -> list[str]:
    """Return validation finding messages in reported order."""
    return [finding.message for finding in result.findings]


def test__validate_harnesses__success_on_valid_fixture(tmp_path: Path) -> None:
    """Validate that a complete minimal harness fixture passes checks."""
    make_repo(tmp_path)

    # Result captures all harness validation findings for the fixture.
    result: ValidationResult = validate_harnesses(tmp_path)

    assert result.count(Severity.ERROR) == 0
    assert result.exit_code() == 0


def test__validate_harnesses__missing_canonical_file(tmp_path: Path) -> None:
    """Validate that a missing canonical harness file is reported."""
    make_repo(tmp_path)
    (tmp_path / "pi/AGENTS.md").unlink()

    # Result captures the expected missing-file validation error.
    result: ValidationResult = validate_harnesses(tmp_path)

    assert "missing canonical harness file" in messages(result)
    assert result.exit_code() == 1


def test__validate_harnesses__broken_relative_reference(tmp_path: Path) -> None:
    """Validate that a broken repo-local reference is reported."""
    make_repo(tmp_path)
    (tmp_path / "opencode/AGENTS.md").write_text(
        OPENCODE_AGENTS.replace("../maps/packages.md", "../maps/missing.md"),
        encoding="utf-8",
    )

    # Result captures the expected broken-reference validation error.
    result: ValidationResult = validate_harnesses(tmp_path)

    assert any("broken repo-local reference" in message for message in messages(result))
    assert result.exit_code() == 1


def test__validate_harnesses__missing_required_heading(tmp_path: Path) -> None:
    """Validate that a missing required heading is reported."""
    make_repo(tmp_path)
    (tmp_path / "goose/AGENTS.md").write_text(
        GOOSE_AGENTS.replace("## Vault rules\n", ""),
        encoding="utf-8",
    )

    # Result captures the expected missing-heading validation error.
    result: ValidationResult = validate_harnesses(tmp_path)

    assert "missing required heading '## Vault rules'" in messages(result)
    assert result.exit_code() == 1


def test__validate_harnesses__missing_opencode_rule_reference(
    tmp_path: Path,
) -> None:
    """Validate that a missing opencode rule reference is reported."""
    make_repo(tmp_path)
    (tmp_path / "opencode/rules/session.md").unlink()

    # Result captures the expected missing-rule validation error.
    result: ValidationResult = validate_harnesses(tmp_path)

    assert "missing opencode rule reference 'rules/session.md'" in messages(result)
    assert result.exit_code() == 1


def test__validate_harnesses__missing_archon_workflow(tmp_path: Path) -> None:
    """Validate that a missing required Archon workflow is reported."""
    make_repo(tmp_path)
    (tmp_path / "archon/workflows/archon-piv-loop.yaml").unlink()

    # Result captures the expected missing-workflow validation error.
    result: ValidationResult = validate_harnesses(tmp_path)

    assert "missing repo-local Archon workflow" in messages(result)
    assert result.exit_code() == 1


def test__validate_harnesses__missing_archon_project_config(tmp_path: Path) -> None:
    """Validate that a missing Archon project config is reported."""
    make_repo(tmp_path)
    (tmp_path / "archon/skills/.archon/config.yaml").unlink()

    # Result captures the expected bootstrap-assumption validation error.
    result: ValidationResult = validate_harnesses(tmp_path)

    assert "missing path assumed by bootstrap CLI code" in messages(result)
    assert result.exit_code() == 1
