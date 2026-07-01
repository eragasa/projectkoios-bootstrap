from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


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


def test__workspaces_help_exposes_init(tmp_path: Path) -> None:
    result = run_projectkoios("bootstrap", "workspaces", "--help", home=tmp_path)

    assert result.returncode == 0
    assert "init" in result.stdout


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
        assert (workspace / "AGENT.md").exists()
        assert (workspace / "state.md").exists()
        assert (workspace / "active.md").exists()
        assert (workspace / "inbox").is_dir()
        assert (workspace / "outbox").is_dir()
        assert (workspace / "sessions").is_dir()
        assert (workspace / "handoffs" / "incoming").is_dir()
        assert (workspace / "handoffs" / "outgoing").is_dir()
        assert (workspace / "decisions").is_dir()
    assert "done: workspaces initialized" in result.stdout
