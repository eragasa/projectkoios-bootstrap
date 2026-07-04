"""Filesystem watcher using stdlib asyncio polling."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
import os
from pathlib import Path

from projectkoios.bootstrap.harness.daemon.exclusions import ExclusionPolicy


@dataclass
class FileSnapshot:
    """A point-in-time snapshot of file mtimes under the repo root."""

    mtimes: dict[str, float] = field(default_factory=dict)


@dataclass
class WatchEvent:
    """A single detected filesystem change."""

    path: Path
    kind: str


def scan_mtimes(repo_root: Path, policy: ExclusionPolicy) -> FileSnapshot:
    """Walk *repo_root* and record mtimes for eligible files."""
    mtimes: dict[str, float] = {}
    root: Path = repo_root.resolve()
    dirpath: str
    dirnames: list[str]
    filenames: list[str]
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dir_path: Path = Path(dirpath)
        try:
            dir_path.relative_to(root)
        except ValueError:
            continue
        if policy.is_excluded(dir_path) and dir_path != root:
            dirnames[:] = []
            continue
        pruned: list[str] = [dirname for dirname in dirnames if policy.is_excluded(dir_path / dirname)]
        dirname: str
        for dirname in pruned:
            dirnames.remove(dirname)
        filename: str
        for filename in filenames:
            file_path: Path = dir_path / filename
            if policy.is_excluded(file_path):
                continue
            try:
                stat_result: os.stat_result = file_path.stat()
            except OSError:
                continue
            rel_posix: str = file_path.relative_to(root).as_posix()
            mtimes[rel_posix] = stat_result.st_mtime
    return FileSnapshot(mtimes=mtimes)


def diff_snapshots(
    prev: FileSnapshot,
    curr: FileSnapshot,
    repo_root: Path,
) -> list[WatchEvent]:
    """Return the set of changed paths between two snapshots."""
    events: list[WatchEvent] = []
    prev_mtimes: dict[str, float] = prev.mtimes
    curr_mtimes: dict[str, float] = curr.mtimes
    rel_path: str
    mtime: float
    for rel_path, mtime in curr_mtimes.items():
        if rel_path not in prev_mtimes:
            events.append(WatchEvent(path=repo_root / rel_path, kind="added"))
        elif prev_mtimes[rel_path] != mtime:
            events.append(WatchEvent(path=repo_root / rel_path, kind="modified"))
    for rel_path in prev_mtimes:
        if rel_path not in curr_mtimes:
            events.append(WatchEvent(path=repo_root / rel_path, kind="removed"))
    return events


async def watch(
    repo_root: Path,
    policy: ExclusionPolicy,
    on_events: Callable[[list[WatchEvent]], Awaitable[None]],
    *,
    poll_interval: float = 2.0,
    stop_event: asyncio.Event | None = None,
) -> None:
    """Poll *repo_root* and call *on_events* with detected changes."""
    previous_snapshots: list[FileSnapshot] = [scan_mtimes(repo_root, policy)]
    while stop_event is None or not stop_event.is_set():
        await asyncio.sleep(poll_interval)
        curr_snapshot: FileSnapshot = scan_mtimes(repo_root, policy)
        events: list[WatchEvent] = diff_snapshots(previous_snapshots[0], curr_snapshot, repo_root)
        if events:
            await on_events(events)
        previous_snapshots[0] = curr_snapshot
