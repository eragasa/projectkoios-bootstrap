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


def test_bootstrap_help_exposes_init_and_install(tmp_path: Path) -> None:
    result = run_projectkoios("bootstrap", "--help", home=tmp_path)

    assert result.returncode == 0
    assert "init" in result.stdout
    assert "install" in result.stdout


def test_bootstrap_init_copies_example_files_and_skips_asset_dirs(
    tmp_path: Path,
) -> None:
    result = run_projectkoios("bootstrap", "init", home=tmp_path)

    assert result.returncode == 0, result.stderr
    assert (tmp_path / ".pi/settings.json").exists()
    assert (tmp_path / ".pi/AGENTS.md").exists()
    assert (tmp_path / ".archon/config.yaml").exists()
    assert (tmp_path / ".opencode/opencode.json").exists()
    assert (tmp_path / ".local/share/goose/AGENT.md").exists()
    assert not (tmp_path / ".pi/skills").exists()
    assert "done: init complete" in result.stdout
