"""Graphify runner — invokes the ``graphify`` CLI and captures metadata."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
from typing import TypeAlias, cast

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    FreshnessState,
    GraphSnapshot,
    RunMetadata,
)


JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]

GRAPHIFY_UPDATE_TIMEOUT_SECONDS: int = 300
GRAPHIFY_VERSION_TIMEOUT_SECONDS: int = 10
DAEMON_VERSION: str = "0.1.0"


def now_iso() -> str:
    """Return the current UTC timestamp as an ISO string."""
    return datetime.now(timezone.utc).isoformat()


def graphify_version() -> str | None:
    """Return the installed Graphify version string when available."""
    # Graphify binary is resolved before running the version command.
    graphify_bin: str | None = shutil.which("graphify")
    if graphify_bin is None:
        return None
    # Version remains absent when the command times out or returns no output.
    version: str | None = None
    try:
        # Result captures the version command output without mutating repository state.
        result: subprocess.CompletedProcess[str] = subprocess.run(
            [graphify_bin, "--version"],
            capture_output=True,
            text=True,
            timeout=GRAPHIFY_VERSION_TIMEOUT_SECONDS,
        )
        if result.returncode == 0 and result.stdout.strip():
            version = result.stdout.strip().splitlines()[0]
    except subprocess.TimeoutExpired:
        version = None
    return version


def read_json_object(path: Path) -> JsonObject | None:
    """Read a JSON object from disk."""
    # Data is populated only when the file contains parseable JSON.
    data: JsonValue | None = None
    try:
        # Data is parsed from UTF-8 JSON content for subsequent shape checks.
        data = cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError):
        data = None
    return data if isinstance(data, dict) else None


def read_chunking_params(repo_root: Path) -> dict[str, str]:
    """Read effective chunking parameters from Graphify's manifest."""
    # Manifest is Graphify's generated metadata file for the latest run.
    manifest: Path = repo_root / "graphify-out" / "manifest.json"
    if not manifest.exists():
        return {}
    # Data is the parsed manifest object when it is valid JSON.
    data: JsonObject | None = read_json_object(manifest)
    if data is None:
        return {}
    # Params records stringified effective chunking metadata for run metadata.
    params: dict[str, str] = {
        "manifest_file_count": str(len(data)),
    }
    # Detect file may include language, chunking, and version metadata.
    detect: Path = repo_root / "graphify-out" / ".graphify_detect.json"
    if detect.exists():
        # Detect data is the parsed Graphify detection metadata object.
        detect_data: JsonObject | None = read_json_object(detect)
        if detect_data is not None:
            key: str
            for key in ("language", "chunking", "version"):
                if key in detect_data:
                    params[key] = str(detect_data[key])
    return params


def read_graph_stats(repo_root: Path) -> tuple[int, int, int]:
    """Return ``(node_count, edge_count, community_count)`` from graph.json."""
    # Graph is the generated Graphify JSON artifact inspected for summary counts.
    graph: Path = repo_root / "graphify-out" / "graph.json"
    if not graph.exists():
        return (0, 0, 0)
    # Data is the parsed graph object when the artifact is valid JSON.
    data: JsonObject | None = read_json_object(graph)
    if data is None:
        return (0, 0, 0)
    # Nodes value is the raw JSON value under the graph nodes key.
    nodes_value: JsonValue = data.get("nodes", [])
    # Edges value is the raw JSON value under the graph edges key.
    edges_value: JsonValue = data.get("edges", [])
    # Nodes keeps only object-shaped node records for count and community extraction.
    nodes: list[JsonObject] = [node for node in nodes_value if isinstance(node, dict)] if isinstance(nodes_value, list) else []
    # Edges keeps raw list entries because only the edge count is needed.
    edges: list[JsonValue] = list(edges_value) if isinstance(edges_value, list) else []
    # Communities records non-null community identifiers from object-shaped nodes.
    communities: set[JsonValue] = {node.get("community") for node in nodes if node.get("community") is not None}
    return (len(nodes), len(edges), len(communities))


def repo_identity(repo_root: Path) -> str:
    """Return a stable repository identity for daemon metadata."""
    return repo_root.resolve().name


def run_graphify(ctx: DaemonContext) -> DaemonContext:
    """Run a Graphify build over the repo root and return an updated context."""
    # Repository root is the concrete path passed to Graphify.
    repo_root: Path = Path(ctx.repo_root)
    # Started is the ISO timestamp recorded in run metadata.
    started: str = now_iso()
    # Started timestamp supports duration calculation after Graphify exits.
    started_timestamp: float = datetime.now(timezone.utc).timestamp()

    # Graphify binary is resolved before subprocess execution for clearer failure metadata.
    graphify_bin: str | None = shutil.which("graphify")
    if graphify_bin is None:
        return replace(
            ctx,
            freshness=FreshnessState.FAILED,
            failures=ctx.failures + ("graphify binary not found on PATH",),
        )

    try:
        # Result captures Graphify update output for return-code and failure reporting.
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

    # Finished is the ISO timestamp recorded after Graphify completes.
    finished: str = now_iso()
    # Duration is measured in seconds for run metadata.
    duration: float = datetime.now(timezone.utc).timestamp() - started_timestamp

    # Graph stats contain node, edge, and community counts from graph.json.
    graph_stats: tuple[int, int, int] = read_graph_stats(repo_root)
    # Nodes is the Graphify node count stored in metadata and snapshot records.
    nodes: int = graph_stats[0]
    # Edges is the Graphify edge count stored in the snapshot record.
    edges: int = graph_stats[1]
    # Communities is the Graphify community count stored in the snapshot record.
    communities: int = graph_stats[2]
    # Chunking stores Graphify manifest and detection metadata as strings.
    chunking: dict[str, str] = read_chunking_params(repo_root)
    # Version stores Graphify CLI version when available.
    version: str | None = graphify_version()

    # Snapshot points to the generated graph artifact and its summary counts.
    snapshot: GraphSnapshot = GraphSnapshot(
        run_id=ctx.run_id,
        path=str(repo_root / "graphify-out" / "graph.json"),
        node_count=nodes,
        edge_count=edges,
        community_count=communities,
    )

    # Metadata captures the Graphify run details consumed by publisher output.
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
