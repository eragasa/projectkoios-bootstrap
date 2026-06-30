"""Filesystem watcher using stdlib asyncio polling.

Polls ``os.scandir`` / ``os.stat`` mtimes on a debounce interval. No native
FS event dependency (e.g. ``watchdog``) — stdlib only, cross-platform.

The watcher compares the current scan against the last scan and emits changed
paths. The scheduler (``scheduler.py``) debounces and coalesces these events.
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
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
    """Walk *repo_root* and record mtimes for eligible files.

    Excluded paths are skipped entirely (no stat call). Symbolic links are
    followed only for the final path; directories are not descended into when
    their name matches a built-in exclude.
    """
    mtimes: dict[str, float] = {}
    root = repo_root.resolve()
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dir_path = Path(dirpath)
        try:
            dir_path.relative_to(root)
        except ValueError:
            continue
        if policy.is_excluded(dir_path) and dir_path != root:
            dirnames[:] = []
            continue
        pruned: list[str] = []
        for d in dirnames:
            if policy.is_excluded(dir_path / d):
                pruned.append(d)
        for d in pruned:
            dirnames.remove(d)
        for fname in filenames:
            fpath = dir_path / fname
            if policy.is_excluded(fpath):
                continue
            try:
                st = fpath.stat()
            except OSError:
                continue
            rel_posix = fpath.relative_to(root).as_posix()
            mtimes[rel_posix] = st.st_mtime
    return FileSnapshot(mtimes=mtimes)


def diff_snapshots(
    prev: FileSnapshot,
    curr: FileSnapshot,
    repo_root: Path,
) -> list[WatchEvent]:
    """Return the set of changed paths between two snapshots.

    A change is a new file, a removed file, or a file whose mtime changed.
    """
    events: list[WatchEvent] = []
    prev_m = prev.mtimes
    curr_m = curr.mtimes
    for rel, mtime in curr_m.items():
        if rel not in prev_m:
            events.append(WatchEvent(path=repo_root / rel, kind="added"))
        elif prev_m[rel] != mtime:
            events.append(WatchEvent(path=repo_root / rel, kind="modified"))
    for rel in prev_m:
        if rel not in curr_m:
            events.append(WatchEvent(path=repo_root / rel, kind="removed"))
    return events


async def watch(
    repo_root: Path,
    policy: ExclusionPolicy,
    on_events,
    *,
    poll_interval: float = 2.0,
    stop_event: asyncio.Event | None = None,
) -> None:
    """Poll *repo_root* and call *on_events* with detected changes.

    Runs until *stop_event* is set. Each poll cycle scans mtimes, diffs
    against the previous snapshot, and invokes *on_events* with the list of
    ``WatchEvent`` objects (which may be empty).
    """
    prev = scan_mtimes(repo_root, policy)
    while stop_event is None or not stop_event.is_set():
        await asyncio.sleep(poll_interval)
        curr = scan_mtimes(repo_root, policy)
        events = diff_snapshots(prev, curr, repo_root)
        if events:
            await on_events(events)
        prev = curr
