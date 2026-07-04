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
    """Create a daemon context fixture for activity enablement tests."""
    return DaemonContext(
        run_id="test-001",
        repo_root=repo_root,
        started_at=datetime.now(timezone.utc).isoformat(),
        trigger_kind="test",
        freshness=FreshnessState.UPDATING,
    )


def test__DaemonToken__kind_and_place_form_color() -> None:
    """Validate daemon token fields keep their string-valued enum forms."""
    # Token uses enum inputs but should compare as stable string values.
    token: DaemonToken = DaemonToken(
        kind=DaemonTokenKind.DAEMON_RUN,
        place=FreshnessState.FRESH,
        run_id="r1",
        created_at="2026-01-01T00:00:00Z",
    )
    assert token.kind == "daemon_run"
    assert token.place == "fresh"


def test__FreshnessState__has_five_states() -> None:
    """Validate the daemon freshness state enum exposes expected states."""
    assert FreshnessState.FRESH == "fresh"
    assert FreshnessState.UPDATING == "updating"
    assert FreshnessState.DEGRADED == "degraded"
    assert FreshnessState.STALE == "stale"
    assert FreshnessState.FAILED == "failed"


def test__RunMetadata__to_dict__serialises_all_fields() -> None:
    """Validate run metadata serialization includes expected default fields."""
    # Metadata fixture includes failures and warnings to exercise list conversion.
    metadata: RunMetadata = RunMetadata(
        run_id="r1",
        repo_path="/repo",
        repo_identity="repo",
        daemon_version="0.1.0",
        graphify_version="1.0",
        freshness=FreshnessState.DEGRADED,
        failures=("bad file",),
        warnings=("degraded",),
    )
    # Serialized metadata should expose JSON-compatible scalar/list values.
    serialized: dict[str, object] = metadata.to_dict()
    assert serialized["run_id"] == "r1"
    assert serialized["freshness"] == "degraded"
    assert serialized["failures"] == ["bad file"]
    assert serialized["warnings"] == ["degraded"]
    assert serialized["ollama_degraded"] is False
    assert serialized["eligible_files_count"] == 0
    assert serialized["indexed_files_count"] == 0
    assert serialized["chunk_batch_count"] == 0
    assert serialized["chunk_batch_source"] is None


def test__build_token__reflects_context_state() -> None:
    """Validate built daemon tokens reflect daemon context state."""
    # Context carries degraded state, failures, and warnings into the token.
    context: DaemonContext = DaemonContext(
        run_id="r1",
        repo_root="/repo",
        started_at="",
        trigger_kind="",
        freshness=FreshnessState.DEGRADED,
        failures=("f1",),
        warnings=("w1",),
    )
    # Token is derived from the context state for daemon publication.
    token: DaemonToken = build_token(context)
    assert token.kind == DaemonTokenKind.DAEMON_RUN
    assert token.place == FreshnessState.DEGRADED
    assert token.failures == ("f1",)
    assert token.warnings == ("w1",)


def test__ALL_ACTIVITIES__has_seven_first_slice_transitions() -> None:
    """Validate the first daemon activity slice exposes expected names."""
    # Names provide a concise assertion over the activity registry contents.
    names: set[str] = {activity.name for activity in ALL_ACTIVITIES}
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
    """Validate initial full build is enabled for a fresh context."""
    # Activity under test should be available before prior metadata exists.
    activity: InitialFullBuild = InitialFullBuild()
    # Context fixture has no prior run metadata attached.
    context: DaemonContext = _make_ctx()
    assert activity.enabled(context) is True


def test__GenerateChunkCards__enabled_when_graph_present() -> None:
    """Validate chunk-card generation requires a graph snapshot."""
    # Activity under test should be disabled without graph output.
    activity: GenerateChunkCards = GenerateChunkCards()
    # Context fixture has no graph snapshot attached.
    context: DaemonContext = _make_ctx()
    assert activity.enabled(context) is False
    # Graph context includes a minimal graph snapshot for enablement.
    graph_context: DaemonContext = DaemonContext(
        run_id="r1",
        repo_root="/repo",
        started_at="",
        trigger_kind="",
        freshness=FreshnessState.UPDATING,
        graph_snapshot=GraphSnapshot(run_id="r1", path="/g", node_count=1, edge_count=0, community_count=0),
    )
    assert activity.enabled(graph_context) is True


def test__PublishDegradedSnapshot__enabled_only_with_failures_and_graph() -> None:
    """Validate degraded snapshot publishing requires failures and graph data."""
    # Activity under test should be disabled until both prerequisites exist.
    activity: PublishDegradedSnapshot = PublishDegradedSnapshot()
    # Context fixture has neither graph data nor failures.
    context: DaemonContext = _make_ctx()
    assert activity.enabled(context) is False
    # Degraded context includes graph output and a failure.
    degraded_context: DaemonContext = DaemonContext(
        run_id="r1",
        repo_root="/repo",
        started_at="",
        trigger_kind="",
        freshness=FreshnessState.UPDATING,
        graph_snapshot=GraphSnapshot(run_id="r1", path="/g", node_count=1, edge_count=0, community_count=0),
        failures=("err",),
    )
    assert activity.enabled(degraded_context) is True


def test__ChunkCardSet__is_role_neutral() -> None:
    """Validate chunk-card metadata remains role-neutral."""
    # Card set fixture contains daemon output metadata without role-specific labels.
    card_set: ChunkCardSet = ChunkCardSet(
        run_id="r1",
        path="/cards.json",
        card_count=5,
        model="llama3.2",
        degraded=False,
    )
    assert card_set.card_count == 5
    assert "role" not in card_set.model.lower()
