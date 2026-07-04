"""ActivityObjects (transitions) for the daemon Petri net."""

from __future__ import annotations

from dataclasses import dataclass, replace
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


def now_iso() -> str:
    """Return the current UTC timestamp as an ISO string.

    Returns:
        Current UTC timestamp formatted with timezone information.
    """

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class DaemonContext:
    """Mutable working state carried through a daemon run cycle."""

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

    name: str = "InitialFullBuild"

    def enabled(self, ctx: DaemonContext) -> bool:
        """Return whether no metadata exists and an initial build is needed."""
        return ctx.metadata is None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        """Run Graphify for the initial daemon build."""
        from projectkoios.bootstrap.harness.daemon.graphify_runner import run_graphify

        # Result is the updated context returned by the Graphify runner.
        result: DaemonContext = run_graphify(ctx)
        return result


class WatchFilesystem:
    """Long-running watcher observing the source root for eligible changes."""

    name: str = "WatchFilesystem"

    def enabled(self, ctx: DaemonContext) -> bool:
        """Return whether the filesystem watcher transition may run."""
        return True

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        """Return the context unchanged for the watcher placeholder transition."""
        return ctx


class ScheduleUpdate:
    """Debounce and coalesce layer."""

    name: str = "ScheduleUpdate"

    def enabled(self, ctx: DaemonContext) -> bool:
        """Return whether update scheduling may run."""
        return True

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        """Return the context unchanged for the scheduling placeholder transition."""
        return ctx


class RunGraphifyRefresh:
    """Incremental or refresh Graphify run using defaults."""

    name: str = "RunGraphifyRefresh"

    def enabled(self, ctx: DaemonContext) -> bool:
        """Return whether existing metadata allows a refresh build."""
        return ctx.metadata is not None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        """Run Graphify for a refresh build."""
        from projectkoios.bootstrap.harness.daemon.graphify_runner import run_graphify

        return run_graphify(ctx)


class GenerateChunkCards:
    """Local Ollama universal chunk-card generation."""

    name: str = "GenerateChunkCards"

    def enabled(self, ctx: DaemonContext) -> bool:
        """Return whether a graph snapshot exists for chunk-card generation."""
        return ctx.graph_snapshot is not None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        """Generate chunk cards for the current graph snapshot."""
        from projectkoios.bootstrap.harness.daemon.ollama import generate_chunk_cards

        return generate_chunk_cards(ctx)


class PublishSnapshot:
    """Write fresh snapshot, chunk cards, metadata, and freshness marker."""

    name: str = "PublishSnapshot"

    def enabled(self, ctx: DaemonContext) -> bool:
        """Return whether a graph snapshot exists for publishing."""
        return ctx.graph_snapshot is not None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        """Publish a normal run snapshot for the current context."""
        from projectkoios.bootstrap.harness.daemon.publisher import publish_run

        return publish_run(ctx)


class PublishDegradedSnapshot:
    """Write partial snapshot with warnings and file-level failure metadata."""

    name: str = "PublishDegradedSnapshot"

    def enabled(self, ctx: DaemonContext) -> bool:
        """Return whether failures and a snapshot require degraded publishing."""
        return bool(ctx.failures) and ctx.graph_snapshot is not None

    def apply(self, ctx: DaemonContext) -> DaemonContext:
        """Mark context degraded and publish the degraded snapshot."""
        from projectkoios.bootstrap.harness.daemon.publisher import publish_run

        # Degraded context carries the freshness state and warning expected by publisher.
        degraded_context: DaemonContext = with_degraded_state(ctx)
        return publish_run(degraded_context)


def with_degraded_state(ctx: DaemonContext) -> DaemonContext:
    """Mark the context as degraded before publishing."""
    # New freshness preserves hard failure state and otherwise marks the run degraded.
    new_freshness: FreshnessState = FreshnessState.FAILED if ctx.freshness == FreshnessState.FAILED else FreshnessState.DEGRADED
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
        created_at=now_iso(),
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
