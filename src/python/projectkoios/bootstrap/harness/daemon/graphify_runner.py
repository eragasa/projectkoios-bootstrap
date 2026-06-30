"""Graphify runner — invokes the ``graphify`` CLI and captures metadata.

Uses Graphify defaults for chunking. Captures the effective chunking
parameters and Graphify tool version from the produced ``manifest.json`` and
``.graphify_detect.json`` so run metadata records what was actually used.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    FreshnessState,
    GraphSnapshot,
    RunMetadata,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _graphify_version() -> str | None:
    try:
        r = subprocess.run(
            ["graphify", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip().splitlines()[0]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return None


def _read_chunking_params(repo_root: Path) -> dict[str, str]:
    """Read effective chunking parameters from Graphify's manifest.

    Graphify records per-file metadata in ``manifest.json``. The first slice
    captures a small summary (file count, any chunking-relevant keys) without
    parsing the full manifest structure.
    """
    manifest = repo_root / "graphify-out" / "manifest.json"
    if not manifest.exists():
        return {}
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    params: dict[str, str] = {
        "manifest_file_count": str(len(data)),
    }
    detect = repo_root / "graphify-out" / ".graphify_detect.json"
    if detect.exists():
        try:
            d = json.loads(detect.read_text(encoding="utf-8"))
            for key in ("language", "chunking", "version"):
                if key in d:
                    params[key] = str(d[key])
        except (json.JSONDecodeError, OSError):
            pass
    return params


def _read_graph_stats(repo_root: Path) -> tuple[int, int, int]:
    """Return (node_count, edge_count, community_count) from graph.json."""
    graph = repo_root / "graphify-out" / "graph.json"
    if not graph.exists():
        return (0, 0, 0)
    try:
        data = json.loads(graph.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return (0, 0, 0)
    nodes = len(data.get("nodes", []))
    edges = len(data.get("edges", []))
    communities = len({n.get("community") for n in data.get("nodes", []) if n.get("community") is not None})
    return (nodes, edges, communities)


def _repo_identity(repo_root: Path) -> str:
    return repo_root.resolve().name


def run_graphify(ctx: DaemonContext) -> DaemonContext:
    """Run a Graphify build over the repo root and return an updated context.

    Invokes ``graphify update .`` (AST-only, no LLM) using Graphify defaults.
    On failure, marks the context as ``failed`` and records the error. On
    success, builds a ``GraphSnapshot`` DataObject and ``RunMetadata``.
    """
    from dataclasses import replace

    repo_root = Path(ctx.repo_root)
    started = _now_iso()
    started_ts = datetime.now(timezone.utc).timestamp()

    graphify_bin = shutil.which("graphify")
    if graphify_bin is None:
        return replace(
            ctx,
            freshness=FreshnessState.FAILED,
            failures=ctx.failures + ("graphify binary not found on PATH",),
        )

    try:
        r = subprocess.run(
            [graphify_bin, "update", "."],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(repo_root),
        )
    except subprocess.TimeoutExpired:
        return replace(
            ctx,
            freshness=FreshnessState.FAILED,
            failures=ctx.failures + ("graphify update timed out after 300s",),
        )

    if r.returncode != 0:
        return replace(
            ctx,
            freshness=FreshnessState.FAILED,
            failures=ctx.failures + (f"graphify update exited {r.returncode}: {r.stderr[:200]}",),
        )

    finished = _now_iso()
    duration = datetime.now(timezone.utc).timestamp() - started_ts

    nodes, edges, communities = _read_graph_stats(repo_root)
    chunking = _read_chunking_params(repo_root)
    version = _graphify_version()

    snapshot = GraphSnapshot(
        run_id=ctx.run_id,
        path=str(repo_root / "graphify-out" / "graph.json"),
        node_count=nodes,
        edge_count=edges,
        community_count=communities,
    )

    metadata = RunMetadata(
        run_id=ctx.run_id,
        repo_path=ctx.repo_root,
        repo_identity=_repo_identity(repo_root),
        daemon_version="0.1.0",
        graphify_version=version,
        chunking_parameters=chunking,
        started_at=started,
        finished_at=finished,
        duration_seconds=duration,
        trigger_kind=ctx.trigger_kind,
        files_processed=nodes,
        freshness=FreshnessState.UPDATING,
    )

    return replace(
        ctx,
        freshness=FreshnessState.UPDATING,
        graph_snapshot=snapshot,
        metadata=metadata,
    )
