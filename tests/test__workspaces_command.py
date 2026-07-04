from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import cast


ROOT = Path(__file__).resolve().parent.parent


def run_projectkoios(*args: str, home: Path) -> subprocess.CompletedProcess[str]:
    """Run the bootstrap module with an isolated home directory."""
    # Environment isolates command effects under the test-provided home path.
    env: dict[str, str] = os.environ.copy()
    env["HOME"] = str(home)
    env["PYTHONPATH"] = str(ROOT / "src/python")
    return subprocess.run(
        [sys.executable, "-m", "projectkoios.bootstrap", *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def top_json_metadata(path: Path) -> dict[str, object]:
    """Load the top fenced JSON metadata block from a Markdown file."""
    # Text contains the generated Markdown control file content.
    text: str = path.read_text(encoding="utf-8")
    assert text.startswith("```json\n")
    # Json text isolates the opening fenced metadata block.
    json_text: str = text.split("\n```", 1)[0].removeprefix("```json\n")
    # Loaded metadata should be a JSON object.
    loaded: object = json.loads(json_text)
    assert isinstance(loaded, dict)
    return cast(dict[str, object], loaded)


def test__workspaces_help_exposes_init(tmp_path: Path) -> None:
    """Validate that workspace command help exposes init without stale wording."""
    # Result captures the workspace command help output for assertion.
    result: subprocess.CompletedProcess[str] = run_projectkoios(
        "bootstrap",
        "workspaces",
        "--help",
        home=tmp_path,
    )

    assert result.returncode == 0
    assert "init" in result.stdout
    assert "handoff folders" not in result.stdout


def test__workspaces_init_creates_agent_workspaces(tmp_path: Path) -> None:
    """Validate that workspace init creates canonical role workspace layouts."""
    # Result captures workspace initialization output and return code.
    result: subprocess.CompletedProcess[str] = run_projectkoios(
        "bootstrap",
        "workspaces",
        "init",
        "--root",
        str(tmp_path),
        home=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    # Agent names enumerate every canonical workspace created by the command.
    agent: str
    for agent in ("hermes", "athena", "vulcan", "koios"):
        # Workspace is the role-local directory expected under the root.
        workspace: Path = tmp_path / "workspaces" / agent
        assert (workspace / "AGENTS.md").exists()
        assert (workspace / "state.md").exists()
        assert (workspace / "active.md").exists()
        assert not (workspace / "inbox").exists()
        assert not (workspace / "outbox").exists()
        assert not (workspace / "handoffs").exists()
        assert not (workspace / "working" / "incoming").exists()
        assert not (workspace / "working" / "outgoing").exists()
        assert (workspace / "sessions").is_dir()
        assert (workspace / "working").is_dir()
        assert (workspace / "scratch").is_dir()
        assert (workspace / "decisions").is_dir()
    assert "done: workspaces initialized" in result.stdout


def test__workspaces_init_seeds_state_and_active_top_json_metadata(tmp_path: Path) -> None:
    """Validate that workspace init seeds control files with top JSON metadata."""
    # Result captures workspace initialization output and return code.
    result: subprocess.CompletedProcess[str] = run_projectkoios(
        "bootstrap",
        "workspaces",
        "init",
        "--root",
        str(tmp_path),
        home=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    # Agent names enumerate every canonical workspace created by the command.
    agent: str
    for agent in ("hermes", "athena", "vulcan", "koios"):
        # Workspace is the role-local directory containing generated control files.
        workspace: Path = tmp_path / "workspaces" / agent
        # State metadata is the resume-snapshot machine-readable block.
        state_metadata: dict[str, object] = top_json_metadata(workspace / "state.md")
        # Active metadata is the priority-surface machine-readable block.
        active_metadata: dict[str, object] = top_json_metadata(workspace / "active.md")
        assert state_metadata["artifact_type"] == "workspace-state"
        assert active_metadata["artifact_type"] == "workspace-active-priorities"
        assert state_metadata["acting_as"] == agent.upper()
        assert active_metadata["acting_as"] == agent.upper()
        assert state_metadata["workspace"] == f"workspaces/{agent}/"
        assert active_metadata["workspace"] == f"workspaces/{agent}/"
        assert state_metadata["control_files"] == ["state.md", "active.md"]
        assert active_metadata["control_files"] == ["state.md", "active.md"]
        assert "document_domain" in state_metadata
        assert "blockers" in active_metadata


def test__workspaces_init_seeds_canonical_architecture_reference(tmp_path: Path) -> None:
    """Validate that seeded workspace instructions name the canonical architecture path."""
    # Result captures workspace initialization output and return code.
    result: subprocess.CompletedProcess[str] = run_projectkoios(
        "bootstrap",
        "workspaces",
        "init",
        "--root",
        str(tmp_path),
        "--agents",
        "vulcan",
        home=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    # Text contains the generated Vulcan workspace instructions.
    text: str = (tmp_path / "workspaces" / "vulcan" / "AGENTS.md").read_text(encoding="utf-8")
    assert "docs/architecture/architecture.00.md" in text
    assert "docs/architecture.00.md" not in text
