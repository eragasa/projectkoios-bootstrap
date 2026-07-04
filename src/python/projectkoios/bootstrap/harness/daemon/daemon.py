"""Daemon orchestrator — runs the activity sequence and the watch loop."""

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import uuid

from projectkoios.bootstrap.harness.daemon.activities import (
    DaemonContext,
    GenerateChunkCards,
    InitialFullBuild,
    PublishDegradedSnapshot,
    PublishSnapshot,
    build_token,
)
from projectkoios.bootstrap.harness.daemon.data import (
    DaemonRunResult,
    FreshnessState,
    RunMetadata,
)
from projectkoios.bootstrap.harness.daemon.exclusions import ExclusionPolicy
from projectkoios.bootstrap.harness.daemon.scheduler import (
    SchedulerState,
    run_with_coalesce,
)
from projectkoios.bootstrap.harness.daemon.watcher import (
    WatchEvent,
    watch,
)


GIT_STATUS_TIMEOUT_SECONDS: int = 15
DAEMON_VERSION: str = "0.1.0"


def now_iso() -> str:
    """Return the current UTC timestamp as an ISO string."""
    return datetime.now(timezone.utc).isoformat()


def new_run_id() -> str:
    """Create a daemon run identifier."""
    timestamp: str = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    suffix: str = uuid.uuid4().hex[:8]
    return timestamp + "-" + suffix


def git_status_short(repo_root: Path) -> str:
    """Return ``git status --short`` output, or empty string if git fails."""
    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=GIT_STATUS_TIMEOUT_SECONDS,
        )
        if result.returncode == 0:
            return result.stdout
    except (subprocess.SubprocessError, OSError):
        return ""
    return ""


def check_source_tree_safety(repo_root: Path, before: str, after: str) -> list[str]:
    """Detect unexpected source-tree changes caused by the daemon's own run."""
    if before == after:
        return []
    before_lines: set[str] = set(before.splitlines())
    after_lines: set[str] = set(after.splitlines())
    new_lines: set[str] = after_lines - before_lines
    unexpected: list[str] = []
    line: str
    for line in new_lines:
        path: str = line[3:].strip()
        if not path:
            continue
        if path.startswith("graphify-out/"):
            continue
        unexpected.append(f"unexpected source-tree change: {line.strip()}")
    return unexpected


def fallback_metadata(ctx: DaemonContext) -> RunMetadata:
    """Build metadata when a daemon run exits before publishing metadata."""
    return RunMetadata(
        run_id=ctx.run_id,
        repo_path=ctx.repo_root,
        repo_identity=Path(ctx.repo_root).name,
        daemon_version=DAEMON_VERSION,
        graphify_version=None,
        freshness=ctx.freshness,
        started_at=ctx.started_at,
        finished_at=now_iso(),
        trigger_kind=ctx.trigger_kind,
        failures=ctx.failures,
        warnings=ctx.warnings,
    )


def add_safety_warnings(ctx: DaemonContext, safety: Sequence[str]) -> DaemonContext:
    """Return context with source-tree safety warnings added."""
    if not safety:
        return ctx
    warning_tuple: tuple[str, ...] = tuple(safety)
    updated_context: DaemonContext = replace(ctx, warnings=ctx.warnings + warning_tuple)
    if updated_context.metadata is None:
        return updated_context
    return replace(
        updated_context,
        metadata=replace(
            updated_context.metadata,
            warnings=updated_context.metadata.warnings + warning_tuple,
        ),
    )


def publish_after_build(ctx: DaemonContext) -> DaemonContext:
    """Generate cards and publish the appropriate daemon snapshot."""
    if ctx.failures:
        return PublishDegradedSnapshot().apply(ctx)
    card_context: DaemonContext = GenerateChunkCards().apply(ctx)
    if card_context.failures:
        return PublishDegradedSnapshot().apply(card_context)
    return PublishSnapshot().apply(card_context)


def run_once(
    repo_root: Path,
    trigger_kind: str = "manual",
) -> DaemonRunResult:
    """Run one full daemon cycle: build → cards → publish."""
    resolved_repo_root: Path = repo_root.resolve()
    run_id: str = new_run_id()
    started_at: str = now_iso()

    git_before: str = git_status_short(resolved_repo_root)

    ctx: DaemonContext = DaemonContext(
        run_id=run_id,
        repo_root=str(resolved_repo_root),
        started_at=started_at,
        trigger_kind=trigger_kind,
        freshness=FreshnessState.UPDATING,
    )

    build: InitialFullBuild = InitialFullBuild()
    built_context: DaemonContext = build.apply(ctx)
    published_context: DaemonContext = publish_after_build(built_context)

    git_after: str = git_status_short(resolved_repo_root)
    safety: list[str] = check_source_tree_safety(resolved_repo_root, git_before, git_after)
    final_context: DaemonContext = add_safety_warnings(published_context, safety)

    result: DaemonRunResult = DaemonRunResult(
        metadata=final_context.metadata or fallback_metadata(final_context),
        graph_snapshot=final_context.graph_snapshot,
        chunk_card_set=final_context.chunk_card_set,
        token=build_token(final_context),
    )
    return result


async def run_daemon(
    repo_root: Path,
    *,
    poll_interval: float = 2.0,
    stop_event: asyncio.Event | None = None,
    max_cycles: int | None = None,
) -> None:
    """Run the daemon as a background watcher."""
    resolved_repo_root: Path = repo_root.resolve()
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(resolved_repo_root)
    state: SchedulerState = SchedulerState()
    cycles: int = 0

    initial: DaemonRunResult = run_once(resolved_repo_root, trigger_kind="initial")
    print_result(initial)

    if max_cycles is not None and cycles >= max_cycles:
        return

    print(
        f"[daemon] watching repo={resolved_repo_root} poll_interval={poll_interval}s",
        flush=True,
    )

    async def do_update(events: list[WatchEvent]) -> None:
        nonlocal cycles
        cycles += 1
        result: DaemonRunResult = run_once(resolved_repo_root, trigger_kind="filesystem")
        print_result(result)
        if max_cycles is not None and cycles >= max_cycles and stop_event is not None:
            stop_event.set()

    await watch(
        resolved_repo_root,
        policy,
        lambda events: run_with_coalesce(events, state, do_update),
        poll_interval=poll_interval,
        stop_event=stop_event,
    )


def print_result(result: DaemonRunResult) -> None:
    """Print a concise daemon result summary."""
    metadata: RunMetadata = result.metadata
    card_count: int = result.chunk_card_set.card_count if result.chunk_card_set else 0
    print(
        f"[daemon] run={metadata.run_id} freshness={metadata.freshness.value} "
        f"trigger={metadata.trigger_kind} nodes={metadata.files_processed} "
        f"cards={card_count}",
        flush=True,
    )
    if (
        metadata.indexed_files_count
        or metadata.chunk_batch_count
        or metadata.skipped_paths_count
        or metadata.eligible_files_count
    ):
        print(
            f"  summary: eligible={metadata.eligible_files_count} indexed={metadata.indexed_files_count} "
            f"batches={metadata.chunk_batch_count} skipped={metadata.skipped_paths_count} "
            f"source={metadata.chunk_batch_source or 'n/a'}",
            flush=True,
        )
    warning: str
    for warning in metadata.warnings:
        print(f"  warn: {warning}", flush=True)
    failure: str
    for failure in metadata.failures:
        print(f"  fail: {failure}", flush=True)
