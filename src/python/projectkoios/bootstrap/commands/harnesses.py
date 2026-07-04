from __future__ import annotations

from argparse import ArgumentParser, Namespace
from collections.abc import Callable
import os
import subprocess
import sys
from typing import Any, TypeAlias

from projectkoios.bootstrap.models import REPO_ROOT


SubparserCollection: TypeAlias = Any

SESSION: str = "koios"
ARCHON_WINDOW: str = "archon"
OPENCODE_WINDOW: str = "opencode"
GOOSE_WINDOW: str = "goose"
SCRATCH_WINDOW: str = "scratch"
WINDOWS: dict[str, str] = {
    "archon": ARCHON_WINDOW,
    "opencode": OPENCODE_WINDOW,
    "goose": GOOSE_WINDOW,
    "scratch": SCRATCH_WINDOW,
}


def register(subparsers: SubparserCollection) -> None:
    """Register tmux harness-management subcommands.

    Args:
        subparsers: Parent argparse subparser collection receiving the command.
    """

    # Parser owns the harnesses command and dispatches by action name.
    parser: ArgumentParser = subparsers.add_parser("harnesses", help="Manage tmux koios session")
    parser.add_argument("action", choices=["start", "show", "connect", "stop"])
    parser.add_argument("name", nargs="?", default="archon", help="Window name (for connect)")
    parser.set_defaults(func=run)


def tmux(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run tmux with captured text output.

    Args:
        *args: Arguments passed after the tmux executable.
        check: Raise when tmux exits non-zero if true.

    Returns:
        Completed process containing captured stdout and stderr.
    """

    return subprocess.run(["tmux", *args], check=check, capture_output=True, text=True)


def session_exists() -> bool:
    """Return whether the canonical Koios tmux session exists.

    Returns:
        True when tmux reports the session exists.
    """

    # Result is inspected manually because absence is an expected state.
    result: subprocess.CompletedProcess[str] = tmux("has-session", "-t", SESSION, check=False)
    return result.returncode == 0


def window_exists(name: str) -> bool:
    """Return whether a named window exists in the canonical tmux session.

    Args:
        name: Window name to find.

    Returns:
        True when the session exists and contains the requested window.
    """

    if not session_exists():
        return False
    # Result contains the current session window names, one per line.
    result: subprocess.CompletedProcess[str] = tmux("list-windows", "-t", SESSION, "-F", "#{window_name}", check=False)
    return name in result.stdout.splitlines()


def in_tmux() -> bool:
    """Return whether the current process is already inside tmux.

    Returns:
        True when the TMUX environment variable is present.
    """

    return "TMUX" in os.environ


def start() -> None:
    """Start the canonical Koios tmux session and workspace windows."""

    if in_tmux():
        print("error: run 'start' from a normal shell, not from inside tmux")
        sys.exit(1)

    if session_exists():
        print(f"exists: {SESSION}")
    else:
        tmux("new-session", "-d", "-s", SESSION, "-n", ARCHON_WINDOW, "-c", str(REPO_ROOT))
        tmux("send-keys", "-t", f"{SESSION}:{ARCHON_WINDOW}", "pi", "C-m")
        print(f"started: {SESSION}")

    # Windows lists workspace windows and their optional startup commands.
    windows: list[tuple[str, str]] = [
        (OPENCODE_WINDOW, "opencode"),
        (GOOSE_WINDOW, "goose run --instructions goose/AGENT.md"),
        (SCRATCH_WINDOW, ""),
    ]
    name: str
    cmd: str
    for name, cmd in windows:
        if window_exists(name):
            print(f"exists: {name}")
            continue
        tmux("new-window", "-t", SESSION, "-n", name, "-c", str(REPO_ROOT))
        if cmd:
            tmux("send-keys", "-t", f"{SESSION}:{name}", cmd, "C-m")
        print(f"started: {name}")

    tmux("select-window", "-t", f"{SESSION}:{ARCHON_WINDOW}")

    if sys.stdout.isatty():
        subprocess.run(["tmux", "attach", "-t", SESSION])
    else:
        print(f"attach with: tmux attach -t {SESSION}")


def show() -> None:
    """Print the canonical Koios tmux session and window status."""

    if not session_exists():
        print(f"{SESSION}  state=missing")
        return

    print(f"{SESSION}  state=running")
    name: str
    for name in (ARCHON_WINDOW, OPENCODE_WINDOW, GOOSE_WINDOW, SCRATCH_WINDOW):
        if not window_exists(name):
            print(f"  {name} state=missing")
            continue
        # Result reports tmux's formatted status for one window.
        result: subprocess.CompletedProcess[str] = tmux(
            "display-message",
            "-p",
            "-t",
            f"{SESSION}:{name}",
            "#{window_name} active=#{window_active} panes=#{window_panes}",
        )
        print(f"  {result.stdout.strip()}")


def connect(name: str) -> None:
    """Connect or switch to a named Koios workspace window.

    Args:
        name: Logical workspace name to connect to.
    """

    # Window lookup maps logical workspace names to tmux window names.
    win: str | None = WINDOWS.get(name)
    if win is None:
        print(f"error: unknown workspace '{name}' (expected: archon, opencode, goose, scratch)")
        sys.exit(1)
    if not session_exists():
        print(f"error: session {SESSION} does not exist (run 'harnesses start' first)")
        sys.exit(1)
    if not window_exists(win):
        print(f"error: workspace '{win}' does not exist (run 'harnesses start' first)")
        sys.exit(1)

    if in_tmux():
        subprocess.run(["tmux", "switch-client", "-t", f"{SESSION}:{win}"])
    else:
        tmux("select-window", "-t", f"{SESSION}:{win}")
        if sys.stdout.isatty():
            subprocess.run(["tmux", "attach", "-t", SESSION])
        else:
            print(f"selected: {SESSION}:{win}")
            print(f"attach with: tmux attach -t {SESSION}")


def stop() -> None:
    """Stop the canonical Koios tmux session if it exists."""

    if in_tmux():
        print("error: run 'stop' from a normal shell, not from inside tmux")
        sys.exit(1)
    if session_exists():
        tmux("kill-session", "-t", SESSION)
        print(f"stopped: {SESSION}")
    else:
        print(f"missing: {SESSION}")


def check_tmux() -> None:
    """Exit with an error message when tmux is unavailable."""

    try:
        subprocess.run(["tmux", "-V"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("error: tmux is not installed or not on PATH")
        sys.exit(1)


def run(args: Namespace) -> None:
    """Dispatch the requested harness-management action.

    Args:
        args: Parsed CLI namespace containing action and optional workspace name.
    """

    check_tmux()
    # Actions maps CLI action names to command handler functions.
    actions: dict[str, Callable[..., None]] = {"start": start, "show": show, "connect": connect, "stop": stop}
    # Selected handler is invoked with a workspace name only for connect.
    fn: Callable[..., None] = actions[args.action]
    if args.action == "connect":
        fn(args.name)
    else:
        fn()
