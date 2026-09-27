from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from projectkoios.bootstrap.harness.repository_session import (
    RepositorySessionError,
    RepositorySessionRequest,
    RepositorySessionSpawner,
)

_REPOSITORY = Path(__file__).parents[2]


def _herdr_environment() -> dict[str, str]:
    return {
        "HERDR_ENV": "1",
        "HERDR_BIN_PATH": "/test/bin/herdr",
        "HERDR_PANE_ID": "w1:p1",
        "HERDR_SOCKET_PATH": "/test/herdr.sock",
        "HERDR_TAB_ID": "w1:t1",
        "HERDR_WORKSPACE_ID": "w1",
    }


def _repository(tmp_path: Path, name: str = "projectkoios-example") -> Path:
    root = tmp_path / name
    root.mkdir()
    (root / ".git").write_text("gitdir: /test/gitdir\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Test\n", encoding="utf-8")
    return root


def _completed(
    command: tuple[str, ...],
    *,
    returncode: int = 0,
    stdout: str = "",
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(command, returncode, stdout, stderr)


def _tab_created(command: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
    return _completed(
        command,
        stdout=json.dumps(
            {
                "id": "cli:tab:create",
                "result": {
                    "type": "tab_created",
                    "tab": {"tab_id": "w4:tA"},
                    "root_pane": {"pane_id": "w4:pA"},
                },
            }
        ),
    )


def test_open_runs_named_pi_in_new_herdr_tab(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    calls: list[tuple[str, ...]] = []

    def run(
        command: tuple[str, ...],
        _environment: object,
        _timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[1:3] == ("tab", "create"):
            return _tab_created(command)
        return _completed(command)

    spawner = RepositorySessionSpawner.from_environment(
        environ=_herdr_environment(),
        find_executable=lambda _command: "/test/bin/pi",
        runner=run,
    )

    launch = spawner.open(RepositorySessionRequest(root, "domain-packages"))

    assert launch.session_name == "projectkoios-example:domain-packages"
    assert launch.tab_id == "w4:tA"
    assert launch.pane_id == "w4:pA"
    assert calls == [
        (
            "/test/bin/herdr",
            "tab",
            "create",
            "--workspace",
            "w1",
            "--cwd",
            str(root.resolve()),
            "--label",
            "projectkoios-example:domain-packages",
            "--focus",
        ),
        (
            "/test/bin/herdr",
            "pane",
            "run",
            "w4:pA",
            "/test/bin/pi",
            "--name",
            "projectkoios-example:domain-packages",
        ),
    ]


def test_no_focus_is_explicit(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    calls: list[tuple[str, ...]] = []

    def run(
        command: tuple[str, ...],
        _environment: object,
        _timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[1:3] == ("tab", "create"):
            return _tab_created(command)
        return _completed(command)

    spawner = RepositorySessionSpawner.from_environment(
        environ=_herdr_environment(),
        find_executable=lambda _command: "/test/bin/pi",
        runner=run,
    )

    spawner.open(RepositorySessionRequest(root, "task", focus=False))

    assert calls[0][-1] == "--no-focus"


def test_environment_preflight_fails_closed() -> None:
    with pytest.raises(RepositorySessionError, match="Herdr-managed"):
        RepositorySessionSpawner.from_environment(environ={})

    with pytest.raises(RepositorySessionError, match="HERDR_BIN_PATH"):
        RepositorySessionSpawner.from_environment(environ={"HERDR_ENV": "1"})

    relative = _herdr_environment()
    relative["HERDR_BIN_PATH"] = "herdr"
    with pytest.raises(RepositorySessionError, match="must be absolute"):
        RepositorySessionSpawner.from_environment(environ=relative)


def test_missing_pi_reports_command_not_found() -> None:
    with pytest.raises(RepositorySessionError, match="not available") as raised:
        RepositorySessionSpawner.from_environment(
            environ=_herdr_environment(),
            find_executable=lambda _command: None,
        )

    assert raised.value.exit_code == 127


@pytest.mark.parametrize("task", ["", "Upper", "two words", " leading", "a_b"])
def test_invalid_task_stops_before_herdr(tmp_path: Path, task: str) -> None:
    root = _repository(tmp_path)
    calls: list[tuple[str, ...]] = []

    def run(
        command: tuple[str, ...],
        _environment: object,
        _timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _completed(command)

    spawner = RepositorySessionSpawner(
        Path("/test/bin/herdr"), Path("/test/bin/pi"), {}, run
    )

    with pytest.raises(RepositorySessionError, match="kebab-case"):
        spawner.open(RepositorySessionRequest(root, task))

    assert calls == []


def test_relative_or_unmarked_root_stops_before_herdr(tmp_path: Path) -> None:
    calls: list[tuple[str, ...]] = []

    def run(
        command: tuple[str, ...],
        _environment: object,
        _timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _completed(command)

    spawner = RepositorySessionSpawner(
        Path("/test/bin/herdr"), Path("/test/bin/pi"), {}, run
    )

    with pytest.raises(RepositorySessionError, match="absolute"):
        spawner.open(
            RepositorySessionRequest(Path("relative/repository"), "task")
        )

    unmarked = tmp_path / "unmarked"
    unmarked.mkdir()
    with pytest.raises(RepositorySessionError, match="Git worktree"):
        spawner.open(RepositorySessionRequest(unmarked, "task"))

    assert calls == []


def test_invalid_tab_evidence_stops_before_run(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    calls: list[tuple[str, ...]] = []

    def run(
        command: tuple[str, ...],
        _environment: object,
        _timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _completed(command, stdout='{"result":{"tab":{}}}')

    spawner = RepositorySessionSpawner(
        Path("/test/bin/herdr"),
        Path("/test/bin/pi"),
        {"HERDR_WORKSPACE_ID": "w1"},
        run,
    )

    with pytest.raises(RepositorySessionError, match="invalid evidence"):
        spawner.open(RepositorySessionRequest(root, "task"))

    assert len(calls) == 1


def test_executable_launcher_exposes_help() -> None:
    result = subprocess.run(
        [str(_REPOSITORY / "scripts/open-repository-session"), "--help"],
        cwd=_REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
    assert "--repository-root" in result.stdout
    assert "--task" in result.stdout


def test_run_failure_preserves_new_tab_and_bounds_error(
    tmp_path: Path,
) -> None:
    root = _repository(tmp_path)
    calls: list[tuple[str, ...]] = []

    def run(
        command: tuple[str, ...],
        _environment: object,
        _timeout: float,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[1:3] == ("tab", "create"):
            return _tab_created(command)
        return _completed(command, returncode=9, stderr="x" * 1000)

    spawner = RepositorySessionSpawner(
        Path("/test/bin/herdr"),
        Path("/test/bin/pi"),
        {"HERDR_WORKSPACE_ID": "w1"},
        run,
    )

    with pytest.raises(RepositorySessionError, match="left intact") as raised:
        spawner.open(RepositorySessionRequest(root, "task"))

    assert "w4:tA" in str(raised.value)
    assert "w4:pA" in str(raised.value)
    assert len(str(raised.value)) < 600
    assert all("close" not in command for command in calls)
