"""Shared run-state types and Archon CLI client.

Usage
-----
    from _run import RunStatus, ArchonClient

    client = ArchonClient()
    run = client.fetch_run("run-id")
    if isinstance(run, RunStatus) and run.is_stale():
        client.abandon_run(run.run_id)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
import subprocess


@dataclass(frozen=True)
class RunStatus:
    """Status of an Archon workflow run at a point in time."""

    run_id: str
    status: str
    pid: int | None
    log_path: str | None
    started_at: str | None
    workflow_name: str | None
    raw: dict | None

    def is_stale(self, max_age_minutes: int = 60) -> str | None:
        """Return a reason string if stale, ``None`` if alive.

        Priority:
        1. PID check — authoritative (process gone = stale).
        2. Age fallback — heuristic when PID is ``None``.
        3. Unknown — return ``None`` if neither check applies.
        """
        if self.status != "running":
            return None

        if self.pid is not None:
            try:
                os.kill(self.pid, 0)
            except OSError:
                return f"process {self.pid} no longer exists"
            else:
                return None

        if self.started_at:
            try:
                since = datetime.now(timezone.utc) - datetime.fromisoformat(self.started_at)
            except (ValueError, TypeError):
                return None
            if since.total_seconds() > max_age_minutes * 60:
                elapsed_m = int(since.total_seconds() // 60)
                return f"running {elapsed_m}m without PID (max {max_age_minutes}m)"
            return None

        return None


class ArchonClient:
    """Thin wrapper over the ``archon`` CLI binary.

    Every public method returns either a success value or an error string,
    making it safe to chain without try/except for expected failure modes.
    """

    def __init__(self, archon_bin: str = "archon") -> None:
        self._bin = archon_bin

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _run(self, *args: str, json_output: bool = False) -> subprocess.CompletedProcess:
        """Invoke the ``archon`` CLI.  Raises ``FileNotFoundError`` if missing."""
        cmd = [self._bin, *args]
        if json_output:
            cmd.append("--json")
        return subprocess.run(cmd, capture_output=True, text=True)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def fetch_run(self, run_id: str) -> RunStatus | str:
        """Fetch the status of one Archon run.

        Returns a ``RunStatus`` on success, or an error string on failure.
        """
        try:
            r = self._run("workflow", "get", run_id, json_output=True)
        except FileNotFoundError:
            return "archon CLI not found on PATH"

        if r.returncode != 0:
            return r.stderr.strip() or f"archon exited with code {r.returncode}"

        try:
            data = json.loads(r.stdout)
        except json.JSONDecodeError as e:
            return f"failed to parse Archon output: {e}"

        return RunStatus(
            run_id=data.get("id", run_id),
            status=data.get("status", "unknown"),
            pid=data.get("pid"),
            log_path=data.get("log"),
            started_at=data.get("started_at"),
            workflow_name=data.get("workflow_name"),
            raw=data,
        )

    def list_runs(self, status: str | None = None) -> list[dict] | str:
        """List Archon runs, optionally filtered by *status*.

        Returns a ``list[dict]`` on success, or an error string on failure.
        Each dict has the shape returned by ``archon workflow runs --json``.
        """
        args = ["workflow", "runs"]
        if status:
            args.extend(["--status", status])
        try:
            r = self._run(*args, json_output=True)
        except FileNotFoundError:
            return "archon CLI not found on PATH"

        if r.returncode != 0:
            return r.stderr.strip() or f"archon exited with code {r.returncode}"

        try:
            data = json.loads(r.stdout)
        except json.JSONDecodeError as e:
            return f"failed to parse Archon output: {e}"

        return data.get("runs", [])

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def abandon_run(self, run_id: str) -> str | None:
        """Abandon (cancel) a non-terminal Archon run.

        Returns ``None`` on success, or an error string on failure.
        """
        try:
            r = self._run("workflow", "abandon", run_id, json_output=True)
        except FileNotFoundError:
            return "archon CLI not found on PATH"

        if r.returncode != 0:
            return r.stderr.strip() or f"archon abandon exited with code {r.returncode}"

        return None
