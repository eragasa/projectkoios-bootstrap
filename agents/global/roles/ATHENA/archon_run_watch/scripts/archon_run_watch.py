"""Monitor Archon runs and detect stale detached runs."""

from __future__ import annotations

from argparse import ArgumentParser
from dataclasses import dataclass
import json
import os
import subprocess
import sys

from _utils import write_json


@dataclass(frozen=True)
class RunStatus:
    run_id: str
    status: str
    pid: int | None
    log_path: str | None
    raw: dict | None


def run_archon(*args: str, json_output: bool = False) -> subprocess.CompletedProcess:
    """Run an Archon CLI command and return the completed process.

    Raises ``FileNotFoundError`` if Archon is not on PATH.
    """
    cmd = ["archon", *args]
    if json_output:
        cmd.append("--json")
    return subprocess.run(cmd, capture_output=True, text=True)


def fetch_run(run_id: str) -> RunStatus | str:
    """Fetch the status of an Archon run.

    Returns a ``RunStatus`` on success, or an error string on failure.
    """
    try:
        r = run_archon("workflow", "get", run_id, json_output=True)
    except FileNotFoundError:
        return "archon CLI not found on PATH"

    if r.returncode != 0:
        return r.stderr.strip() or f"archon exited with code {r.returncode}"

    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError as e:
        return f"failed to parse Archon output: {e}"

    status = data.get("status", "unknown")
    pid = data.get("pid")
    log_path = data.get("log")

    return RunStatus(
        run_id=run_id,
        status=status,
        pid=pid,
        log_path=log_path,
        raw=data,
    )


def detect_stale(run: RunStatus) -> str | None:
    """Check whether *run* appears stale.

    Returns a reason string if stale, ``None`` if not stale.
    """
    if run.status != "running":
        return None

    if run.pid is not None:
        try:
            os.kill(run.pid, 0)
        except OSError:
            return f"process {run.pid} no longer exists"
        else:
            return None
    else:
        return "process inspection unavailable (no PID in run status)"

    return None


def abandon_run(run_id: str) -> str | None:
    """Abandon an Archon run.

    Returns ``None`` on success, or an error string on failure.
    """
    try:
        r = run_archon("workflow", "abandon", run_id, json_output=True)
    except FileNotFoundError:
        return "archon CLI not found on PATH"

    if r.returncode != 0:
        return r.stderr.strip() or f"archon abandon exited with code {r.returncode}"

    return None


def main() -> None:
    p = ArgumentParser(description="Monitor an Archon run and detect stale detached runs")
    p.add_argument("--run-id", required=True, help="Archon workflow run ID")
    p.add_argument("--log", help="Path to detached child log file")
    p.add_argument("--abandon-stale", action="store_true", help="Automatically abandon stale runs")
    p.add_argument("--json", action="store_true", help="Output JSON")
    args = p.parse_args()

    run = fetch_run(args.run_id)
    if isinstance(run, str):
        result = {"run_id": args.run_id, "error": run}
        if args.json:
            write_json(result)
        else:
            print(f"error: {run}")
        sys.exit(1)

    stale_reason = detect_stale(run)
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
        abandon_err = abandon_run(args.run_id)
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
