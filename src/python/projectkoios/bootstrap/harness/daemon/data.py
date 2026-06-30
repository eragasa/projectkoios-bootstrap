"""Colored Petri net DataObjects for the Graphify ingestion daemon.

These types model daemon runtime state as CPN tokens. They reuse the existing
``Marking`` and ``Violation`` types from ``harness/data/`` and define new
token kinds (not a parallel type hierarchy) for the daemon's first slice.

Freshness places follow the five states named in the ADR:
``fresh``, ``updating``, ``degraded``, ``stale``, ``failed``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class FreshnessState(StrEnum):
    """Daemon freshness places — the places a daemon token may occupy."""

    FRESH = "fresh"
    UPDATING = "updating"
    DEGRADED = "degraded"
    STALE = "stale"
    FAILED = "failed"


class DaemonTokenKind(StrEnum):
    """Kinds of colored tokens the daemon produces and consumes."""

    DAEMON_RUN = "daemon_run"
    GRAPH_SNAPSHOT = "graph_snapshot"
    CHUNK_CARD_SET = "chunk_card_set"
    RUN_METADATA = "run_metadata"


@dataclass(frozen=True)
class DaemonToken:
    """A colored token in the daemon Petri net.

    Mirrors the shape of ``HandoffArtifact`` (a colored token with metadata
    that determines which guards apply) but carries daemon-specific fields
    rather than handoff-header fields. The ``kind`` and ``place`` fields form
    the token's color.
    """

    kind: DaemonTokenKind
    place: FreshnessState
    run_id: str
    created_at: str
    snapshot_path: str | None = None
    card_set_path: str | None = None
    failures: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class GraphSnapshot:
    """Reference to a published Graphify graph snapshot.

    A DataObject pointing at a Hermes-local runtime artifact. Not the graph
    itself — the graph lives on disk under Hermes-local runtime state.
    """

    run_id: str
    path: str
    node_count: int
    edge_count: int
    community_count: int


@dataclass(frozen=True)
class ChunkCard:
    """One universal (role-neutral) chunk card produced by local Ollama.

    Universal chunk cards are repo-local, role-neutral summary objects
    intended to help any agent orient to changed or indexed content. They are
    not role-specific overlays, review-only hints, or a durable knowledge
    ontology.
    """

    chunk_id: str
    source_path: str
    summary: str
    model: str


@dataclass(frozen=True)
class ChunkCardSet:
    """Reference to a published set of universal chunk cards."""

    run_id: str
    path: str
    card_count: int
    model: str
    degraded: bool


@dataclass(frozen=True)
class RunMetadata:
    """Metadata recorded for one daemon run cycle.

    Captures the fields required by ADR adr.20260701.004713 ``architecture-spec``:
    repository identity, tool versions, effective chunking parameters, timing,
    trigger kind, file counts, freshness state, and degraded references.
    """

    run_id: str
    repo_path: str
    repo_identity: str
    daemon_version: str
    graphify_version: str | None
    chunking_parameters: dict[str, str] = field(default_factory=dict)
    ollama_model: str | None = None
    ollama_endpoint: str | None = None
    ollama_degraded: bool = False
    started_at: str = ""
    finished_at: str = ""
    duration_seconds: float = 0.0
    trigger_kind: str = ""
    changed_paths: tuple[str, ...] = ()
    eligible_files_count: int = 0
    indexed_files_count: int = 0
    chunk_batch_count: int = 0
    chunk_batch_source: str | None = None
    skipped_paths_count: int = 0
    exclusion_reasons: tuple[str, ...] = ()
    files_processed: int = 0
    files_failed: int = 0
    files_stale: int = 0
    graph_snapshot_path: str | None = None
    chunk_card_set_path: str | None = None
    freshness: FreshnessState = FreshnessState.FRESH
    previous_snapshot_path: str | None = None
    failures: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Serialise to a JSON-friendly dict for the publisher."""
        return {
            "run_id": self.run_id,
            "repo_path": self.repo_path,
            "repo_identity": self.repo_identity,
            "daemon_version": self.daemon_version,
            "graphify_version": self.graphify_version,
            "chunking_parameters": dict(self.chunking_parameters),
            "ollama_model": self.ollama_model,
            "ollama_endpoint": self.ollama_endpoint,
            "ollama_degraded": self.ollama_degraded,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "trigger_kind": self.trigger_kind,
            "changed_paths": list(self.changed_paths),
            "eligible_files_count": self.eligible_files_count,
            "indexed_files_count": self.indexed_files_count,
            "chunk_batch_count": self.chunk_batch_count,
            "chunk_batch_source": self.chunk_batch_source,
            "skipped_paths_count": self.skipped_paths_count,
            "exclusion_reasons": list(self.exclusion_reasons),
            "files_processed": self.files_processed,
            "files_failed": self.files_failed,
            "files_stale": self.files_stale,
            "graph_snapshot_path": self.graph_snapshot_path,
            "chunk_card_set_path": self.chunk_card_set_path,
            "freshness": self.freshness.value,
            "previous_snapshot_path": self.previous_snapshot_path,
            "failures": list(self.failures),
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class DaemonRunResult:
    """Outcome of one daemon run cycle — DataObjects produced by the run."""

    metadata: RunMetadata
    graph_snapshot: GraphSnapshot | None
    chunk_card_set: ChunkCardSet | None
    token: DaemonToken
