#!/usr/bin/env python3.14

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_TASK_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
_REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_WORKSPACE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
_PANE_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_.-]*:p[A-Za-z0-9][A-Za-z0-9_.-]*$"
)
_TAB_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9_.-]*:t[A-Za-z0-9][A-Za-z0-9_.-]*$"
)
_ERROR_LIMIT = 500

CommandRunner = Callable[
    [tuple[str, ...], Mapping[str, str], float],
    subprocess.CompletedProcess[str],
]


class RepositorySessionError(RuntimeError):
    """A fail-closed repository-session launch error."""

    def __init__(self, message: str, *, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True, slots=True)
class RepositorySessionRequest:
    """Explicit authority for one named repository task session."""

    repository_root: Path
    task: str
    focus: bool = True


@dataclass(frozen=True, slots=True)
class RepositorySessionLaunch:
    """Evidence returned after Herdr starts one named Pi session."""

    repository_root: Path
    task: str
    session_name: str
    tab_id: str
    pane_id: str
    herdr_executable: Path
    pi_executable: Path

    def to_dict(self) -> dict[str, str]:
        return {
            "repository_root": str(self.repository_root),
            "task": self.task,
            "session_name": self.session_name,
            "tab_id": self.tab_id,
            "pane_id": self.pane_id,
            "herdr_executable": str(self.herdr_executable),
            "pi_executable": str(self.pi_executable),
        }


@dataclass(frozen=True, slots=True)
class RepositorySessionSpawner:
    """Open a Herdr tab and run Pi with a deterministic session name."""

    herdr_executable: Path
    pi_executable: Path
    environment: Mapping[str, str]
    runner: CommandRunner
    timeout_seconds: float = 15.0

    @classmethod
    def from_environment(
        cls,
        *,
        environ: Mapping[str, str] | None = None,
        find_executable: Callable[[str], str | None] = shutil.which,
        runner: CommandRunner | None = None,
        timeout_seconds: float = 15.0,
    ) -> RepositorySessionSpawner:
        environment = dict(os.environ if environ is None else environ)
        if environment.get("HERDR_ENV") != "1":
            raise RepositorySessionError(
                "repository sessions must be opened from a Herdr-managed pane"
            )
        required_herdr_environment = (
            "HERDR_BIN_PATH",
            "HERDR_PANE_ID",
            "HERDR_SOCKET_PATH",
            "HERDR_TAB_ID",
            "HERDR_WORKSPACE_ID",
        )
        missing = [
            name
            for name in required_herdr_environment
            if not environment.get(name)
        ]
        if missing:
            raise RepositorySessionError(
                "Herdr-managed environment is missing " + ", ".join(missing)
            )
        raw_herdr = environment["HERDR_BIN_PATH"]
        herdr = Path(raw_herdr)
        if not herdr.is_absolute():
            raise RepositorySessionError("HERDR_BIN_PATH must be absolute")
        pi = find_executable("pi")
        if pi is None:
            raise RepositorySessionError(
                "pi is not available on PATH",
                exit_code=127,
            )
        return cls(
            herdr_executable=herdr.resolve(),
            pi_executable=Path(pi).resolve(),
            environment=environment,
            runner=_run_command if runner is None else runner,
            timeout_seconds=timeout_seconds,
        )

    def open(
        self, request: RepositorySessionRequest
    ) -> RepositorySessionLaunch:
        root = _validate_repository_root(request.repository_root)
        task = _validate_task(request.task)
        repository_name = root.name
        if _REPOSITORY_PATTERN.fullmatch(repository_name) is None:
            raise RepositorySessionError(
                "repository directory name cannot form a safe session name"
            )
        session_name = f"{repository_name}:{task}"
        workspace_id = self.environment.get("HERDR_WORKSPACE_ID")
        if (
            workspace_id is None
            or _WORKSPACE_PATTERN.fullmatch(workspace_id) is None
        ):
            raise RepositorySessionError(
                "HERDR_WORKSPACE_ID has an invalid format"
            )
        create_arguments = [
            str(self.herdr_executable),
            "tab",
            "create",
            "--workspace",
            workspace_id,
            "--cwd",
            str(root),
            "--label",
            session_name,
            "--focus" if request.focus else "--no-focus",
        ]
        created = self._invoke(tuple(create_arguments), operation="tab create")
        tab_id, pane_id = _parse_tab_creation(
            created.stdout,
            expected_workspace_id=workspace_id,
        )

        run_arguments = (
            str(self.herdr_executable),
            "pane",
            "run",
            pane_id,
            str(self.pi_executable),
            "--name",
            session_name,
        )
        try:
            self._invoke(run_arguments, operation="pane run")
        except RepositorySessionError as error:
            raise RepositorySessionError(
                f"{error}; newly created tab {tab_id} with pane {pane_id} "
                "was left intact",
                exit_code=error.exit_code,
            ) from error

        return RepositorySessionLaunch(
            repository_root=root,
            task=task,
            session_name=session_name,
            tab_id=tab_id,
            pane_id=pane_id,
            herdr_executable=self.herdr_executable,
            pi_executable=self.pi_executable,
        )

    def _invoke(
        self,
        command: tuple[str, ...],
        *,
        operation: str,
    ) -> subprocess.CompletedProcess[str]:
        try:
            result = self.runner(
                command, self.environment, self.timeout_seconds
            )
        except subprocess.TimeoutExpired as error:
            raise RepositorySessionError(
                f"Herdr {operation} timed out"
            ) from error
        except OSError as error:
            raise RepositorySessionError(
                f"could not execute Herdr: {_bounded(str(error))}",
                exit_code=127,
            ) from error
        if result.returncode != 0:
            detail = _bounded(result.stderr.strip())
            suffix = f": {detail}" if detail else ""
            raise RepositorySessionError(f"Herdr {operation} failed{suffix}")
        return result


