from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


def run_projectkoios(*args: str, home: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
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


def top_json_metadata(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("```json\n")
    json_text = text.split("\n```", 1)[0].removeprefix("```json\n")
    loaded = json.loads(json_text)
    assert isinstance(loaded, dict)
    return loaded


def test__workspaces_help_exposes_init(tmp_path: Path) -> None:
    result = run_projectkoios("bootstrap", "workspaces", "--help", home=tmp_path)

    assert result.returncode == 0
    assert "init" in result.stdout
    assert "handoff folders" not in result.stdout


def test__workspaces_init_creates_agent_workspaces(tmp_path: Path) -> None:
    result = run_projectkoios(
        "bootstrap",
        "workspaces",
        "init",
        "--root",
        str(tmp_path),
        home=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    for agent in ("hermes", "athena", "vulcan", "koios"):
        workspace = tmp_path / "workspaces" / agent
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
    result = run_projectkoios(
        "bootstrap",
        "workspaces",
        "init",
        "--root",
        str(tmp_path),
        home=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    for agent in ("hermes", "athena", "vulcan", "koios"):
        workspace = tmp_path / "workspaces" / agent
        state_metadata = top_json_metadata(workspace / "state.md")
        active_metadata = top_json_metadata(workspace / "active.md")
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
    result = run_projectkoios(
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
    text = (tmp_path / "workspaces" / "vulcan" / "AGENTS.md").read_text(encoding="utf-8")
    assert "docs/architecture/architecture.00.md" in text
    assert "docs/architecture.00.md" not in text
