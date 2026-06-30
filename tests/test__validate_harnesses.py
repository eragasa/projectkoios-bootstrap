from __future__ import annotations

from pathlib import Path

from projectkoios.bootstrap.validation.harnesses import (
    Severity,
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
## Routing guide
## Artifact handoff
"""

PI_AGENTS = """# Pi

## Direct capabilities
## Delegation
## Scope
See `opencode/AGENTS.md` and `goose/AGENT.md`.
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

GOOSE_AGENT = """# Goose

## Domain
## Maps
See `../maps/vault_paths.md`.
## Vault rules
## Handoff support
"""

META_HARNESS = """# Meta

## Skill model
## Disagreement handling
## Completion gates
## Escalation rules
"""

HARNESS_ROUTING = """# Routing

## Harness definitions
Athena Vulcan Koios pi
## Rules
## Output requirement
"""


def write(path: Path, text: str = "x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(root: Path) -> None:
    write(root / "AGENTS.md", ROOT_AGENTS)
    write(root / "pi/AGENTS.md", PI_AGENTS)
    write(root / "opencode/AGENTS.md", OPENCODE_AGENTS)
    write(root / "goose/AGENT.md", GOOSE_AGENT)
    write(root / "doc/meta-harness.md", META_HARNESS)
    write(root / "archon/prompts/harness-routing.md", HARNESS_ROUTING)
    write(root / "archon/skills/.archon/config.yaml")
    write(root / "maps/repositories.md")
    write(root / "maps/packages.md")
    write(root / "maps/vault_paths.md")
    write(root / "src/python/projectkoios/bootstrap/commands/init.py")
    write(root / "src/python/projectkoios/bootstrap/commands/install.py")
    write(root / "src/python/projectkoios/bootstrap/models.py")

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

    for harness in ("pi", "archon", "opencode", "goose"):
        write(root / f"agents/global/{harness}/config.example")
    write(root / "agents/global/archon/config.yaml.example")

    for workflow in (
        "archon-piv-loop",
        "archon-architect",
        "create-adr",
        "design-review",
        "plan-feature",
    ):
        write(root / f"archon/workflows/{workflow}.yaml")


def messages(result) -> list[str]:
    return [finding.message for finding in result.findings]


def test__validate_harnesses__success_on_valid_fixture(tmp_path: Path) -> None:
    make_repo(tmp_path)

    result = validate_harnesses(tmp_path)

    assert result.count(Severity.ERROR) == 0
    assert result.exit_code() == 0


def test__validate_harnesses__missing_canonical_file(tmp_path: Path) -> None:
    make_repo(tmp_path)
    (tmp_path / "pi/AGENTS.md").unlink()

    result = validate_harnesses(tmp_path)

    assert "missing canonical harness file" in messages(result)
    assert result.exit_code() == 1


def test__validate_harnesses__broken_relative_reference(tmp_path: Path) -> None:
    make_repo(tmp_path)
    (tmp_path / "opencode/AGENTS.md").write_text(
        OPENCODE_AGENTS.replace("../maps/packages.md", "../maps/missing.md"),
        encoding="utf-8",
    )

    result = validate_harnesses(tmp_path)

    assert any("broken repo-local reference" in message for message in messages(result))
    assert result.exit_code() == 1


def test__validate_harnesses__missing_required_heading(tmp_path: Path) -> None:
    make_repo(tmp_path)
    (tmp_path / "goose/AGENT.md").write_text(
        GOOSE_AGENT.replace("## Vault rules\n", ""),
        encoding="utf-8",
    )

    result = validate_harnesses(tmp_path)

    assert "missing required heading '## Vault rules'" in messages(result)
    assert result.exit_code() == 1


def test__validate_harnesses__does_not_require_plural_goose_agents(
    tmp_path: Path,
) -> None:
    make_repo(tmp_path)

    result = validate_harnesses(tmp_path)

    assert not (tmp_path / "goose/AGENTS.md").exists()
    assert result.count(Severity.ERROR) == 0


def test__validate_harnesses__missing_opencode_rule_reference(
    tmp_path: Path,
) -> None:
    make_repo(tmp_path)
    (tmp_path / "opencode/rules/session.md").unlink()

    result = validate_harnesses(tmp_path)

    assert "missing opencode rule reference 'rules/session.md'" in messages(result)
    assert result.exit_code() == 1


def test__validate_harnesses__missing_archon_workflow(tmp_path: Path) -> None:
    make_repo(tmp_path)
    (tmp_path / "archon/workflows/archon-piv-loop.yaml").unlink()

    result = validate_harnesses(tmp_path)

    assert "missing repo-local Archon workflow" in messages(result)
    assert result.exit_code() == 1


def test__validate_harnesses__missing_archon_project_config(tmp_path: Path) -> None:
    make_repo(tmp_path)
    (tmp_path / "archon/skills/.archon/config.yaml").unlink()

    result = validate_harnesses(tmp_path)

    assert "missing path assumed by bootstrap CLI code" in messages(result)
    assert result.exit_code() == 1
