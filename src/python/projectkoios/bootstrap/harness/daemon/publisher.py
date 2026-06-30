"""Publisher — writes daemon output to Hermes-local runtime state.

All generated output (graph snapshots, chunk cards, run metadata, freshness
markers, degraded-state reports) is written under
``~/.pi/koios-ingestion/projectkoios-bootstrap/``. This is Hermes-local runtime
state and must never be committed to the repository.

The default output path convention is documented in the run metadata so
agents can discover output without committed per-agent bootstrap folders.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from projectkoios.bootstrap.harness.daemon.activities import DaemonContext
from projectkoios.bootstrap.harness.daemon.data import (
    FreshnessState,
)


DEFAULT_RUNTIME_ROOT = Path.home() / ".pi" / "koios-ingestion"
"""Default Hermes-local runtime root for all ingestion daemon output."""


def runtime_dir_for(repo_identity: str) -> Path:
    """Return the runtime output directory for a given repository identity."""
    return DEFAULT_RUNTIME_ROOT / repo_identity


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def publish_run(ctx: DaemonContext) -> DaemonContext:
    """Publish the current run's DataObjects to Hermes-local runtime state.

    Writes:
    - ``graph.json`` — a copy of the current Graphify graph snapshot
    - ``chunk_cards.json`` — the universal chunk card set (if any)
    - ``run_metadata.json`` — the run metadata block
    - ``freshness`` — a single-line freshness marker file
    - ``degraded.json`` — degraded-state report (only when degraded)
    - ``latest`` — symlink or pointer to the latest run directory

    Returns the context with freshness finalised.
    """
    from dataclasses import replace

    if ctx.graph_snapshot is None or ctx.metadata is None:
        return ctx

    repo_identity = ctx.metadata.repo_identity
    run_dir = runtime_dir_for(repo_identity) / ctx.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    graph_snapshot_path = Path(ctx.graph_snapshot.path)
    if graph_snapshot_path.exists():
        shutil.copy2(graph_snapshot_path, run_dir / "graph.json")

    card_set_path = ""
    if ctx.chunk_card_set is not None and ctx.chunk_cards:
        card_set_path = str(run_dir / "chunk_cards.json")
        cards_payload = [
            {
                "chunk_id": c.chunk_id,
                "source_path": c.source_path,
                "summary": c.summary,
                "model": c.model,
            }
            for c in ctx.chunk_cards
        ]
        Path(card_set_path).write_text(
            json.dumps({
                "run_id": ctx.run_id,
                "model": ctx.chunk_card_set.model,
                "degraded": ctx.chunk_card_set.degraded,
                "card_count": len(cards_payload),
                "cards": cards_payload,
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    freshness = ctx.freshness if ctx.freshness != FreshnessState.UPDATING else FreshnessState.FRESH
    if ctx.failures:
        freshness = FreshnessState.DEGRADED

    metadata = replace(
        ctx.metadata,
        graph_snapshot_path=str(run_dir / "graph.json"),
        chunk_card_set_path=card_set_path or None,
        freshness=freshness,
        finished_at=_now_iso(),
        warnings=ctx.warnings,
        failures=ctx.failures,
    )

    (run_dir / "run_metadata.json").write_text(
        json.dumps(metadata.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (run_dir / "freshness").write_text(freshness.value + "\n", encoding="utf-8")

    if freshness == FreshnessState.DEGRADED:
        degraded_report = {
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

    latest = runtime_dir_for(repo_identity) / "latest"
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(run_dir, target_is_directory=True)

    return replace(ctx, freshness=freshness, metadata=metadata)
