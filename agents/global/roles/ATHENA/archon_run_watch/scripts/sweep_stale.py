"""Sweep stale Archon runs and optionally clean them up."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from typing import Any
import sys

from _run import ArchonClient, RunStatus
from _utils import write_json


DEFAULT_HANDOFF_DIR: str = "docs/archive/handoffs/hermes"


def list_running_runs(client: ArchonClient) -> list[dict[str, Any]] | str:
    """Return all runs currently in ``running`` status."""
    return client.list_runs(status="running")


def handoff_artifact_path(root: Path, handoff_dir: str) -> Path:
    now: datetime = datetime.now()
    timestamp: str = now.strftime("%Y%m%d.%H%M%S")
    return root / handoff_dir / f"{timestamp}_stale-run-sweep.md"


def write_handoff(
    path: Path,
    results: list[dict[str, Any]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    now: str = datetime.now().strftime("%Y-%m-%d %H:%M")

    rows: list[str] = []
    result: dict[str, Any]
    for result in results:
        abandoned: str = "yes" if result.get("abandoned") else "no"
        stale: object = result.get("stale_reason", "")
        workflow: object = result.get("workflow_name", "?")
        rows.append(f"| {result['run_id']} | {workflow} | {stale} | {abandoned} |")

    body: str = f"""Origin: projectkoios-bootstrap
Created: {now}
From: archon-run-sweeper
Status: completed
Kind: stale-run-sweep

# Archon stale-run sweep

| run_id | workflow | reason | abandoned |
|--------|----------|--------|-----------|
{chr(10).join(rows)}

"""
    path.write_text(body, encoding="utf-8")


def stale_entry_for_run(client: ArchonClient, stub: dict[str, Any], max_age_minutes: int, abandon: bool) -> dict[str, Any]:
    run_id: str = str(stub.get("id", "?"))
    workflow: str = str(stub.get("workflow_name", "?"))

    run: RunStatus | str = client.fetch_run(run_id)
    if isinstance(run, str):
        return {
            "run_id": run_id,
            "workflow_name": workflow,
            "error": run,
            "stale": False,
        }

    reason: str | None = run.is_stale(max_age_minutes=max_age_minutes)
    entry: dict[str, Any] = {
        "run_id": run.run_id,
        "workflow_name": run.workflow_name or workflow,
        "status": run.status,
        "stale": reason is not None,
        "stale_reason": reason,
    }

    if reason and abandon:
        err: str | None = client.abandon_run(run.run_id)
        entry["abandoned"] = err is None
        if err is not None:
            entry["error"] = err
    else:
        entry["abandoned"] = False
    return entry


def sweep_stale(
    client: ArchonClient,
    max_age_minutes: int = 60,
    abandon: bool = False,
    handoff_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Check all running runs for staleness."""
    stubs: list[dict[str, Any]] | str = list_running_runs(client)
    if isinstance(stubs, str):
        return [{"error": stubs}]

    results: list[dict[str, Any]] = [
        stale_entry_for_run(client, stub, max_age_minutes, abandon)
        for stub in stubs
    ]

    if handoff_path:
        abandoned_results: list[dict[str, Any]] = [result for result in results if result.get("abandoned")]
        if abandoned_results:
            write_handoff(handoff_path, abandoned_results)

    return results


def format_text(results: list[dict[str, Any]]) -> str:
    """Render sweep results as human-readable text."""
    lines: list[str] = []
    total: int = len(results)
    stale: int = sum(1 for result in results if result.get("stale"))
    abandoned: int = sum(1 for result in results if result.get("abandoned"))
    errors: list[dict[str, Any]] = [result for result in results if result.get("error")]

    lines.append(f"Runs checked: {total}")
    lines.append(f"Stale: {stale}")
    lines.append(f"Abandoned: {abandoned}")
    if errors:
        lines.append(f"Errors: {len(errors)}")
    lines.append("")

    result: dict[str, Any]
    for result in results:
        if result.get("error"):
            lines.append(f"  ! {result['run_id']}: error — {result['error']}")
        elif result.get("stale"):
            lines.append(f"  ✗ {result['run_id']} ({result.get('workflow_name', '?')}): {result['stale_reason']}")
            if result.get("abandoned"):
                lines.append("    → abandoned")
        else:
            lines.append(f"  ✓ {result['run_id']} ({result.get('workflow_name', '?')}): alive")

    return "\n".join(lines)


def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="Sweep stale Archon runs and optionally abandon them")
    parser.add_argument("--abandon-stale", action="store_true", help="Automatically abandon stale runs")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument(
        "--max-age-minutes",
        type=int,
        default=60,
        help="Max age in minutes for PID-less runs before considered stale (default: 60)",
    )
    parser.add_argument(
        "--handoff-dir",
        default=DEFAULT_HANDOFF_DIR,
        help=f"Handoff artifact directory relative to repo root (default: {DEFAULT_HANDOFF_DIR})",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: cwd)",
    )
    return parser


def summary_output(results: list[dict[str, Any]]) -> dict[str, Any]:
    stale: int = sum(1 for result in results if result.get("stale"))
    abandoned: int = sum(1 for result in results if result.get("abandoned"))
    errors: list[dict[str, Any]] = [result for result in results if result.get("error")]
    return {
        "checked": len(results),
        "stale": stale,
        "abandoned": abandoned,
        "errors": len(errors),
        "results": results,
    }


def main() -> None:
    args: Namespace = build_parser().parse_args()
    root: Path = args.root.resolve()

    handoff_path: Path = handoff_artifact_path(root, args.handoff_dir)

    client: ArchonClient = ArchonClient()
    results: list[dict[str, Any]] = sweep_stale(
        client,
        max_age_minutes=args.max_age_minutes,
        abandon=args.abandon_stale,
        handoff_path=handoff_path,
    )

    output: dict[str, Any] = summary_output(results)
    if args.json:
        write_json(output)
    else:
        print(format_text(results))

    sys.exit(1 if output["stale"] else 0)


if __name__ == "__main__":
    main()
