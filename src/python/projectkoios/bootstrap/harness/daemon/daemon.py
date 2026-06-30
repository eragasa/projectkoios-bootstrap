"""Daemon orchestrator — runs the activity sequence and the watch loop.

Ties together the CPN ActivityObjects (InitialFullBuild, GenerateChunkCards,
PublishSnapshot) for a single run cycle, then drives the watch loop
(WatchFilesystem, ScheduleUpdate, RunGraphifyRefresh, ...) when running as
a background service.

Also implements the safety gate: detects unexpected source-tree changes
caused by its own run by checking ``git status --short`` before and after.
"""

from __future__ import annotations

import asyncio
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

from projectkoios.bootstrap.harness.daemon.activities import (
    DaemonContext,
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


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:8]


def _git_status_short(repo_root: Path) -> str:
    """Return ``git status --short`` output, or empty string if git fails."""
    try:
        r = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            timeout=15,
        )
        if r.returncode == 0:
            return r.stdout
    except (subprocess.SubprocessError, OSError):
        pass
    return ""


def _check_source_tree_safety(repo_root: Path, before: str, after: str) -> list[str]:
    """Detect unexpected source-tree changes caused by the daemon's own run.

    Returns a list of warning strings. The daemon is expected to only read
    the source tree and write to Hermes-local runtime state outside the repo.
    Any new untracked or modified files that appeared during the run are
    flagged unless they match known daemon-output patterns.
    """
    if before == after:
        return []
    before_lines = set(before.splitlines())
    after_lines = set(after.splitlines())
    new_lines = after_lines - before_lines
    unexpected = []
    for line in new_lines:
        path = line[3:].strip()
        if not path:
            continue
        if path.startswith("graphify-out/"):
            continue
        unexpected.append(f"unexpected source-tree change: {line.strip()}")
    return unexpected


def run_once(
    repo_root: Path,
    trigger_kind: str = "manual",
) -> DaemonRunResult:
    """Run one full daemon cycle: build → cards → publish.

    Performs the initial full Graphify build (or a refresh), generates chunk
    cards via local Ollama, and publishes the result to Hermes-local runtime
    state. Includes the source-tree safety gate.
    """
    from dataclasses import replace

    from projectkoios.bootstrap.harness.daemon.activities import (
        GenerateChunkCards,
        InitialFullBuild,
        PublishDegradedSnapshot,
        PublishSnapshot,
    )

    repo_root = repo_root.resolve()
    run_id = _new_run_id()
    started_at = _now_iso()

    git_before = _git_status_short(repo_root)

    ctx = DaemonContext(
        run_id=run_id,
        repo_root=str(repo_root),
        started_at=started_at,
        trigger_kind=trigger_kind,
        freshness=FreshnessState.UPDATING,
    )

    build = InitialFullBuild()
    ctx = build.apply(ctx)

    if ctx.failures:
        git_after = _git_status_short(repo_root)
        safety = _check_source_tree_safety(repo_root, git_before, git_after)
        ctx = replace(ctx, warnings=ctx.warnings + tuple(safety))
        ctx = PublishDegradedSnapshot().apply(ctx)
    else:
        ctx = GenerateChunkCards().apply(ctx)

        if ctx.failures:
            ctx = PublishDegradedSnapshot().apply(ctx)
        else:
            ctx = PublishSnapshot().apply(ctx)

    git_after = _git_status_short(repo_root)
    safety = _check_source_tree_safety(repo_root, git_before, git_after)
    if safety:
        ctx = replace(ctx, warnings=ctx.warnings + tuple(safety))
        if ctx.metadata is not None:
            ctx = replace(
                ctx,
                metadata=replace(
                    ctx.metadata,
                    warnings=ctx.metadata.warnings + tuple(safety),
                ),
            )

    token = build_token(ctx)
    result = DaemonRunResult(
        metadata=ctx.metadata or _fallback_metadata(ctx),
        graph_snapshot=ctx.graph_snapshot,
        chunk_card_set=ctx.chunk_card_set,
        token=token,
    )
    return result


def _fallback_metadata(ctx: DaemonContext) -> RunMetadata:
    return RunMetadata(
        run_id=ctx.run_id,
        repo_path=ctx.repo_root,
        repo_identity=Path(ctx.repo_root).name,
        daemon_version="0.1.0",
        graphify_version=None,
        freshness=ctx.freshness,
        started_at=ctx.started_at,
        finished_at=_now_iso(),
        trigger_kind=ctx.trigger_kind,
        failures=ctx.failures,
        warnings=ctx.warnings,
    )


async def run_daemon(
    repo_root: Path,
    *,
    poll_interval: float = 2.0,
    stop_event: asyncio.Event | None = None,
    max_cycles: int | None = None,
) -> None:
    """Run the daemon as a background watcher.

    Performs an initial full build, then watches the repository filesystem
    for eligible changes. When changes are detected, debounces and coalesces
    them into a single update request, runs a refresh, generates chunk cards,
    and publishes. Schedules exactly one follow-up update when changes arrive
    during an active update.

    ``max_cycles`` is for testing; when set, the daemon stops after that many
    update cycles (0 means only the initial build).
    """
    repo_root = repo_root.resolve()
    policy = ExclusionPolicy.for_repo(repo_root)
    state = SchedulerState()
    cycles = 0

    initial = run_once(repo_root, trigger_kind="initial")
    _print_result(initial)

    if max_cycles is not None and cycles >= max_cycles:
        return

    print(
        f"[daemon] watching repo={repo_root} poll_interval={poll_interval}s",
        flush=True,
    )

    async def do_update(events: list[WatchEvent]) -> None:
        nonlocal cycles
        cycles += 1
        result = run_once(repo_root, trigger_kind="filesystem")
        _print_result(result)
        if max_cycles is not None and cycles >= max_cycles:
            if stop_event is not None:
                stop_event.set()

    await watch(
        repo_root,
        policy,
        lambda events: run_with_coalesce(events, state, do_update),
        poll_interval=poll_interval,
        stop_event=stop_event,
    )


def _print_result(result: DaemonRunResult) -> None:
    m = result.metadata
    print(
        f"[daemon] run={m.run_id} freshness={m.freshness.value} "
        f"trigger={m.trigger_kind} nodes={m.files_processed} "
        f"cards={result.chunk_card_set.card_count if result.chunk_card_set else 0}",
        flush=True,
    )
    if m.indexed_files_count or m.chunk_batch_count or m.skipped_paths_count or m.eligible_files_count:
        print(
            f"  summary: eligible={m.eligible_files_count} indexed={m.indexed_files_count} "
            f"batches={m.chunk_batch_count} skipped={m.skipped_paths_count} source={m.chunk_batch_source or 'n/a'}",
            flush=True,
        )
    if m.warnings:
        for w in m.warnings:
            print(f"  warn: {w}", flush=True)
    if m.failures:
        for f in m.failures:
            print(f"  fail: {f}", flush=True)
