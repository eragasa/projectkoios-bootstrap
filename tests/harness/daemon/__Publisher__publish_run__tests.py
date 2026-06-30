from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    FreshnessState,
    GraphSnapshot,
    RunMetadata,
)
from projectkoios.bootstrap.harness.daemon.publisher import (
    publish_run,
    runtime_dir_for,
)


def _make_ctx(repo_root: Path, run_id: str = "test-001") -> DaemonContext:
    return DaemonContext(
        run_id=run_id,
        repo_root=str(repo_root),
        started_at=datetime.now(timezone.utc).isoformat(),
        trigger_kind="test",
        freshness=FreshnessState.UPDATING,
        graph_snapshot=GraphSnapshot(
            run_id=run_id,
            path=str(repo_root / "graphify-out" / "graph.json"),
            node_count=10,
            edge_count=20,
            community_count=3,
        ),
        metadata=RunMetadata(
            run_id=run_id,
            repo_path=str(repo_root),
            repo_identity=repo_root.name,
            daemon_version="0.1.0",
            graphify_version="1.0",
            freshness=FreshnessState.UPDATING,
        ),
    )


def _make_graphify_out(repo_root: Path) -> None:
    out = repo_root / "graphify-out"
    out.mkdir(exist_ok=True)
    (out / "graph.json").write_text(
        json.dumps({"nodes": [], "edges": []}), encoding="utf-8",
    )


def test__publish_run__writes_graph_snapshot(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    ctx = _make_ctx(repo)
    result = publish_run(ctx)
    run_dir = runtime / repo.name / ctx.run_id
    assert (run_dir / "graph.json").exists()
    assert result.freshness == FreshnessState.FRESH


def test__publish_run__writes_run_metadata(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    ctx = _make_ctx(repo)
    publish_run(ctx)
    run_dir = runtime / repo.name / ctx.run_id
    meta = json.loads((run_dir / "run_metadata.json").read_text())
    assert meta["run_id"] == ctx.run_id
    assert meta["repo_identity"] == repo.name
    assert meta["daemon_version"] == "0.1.0"
    assert meta["graphify_version"] == "1.0"
    assert meta["freshness"] == "fresh"


def test__publish_run__writes_freshness_marker(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    ctx = _make_ctx(repo)
    publish_run(ctx)
    run_dir = runtime / repo.name / ctx.run_id
    freshness = (run_dir / "freshness").read_text().strip()
    assert freshness == "fresh"


def test__publish_run__writes_degraded_report_on_failures(tmp_path: Path, monkeypatch) -> None:
    from dataclasses import replace

    repo = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    ctx = replace(
        _make_ctx(repo),
        failures=("file X failed to process",),
        warnings=("partial failure",),
    )
    result = publish_run(ctx)
    run_dir = runtime / repo.name / ctx.run_id
    assert (run_dir / "degraded.json").exists()
    degraded = json.loads((run_dir / "degraded.json").read_text())
    assert "file X failed to process" in degraded["failures"]
    assert result.freshness == FreshnessState.DEGRADED


def test__publish_run__writes_chunk_cards(tmp_path: Path, monkeypatch) -> None:
    from dataclasses import replace

    from projectkoios.bootstrap.harness.daemon.data import (
        ChunkCard,
        ChunkCardSet,
    )

    repo = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    base_ctx = _make_ctx(repo)
    ctx = replace(
        base_ctx,
        chunk_card_set=ChunkCardSet(
            run_id=base_ctx.run_id,
            path="",
            card_count=1,
            model="llama3.2",
            degraded=False,
        ),
        chunk_cards=(
            ChunkCard(
                chunk_id="c1",
                source_path="src/main.py",
                summary="Entry point module",
                model="llama3.2",
            ),
        ),
    )
    publish_run(ctx)
    run_dir = runtime / repo.name / ctx.run_id
    cards = json.loads((run_dir / "chunk_cards.json").read_text())
    assert cards["card_count"] == 1
    assert cards["cards"][0]["chunk_id"] == "c1"
    assert "role" not in cards["cards"][0]["summary"].lower()


def test__publish_run__creates_latest_symlink(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    ctx = _make_ctx(repo)
    publish_run(ctx)
    latest = runtime / repo.name / "latest"
    assert latest.is_symlink()
    assert (latest / "graph.json").exists()


def test__publish_run__output_not_in_repo(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    runtime = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    ctx = _make_ctx(repo)
    publish_run(ctx)
    run_dir = runtime / repo.name / ctx.run_id
    assert str(run_dir).startswith(str(runtime))
    assert not str(run_dir).startswith(str(repo))


def test__runtime_dir_for__returns_expected_path(tmp_path: Path) -> None:
    d = runtime_dir_for("projectkoios-bootstrap")
    assert d.name == "projectkoios-bootstrap"
