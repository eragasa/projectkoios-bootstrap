"""ActivityObjects (transitions) for the daemon Petri net.

Each ActivityObject has ``enabled()`` and ``apply()`` shape, mirroring the
guard/transition pattern in ``harness/handoffs/guards.py``. A transition fires
only when ``enabled()`` returns True, consuming input DataObjects and producing
output DataObjects, updating the daemon marking.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from projectkoios.bootstrap.harness.daemon.data import (
    ChunkCard,
    ChunkCardSet,
    DaemonToken,
    DaemonTokenKind,
    FreshnessState,
    GraphSnapshot,
    RunMetadata,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class DaemonContext:
    """Mutable working state carried through a daemon run cycle.

    The context bundles the marking-level state (current freshness, run id,
    produced DataObjects) so each ActivityObject can inspect and update it
    without touching the filesystem directly. Side effects are performed by
    the orchestrator in ``daemon.py`` using the result DataObjects.
    """

    run_id: str
    repo_root: str
    started_at: str
    trigger_kind: str
    freshness: FreshnessState
    graph_snapshot: GraphSnapshot | None = None
    chunk_card_set: ChunkCardSet | None = None
    chunk_cards: tuple[ChunkCard, ...] = ()
    metadata: RunMetadata | None = None
    failures: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


class Activity(Protocol):
    """An ActivityObject — a transition in the daemon Petri net."""

    name: str

    def enabled(self, ctx: DaemonContext) -> bool:
        """True when this transition may fire given the current context."""
        ...

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        """Fire the transition, returning a new context with updated state."""
        ...


class InitialFullBuild:
    """Performs the first full Graphify build over the repository root."""

    name = "InitialFullBuild"

    def enabled(self, ctx: DaemonContext) -> bool:
        return ctx.metadata is None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        from projectkoios.bootstrap.harness.daemon.graphify_runner import run_graphify

        result = run_graphify(ctx)
        return result


class WatchFilesystem:
    """Long-running watcher observing the source root for eligible changes.

    This transition is always enabled while the daemon is running; the
    orchestrator drives the actual polling loop in ``daemon.py``.
    """

    name = "WatchFilesystem"

    def enabled(self, ctx: DaemonContext) -> bool:
        return True

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        return ctx


class ScheduleUpdate:
    """Debounce and coalesce layer.

    Turns a burst of file events into a single update request. When an update
    is already in flight, schedules exactly one follow-up update rather than
    running overlapping refreshes.
    """

    name = "ScheduleUpdate"

    def enabled(self, ctx: DaemonContext) -> bool:
        return True

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        return ctx


class RunGraphifyRefresh:
    """Incremental or refresh Graphify run using defaults."""

    name = "RunGraphifyRefresh"

    def enabled(self, ctx: DaemonContext) -> bool:
        return ctx.metadata is not None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        from projectkoios.bootstrap.harness.daemon.graphify_runner import run_graphify

        return run_graphify(ctx)


class GenerateChunkCards:
    """Local Ollama universal chunk-card generation.

    Degrades gracefully (warns, skips cards, keeps graph fresh) when Ollama
    is absent or unreachable.
    """

    name = "GenerateChunkCards"

    def enabled(self, ctx: DaemonContext) -> bool:
        return ctx.graph_snapshot is not None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        from projectkoios.bootstrap.harness.daemon.ollama import generate_chunk_cards

        return generate_chunk_cards(ctx)


class PublishSnapshot:
    """Write fresh snapshot, chunk cards, metadata, and freshness marker."""

    name = "PublishSnapshot"

    def enabled(self, ctx: DaemonContext) -> bool:
        return ctx.graph_snapshot is not None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        from projectkoios.bootstrap.harness.daemon.publisher import publish_run

        return publish_run(ctx)


class PublishDegradedSnapshot:
    """Write partial snapshot with warnings and file-level failure metadata."""

    name = "PublishDegradedSnapshot"

    def enabled(self, ctx: DaemonContext) -> bool:
        return bool(ctx.failures) and ctx.graph_snapshot is not None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        from projectkoios.bootstrap.harness.daemon.publisher import publish_run

        ctx = _with_degraded_state(ctx)
        return publish_run(ctx)


def _with_degraded_state(ctx: DaemonContext) -> DaemonContext:
    """Mark the context as degraded before publishing.

    Preserves ``FAILED`` freshness (a build failure is worse than degraded)
    and only sets ``DEGRADED`` when the current state is not already failed.
    """
    from dataclasses import replace

    new_freshness = FreshnessState.FAILED if ctx.freshness == FreshnessState.FAILED else FreshnessState.DEGRADED
    return replace(
        ctx,
        freshness=new_freshness,
        warnings=ctx.warnings + (
            f"publishing degraded snapshot: {len(ctx.failures)} failure(s)",
        ),
    )


def build_token(ctx: DaemonContext) -> DaemonToken:
    """Construct the daemon token representing the run's outcome."""
    return DaemonToken(
        kind=DaemonTokenKind.DAEMON_RUN,
        place=ctx.freshness,
        run_id=ctx.run_id,
        created_at=_now_iso(),
        snapshot_path=ctx.graph_snapshot.path if ctx.graph_snapshot else None,
        card_set_path=ctx.chunk_card_set.path if ctx.chunk_card_set else None,
        failures=ctx.failures,
        warnings=ctx.warnings,
    )


ALL_ACTIVITIES: list[Activity] = [
    InitialFullBuild(),
    WatchFilesystem(),
    ScheduleUpdate(),
    RunGraphifyRefresh(),
    GenerateChunkCards(),
    PublishSnapshot(),
    PublishDegradedSnapshot(),
]
"""Ordered transition list for the first daemon slice."""
