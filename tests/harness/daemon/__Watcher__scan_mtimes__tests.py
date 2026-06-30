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
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".gitignore").write_text("*.log\n", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "a.py").write_text("a = 1\n", encoding="utf-8")
    (root / "src" / "b.py").write_text("b = 2\n", encoding="utf-8")
    return root


def test__scan_mtimes__records_eligible_files(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    policy = ExclusionPolicy.for_repo(root)
    snap = scan_mtimes(root, policy)
    assert "src/a.py" in snap.mtimes
    assert "src/b.py" in snap.mtimes


def test__scan_mtimes__excludes_builtins(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    (root / "graphify-out").mkdir()
    (root / "graphify-out" / "graph.json").write_text("{}", encoding="utf-8")
    (root / "app.log").write_text("log", encoding="utf-8")
    (root / ".venv").mkdir()
    (root / ".venv" / "bin").mkdir()
    (root / ".venv" / "bin" / "python").write_text("#", encoding="utf-8")
    policy = ExclusionPolicy.for_repo(root)
    snap = scan_mtimes(root, policy)
    assert "graphify-out/graph.json" not in snap.mtimes
    assert "app.log" not in snap.mtimes
    assert ".venv/bin/python" not in snap.mtimes


def test__diff_snapshots__detects_added(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    prev = FileSnapshot(mtimes={"src/a.py": 1000.0})
    curr = FileSnapshot(mtimes={"src/a.py": 1000.0, "src/b.py": 2000.0})
    events = diff_snapshots(prev, curr, root)
    assert len(events) == 1
    assert events[0].kind == "added"
    assert events[0].path == root / "src" / "b.py"


def test__diff_snapshots__detects_modified(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    prev = FileSnapshot(mtimes={"src/a.py": 1000.0})
    curr = FileSnapshot(mtimes={"src/a.py": 2000.0})
    events = diff_snapshots(prev, curr, root)
    assert len(events) == 1
    assert events[0].kind == "modified"


def test__diff_snapshots__detects_removed(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    prev = FileSnapshot(mtimes={"src/a.py": 1000.0})
    curr = FileSnapshot(mtimes={})
    events = diff_snapshots(prev, curr, root)
    assert len(events) == 1
    assert events[0].kind == "removed"


def test__diff_snapshots__no_changes_returns_empty(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    prev = FileSnapshot(mtimes={"src/a.py": 1000.0})
    curr = FileSnapshot(mtimes={"src/a.py": 1000.0})
    events = diff_snapshots(prev, curr, root)
    assert events == []


def test__watch__emits_events_on_change(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    policy = ExclusionPolicy.for_repo(root)
    received: list[list[WatchEvent]] = []
    stop = asyncio.Event()

    async def on_events(events: list[WatchEvent]) -> None:
        received.append(events)
        stop.set()

    async def _trigger() -> None:
        await asyncio.sleep(0.15)
        (root / "src" / "c.py").write_text("c = 3\n", encoding="utf-8")

    async def _run() -> None:
        await asyncio.gather(
            watch(root, policy, on_events, poll_interval=0.05, stop_event=stop),
            _trigger(),
        )

    asyncio.run(asyncio.wait_for(_run(), timeout=5.0))
    assert len(received) >= 1
    all_events = [e for batch in received for e in batch]
    assert any(e.kind == "added" and e.path.name == "c.py" for e in all_events)
