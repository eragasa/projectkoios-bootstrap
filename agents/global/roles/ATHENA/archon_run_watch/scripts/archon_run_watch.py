"""Monitor one Archon run and detect stale detached runs.

Usage
-----
    python archon_run_watch.py --run-id <id> [--abandon-stale] [--json]
"""

from __future__ import annotations

from argparse import ArgumentParser
import os
import sys

from _run import ArchonClient, RunStatus
from _utils import write_json


def main() -> None:
    p = ArgumentParser(description="Monitor an Archon run and detect stale detached runs")
    p.add_argument("--run-id", required=True, help="Archon workflow run ID")
    p.add_argument("--log", help="Path to detached child log file")
    p.add_argument("--abandon-stale", action="store_true", help="Automatically abandon stale runs")
    p.add_argument("--json", action="store_true", help="Output JSON")
    args = p.parse_args()

    client = ArchonClient()
    run = client.fetch_run(args.run_id)
    if isinstance(run, str):
        result = {"run_id": args.run_id, "error": run}
        if args.json:
            write_json(result)
        else:
            print(f"error: {run}")
        sys.exit(1)

    stale_reason = run.is_stale()
    log_info: str | None = None
    if args.log:
        log_info = f"{args.log} exists" if os.path.exists(args.log) else f"{args.log} not found"

    result = {
        "run_id": run.run_id,
        "status": run.status,
        "pid": run.pid,
        "stale": stale_reason is not None,
        "stale_reason": stale_reason,
        "log": log_info,
    }

    if stale_reason and args.abandon_stale:
        abandon_err = client.abandon_run(args.run_id)
        result["abandoned"] = abandon_err is None
        if abandon_err:
            result["abandon_error"] = abandon_err

    if args.json:
        write_json(result)
    else:
        parts = [
            f"run_id: {run.run_id}",
            f"status: {run.status}",
        ]
        if run.pid is not None:
            parts.append(f"pid: {run.pid}")
        if stale_reason:
            parts.append(f"stale: {stale_reason}")
        else:
            parts.append("stale: no")
        if log_info:
            parts.append(f"log: {log_info}")
        if result.get("abandoned"):
            parts.append("abandoned: yes")
        elif result.get("abandon_error"):
            parts.append(f"abandon_error: {result['abandon_error']}")
        print(" | ".join(parts))

    sys.exit(1 if stale_reason else 0)


if __name__ == "__main__":
    main()
