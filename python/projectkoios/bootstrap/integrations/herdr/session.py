"""Read-only Herdr session-continuity evidence.

This external-application integration follows the adapter taxonomy extracted
from Project Koios Frankenstein and the official Herdr 0.9.1 references in
:mod:`projectkoios.bootstrap.integrations.herdr.references`.

It does not detach clients, close panes, start agents, restore sessions, write
runtime state, or replace pi-intercom. It only invokes documented read-only
Herdr CLI commands and validates their evidence. The Herdr documentation makes
an important distinction: client detach keeps pane processes live, while a
server restart ends those processes and can only reconstruct eligible agent
sessions from integration-reported native session references.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from projectkoios.bootstrap.adapters.base import Integration
from projectkoios.bootstrap.integrations.herdr.references import (
    HERDR_DOCUMENTATION_BASELINE,
    HERDR_PI_RESTORE_MINIMUM_INTEGRATION_VERSION,
    HERDR_REFERENCES,
)

_SCHEMA_VERSION = 1
_AGENT_STATES = frozenset({"blocked", "done", "idle", "unknown", "working"})
_INTEGRATION_STATUS_PATTERN = re.compile(
    r"^pi: current \(v(?P<version>[1-9][0-9]*)\)(?: .*)?$",
    re.MULTILINE,
)
_VERSION_PATTERN = re.compile(r"^herdr (?P<version>[0-9]+\.[0-9]+\.[0-9]+)$")
_PANE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*:p[1-9][0-9]*$")
_ERROR_OUTPUT_LIMIT = 500

CommandRunner = Callable[
    [tuple[str, ...], Mapping[str, str], float],
    subprocess.CompletedProcess[str],
]


class HerdrIntegrationError(RuntimeError):
    """A bounded Herdr inspection or evidence-validation failure."""

    def __init__(self, message: str, *, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True, slots=True)
class HerdrAgentSession:
    """Native Pi session identity reported by the official Herdr integration."""

    agent: str
    kind: str
    source: str
    value: str

    def to_dict(self) -> dict[str, str]:
        """Return deterministic JSON-ready evidence."""
        return {
            "agent": self.agent,
            "kind": self.kind,
            "source": self.source,
            "value": self.value,
        }


@dataclass(frozen=True, slots=True)
class HerdrPaneEvidence:
    """Live Herdr pane and Pi-agent evidence."""

    pane_id: str
    tab_id: str
    workspace_id: str
    terminal_id: str
    cwd: str
    foreground_cwd: str
    agent: str
    agent_status: str
    agent_session: HerdrAgentSession

    def to_dict(self) -> dict[str, object]:
        """Return deterministic JSON-ready evidence."""
        return {
            "pane_id": self.pane_id,
            "tab_id": self.tab_id,
            "workspace_id": self.workspace_id,
            "terminal_id": self.terminal_id,
            "cwd": self.cwd,
            "foreground_cwd": self.foreground_cwd,
            "agent": self.agent,
            "agent_status": self.agent_status,
            "agent_session": self.agent_session.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class HerdrSessionEvidence:
    """Validated facts needed to reason about Herdr session continuity."""

    herdr_version: str
    herdr_executable: str
    session_name: str
    session_is_default: bool
    socket_path: str
    requested_pane_id: str
    pi_integration_version: int
    pane: HerdrPaneEvidence

    def to_dict(self) -> dict[str, object]:
        """Return stable schema-versioned evidence with reviewed references."""
        return {
            "schema_version": _SCHEMA_VERSION,
            "documentation_baseline": HERDR_DOCUMENTATION_BASELINE,
            "herdr_version": self.herdr_version,
            "herdr_executable": self.herdr_executable,
            "session": {
                "name": self.session_name,
                "default": self.session_is_default,
                "running": True,
                "socket_path": self.socket_path,
            },
            "inspection_target": {
                "requested_pane_id": self.requested_pane_id,
                "resolved_pane_id": self.pane.pane_id,
                "resolved_via_pane_alias": (
                    self.requested_pane_id != self.pane.pane_id
                ),
            },
            "pane": self.pane.to_dict(),
            "pi_integration": {
                "version": self.pi_integration_version,
                "minimum_native_restore_version": (
                    HERDR_PI_RESTORE_MINIMUM_INTEGRATION_VERSION
                ),
                "native_session_reference_reported": True,
            },
            "continuity": {
                "documented_client_detach_keys": ["ctrl+b", "q"],
                "reattach_argv": [
                    self.herdr_executable,
                    "session",
                    "attach",
                    self.session_name,
                ],
                "live_process_requires_running_server_and_pane": True,
                "pane_close_is_not_client_detach": True,
            },
            "references": [
                {
                    "topic": reference.topic,
                    "documentation_url": reference.documentation_url,
                    "versioned_source_url": reference.versioned_source_url,
                }
                for reference in HERDR_REFERENCES
            ],
        }


@dataclass(frozen=True, slots=True)
class HerdrIntegration(Integration):
    """Read-only adapter to the official Herdr command-line application."""

    executable: Path
    environment: Mapping[str, str]
    timeout_seconds: float = 10.0
    runner: CommandRunner | None = None

    def __post_init__(self) -> None:
        if not self.executable.is_absolute():
            raise HerdrIntegrationError("HERDR_BIN_PATH must be absolute")
        if self.timeout_seconds <= 0:
            raise HerdrIntegrationError(
                "Herdr command timeout must be positive"
            )
        if self.runner is None:
            object.__setattr__(self, "runner", _run_command)

    @classmethod
    def from_environment(
        cls,
        *,
        environ: Mapping[str, str] | None = None,
        runner: CommandRunner | None = None,
        timeout_seconds: float = 10.0,
    ) -> HerdrIntegration:
        """Construct from authoritative Herdr pane environment data."""
        environment = dict(os.environ if environ is None else environ)
        if environment.get("HERDR_ENV") != "1":
            raise HerdrIntegrationError(
                "session continuity can only be inspected from a "
                "Herdr-managed pane (HERDR_ENV=1)"
            )
        for name in (
            "HERDR_BIN_PATH",
            "HERDR_PANE_ID",
            "HERDR_SOCKET_PATH",
            "HERDR_TAB_ID",
            "HERDR_WORKSPACE_ID",
        ):
            if not environment.get(name):
                raise HerdrIntegrationError(
                    f"Herdr-managed environment is missing {name}"
                )
        executable = Path(environment["HERDR_BIN_PATH"])
        return cls(
            executable=executable,
            environment=MappingProxyType(environment),
            timeout_seconds=timeout_seconds,
            runner=_run_command if runner is None else runner,
        )

    def inspect_session(
        self,
        *,
        pane_id: str | None = None,
    ) -> HerdrSessionEvidence:
        """Inspect the current session and one live Pi pane without mutation."""
        version = self._read_version()
        session = self._read_running_session()
        pane = self._read_pane(pane_id)
        self._verify_agent_listing(pane)
        integration_version = self._read_pi_integration_version()
        requested_pane_id = (
            self.environment["HERDR_PANE_ID"] if pane_id is None else pane_id
        )
        return HerdrSessionEvidence(
            herdr_version=version,
            herdr_executable=str(self.executable),
            session_name=_required_string(session, "name", "session"),
            session_is_default=_required_bool(session, "default", "session"),
            socket_path=_required_string(session, "socket_path", "session"),
            requested_pane_id=requested_pane_id,
            pi_integration_version=integration_version,
            pane=pane,
        )

    def _invoke(self, *arguments: str) -> str:
        command = (str(self.executable), *arguments)
        runner = self.runner
        if runner is None:  # Defensive for nonstandard construction.
            raise HerdrIntegrationError("Herdr command runner is unavailable")
        try:
            result = runner(command, self.environment, self.timeout_seconds)
        except subprocess.TimeoutExpired as error:
            raise HerdrIntegrationError(
                f"Herdr command timed out: {' '.join(arguments)}"
            ) from error
        except OSError as error:
            raise HerdrIntegrationError(
                f"could not execute Herdr: {_bounded(str(error))}",
                exit_code=127,
            ) from error
        if result.returncode != 0:
            detail = _bounded(result.stderr.strip())
            suffix = f": {detail}" if detail else ""
            raise HerdrIntegrationError(
                f"Herdr command failed ({' '.join(arguments)}){suffix}"
            )
        return result.stdout

    def _read_version(self) -> str:
        output = self._invoke("--version").strip()
        match = _VERSION_PATTERN.fullmatch(output)
        if match is None:
            raise HerdrIntegrationError(
                "Herdr returned an invalid version string"
            )
        version = match.group("version")
        if version != HERDR_DOCUMENTATION_BASELINE:
            raise HerdrIntegrationError(
                "Herdr version is outside the reviewed documentation baseline: "
                f"expected {HERDR_DOCUMENTATION_BASELINE}, observed {version}"
            )
        return version

    def _read_running_session(self) -> Mapping[str, Any]:
        payload = _parse_json(
            self._invoke("session", "list", "--json"), "session list"
        )
        sessions = _required_list(payload, "sessions", "session list")
        socket_path = self.environment["HERDR_SOCKET_PATH"]
        matching = [
            _mapping(item, "session list item")
            for item in sessions
            if isinstance(item, Mapping)
            and item.get("socket_path") == socket_path
        ]
        if len(matching) != 1:
            raise HerdrIntegrationError(
                "current Herdr socket did not identify exactly one session"
            )
        session = matching[0]
        if not _required_bool(session, "running", "session"):
            raise HerdrIntegrationError("current Herdr session is not running")
        _required_string(session, "name", "session")
        _required_bool(session, "default", "session")
        _required_string(session, "session_dir", "session")
        return session

    def _read_pane(self, pane_id: str | None) -> HerdrPaneEvidence:
        if pane_id is None:
            payload = _parse_json(
                self._invoke("pane", "current", "--current"),
                "current pane",
            )
        else:
            if _PANE_ID_PATTERN.fullmatch(pane_id) is None:
                raise HerdrIntegrationError("pane id has an invalid format")
            payload = _parse_json(
                self._invoke("pane", "get", pane_id),
                "pane",
            )
        expected_id = "cli:pane:current" if pane_id is None else "cli:pane:get"
        if _required_string(payload, "id", "pane response") != expected_id:
            raise HerdrIntegrationError(
                "Herdr returned the wrong pane response"
            )
        result = _required_mapping(payload, "result", "pane response")
        expected_type = "pane_current" if pane_id is None else "pane_info"
        if (
            _required_string(result, "type", "pane response result")
            != expected_type
        ):
            raise HerdrIntegrationError(
                "Herdr returned the wrong pane result type"
            )
        raw_pane = _required_mapping(result, "pane", "pane response result")
        agent = _required_string(raw_pane, "agent", "pane")
        if agent != "pi":
            raise HerdrIntegrationError(
                f"inspected pane does not host Pi: observed {agent!r}"
            )
        agent_status = _required_string(raw_pane, "agent_status", "pane")
        if agent_status not in _AGENT_STATES:
            raise HerdrIntegrationError(
                f"pane has unknown agent status: {agent_status!r}"
            )
        return HerdrPaneEvidence(
            pane_id=_required_string(raw_pane, "pane_id", "pane"),
            tab_id=_required_string(raw_pane, "tab_id", "pane"),
            workspace_id=_required_string(raw_pane, "workspace_id", "pane"),
            terminal_id=_required_string(raw_pane, "terminal_id", "pane"),
            cwd=_required_string(raw_pane, "cwd", "pane"),
            foreground_cwd=_required_string(raw_pane, "foreground_cwd", "pane"),
            agent=agent,
            agent_status=agent_status,
            agent_session=_parse_agent_session(raw_pane),
        )

    def _verify_agent_listing(self, pane: HerdrPaneEvidence) -> None:
        payload = _parse_json(self._invoke("agent", "list"), "agent list")
        if _required_string(payload, "id", "agent list") != "cli:agent:list":
            raise HerdrIntegrationError(
                "Herdr returned the wrong agent response"
            )
        result = _required_mapping(payload, "result", "agent list")
        if (
            _required_string(result, "type", "agent list result")
            != "agent_list"
        ):
            raise HerdrIntegrationError(
                "Herdr returned the wrong agent result type"
            )
        agents = _required_list(result, "agents", "agent list result")
        matching = [
            _mapping(item, "agent list item")
            for item in agents
            if isinstance(item, Mapping) and item.get("pane_id") == pane.pane_id
        ]
        if len(matching) != 1:
            raise HerdrIntegrationError(
                "inspected pane did not identify exactly one live Herdr agent"
            )
        listed = matching[0]
        if _required_string(listed, "agent", "agent list item") != pane.agent:
            raise HerdrIntegrationError(
                "pane and agent-list identities disagree"
            )
        if _parse_agent_session(listed) != pane.agent_session:
            raise HerdrIntegrationError(
                "pane and agent-list native session references disagree"
            )

    def _read_pi_integration_version(self) -> int:
        output = self._invoke("integration", "status")
        match = _INTEGRATION_STATUS_PATTERN.search(output)
        if match is None:
            raise HerdrIntegrationError(
                "the current official Pi integration was not reported"
            )
        version = int(match.group("version"))
        if version < HERDR_PI_RESTORE_MINIMUM_INTEGRATION_VERSION:
            raise HerdrIntegrationError(
                "Pi integration is too old for documented native restore: "
                f"need v{HERDR_PI_RESTORE_MINIMUM_INTEGRATION_VERSION}, "
                f"observed v{version}"
            )
        return version


def _run_command(
    command: tuple[str, ...],
    environment: Mapping[str, str],
    timeout_seconds: float,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        env=dict(environment),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
        text=True,
        timeout=timeout_seconds,
    )


def _parse_json(output: str, context: str) -> Mapping[str, Any]:
    if not output.strip():
        raise HerdrIntegrationError(f"Herdr {context} returned empty output")
    try:
        payload = json.loads(output)
    except json.JSONDecodeError as error:
        raise HerdrIntegrationError(
            f"Herdr {context} returned invalid JSON"
        ) from error
    return _mapping(payload, context)


def _mapping(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise HerdrIntegrationError(f"Herdr {context} must be an object")
    return value


def _required_mapping(
    payload: Mapping[str, Any], key: str, context: str
) -> Mapping[str, Any]:
    if key not in payload:
        raise HerdrIntegrationError(f"Herdr {context} is missing {key}")
    return _mapping(payload[key], f"{context}.{key}")


def _required_list(
    payload: Mapping[str, Any], key: str, context: str
) -> list[object]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise HerdrIntegrationError(f"Herdr {context}.{key} must be a list")
    return value


def _required_string(payload: Mapping[str, Any], key: str, context: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise HerdrIntegrationError(
            f"Herdr {context}.{key} must be a non-empty string"
        )
    return value


def _required_bool(payload: Mapping[str, Any], key: str, context: str) -> bool:
    value = payload.get(key)
    if not isinstance(value, bool):
        raise HerdrIntegrationError(f"Herdr {context}.{key} must be a boolean")
    return value


def _parse_agent_session(payload: Mapping[str, Any]) -> HerdrAgentSession:
    raw_session = _required_mapping(payload, "agent_session", "agent")
    session = HerdrAgentSession(
        agent=_required_string(raw_session, "agent", "agent session"),
        kind=_required_string(raw_session, "kind", "agent session"),
        source=_required_string(raw_session, "source", "agent session"),
        value=_required_string(raw_session, "value", "agent session"),
    )
    if session.agent != "pi" or session.source != "herdr:pi":
        raise HerdrIntegrationError(
            "pane lacks an official Herdr Pi native session reference"
        )
    if session.kind not in {"id", "path"}:
        raise HerdrIntegrationError(
            f"unsupported Pi native session reference kind: {session.kind!r}"
        )
    return session


def _bounded(value: str) -> str:
    normalized = " ".join(value.split())
    if len(normalized) <= _ERROR_OUTPUT_LIMIT:
        return normalized
    return normalized[: _ERROR_OUTPUT_LIMIT - 3] + "..."


def main(argv: Sequence[str] | None = None) -> int:
    """Inspect Herdr continuity and write one JSON document to stdout."""
    import argparse

    parser = argparse.ArgumentParser(
        description="inspect read-only Herdr session-continuity evidence"
    )
    parser.add_argument(
        "--pane-id",
        help="inspect this live pane instead of the calling pane",
    )
    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        evidence = HerdrIntegration.from_environment().inspect_session(
            pane_id=arguments.pane_id
        )
    except HerdrIntegrationError as error:
        print(f"error: {error}", file=sys.stderr)
        return error.exit_code
    print(json.dumps(evidence.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
