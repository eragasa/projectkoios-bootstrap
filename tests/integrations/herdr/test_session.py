from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Mapping
from pathlib import Path

import pytest
from projectkoios.bootstrap.adapters.base import Integration
from projectkoios.bootstrap.integrations.herdr.references import (
    HERDR_DOCUMENTATION_BASELINE,
    HERDR_REFERENCES,
)
from projectkoios.bootstrap.integrations.herdr.session import (
    HerdrIntegration,
    HerdrIntegrationError,
)

_REPOSITORY = Path(__file__).parents[3]
_EXECUTABLE = Path("/test/bin/herdr")
_PANE_ID = "w4:p1"
_SOCKET_PATH = "/test/herdr.sock"
_SESSION_PATH = "/test/pi/session.jsonl"


def _environment(**updates: str) -> dict[str, str]:
    environment = {
        "HERDR_BIN_PATH": str(_EXECUTABLE),
        "HERDR_ENV": "1",
        "HERDR_PANE_ID": _PANE_ID,
        "HERDR_SOCKET_PATH": _SOCKET_PATH,
        "HERDR_TAB_ID": "w4:t1",
        "HERDR_WORKSPACE_ID": "w4",
    }
    environment.update(updates)
    return environment


def _agent_session(**updates: object) -> dict[str, object]:
    value: dict[str, object] = {
        "agent": "pi",
        "kind": "path",
        "source": "herdr:pi",
        "value": _SESSION_PATH,
    }
    value.update(updates)
    return value


def _pane(**updates: object) -> dict[str, object]:
    value: dict[str, object] = {
        "agent": "pi",
        "agent_session": _agent_session(),
        "agent_status": "working",
        "cwd": "/test/repository",
        "foreground_cwd": "/test/repository",
        "pane_id": _PANE_ID,
        "tab_id": "w4:t1",
        "terminal_id": "term_test",
        "workspace_id": "w4",
    }
    value.update(updates)
    return value


def _responses(
    *,
    version: str = HERDR_DOCUMENTATION_BASELINE,
    session: Mapping[str, object] | None = None,
    pane: Mapping[str, object] | None = None,
    listed_pane: Mapping[str, object] | None = None,
    integration_status: str = "pi: current (v9) (/test/pi-extension.ts)\n",
) -> dict[tuple[str, ...], subprocess.CompletedProcess[str]]:
    session_value = {
        "default": True,
        "name": "default",
        "running": True,
        "session_dir": "/test/herdr",
        "socket_path": _SOCKET_PATH,
    }
    if session is not None:
        session_value = dict(session)
    pane_value = _pane() if pane is None else dict(pane)
    listed_value = pane_value if listed_pane is None else dict(listed_pane)
    return {
        ("--version",): _result(stdout=f"herdr {version}\n"),
        ("session", "list", "--json"): _result(
            stdout=json.dumps({"sessions": [session_value]})
        ),
        ("pane", "current", "--current"): _result(
            stdout=json.dumps(
                {
                    "id": "cli:pane:current",
                    "result": {"pane": pane_value, "type": "pane_current"},
                }
            )
        ),
        ("agent", "list"): _result(
            stdout=json.dumps(
                {
                    "id": "cli:agent:list",
                    "result": {
                        "agents": [listed_value],
                        "type": "agent_list",
                    },
                }
            )
        ),
        ("integration", "status"): _result(stdout=integration_status),
    }


