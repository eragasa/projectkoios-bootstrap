from __future__ import annotations

from collections.abc import Callable
from argparse import ArgumentParser, Namespace
import os
import subprocess
import sys

from projectkoios.bootstrap.models import REPO_ROOT


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


def register(subparsers) -> None:
    parser: ArgumentParser = subparsers.add_parser("harnesses", help="Manage tmux koios session")
    parser.add_argument("action", choices=["start", "show", "connect", "stop"])
    parser.add_argument("name", nargs="?", default="archon", help="Window name (for connect)")
    parser.set_defaults(func=run)


def tmux(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["tmux", *args], check=check, capture_output=True, text=True)


def session_exists() -> bool:
    result: subprocess.CompletedProcess[str] = tmux("has-session", "-t", SESSION, check=False)
    return result.returncode == 0


def window_exists(name: str) -> bool:
    if not session_exists():
        return False
    result: subprocess.CompletedProcess[str] = tmux("list-windows", "-t", SESSION, "-F", "#{window_name}", check=False)
    return name in result.stdout.splitlines()


def in_tmux() -> bool:
    return "TMUX" in os.environ


def start() -> None:
    if in_tmux():
        print("error: run 'start' from a normal shell, not from inside tmux")
        sys.exit(1)

    if session_exists():
        print(f"exists: {SESSION}")
    else:
        tmux("new-session", "-d", "-s", SESSION, "-n", ARCHON_WINDOW, "-c", str(REPO_ROOT))
        tmux("send-keys", "-t", f"{SESSION}:{ARCHON_WINDOW}", "pi", "C-m")
        print(f"started: {SESSION}")

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
    if not session_exists():
        print(f"{SESSION}  state=missing")
        return

    print(f"{SESSION}  state=running")
    name: str
    for name in (ARCHON_WINDOW, OPENCODE_WINDOW, GOOSE_WINDOW, SCRATCH_WINDOW):
        if not window_exists(name):
            print(f"  {name} state=missing")
            continue
        result: subprocess.CompletedProcess[str] = tmux(
            "display-message",
            "-p",
            "-t",
            f"{SESSION}:{name}",
            "#{window_name} active=#{window_active} panes=#{window_panes}",
        )
        print(f"  {result.stdout.strip()}")


def connect(name: str) -> None:
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
    if in_tmux():
        print("error: run 'stop' from a normal shell, not from inside tmux")
        sys.exit(1)
    if session_exists():
        tmux("kill-session", "-t", SESSION)
        print(f"stopped: {SESSION}")
    else:
        print(f"missing: {SESSION}")


def check_tmux() -> None:
    try:
        subprocess.run(["tmux", "-V"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("error: tmux is not installed or not on PATH")
        sys.exit(1)


def run(args: Namespace) -> None:
    check_tmux()
    actions: dict[str, Callable[..., None]] = {"start": start, "show": show, "connect": connect, "stop": stop}
    fn: Callable[..., None] = actions[args.action]
    if args.action == "connect":
        fn(args.name)
    else:
        fn()
