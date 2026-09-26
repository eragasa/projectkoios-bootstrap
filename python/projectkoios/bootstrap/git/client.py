from __future__ import annotations

import os
import subprocess
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

_GIT_REDIRECTION_VARIABLES = frozenset(
    {
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_COMMON_DIR",
        "GIT_CONFIG_COUNT",
        "GIT_CONFIG_PARAMETERS",
        "GIT_DIR",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_WORK_TREE",
    }
)
_GIT_CONFIG = (
    "-c",
    "color.ui=false",
    "-c",
    "core.fsmonitor=false",
    "-c",
    "core.untrackedCache=false",
    "-c",
    "diff.ignoreSubmodules=none",
    "-c",
    "gc.auto=0",
    "-c",
    "maintenance.auto=false",
)


class GitCommandError(RuntimeError):
    """A bounded Git command could not produce accepted evidence."""


@dataclass(frozen=True)
class GitClient:
    """Run bounded Git commands with repository redirection disabled."""

    disable_optional_locks: bool
    preserve_global_config: bool
    timeout_seconds: int = 30

    def run(
        self,
        repository: str | Path | None,
        *arguments: str,
        allowed: Iterable[int] = (0,),
        environment: Mapping[str, str] | None = None,
        configuration: Mapping[str, str] | None = None,
        input_bytes: bytes | None = None,
    ) -> subprocess.CompletedProcess[bytes]:
        command = ["git", *_GIT_CONFIG]
        for key, value in (configuration or {}).items():
            command.extend(("-c", f"{key}={value}"))
        if repository is not None:
            command.extend(("-C", os.fspath(repository)))
        command.extend(arguments)
        accepted = frozenset(allowed)
        try:
            result = subprocess.run(
                command,
                input=input_bytes,
                stdin=subprocess.DEVNULL if input_bytes is None else None,
                capture_output=True,
                check=False,
                env=self.environment(environment),
                timeout=self.timeout_seconds,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise GitCommandError(
                f"Git command could not complete: {_operation(arguments)}"
            ) from error
        if result.returncode not in accepted:
            raise GitCommandError(
                "Git command failed "
                f"({_operation(arguments)}, exit {result.returncode})"
            )
        return result

    def environment(
        self,
        supplied: Mapping[str, str] | None = None,
    ) -> dict[str, str]:
        source = os.environ if supplied is None else supplied
        result = {
            key: value
            for key, value in source.items()
            if key not in _GIT_REDIRECTION_VARIABLES
            and not key.startswith(
                ("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_", "GIT_TRACE")
            )
        }
        result.update(
            {
                "GIT_NO_LAZY_FETCH": "1",
                "GIT_TERMINAL_PROMPT": "0",
                "LANG": "C",
                "LC_ALL": "C",
            }
        )
        if self.disable_optional_locks:
            result["GIT_OPTIONAL_LOCKS"] = "0"
        else:
            result.pop("GIT_OPTIONAL_LOCKS", None)
        if not self.preserve_global_config:
            result.update(
                {
                    "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_CONFIG_NOSYSTEM": "1",
                }
            )
        return result


def parse_worktree_records(
    payload: bytes,
) -> tuple[dict[str, str | bool], ...]:
    records: list[dict[str, str | bool]] = []
    current: dict[str, str | bool] = {}
    for field in payload.split(b"\0"):
        if not field:
            if current:
                records.append(current)
                current = {}
            continue
        key, separator, value = field.partition(b" ")
        name = os.fsdecode(key)
        parsed: str | bool = os.fsdecode(value) if separator else True
        if name in current:
            raise GitCommandError(f"duplicate worktree metadata field: {name}")
        current[name] = parsed
    if current:
        records.append(current)
    if not records:
        raise GitCommandError("Git reported no registered worktrees")
    return tuple(records)


def decode(payload: bytes, label: str = "Git output") -> str:
    try:
        return payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise GitCommandError(f"{label} is not UTF-8") from error


def one_line(
    result: subprocess.CompletedProcess[bytes],
    label: str = "Git output",
) -> str:
    return decode(result.stdout.rstrip(b"\n"), label)


def _operation(arguments: Sequence[str]) -> str:
    return " ".join(arguments[:2]) or "<none>"
