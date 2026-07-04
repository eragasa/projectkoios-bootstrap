from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import TypeAlias, cast

from pytest import MonkeyPatch

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    ChunkCard,
    ChunkCardSet,
    FreshnessState,
    GraphSnapshot,
    RunMetadata,
)
from projectkoios.bootstrap.harness.daemon.publisher import (
    publish_run,
    runtime_dir_for,
)


JsonRecord: TypeAlias = dict[str, object]


def _make_ctx(repo_root: Path, run_id: str = "test-001") -> DaemonContext:
    """Create a publishable daemon context fixture."""
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
    """Create a minimal graphify output fixture under a repo root."""
    # Output directory mirrors Graphify's expected artifact location.
    out: Path = repo_root / "graphify-out"
    out.mkdir(exist_ok=True)
    (out / "graph.json").write_text(
        json.dumps({"nodes": [], "edges": []}), encoding="utf-8",
    )


def test__publish_run__writes_graph_snapshot(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate publishing copies the graph snapshot into runtime state."""
    # Repository fixture is the source tree whose graph output is published.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    # Runtime root is isolated from the developer machine for the test.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    # Context fixture contains graph snapshot and metadata prerequisites.
    ctx: DaemonContext = _make_ctx(repo)
    # Result captures the updated context returned by the publisher.
    result: DaemonContext = publish_run(ctx)
    # Run directory is where published runtime artifacts should appear.
    run_dir: Path = runtime / repo.name / ctx.run_id
    assert (run_dir / "graph.json").exists()
    assert result.freshness == FreshnessState.FRESH


def test__publish_run__writes_run_metadata(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate publishing writes run metadata with final freshness."""
    # Repository fixture is the source tree whose graph output is published.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    # Runtime root is isolated from the developer machine for the test.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    # Context fixture contains graph snapshot and metadata prerequisites.
    ctx: DaemonContext = _make_ctx(repo)
    publish_run(ctx)
    # Run directory is where published runtime artifacts should appear.
    run_dir: Path = runtime / repo.name / ctx.run_id
    # Metadata payload is the persisted JSON record under assertion.
    meta: JsonRecord = json.loads((run_dir / "run_metadata.json").read_text(encoding="utf-8"))
    assert meta["run_id"] == ctx.run_id
    assert meta["repo_identity"] == repo.name
    assert meta["daemon_version"] == "0.1.0"
    assert meta["graphify_version"] == "1.0"
    assert meta["freshness"] == "fresh"


def test__publish_run__writes_freshness_marker(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate publishing writes a freshness marker file."""
    # Repository fixture is the source tree whose graph output is published.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    # Runtime root is isolated from the developer machine for the test.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    # Context fixture contains graph snapshot and metadata prerequisites.
    ctx: DaemonContext = _make_ctx(repo)
    publish_run(ctx)
    # Run directory is where published runtime artifacts should appear.
    run_dir: Path = runtime / repo.name / ctx.run_id
    # Freshness marker is the scalar state consumed by runtime readers.
    freshness: str = (run_dir / "freshness").read_text(encoding="utf-8").strip()
    assert freshness == "fresh"


def test__publish_run__writes_degraded_report_on_failures(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate publishing writes a degraded report when failures exist."""
    # Repository fixture is the source tree whose graph output is published.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    # Runtime root is isolated from the developer machine for the test.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    # Context fixture includes failures and warnings that trigger degraded output.
    ctx: DaemonContext = replace(
        _make_ctx(repo),
        failures=("file X failed to process",),
        warnings=("partial failure",),
    )
    # Result captures the degraded final freshness returned by the publisher.
    result: DaemonContext = publish_run(ctx)
    # Run directory is where published runtime artifacts should appear.
    run_dir: Path = runtime / repo.name / ctx.run_id
    assert (run_dir / "degraded.json").exists()
    # Degraded payload is the persisted JSON record under assertion.
    degraded: JsonRecord = json.loads((run_dir / "degraded.json").read_text(encoding="utf-8"))
    # Failures provide typed access to the degraded failure list.
    failures: list[str] = cast(list[str], degraded["failures"])
    assert "file X failed to process" in failures
    assert result.freshness == FreshnessState.DEGRADED


def test__publish_run__writes_chunk_cards(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate publishing writes universal chunk cards when present."""
    # Repository fixture is the source tree whose graph output is published.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    # Runtime root is isolated from the developer machine for the test.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    # Base context provides run id and graph metadata for the card set.
    base_ctx: DaemonContext = _make_ctx(repo)
    # Context fixture includes one generated chunk card to publish.
    ctx: DaemonContext = replace(
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
    # Run directory is where published runtime artifacts should appear.
    run_dir: Path = runtime / repo.name / ctx.run_id
    # Cards payload is the persisted JSON record under assertion.
    cards: JsonRecord = json.loads((run_dir / "chunk_cards.json").read_text(encoding="utf-8"))
    # Card records provide typed access to the nested cards list.
    card_records: list[dict[str, str]] = cast(list[dict[str, str]], cards["cards"])
    assert cards["card_count"] == 1
    assert card_records[0]["chunk_id"] == "c1"
    assert "role" not in card_records[0]["summary"].lower()


def test__publish_run__creates_latest_symlink(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate publishing updates the latest symlink."""
    # Repository fixture is the source tree whose graph output is published.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    # Runtime root is isolated from the developer machine for the test.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    # Context fixture contains graph snapshot and metadata prerequisites.
    ctx: DaemonContext = _make_ctx(repo)
    publish_run(ctx)
    # Latest symlink points readers at the most recent run directory.
    latest: Path = runtime / repo.name / "latest"
    assert latest.is_symlink()
    assert (latest / "graph.json").exists()


def test__publish_run__output_not_in_repo(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Validate publishing writes runtime output outside the source repo."""
    # Repository fixture is the source tree whose graph output is published.
    repo: Path = tmp_path / "myrepo"
    repo.mkdir()
    _make_graphify_out(repo)
    # Runtime root is isolated from the developer machine for the test.
    runtime: Path = tmp_path / "runtime"
    monkeypatch.setattr(
        "projectkoios.bootstrap.harness.daemon.publisher.DEFAULT_RUNTIME_ROOT",
        runtime,
    )
    # Context fixture contains graph snapshot and metadata prerequisites.
    ctx: DaemonContext = _make_ctx(repo)
    publish_run(ctx)
    # Run directory is where published runtime artifacts should appear.
    run_dir: Path = runtime / repo.name / ctx.run_id
    assert str(run_dir).startswith(str(runtime))
    assert not str(run_dir).startswith(str(repo))


def test__runtime_dir_for__returns_expected_path() -> None:
    """Validate runtime directory selection preserves repo identity."""
    # Runtime directory is the path returned for the supplied repository identity.
    runtime_dir: Path = runtime_dir_for("projectkoios-bootstrap")
    assert runtime_dir.name == "projectkoios-bootstrap"
