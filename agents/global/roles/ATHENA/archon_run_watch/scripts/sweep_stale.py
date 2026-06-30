"""Sweep stale Archon runs and optionally clean them up.

Detects orphaned ``running`` rows whose child process has exited without
updating the run status.  Runs at session start or on demand.

Usage
-----
    python sweep_stale.py [--abandon-stale] [--json] [--max-age-minutes 60]
"""

from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import sys

from _run import ArchonClient, RunStatus
from _utils import write_json


DEFAULT_HANDOFF_DIR = "docs/archive/handoffs/hermes"


def list_running_runs(client: ArchonClient) -> list[dict] | str:
    """Return all runs currently in ``running`` status.

    Returns a list of run stubs on success, or an error string.
    """
    return client.list_runs(status="running")


def _handoff_artifact_path(root: Path, handoff_dir: str) -> Path:
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d.%H%M%S")
    return root / handoff_dir / f"{timestamp}_stale-run-sweep.md"


def _write_handoff(
    path: Path,
    results: list[dict],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    rows: list[str] = []
    for r in results:
        abandoned = "yes" if r.get("abandoned") else "no"
        stale = r.get("stale_reason", "")
        wf = r.get("workflow_name", "?")
        rows.append(f"| {r['run_id']} | {wf} | {stale} | {abandoned} |")

    body = f"""Origin: projectkoios-bootstrap
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


def sweep_stale(
    client: ArchonClient,
    max_age_minutes: int = 60,
    abandon: bool = False,
    handoff_path: Path | None = None,
) -> list[dict]:
    """Check all running runs for staleness.

    Parameters
    ----------
    client:
        ArchonCLI client.
    max_age_minutes:
        Maximum age in minutes before a PID-less run is considered stale.
    abandon:
        Whether to abandon stale runs automatically.
    handoff_path:
        If set, write a handoff artifact for abandoned runs.

    Returns
    -------
    list[dict]
        One dict per run checked, each with keys:
        ``run_id``, ``status``, ``workflow_name``, ``stale``, ``stale_reason``,
        ``abandoned``, ``error``.
    """
    stubs = list_running_runs(client)
    if isinstance(stubs, str):
        return [{"error": stubs}]

    results: list[dict] = []
    needs_handoff = False

    for stub in stubs:
        run_id = stub.get("id", "?")
        workflow = stub.get("workflow_name", "?")

        run = client.fetch_run(run_id)
        if isinstance(run, str):
            results.append({
                "run_id": run_id,
                "workflow_name": workflow,
                "error": run,
                "stale": False,
            })
            continue

        reason = run.is_stale(max_age_minutes=max_age_minutes)
        entry: dict = {
            "run_id": run.run_id,
            "workflow_name": run.workflow_name or workflow,
            "status": run.status,
            "stale": reason is not None,
            "stale_reason": reason,
        }

        if reason and abandon:
            err = client.abandon_run(run.run_id)
            entry["abandoned"] = err is None
            if err is None:
                needs_handoff = True
            else:
                entry["error"] = err
        else:
            entry["abandoned"] = False

        results.append(entry)

    if needs_handoff and handoff_path:
        abandoned = [r for r in results if r.get("abandoned")]
        if abandoned:
            _write_handoff(handoff_path, abandoned)

    return results


def format_text(results: list[dict]) -> str:
    """Render sweep results as human-readable text."""
    lines: list[str] = []
    total = len(results)
    stale = sum(1 for r in results if r.get("stale"))
    abandoned = sum(1 for r in results if r.get("abandoned"))
    errors = [r for r in results if r.get("error")]

    lines.append(f"Runs checked: {total}")
    lines.append(f"Stale: {stale}")
    lines.append(f"Abandoned: {abandoned}")
    if errors:
        lines.append(f"Errors: {len(errors)}")
    lines.append("")

    for r in results:
        if r.get("error"):
            lines.append(f"  ! {r['run_id']}: error — {r['error']}")
        elif r.get("stale"):
            lines.append(f"  ✗ {r['run_id']} ({r.get('workflow_name', '?')}): {r['stale_reason']}")
            if r.get("abandoned"):
                lines.append(f"    → abandoned")
        else:
            lines.append(f"  ✓ {r['run_id']} ({r.get('workflow_name', '?')}): alive")

    return "\n".join(lines)


def build_parser() -> ArgumentParser:
    p = ArgumentParser(description="Sweep stale Archon runs and optionally abandon them")
    p.add_argument("--abandon-stale", action="store_true", help="Automatically abandon stale runs")
    p.add_argument("--json", action="store_true", help="Output JSON")
    p.add_argument(
        "--max-age-minutes",
        type=int,
        default=60,
        help="Max age in minutes for PID-less runs before considered stale (default: 60)",
    )
    p.add_argument(
        "--handoff-dir",
        default=DEFAULT_HANDOFF_DIR,
        help=f"Handoff artifact directory relative to repo root (default: {DEFAULT_HANDOFF_DIR})",
    )
    p.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: cwd)",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()
    root = args.root.resolve()

    handoff_path = _handoff_artifact_path(root, args.handoff_dir)

    client = ArchonClient()
    results = sweep_stale(
        client,
        max_age_minutes=args.max_age_minutes,
        abandon=args.abandon_stale,
        handoff_path=handoff_path,
    )

    if not results:
        output = {"checked": 0, "stale": 0, "abandoned": 0, "results": []}
        if args.json:
            write_json(output)
        else:
            print(format_text([]))
        sys.exit(0)

    stale = sum(1 for r in results if r.get("stale"))
    abandoned = sum(1 for r in results if r.get("abandoned"))
    errors = [r for r in results if r.get("error")]

    output = {
        "checked": len(results),
        "stale": stale,
        "abandoned": abandoned,
        "errors": len(errors),
        "results": results,
    }

    if args.json:
        write_json(output)
    else:
        print(format_text(results))

    sys.exit(1 if stale else 0)


if __name__ == "__main__":
    main()
