from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest
from projectkoios.bootstrap.harness import coordinator_startup
from projectkoios.bootstrap.harness.coordinator_startup import (
    CoordinatorLaunch,
    CoordinatorStartupError,
    execute_coordinator_startup,
    plan_coordinator_startup,
)

_REPOSITORY = Path(__file__).parents[2]


def _repository_root(tmp_path: Path) -> Path:
    (tmp_path / "maps").mkdir(parents=True)
    (tmp_path / "AGENTS.md").write_text(
        "# Test instructions\n",
        encoding="utf-8",
    )
    (tmp_path / "maps/repositories.md").write_text(
        "# Test repository map\n",
        encoding="utf-8",
    )
    return tmp_path


def test_plan_rejects_startup_outside_herdr(tmp_path: Path) -> None:
    with pytest.raises(
        CoordinatorStartupError,
        match="must run in a Herdr-managed pane",
    ) as raised:
        plan_coordinator_startup(tmp_path, environ={})

    assert raised.value.exit_code == 2


def test_plan_rejects_caller_option_terminator(tmp_path: Path) -> None:
    with pytest.raises(
        CoordinatorStartupError,
        match="launcher supplies it after its fixed options",
    ):
        plan_coordinator_startup(
            tmp_path,
            ("--model", "test", "--"),
            environ={"HERDR_ENV": "1"},
        )


def test_plan_rejects_root_without_repository_markers(tmp_path: Path) -> None:
    with pytest.raises(
        CoordinatorStartupError,
        match=r"missing: AGENTS\.md, maps/repositories\.md",
    ):
        plan_coordinator_startup(
            tmp_path,
            environ={"HERDR_ENV": "1"},
            find_executable=lambda _command: "/test/bin/pi",
        )


def test_plan_reports_missing_pi_with_command_not_found_status(
    tmp_path: Path,
) -> None:
    root = _repository_root(tmp_path)

    with pytest.raises(
        CoordinatorStartupError,
        match="not available on PATH",
    ) as raised:
        plan_coordinator_startup(
            root,
            environ={"HERDR_ENV": "1"},
            find_executable=lambda _command: None,
        )

    assert raised.value.exit_code == 127


def test_plan_builds_exact_customized_pi_invocation(tmp_path: Path) -> None:
    root = _repository_root(tmp_path)

    launch = plan_coordinator_startup(
        root,
        ("--model", "test-model"),
        environ={
            "HERDR_ENV": "1",
            "PROJECTKOIOS_COORDINATOR_NAME": "test-coordinator",
        },
        find_executable=lambda _command: "/test/bin/pi",
    )

    assert launch.repository_root == root.resolve()
    assert launch.executable == "/test/bin/pi"
    assert launch.argv[:6] == (
        "/test/bin/pi",
        "--model",
        "test-model",
        "--name",
        "test-coordinator",
        "--",
    )
    assert launch.argv[6] == coordinator_startup.STARTUP_PROMPT
    assert "Use pi-intercom to list the live Pi sessions." in launch.argv[6]
    assert "resolve every deferred finding" in launch.argv[6]
    assert "Do not create a local deferred-decision" in launch.argv[6]
    assert "prioritize an executable deterministic" in launch.argv[6]
    assert "send the script to this coordinator" in launch.argv[6]
    assert "machine-specific defaults" in launch.argv[6]
    assert "Do not open panes, delegate work, modify files," in launch.argv[6]


def test_plan_makes_relative_executable_absolute_before_chdir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    launch_directory = tmp_path / "launch"
    launch_directory.mkdir()
    root = _repository_root(tmp_path / "repository")
    monkeypatch.chdir(launch_directory)

    launch = plan_coordinator_startup(
        root,
        environ={"HERDR_ENV": "1"},
        find_executable=lambda _command: "relative-bin/pi",
    )

    assert launch.executable == str(
        (launch_directory / "relative-bin/pi").resolve()
    )
    assert launch.argv[0] == launch.executable


def test_plan_uses_default_name_when_override_is_empty(tmp_path: Path) -> None:
    root = _repository_root(tmp_path)

    launch = plan_coordinator_startup(
        root,
        environ={
            "HERDR_ENV": "1",
            "PROJECTKOIOS_COORDINATOR_NAME": "",
        },
        find_executable=lambda _command: "/test/bin/pi",
    )

    assert launch.argv[1:3] == (
        "--name",
        coordinator_startup.DEFAULT_SESSION_NAME,
    )


def test_execute_changes_directory_then_replaces_process(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[object, ...]] = []
    launch = CoordinatorLaunch(
        repository_root=tmp_path,
        executable="/test/bin/pi",
        argv=("/test/bin/pi", "--", "prompt"),
    )
    monkeypatch.setattr(
        coordinator_startup.os,
        "chdir",
        lambda path: calls.append(("chdir", path)),
    )
    monkeypatch.setattr(
        coordinator_startup.os,
        "execv",
        lambda executable, argv: calls.append(
            ("execv", executable, tuple(argv))
        ),
    )

    execute_coordinator_startup(launch)

    assert calls == [
        ("chdir", tmp_path),
        ("execv", "/test/bin/pi", ("/test/bin/pi", "--", "prompt")),
    ]


def test_main_renders_bounded_preflight_error(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("HERDR_ENV", raising=False)

    status = coordinator_startup.main((), repository_root=tmp_path)

    captured = capsys.readouterr()
    assert status == 2
    assert captured.out == ""
    assert captured.err.startswith("error: ")
    assert "must run in a Herdr-managed pane" in captured.err


def test_executable_launcher_resolves_repository_from_another_directory(
    tmp_path: Path,
) -> None:
    binary_directory = tmp_path / "bin"
    binary_directory.mkdir()
    fake_pi = binary_directory / "pi"
    fake_pi.write_text(
        "#!/usr/bin/env python3.14\n"
        "import json, os, sys\n"
        "print(json.dumps({'argv': sys.argv[1:], 'cwd': os.getcwd()}))\n",
        encoding="utf-8",
    )
    fake_pi.chmod(0o755)
    environment = os.environ.copy()
    environment.update(
        {
            "HERDR_ENV": "1",
            "PATH": f"{binary_directory}{os.pathsep}{environment['PATH']}",
            "PROJECTKOIOS_COORDINATOR_NAME": "integration-coordinator",
        }
    )

    result = subprocess.run(
        [str(_REPOSITORY / "scripts/start-coordinator"), "--model", "test"],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        check=False,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    output = json.loads(result.stdout)
    assert output["cwd"] == str(_REPOSITORY)
    assert output["argv"][:5] == [
        "--model",
        "test",
        "--name",
        "integration-coordinator",
        "--",
    ]
    assert output["argv"][5] == coordinator_startup.STARTUP_PROMPT
