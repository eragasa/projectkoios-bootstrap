from __future__ import annotations

import asyncio
from pathlib import Path

from projectkoios.bootstrap.harness.daemon.exclusions import ExclusionPolicy
from projectkoios.bootstrap.harness.daemon.watcher import (
    FileSnapshot,
    WatchEvent,
    diff_snapshots,
    scan_mtimes,
    watch,
)


def _make_repo(tmp_path: Path) -> Path:
    """Create a repository fixture for watcher tests."""
    # Root is the temporary repository path scanned by watcher helpers.
    root: Path = tmp_path / "repo"
    root.mkdir()
    (root / ".gitignore").write_text("*.log\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "a.py").write_text("a = 1\n", encoding="utf-8")
    (root / "src" / "b.py").write_text("b = 2\n", encoding="utf-8")
    return root


def test__scan_mtimes__records_eligible_files(tmp_path: Path) -> None:
    """Validate mtime scanning records eligible source files."""
    # Root is the repository fixture scanned by watcher helpers.
    root: Path = _make_repo(tmp_path)
    # Policy filters built-in and gitignore-excluded paths.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    # Snapshot contains mtimes for eligible repository files.
    snapshot: FileSnapshot = scan_mtimes(root, policy)
    assert "src/a.py" in snapshot.mtimes
    assert "src/b.py" in snapshot.mtimes


def test__scan_mtimes__excludes_builtins(tmp_path: Path) -> None:
    """Validate mtime scanning excludes generated and ignored paths."""
    # Root is the repository fixture scanned by watcher helpers.
    root: Path = _make_repo(tmp_path)
    (root / "graphify-out").mkdir()
    (root / "graphify-out" / "graph.json").write_text("{}", encoding="utf-8")
    (root / "app.log").write_text("log", encoding="utf-8")
    (root / ".venv").mkdir()
    (root / ".venv" / "bin").mkdir()
    (root / ".venv" / "bin" / "python").write_text("#", encoding="utf-8")
    # Policy filters built-in and gitignore-excluded paths.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    # Snapshot contains only eligible repository files.
    snapshot: FileSnapshot = scan_mtimes(root, policy)
    assert "graphify-out/graph.json" not in snapshot.mtimes
    assert "app.log" not in snapshot.mtimes
    assert ".venv/bin/python" not in snapshot.mtimes


def test__diff_snapshots__detects_added(tmp_path: Path) -> None:
    """Validate snapshot diffing reports added files."""
    # Root is used to resolve relative snapshot paths into event paths.
    root: Path = _make_repo(tmp_path)
    # Previous snapshot contains the pre-change file set.
    previous: FileSnapshot = FileSnapshot(mtimes={"src/a.py": 1000.0})
    # Current snapshot contains one additional file.
    current: FileSnapshot = FileSnapshot(mtimes={"src/a.py": 1000.0, "src/b.py": 2000.0})
    # Events describe the difference between snapshots.
    events: list[WatchEvent] = diff_snapshots(previous, current, root)
    assert len(events) == 1
    assert events[0].kind == "added"
    assert events[0].path == root / "src" / "b.py"


def test__diff_snapshots__detects_modified(tmp_path: Path) -> None:
    """Validate snapshot diffing reports modified files."""
    # Root is used to resolve relative snapshot paths into event paths.
    root: Path = _make_repo(tmp_path)
    # Previous snapshot contains the original mtime.
    previous: FileSnapshot = FileSnapshot(mtimes={"src/a.py": 1000.0})
    # Current snapshot contains an updated mtime.
    current: FileSnapshot = FileSnapshot(mtimes={"src/a.py": 2000.0})
    # Events describe the difference between snapshots.
    events: list[WatchEvent] = diff_snapshots(previous, current, root)
    assert len(events) == 1
    assert events[0].kind == "modified"


def test__diff_snapshots__detects_removed(tmp_path: Path) -> None:
    """Validate snapshot diffing reports removed files."""
    # Root is used to resolve relative snapshot paths into event paths.
    root: Path = _make_repo(tmp_path)
    # Previous snapshot contains a file before removal.
    previous: FileSnapshot = FileSnapshot(mtimes={"src/a.py": 1000.0})
    # Current snapshot is empty after removal.
    current: FileSnapshot = FileSnapshot(mtimes={})
    # Events describe the difference between snapshots.
    events: list[WatchEvent] = diff_snapshots(previous, current, root)
    assert len(events) == 1
    assert events[0].kind == "removed"


def test__diff_snapshots__no_changes_returns_empty(tmp_path: Path) -> None:
    """Validate identical snapshots produce no events."""
    # Root is used to resolve relative snapshot paths into event paths.
    root: Path = _make_repo(tmp_path)
    # Previous snapshot contains the pre-change file set.
    previous: FileSnapshot = FileSnapshot(mtimes={"src/a.py": 1000.0})
    # Current snapshot has the same file and mtime.
    current: FileSnapshot = FileSnapshot(mtimes={"src/a.py": 1000.0})
    # Events describe the difference between snapshots.
    events: list[WatchEvent] = diff_snapshots(previous, current, root)
    assert events == []


def test__watch__emits_events_on_change(tmp_path: Path) -> None:
    """Validate watcher emits events when an eligible file changes."""
    # Root is the repository fixture watched for filesystem changes.
    root: Path = _make_repo(tmp_path)
    # Policy filters watcher events to eligible source paths.
    policy: ExclusionPolicy = ExclusionPolicy.for_repo(root)
    # Received batches collect events emitted by the watcher callback.
    received: list[list[WatchEvent]] = []
    # Stop event terminates the watcher after the first callback.
    stop: asyncio.Event = asyncio.Event()

    async def on_events(events: list[WatchEvent]) -> None:
        """Collect emitted watcher events and stop the watcher."""
        received.append(events)
        stop.set()

    async def trigger_change() -> None:
        """Create an eligible file after watcher startup."""
        await asyncio.sleep(0.15)
        (root / "src" / "c.py").write_text("c = 3\n", encoding="utf-8")

    async def run_watcher() -> None:
        """Run watcher and trigger coroutines together."""
        await asyncio.gather(
            watch(root, policy, on_events, poll_interval=0.05, stop_event=stop),
            trigger_change(),
        )

    asyncio.run(asyncio.wait_for(run_watcher(), timeout=5.0))
    assert len(received) >= 1
    # All events flattens callback batches for the final assertion.
    all_events: list[WatchEvent] = [event for batch in received for event in batch]
    assert any(event.kind == "added" and event.path.name == "c.py" for event in all_events)
