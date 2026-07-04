from __future__ import annotations

import json
from pathlib import Path
import subprocess
from typing import TypeAlias
from unittest.mock import patch

from pytest import MonkeyPatch

from projectkoios.bootstrap.harness.daemon.daemon import (
    check_source_tree_safety,
    git_status_short,
    run_once,
)
from projectkoios.bootstrap.harness.daemon.data import DaemonRunResult, FreshnessState


CommandArgs: TypeAlias = list[str]
CommandKwargs: TypeAlias = dict[str, object]


def _completed(stdout: str = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    """Create a completed-process fixture for subprocess patches."""
    return subprocess.CompletedProcess(
        args=[],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_git_status_short__returns_output(tmp_path: Path) -> None:
    """Validate git status helper returns a string for a git repo."""
    # Repository fixture gives git_status_short a filesystem target.
    repo: Path = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    # Result captures the porcelain status output or safe fallback.
    result: str = git_status_short(repo)
    assert isinstance(result, str)


def test_check_source_tree_safety__no_change_returns_empty() -> None:
    """Validate unchanged source tree status produces no warnings."""
    assert check_source_tree_safety(Path("/tmp"), "", "") == []


def test_check_source_tree_safety__graphify_out_ignored() -> None:
    """Validate graphify output changes are ignored by source safety."""
    # Before status captures the source-tree state before daemon execution.
    before: str = ""
    # After status includes only generated Graphify output.
    after: str = "?? graphify-out/graph.json\n"
    # Result captures source-tree safety warnings under assertion.
    result: list[str] = check_source_tree_safety(Path("/tmp"), before, after)
    assert result == []


def test_check_source_tree_safety__unexpected_change_flagged() -> None:
    """Validate unexpected source changes produce safety warnings."""
    # Before status captures the source-tree state before daemon execution.
    before: str = ""
    # After status includes a non-runtime source change.
    after: str = "?? src/unexpected.py\n"
    # Result captures source-tree safety warnings under assertion.
    result: list[str] = check_source_tree_safety(Path("/tmp"), before, after)
    assert len(result) == 1
    assert "unexpected" in result[0]


def test__run_once__fails_gracefully_without_graphify(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate one daemon cycle fails gracefully when Graphify is absent."""
    # Repository fixture contains minimal tracked configuration.
    repo: Path = tmp_path / "repo"
    repo.mkdir()
    (repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
    # Runtime root is isolated from developer-local state.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    # Git result keeps source safety checks deterministic.
    git_result: subprocess.CompletedProcess[str] = _completed()
    with (
        patch("shutil.which", return_value=None),
        patch("subprocess.run", return_value=git_result),
    ):
        # Result captures the daemon cycle outcome under assertion.
        result: DaemonRunResult = run_once(repo, trigger_kind="test")
    assert result.token.place == FreshnessState.FAILED
    assert any("graphify" in failure.lower() for failure in result.metadata.failures)


def test__run_once__publishes_to_runtime_not_repo(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate one daemon cycle publishes runtime artifacts outside the repo."""
    # Repository fixture contains source and Graphify output inputs.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    (repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("x = 1\n", encoding="utf-8")
    # Graphify output directory contains prebuilt graph artifacts.
    out: Path = repo / "graphify-out"
    out.mkdir()
    (out / "graph.json").write_text(json.dumps({"nodes": [{"id": "n1"}], "edges": []}), encoding="utf-8")
    (out / "manifest.json").write_text('{"file.py": {}}', encoding="utf-8")

    # Runtime root is isolated from developer-local state.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )

    # Git result keeps source safety checks deterministic.
    git_result: subprocess.CompletedProcess[str] = _completed()
    # Graphify result simulates a successful refresh command.
    graphify_result: subprocess.CompletedProcess[str] = _completed(stdout="done")

    def mock_subprocess(args: CommandArgs, **kwargs: object) -> subprocess.CompletedProcess[str]:
        """Return command-specific subprocess fixtures."""
        if args and args[0] == "git":
            return git_result
        return graphify_result

    with (
        patch("shutil.which", return_value="/usr/local/bin/graphify"),
        patch("subprocess.run", side_effect=mock_subprocess),
        patch(
            "projectkoios.bootstrap.harness.daemon.graphify_runner.read_graph_stats",
            return_value=(5, 3, 1),
        ),
        patch(
            "projectkoios.bootstrap.harness.daemon.graphify_runner.graphify_version",
            return_value="graphify 1.0",
        ),
    ):
        # Result captures the daemon cycle outcome under assertion.
        result: DaemonRunResult = run_once(repo, trigger_kind="test")

    assert result.token.place != FreshnessState.FAILED
    # Run directory is the runtime publication path for this daemon cycle.
    run_dir: Path = runtime / repo.name / result.metadata.run_id
    assert (run_dir / "run_metadata.json").exists()
    assert not str(run_dir).startswith(str(repo))
    # Metadata payload is the persisted runtime record under assertion.
    metadata: dict[str, object] = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))
    assert metadata["graphify_version"] == "graphify 1.0"
    assert metadata["files_processed"] == 5


def test__run_once__source_tree_safety_gate(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate one daemon cycle reports unexpected source-tree changes."""
    # Repository fixture contains minimal graph output inputs.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    (repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
    # Graphify output directory contains prebuilt graph artifacts.
    out: Path = repo / "graphify-out"
    out.mkdir()
    (out / "graph.json").write_text(json.dumps({"nodes": [], "edges": []}), encoding="utf-8")

    # Runtime root is isolated from developer-local state.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )

    # Git calls tracks before/after status checks for source safety.
    git_calls: list[int] = [0]

    def mock_subprocess(args: CommandArgs, **kwargs: object) -> subprocess.CompletedProcess[str]:
        """Return command fixtures while mutating second git status output."""
        if args and args[0] == "git":
            git_calls[0] += 1
            # Git result starts clean and changes after the daemon run.
            git_result: subprocess.CompletedProcess[str] = _completed()
            if git_calls[0] >= 2:
                git_result.stdout = "?? src/unexpected.py\n"
            return git_result
        return _completed(stdout="done")

    with (
        patch("shutil.which", return_value="/usr/local/bin/graphify"),
        patch("subprocess.run", side_effect=mock_subprocess),
        patch(
            "projectkoios.bootstrap.harness.daemon.graphify_runner.read_graph_stats",
            return_value=(0, 0, 0),
        ),
        patch(
            "projectkoios.bootstrap.harness.daemon.graphify_runner.graphify_version",
            return_value="1.0",
        ),
    ):
        # Result captures the daemon cycle outcome under assertion.
        result: DaemonRunResult = run_once(repo, trigger_kind="test")

    assert any("unexpected" in warning for warning in result.metadata.warnings)
