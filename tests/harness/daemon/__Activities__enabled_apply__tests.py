from __future__ import annotations

from datetime import datetime, timezone

from projectkoios.bootstrap.harness.daemon.activities import (
    ALL_ACTIVITIES,
    DaemonContext,
    GenerateChunkCards,
    InitialFullBuild,
    PublishDegradedSnapshot,
    build_token,
)
from projectkoios.bootstrap.harness.daemon.data import (
    ChunkCardSet,
    DaemonToken,
    DaemonTokenKind,
    FreshnessState,
    GraphSnapshot,
    RunMetadata,
)


def _make_ctx(repo_root: str = "/tmp/repo") -> DaemonContext:
    return DaemonContext(
        run_id="test-001",
        repo_root=repo_root,
        started_at=datetime.now(timezone.utc).isoformat(),
        trigger_kind="test",
        freshness=FreshnessState.UPDATING,
    )


def test__DaemonToken__kind_and_place_form_color() -> None:
    token = DaemonToken(
        kind=DaemonTokenKind.DAEMON_RUN,
        place=FreshnessState.FRESH,
        run_id="r1",
        created_at="2026-01-01T00:00:00Z",
    )
    assert token.kind == "daemon_run"
    assert token.place == "fresh"


def test__FreshnessState__has_five_states() -> None:
    assert FreshnessState.FRESH == "fresh"
    assert FreshnessState.UPDATING == "updating"
    assert FreshnessState.DEGRADED == "degraded"
    assert FreshnessState.STALE == "stale"
    assert FreshnessState.FAILED == "failed"


def test__RunMetadata__to_dict__serialises_all_fields() -> None:
    m = RunMetadata(
        run_id="r1",
        repo_path="/repo",
        repo_identity="repo",
        daemon_version="0.1.0",
        graphify_version="1.0",
        freshness=FreshnessState.DEGRADED,
        failures=("bad file",),
        warnings=("degraded",),
    )
    d = m.to_dict()
    assert d["run_id"] == "r1"
    assert d["freshness"] == "degraded"
    assert d["failures"] == ["bad file"]
    assert d["warnings"] == ["degraded"]
    assert d["ollama_degraded"] is False
    assert d["eligible_files_count"] == 0
    assert d["indexed_files_count"] == 0
    assert d["chunk_batch_count"] == 0
    assert d["chunk_batch_source"] is None


def test__build_token__reflects_context_state() -> None:
    ctx = _make_ctx()
    ctx = DaemonContext(
        run_id="r1",
        repo_root="/repo",
        started_at="",
        trigger_kind="",
        freshness=FreshnessState.DEGRADED,
        failures=("f1",),
        warnings=("w1",),
    )
    token = build_token(ctx)
    assert token.kind == DaemonTokenKind.DAEMON_RUN
    assert token.place == FreshnessState.DEGRADED
    assert token.failures == ("f1",)
    assert token.warnings == ("w1",)


def test__ALL_ACTIVITIES__has_seven_first_slice_transitions() -> None:
    names = {a.name for a in ALL_ACTIVITIES}
    assert names == {
        "InitialFullBuild",
        "WatchFilesystem",
        "ScheduleUpdate",
        "RunGraphifyRefresh",
        "GenerateChunkCards",
        "PublishSnapshot",
        "PublishDegradedSnapshot",
    }


def test__InitialFullBuild__enabled_when_no_metadata() -> None:
    act = InitialFullBuild()
    ctx = _make_ctx()
    assert act.enabled(ctx) is True


def test__GenerateChunkCards__enabled_when_graph_present() -> None:
    act = GenerateChunkCards()
    ctx = _make_ctx()
    assert act.enabled(ctx) is False
    ctx = DaemonContext(
        run_id="r1",
        repo_root="/repo",
        started_at="",
        trigger_kind="",
        freshness=FreshnessState.UPDATING,
        graph_snapshot=GraphSnapshot(run_id="r1", path="/g", node_count=1, edge_count=0, community_count=0),
    )
    assert act.enabled(ctx) is True


def test__PublishDegradedSnapshot__enabled_only_with_failures_and_graph() -> None:
    act = PublishDegradedSnapshot()
    ctx = _make_ctx()
    assert act.enabled(ctx) is False
    ctx = DaemonContext(
        run_id="r1",
        repo_root="/repo",
        started_at="",
        trigger_kind="",
        freshness=FreshnessState.UPDATING,
        graph_snapshot=GraphSnapshot(run_id="r1", path="/g", node_count=1, edge_count=0, community_count=0),
        failures=("err",),
    )
    assert act.enabled(ctx) is True


def test__ChunkCardSet__is_role_neutral() -> None:
    cs = ChunkCardSet(
        run_id="r1",
        path="/cards.json",
        card_count=5,
        model="llama3.2",
        degraded=False,
    )
    assert cs.card_count == 5
    assert "role" not in cs.model.lower()
