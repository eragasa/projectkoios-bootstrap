from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from projectkoios.bootstrap.harness.daemon.daemon import (
    _check_source_tree_safety,
    _git_status_short,
    run_once,
)
from projectkoios.bootstrap.harness.daemon.data import FreshnessState


def test__git_status_short__returns_output(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    result = _git_status_short(repo)
    assert isinstance(result, str)


def test__check_source_tree_safety__no_change_returns_empty() -> None:
    assert _check_source_tree_safety(Path("/tmp"), "", "") == []


def test__check_source_tree_safety__graphify_out_ignored() -> None:
    before = ""
    after = "?? graphify-out/graph.json\n"
    result = _check_source_tree_safety(Path("/tmp"), before, after)
    assert result == []


def test__check_source_tree_safety__unexpected_change_flagged() -> None:
    before = ""
    after = "?? src/unexpected.py\n"
    result = _check_source_tree_safety(Path("/tmp"), before, after)
    assert len(result) == 1
    assert "unexpected" in result[0]


def test__run_once__fails_gracefully_without_graphify(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    git_result = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
    with patch("shutil.which", return_value=None), \
         patch("subprocess.run", return_value=git_result):
        result = run_once(repo, trigger_kind="test")
    assert result.token.place == FreshnessState.FAILED
    assert any("graphify" in f.lower() for f in result.metadata.failures)


def test__run_once__publishes_to_runtime_not_repo(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "myrepo"
    repo.mkdir()
    (repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("x = 1\n", encoding="utf-8")
    out = repo / "graphify-out"
    out.mkdir()
    (out / "graph.json").write_text(json.dumps({"nodes": [{"id": "n1"}], "edges": []}), encoding="utf-8")
    (out / "manifest.json").write_text('{"file.py": {}}', encoding="utf-8")

    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )

    git_result = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
    gf_result = type("R", (), {"returncode": 0, "stdout": "done", "stderr": ""})()

    call_count = [0]
    def mock_subprocess(args, **kwargs):
        call_count[0] += 1
        if args and args[0] == "git":
            return git_result
        return gf_result

    with patch("shutil.which", return_value="/usr/local/bin/graphify"), \
         patch("subprocess.run", side_effect=mock_subprocess), \
         patch(
             "projectkoios.bootstrap.harness.daemon.graphify_runner._read_graph_stats",
             return_value=(5, 3, 1),
         ), \
         patch(
             "projectkoios.bootstrap.harness.daemon.graphify_runner._graphify_version",
             return_value="graphify 1.0",
         ):
        result = run_once(repo, trigger_kind="test")

    assert result.token.place != FreshnessState.FAILED
    run_dir = runtime / repo.name / result.metadata.run_id
    assert (run_dir / "run_metadata.json").exists()
    assert not str(run_dir).startswith(str(repo))
    meta = json.loads((run_dir / "run_metadata.json").read_text())
    assert meta["graphify_version"] == "graphify 1.0"
    assert meta["files_processed"] == 5


def test__run_once__source_tree_safety_gate(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "myrepo"
    repo.mkdir()
    (repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
    out = repo / "graphify-out"
    out.mkdir()
    (out / "graph.json").write_text(json.dumps({"nodes": [], "edges": []}), encoding="utf-8")

    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )

    git_calls = [0]

    def mock_subprocess(args, **kwargs):
        if args and args[0] == "git":
            git_calls[0] += 1
            r = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            if git_calls[0] >= 2:
                r.stdout = "?? src/unexpected.py\n"
            return r
        return type("R", (), {"returncode": 0, "stdout": "done", "stderr": ""})()

    with patch("shutil.which", return_value="/usr/local/bin/graphify"), \
         patch("subprocess.run", side_effect=mock_subprocess), \
         patch(
             "projectkoios.bootstrap.harness.daemon.graphify_runner._read_graph_stats",
             return_value=(0, 0, 0),
         ), \
         patch(
             "projectkoios.bootstrap.harness.daemon.graphify_runner._graphify_version",
             return_value="1.0",
         ):
        result = run_once(repo, trigger_kind="test")

    assert any("unexpected" in w for w in result.metadata.warnings)