def _validate_repository_root(repository_root: Path) -> Path:
    if not repository_root.is_absolute():
        raise RepositorySessionError("repository root must be an absolute path")
    try:
        root = repository_root.resolve(strict=True)
    except OSError as error:
        raise RepositorySessionError(
            f"repository root could not be resolved: {_bounded(str(error))}"
        ) from error
    if not root.is_dir():
        raise RepositorySessionError("repository root must be a directory")
    if not (root / ".git").exists():
        raise RepositorySessionError("repository root is not a Git worktree")
    if not (root / "AGENTS.md").is_file():
        raise RepositorySessionError("repository root is missing AGENTS.md")
    return root


def _validate_task(task: str) -> str:
    normalized = task.strip()
    if normalized != task or _TASK_PATTERN.fullmatch(normalized) is None:
        raise RepositorySessionError(
            "task must be a lowercase kebab-case slug of at most 64 characters"
        )
    return normalized


def _parse_tab_creation(
    output: str,
    *,
    expected_workspace_id: str,
) -> tuple[str, str]:
    try:
        payload: Any = json.loads(output)
    except json.JSONDecodeError as error:
        raise RepositorySessionError(
            "Herdr tab create returned invalid JSON"
        ) from error
    if not isinstance(payload, dict):
        raise RepositorySessionError(
            "Herdr tab create returned invalid evidence"
        )
    result = payload.get("result", payload)
    if not isinstance(result, dict):
        raise RepositorySessionError(
            "Herdr tab create returned invalid evidence"
        )
    tab = result.get("tab")
    pane = result.get("root_pane")
    if not isinstance(tab, dict) or not isinstance(pane, dict):
        raise RepositorySessionError(
            "Herdr tab create returned invalid evidence"
        )
    tab_id = tab.get("tab_id")
    pane_id = pane.get("pane_id")
    if not isinstance(tab_id, str) or _TAB_PATTERN.fullmatch(tab_id) is None:
        raise RepositorySessionError(
            "Herdr tab create did not return a valid tab id"
        )
    if not isinstance(pane_id, str) or _PANE_PATTERN.fullmatch(pane_id) is None:
        raise RepositorySessionError(
            "Herdr tab create did not return a valid pane id"
        )
    if (
        tab_id.partition(":")[0] != expected_workspace_id
        or pane_id.partition(":")[0] != expected_workspace_id
    ):
        raise RepositorySessionError(
            "Herdr tab create returned evidence from a different workspace"
        )
    return tab_id, pane_id


def _run_command(
    command: tuple[str, ...],
    environment: Mapping[str, str],
    timeout_seconds: float,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        env=dict(environment),
        text=True,
        timeout=timeout_seconds,
    )


def _bounded(value: str) -> str:
    return value[:_ERROR_LIMIT]


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Open one named Project Koios repository session in Herdr."
    )
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--task", required=True)
    parser.add_argument("--no-focus", action="store_true")
    arguments = parser.parse_args(argv)

    try:
        spawner = RepositorySessionSpawner.from_environment()
        launch = spawner.open(
            RepositorySessionRequest(
                repository_root=arguments.repository_root,
                task=arguments.task,
                focus=not arguments.no_focus,
            )
        )
    except RepositorySessionError as error:
        print(f"error: {error}", file=sys.stderr)
        return error.exit_code

    print(json.dumps(launch.to_dict(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
