"""Monitor one Archon run and detect stale detached runs."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from typing import Any
import os
import sys

from _run import ArchonClient, RunStatus
from _utils import write_json


def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="Monitor an Archon run and detect stale detached runs")
    parser.add_argument("--run-id", required=True, help="Archon workflow run ID")
    parser.add_argument("--log", help="Path to detached child log file")
    parser.add_argument("--abandon-stale", action="store_true", help="Automatically abandon stale runs")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    return parser


def render_text(run: RunStatus, stale_reason: str | None, log_info: str | None, result: dict[str, Any]) -> str:
    parts: list[str] = [
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
    return " | ".join(parts)


def main() -> None:
    args: Namespace = build_parser().parse_args()

    client: ArchonClient = ArchonClient()
    run: RunStatus | str = client.fetch_run(args.run_id)
    if isinstance(run, str):
        error_result: dict[str, Any] = {"run_id": args.run_id, "error": run}
        if args.json:
            write_json(error_result)
        else:
            print(f"error: {run}")
        sys.exit(1)

    stale_reason: str | None = run.is_stale()
    log_info: str | None = (
        f"{args.log} exists" if args.log and os.path.exists(args.log)
        else f"{args.log} not found" if args.log
        else None
    )

    result: dict[str, Any] = {
        "run_id": run.run_id,
        "status": run.status,
        "pid": run.pid,
        "stale": stale_reason is not None,
        "stale_reason": stale_reason,
        "log": log_info,
    }

    if stale_reason and args.abandon_stale:
        abandon_err: str | None = client.abandon_run(args.run_id)
        result["abandoned"] = abandon_err is None
        if abandon_err:
            result["abandon_error"] = abandon_err

    if args.json:
        write_json(result)
    else:
        print(render_text(run, stale_reason, log_info, result))

    sys.exit(1 if stale_reason else 0)


if __name__ == "__main__":
    main()
