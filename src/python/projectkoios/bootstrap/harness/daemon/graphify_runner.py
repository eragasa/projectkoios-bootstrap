"""Graphify runner — invokes the ``graphify`` CLI and captures metadata."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    FreshnessState,
    GraphSnapshot,
    RunMetadata,
)


GRAPHIFY_UPDATE_TIMEOUT_SECONDS: int = 300
GRAPHIFY_VERSION_TIMEOUT_SECONDS: int = 10
DAEMON_VERSION: str = "0.1.0"


def now_iso() -> str:
    """Return the current UTC timestamp as an ISO string."""
    return datetime.now(timezone.utc).isoformat()


def graphify_version() -> str | None:
    """Return the installed Graphify version string when available."""
    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            ["graphify", "--version"],
            capture_output=True,
            text=True,
            timeout=GRAPHIFY_VERSION_TIMEOUT_SECONDS,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().splitlines()[0]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return None


def read_json_object(path: Path) -> dict[str, Any] | None:
    """Read a JSON object from disk."""
    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def read_chunking_params(repo_root: Path) -> dict[str, str]:
    """Read effective chunking parameters from Graphify's manifest."""
    manifest: Path = repo_root / "graphify-out" / "manifest.json"
    if not manifest.exists():
        return {}
    data: dict[str, Any] | None = read_json_object(manifest)
    if data is None:
        return {}
    params: dict[str, str] = {
        "manifest_file_count": str(len(data)),
    }
    detect: Path = repo_root / "graphify-out" / ".graphify_detect.json"
    if detect.exists():
        detect_data: dict[str, Any] | None = read_json_object(detect)
        if detect_data is not None:
            key: str
            for key in ("language", "chunking", "version"):
                if key in detect_data:
                    params[key] = str(detect_data[key])
    return params


def read_graph_stats(repo_root: Path) -> tuple[int, int, int]:
    """Return ``(node_count, edge_count, community_count)`` from graph.json."""
    graph: Path = repo_root / "graphify-out" / "graph.json"
    if not graph.exists():
        return (0, 0, 0)
    data: dict[str, Any] | None = read_json_object(graph)
    if data is None:
        return (0, 0, 0)
    nodes_value: object = data.get("nodes", [])
    edges_value: object = data.get("edges", [])
    nodes: list[dict[str, Any]] = [node for node in nodes_value if isinstance(node, dict)] if isinstance(nodes_value, list) else []
    edges: list[Any] = list(edges_value) if isinstance(edges_value, list) else []
    communities: set[Any] = {node.get("community") for node in nodes if node.get("community") is not None}
    return (len(nodes), len(edges), len(communities))


def repo_identity(repo_root: Path) -> str:
    """Return a stable repository identity for daemon metadata."""
    return repo_root.resolve().name


def run_graphify(ctx: DaemonContext) -> DaemonContext:
    """Run a Graphify build over the repo root and return an updated context."""
    repo_root: Path = Path(ctx.repo_root)
    started: str = now_iso()
    started_timestamp: float = datetime.now(timezone.utc).timestamp()

    graphify_bin: str | None = shutil.which("graphify")
    if graphify_bin is None:
        return replace(
            ctx,
            freshness=FreshnessState.FAILED,
            failures=ctx.failures + ("graphify binary not found on PATH",),
        )

    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            [graphify_bin, "update", "."],
            capture_output=True,
            text=True,
            timeout=GRAPHIFY_UPDATE_TIMEOUT_SECONDS,
            cwd=str(repo_root),
        )
    except subprocess.TimeoutExpired:
        return replace(
            ctx,
            freshness=FreshnessState.FAILED,
            failures=ctx.failures + (f"graphify update timed out after {GRAPHIFY_UPDATE_TIMEOUT_SECONDS}s",),
        )

    if result.returncode != 0:
        return replace(
            ctx,
            freshness=FreshnessState.FAILED,
            failures=ctx.failures + (f"graphify update exited {result.returncode}: {result.stderr[:200]}",),
        )

    finished: str = now_iso()
    duration: float = datetime.now(timezone.utc).timestamp() - started_timestamp

    graph_stats: tuple[int, int, int] = read_graph_stats(repo_root)
    nodes: int = graph_stats[0]
    edges: int = graph_stats[1]
    communities: int = graph_stats[2]
    chunking: dict[str, str] = read_chunking_params(repo_root)
    version: str | None = graphify_version()

    snapshot: GraphSnapshot = GraphSnapshot(
        run_id=ctx.run_id,
        path=str(repo_root / "graphify-out" / "graph.json"),
        node_count=nodes,
        edge_count=edges,
        community_count=communities,
    )

    metadata: RunMetadata = RunMetadata(
        run_id=ctx.run_id,
        repo_path=ctx.repo_root,
        repo_identity=repo_identity(repo_root),
        daemon_version=DAEMON_VERSION,
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
