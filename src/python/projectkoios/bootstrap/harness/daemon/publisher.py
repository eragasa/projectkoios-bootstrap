"""Publisher — writes daemon output to Hermes-local runtime state."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    FreshnessState,
    RunMetadata,
)


DEFAULT_RUNTIME_ROOT: Path = Path.home() / ".pi" / "koios-ingestion"
"""Default Hermes-local runtime root for all ingestion daemon output."""


def runtime_dir_for(repo_identity: str) -> Path:
    """Return the runtime output directory for a given repository identity."""
    return DEFAULT_RUNTIME_ROOT / repo_identity


def now_iso() -> str:
    """Return the current UTC timestamp as an ISO string."""
    return datetime.now(timezone.utc).isoformat()


def chunk_cards_payload(ctx: DaemonContext) -> list[dict[str, str]]:
    """Return JSON-ready chunk card records for a daemon context."""
    return [
        {
            "chunk_id": card.chunk_id,
            "source_path": card.source_path,
            "summary": card.summary,
            "model": card.model,
        }
        for card in ctx.chunk_cards
    ]


def write_chunk_cards(ctx: DaemonContext, run_dir: Path) -> str:
    """Write chunk cards when present and return the written path or empty string."""
    if ctx.chunk_card_set is None or not ctx.chunk_cards:
        return ""
    card_set_path: Path = run_dir / "chunk_cards.json"
    cards_payload: list[dict[str, str]] = chunk_cards_payload(ctx)
    payload: dict[str, Any] = {
        "run_id": ctx.run_id,
        "model": ctx.chunk_card_set.model,
        "degraded": ctx.chunk_card_set.degraded,
        "card_count": len(cards_payload),
        "cards": cards_payload,
    }
    card_set_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return str(card_set_path)


def final_freshness(ctx: DaemonContext) -> FreshnessState:
    """Return the final freshness state to publish."""
    if ctx.failures:
        return FreshnessState.DEGRADED
    return ctx.freshness if ctx.freshness != FreshnessState.UPDATING else FreshnessState.FRESH


def write_degraded_report(ctx: DaemonContext, metadata: RunMetadata, run_dir: Path, freshness: FreshnessState) -> None:
    """Write degraded-state report when the run is degraded."""
    if freshness != FreshnessState.DEGRADED:
        return
    degraded_report: dict[str, Any] = {
        "run_id": ctx.run_id,
        "freshness": freshness.value,
        "failures": list(ctx.failures),
        "warnings": list(ctx.warnings),
        "previous_snapshot": metadata.previous_snapshot_path,
    }
    (run_dir / "degraded.json").write_text(
        json.dumps(degraded_report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def update_latest_symlink(repo_identity: str, run_dir: Path) -> None:
    """Update the latest symlink for a repository runtime directory."""
    latest: Path = runtime_dir_for(repo_identity) / "latest"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(run_dir, target_is_directory=True)


def publish_run(ctx: DaemonContext) -> DaemonContext:
    """Publish the current run's DataObjects to Hermes-local runtime state."""
    if ctx.graph_snapshot is None or ctx.metadata is None:
        return ctx

    repo_identity: str = ctx.metadata.repo_identity
    run_dir: Path = runtime_dir_for(repo_identity) / ctx.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    graph_snapshot_path: Path = Path(ctx.graph_snapshot.path)
    if graph_snapshot_path.exists():
        shutil.copy2(graph_snapshot_path, run_dir / "graph.json")

    card_set_path: str = write_chunk_cards(ctx, run_dir)
    freshness: FreshnessState = final_freshness(ctx)

    metadata: RunMetadata = replace(
        ctx.metadata,
        graph_snapshot_path=str(run_dir / "graph.json"),
        chunk_card_set_path=card_set_path or None,
        freshness=freshness,
        finished_at=now_iso(),
        warnings=ctx.warnings,
        failures=ctx.failures,
    )

    (run_dir / "run_metadata.json").write_text(
        json.dumps(metadata.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (run_dir / "freshness").write_text(freshness.value + "\n", encoding="utf-8")

    write_degraded_report(ctx, metadata, run_dir, freshness)
    update_latest_symlink(repo_identity, run_dir)

    return replace(ctx, freshness=freshness, metadata=metadata)
