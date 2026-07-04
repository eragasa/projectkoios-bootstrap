"""Shared run-state types and Archon CLI client."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
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
    raw: dict[str, Any] | None

    def is_stale(self, max_age_minutes: int = 60) -> str | None:
        """Return a reason string if stale, ``None`` if alive."""
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
                since: timedelta = datetime.now(timezone.utc) - datetime.fromisoformat(self.started_at)
            except (ValueError, TypeError):
                return None
            if since.total_seconds() > max_age_minutes * 60:
                elapsed_m: int = int(since.total_seconds() // 60)
                return f"running {elapsed_m}m without PID (max {max_age_minutes}m)"
            return None

        return None


class ArchonClient:
    """Thin wrapper over the ``archon`` CLI binary."""

    def __init__(self, archon_bin: str = "archon") -> None:
        self.bin: str = archon_bin

    def run_process(self, *args: str, json_output: bool = False) -> subprocess.CompletedProcess[str]:
        """Invoke the ``archon`` CLI. Raises ``FileNotFoundError`` if missing."""
        cmd: list[str] = [self.bin, *args]
        if json_output:
            cmd.append("--json")
        return subprocess.run(cmd, capture_output=True, text=True)

    def run_cli(self, *args: str, json_output: bool = False) -> subprocess.CompletedProcess[str]:
        """Invoke the ``archon`` CLI through the monkeypatchable runner."""
        return self.run_process(*args, json_output=json_output)

    def fetch_run(self, run_id: str) -> RunStatus | str:
        """Fetch the status of one Archon run."""
        try:
            result: subprocess.CompletedProcess[str] = self.run_cli("workflow", "get", run_id, json_output=True)
        except FileNotFoundError:
            return "archon CLI not found on PATH"

        if result.returncode != 0:
            return result.stderr.strip() or f"archon exited with code {result.returncode}"

        try:
            data: Any = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            return f"failed to parse Archon output: {exc}"
        if not isinstance(data, dict):
            return "failed to parse Archon output: expected object"

        return RunStatus(
            run_id=str(data.get("id", run_id)),
            status=str(data.get("status", "unknown")),
            pid=data.get("pid") if isinstance(data.get("pid"), int) else None,
            log_path=str(data.get("log")) if data.get("log") is not None else None,
            started_at=str(data.get("started_at")) if data.get("started_at") is not None else None,
            workflow_name=str(data.get("workflow_name")) if data.get("workflow_name") is not None else None,
            raw=data,
        )

    def list_runs(self, status: str | None = None) -> list[dict[str, Any]] | str:
        """List Archon runs, optionally filtered by *status*."""
        args: list[str] = ["workflow", "runs"]
        if status:
            args.extend(["--status", status])
        try:
            result: subprocess.CompletedProcess[str] = self.run_cli(*args, json_output=True)
        except FileNotFoundError:
            return "archon CLI not found on PATH"

        if result.returncode != 0:
            return result.stderr.strip() or f"archon exited with code {result.returncode}"

        try:
            data: Any = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            return f"failed to parse Archon output: {exc}"
        if not isinstance(data, dict):
            return "failed to parse Archon output: expected object"
        runs: object = data.get("runs", [])
        return [run for run in runs if isinstance(run, dict)] if isinstance(runs, list) else []

    def abandon_run(self, run_id: str) -> str | None:
        """Abandon a non-terminal Archon run."""
        try:
            result: subprocess.CompletedProcess[str] = self.run_cli("workflow", "abandon", run_id, json_output=True)
        except FileNotFoundError:
            return "archon CLI not found on PATH"

        if result.returncode != 0:
            return result.stderr.strip() or f"archon abandon exited with code {result.returncode}"

        return None