def _result(
    *,
    stdout: str = "",
    stderr: str = "",
    returncode: int = 0,
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=(),
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


class _Runner:
    def __init__(
        self,
        responses: Mapping[tuple[str, ...], subprocess.CompletedProcess[str]],
    ) -> None:
        self.responses = responses
        self.calls: list[tuple[str, ...]] = []

    def __call__(
        self,
        command: tuple[str, ...],
        environment: Mapping[str, str],
        timeout_seconds: float,
    ) -> subprocess.CompletedProcess[str]:
        assert command[0] == str(_EXECUTABLE)
        assert environment["HERDR_ENV"] == "1"
        assert timeout_seconds == 10.0
        arguments = command[1:]
        self.calls.append(arguments)
        return self.responses[arguments]


def _integration(
    responses: Mapping[tuple[str, ...], subprocess.CompletedProcess[str]],
) -> tuple[HerdrIntegration, _Runner]:
    runner = _Runner(responses)
    integration = HerdrIntegration.from_environment(
        environ=_environment(),
        runner=runner,
    )
    return integration, runner


def test_integration_is_an_external_application_adapter() -> None:
    integration, _runner = _integration(_responses())

    assert isinstance(integration, Integration)


def test_environment_preflight_rejects_unmanaged_and_incomplete_contexts() -> (
    None
):
    with pytest.raises(HerdrIntegrationError, match="HERDR_ENV=1"):
        HerdrIntegration.from_environment(environ={})

    incomplete = _environment()
    del incomplete["HERDR_SOCKET_PATH"]
    with pytest.raises(HerdrIntegrationError, match="HERDR_SOCKET_PATH"):
        HerdrIntegration.from_environment(environ=incomplete)

    with pytest.raises(HerdrIntegrationError, match="must be absolute"):
        HerdrIntegration.from_environment(
            environ=_environment(HERDR_BIN_PATH="herdr")
        )


def test_inspection_emits_versioned_evidence_and_official_references() -> None:
    integration, runner = _integration(_responses())

    evidence = integration.inspect_session().to_dict()

    assert evidence["schema_version"] == 1
    assert evidence["documentation_baseline"] == "0.9.1"
    assert evidence["herdr_version"] == "0.9.1"
    assert evidence["herdr_executable"] == str(_EXECUTABLE)
    assert evidence["session"] == {
        "default": True,
        "name": "default",
        "running": True,
        "socket_path": _SOCKET_PATH,
    }
    assert evidence["inspection_target"] == {
        "requested_pane_id": _PANE_ID,
        "resolved_pane_id": _PANE_ID,
        "resolved_via_pane_alias": False,
    }
    assert evidence["pane"] == {
        "agent": "pi",
        "agent_session": _agent_session(),
        "agent_status": "working",
        "cwd": "/test/repository",
        "foreground_cwd": "/test/repository",
        "pane_id": _PANE_ID,
        "tab_id": "w4:t1",
        "terminal_id": "term_test",
        "workspace_id": "w4",
    }
    assert evidence["pi_integration"] == {
        "minimum_native_restore_version": 2,
        "native_session_reference_reported": True,
        "version": 9,
    }
    assert evidence["continuity"] == {
        "documented_client_detach_keys": ["ctrl+b", "q"],
        "live_process_requires_running_server_and_pane": True,
        "pane_close_is_not_client_detach": True,
        "reattach_argv": [
            str(_EXECUTABLE),
            "session",
            "attach",
            "default",
        ],
    }
    assert evidence["references"] == [
        {
            "topic": reference.topic,
            "documentation_url": reference.documentation_url,
            "versioned_source_url": reference.versioned_source_url,
        }
        for reference in HERDR_REFERENCES
    ]
    assert runner.calls == [
        ("--version",),
        ("session", "list", "--json"),
        ("pane", "current", "--current"),
        ("agent", "list"),
        ("integration", "status"),
    ]


def test_explicit_pane_uses_documented_get_command() -> None:
    selected_pane = _pane(pane_id="w4:p2")
    responses = _responses(pane=selected_pane)
    responses.pop(("pane", "current", "--current"))
    responses[("pane", "get", "w4:p2")] = _result(
        stdout=json.dumps(
            {
                "id": "cli:pane:get",
                "result": {"pane": selected_pane, "type": "pane_info"},
            }
        )
    )
    integration, runner = _integration(responses)

    evidence = integration.inspect_session(pane_id="w4:p2").to_dict()

    assert ("pane", "get", "w4:p2") in runner.calls
    assert evidence["inspection_target"] == {
        "requested_pane_id": "w4:p2",
        "resolved_pane_id": "w4:p2",
        "resolved_via_pane_alias": False,
    }


def test_documented_pane_alias_resolution_is_explicit_in_evidence() -> None:
    responses = _responses()
    responses.pop(("pane", "current", "--current"))
    responses[("pane", "get", "w4:p2")] = _result(
        stdout=json.dumps(
            {
                "id": "cli:pane:get",
                "result": {"pane": _pane(), "type": "pane_info"},
            }
        )
    )
    integration, _runner = _integration(responses)

    evidence = integration.inspect_session(pane_id="w4:p2").to_dict()

    assert evidence["inspection_target"] == {
        "requested_pane_id": "w4:p2",
        "resolved_pane_id": _PANE_ID,
        "resolved_via_pane_alias": True,
    }


def test_explicit_pane_rejects_cli_option_shaped_input() -> None:
    integration, runner = _integration(_responses())

    with pytest.raises(HerdrIntegrationError, match="invalid format"):
        integration.inspect_session(pane_id="--help")

    assert ("pane", "get", "--help") not in runner.calls


@pytest.mark.parametrize(
    ("version", "message"),
    [
        ("0.9.2", "outside the reviewed documentation baseline"),
        ("invalid", "invalid version string"),
    ],
)
def test_version_evidence_fails_closed(version: str, message: str) -> None:
    integration, _runner = _integration(_responses(version=version))

    with pytest.raises(HerdrIntegrationError, match=message):
        integration.inspect_session()


def test_session_must_match_the_inherited_socket_and_be_running() -> None:
    integration, _runner = _integration(
        _responses(
            session={
                "default": True,
                "name": "default",
                "running": True,
                "session_dir": "/test/other",
                "socket_path": "/test/other.sock",
            }
        )
    )
    with pytest.raises(HerdrIntegrationError, match="exactly one session"):
        integration.inspect_session()

    stopped = {
        "default": True,
        "name": "default",
        "running": False,
        "session_dir": "/test/herdr",
        "socket_path": _SOCKET_PATH,
    }
    integration, _runner = _integration(_responses(session=stopped))
    with pytest.raises(HerdrIntegrationError, match="is not running"):
        integration.inspect_session()


def test_command_response_identity_fails_closed() -> None:
    responses = _responses()
    responses[("agent", "list")] = _result(
        stdout=json.dumps(
            {
                "id": "cli:pane:list",
                "result": {"agents": [_pane()], "type": "agent_list"},
            }
        )
    )
    integration, _runner = _integration(responses)

    with pytest.raises(HerdrIntegrationError, match="wrong agent response"):
        integration.inspect_session()


def test_pi_pane_requires_known_state_and_native_session_identity() -> None:
    integration, _runner = _integration(
        _responses(pane=_pane(agent_status="surprising"))
    )
    with pytest.raises(HerdrIntegrationError, match="unknown agent status"):
        integration.inspect_session()

    integration, _runner = _integration(
        _responses(pane=_pane(agent_session=None))
    )
    with pytest.raises(HerdrIntegrationError, match="agent_session"):
        integration.inspect_session()


def test_pane_and_agent_list_must_agree() -> None:
    integration, _runner = _integration(
        _responses(
            listed_pane=_pane(agent_session=_agent_session(value="other"))
        )
    )

    with pytest.raises(HerdrIntegrationError, match="references disagree"):
        integration.inspect_session()


def test_pi_integration_must_be_current_and_support_native_restore() -> None:
    integration, _runner = _integration(
        _responses(integration_status="pi: not installed (/test/pi)\n")
    )
    with pytest.raises(HerdrIntegrationError, match="was not reported"):
        integration.inspect_session()

    integration, _runner = _integration(
        _responses(integration_status="pi: current (v1) (/test/pi)\n")
    )
    with pytest.raises(HerdrIntegrationError, match="too old"):
        integration.inspect_session()


def test_additive_fields_are_tolerated_within_schema_version_one() -> None:
    session = {
        "default": True,
        "future": {"field": True},
        "name": "default",
        "running": True,
        "session_dir": "/test/herdr",
        "socket_path": _SOCKET_PATH,
    }
    pane = _pane(future_field=[1, 2, 3])
    raw_agent_session = pane["agent_session"]
    assert isinstance(raw_agent_session, dict)
    agent_session = dict(raw_agent_session)
    agent_session["future_field"] = "accepted"
    pane["agent_session"] = agent_session
    integration, _runner = _integration(_responses(session=session, pane=pane))

    evidence = integration.inspect_session()

    assert evidence.session_name == "default"
    assert evidence.pane.agent_session.value == _SESSION_PATH


def test_failed_and_malformed_cli_output_is_bounded() -> None:
    responses = _responses()
    responses[("session", "list", "--json")] = _result(
        returncode=1,
        stderr="failure " * 200,
    )
    integration, _runner = _integration(responses)
    with pytest.raises(HerdrIntegrationError) as raised:
        integration.inspect_session()
    assert len(str(raised.value)) < 600
    assert "failure" in str(raised.value)

    responses = _responses()
    responses[("session", "list", "--json")] = _result(stdout="not-json")
    integration, _runner = _integration(responses)
    with pytest.raises(HerdrIntegrationError, match="invalid JSON"):
        integration.inspect_session()


def test_executable_script_reports_live_evidence_from_a_fake_cli(
    tmp_path: Path,
) -> None:
    fake_herdr = tmp_path / "herdr"
    responses = {
        "--version": _responses()[("--version",)].stdout,
        "session list --json": _responses()[
            ("session", "list", "--json")
        ].stdout,
        "pane current --current": _responses()[
            ("pane", "current", "--current")
        ].stdout,
        "agent list": _responses()[("agent", "list")].stdout,
        "integration status": _responses()[("integration", "status")].stdout,
    }
    fake_herdr.write_text(
        "#!/usr/bin/env python3.14\n"
        "import json, sys\n"
        f"responses = {responses!r}\n"
        "key = ' '.join(sys.argv[1:])\n"
        "if key not in responses:\n"
        "    raise SystemExit(2)\n"
        "sys.stdout.write(responses[key])\n",
        encoding="utf-8",
    )
    fake_herdr.chmod(0o755)
    environment = os.environ.copy()
    environment.update(_environment(HERDR_BIN_PATH=str(fake_herdr)))

    result = subprocess.run(
        [str(_REPOSITORY / "scripts/inspect-herdr-session")],
        env=environment,
        capture_output=True,
        check=False,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == 1
    assert payload["session"]["name"] == "default"
    assert payload["pane"]["agent_session"]["value"] == _SESSION_PATH
