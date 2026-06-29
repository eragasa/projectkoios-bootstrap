import os
import shlex
import subprocess
import sys
from pathlib import Path

from projectkoios.bootstrap.models import REPO_ROOT

SESSION = "koios"
ARCHON_WINDOW = "archon"
OPENCODE_WINDOW = "opencode"
GOOSE_WINDOW = "goose"
SCRATCH_WINDOW = "scratch"


def register(subparsers) -> None:
    p = subparsers.add_parser("harnesses", help="Manage tmux koios session")
    p.add_argument("action", choices=["start", "show", "connect", "stop"])
    p.add_argument("name", nargs="?", default="archon", help="Window name (for connect)")
    p.set_defaults(func=run)


def _tmux(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["tmux", *args], check=check, capture_output=True, text=True)


def _session_exists() -> bool:
    r = _tmux("has-session", "-t", SESSION, check=False)
    return r.returncode == 0


def _window_exists(name: str) -> bool:
    if not _session_exists():
        return False
    r = _tmux("list-windows", "-t", SESSION, "-F", "#{window_name}", check=False)
    return name in r.stdout.splitlines()


def _in_tmux() -> bool:
    return "TMUX" in os.environ


def _start() -> None:
    if _in_tmux():
        print("error: run 'start' from a normal shell, not from inside tmux")
        sys.exit(1)

    if _session_exists():
        print(f"exists: {SESSION}")
    else:
        _tmux("new-session", "-d", "-s", SESSION, "-n", ARCHON_WINDOW, "-c", str(REPO_ROOT))
        _tmux("send-keys", "-t", f"{SESSION}:{ARCHON_WINDOW}", "pi", "C-m")
        print(f"started: {SESSION}")

    windows: list[tuple[str, str]] = [
        (OPENCODE_WINDOW, "opencode"),
        (GOOSE_WINDOW, f"goose run --instructions goose/AGENT.md"),
        (SCRATCH_WINDOW, ""),
    ]
    for name, cmd in windows:
        if _window_exists(name):
            print(f"exists: {name}")
            continue
        _tmux("new-window", "-t", SESSION, "-n", name, "-c", str(REPO_ROOT))
        if cmd:
            _tmux("send-keys", "-t", f"{SESSION}:{name}", cmd, "C-m")
        print(f"started: {name}")

    _tmux("select-window", "-t", f"{SESSION}:{ARCHON_WINDOW}")

    if sys.stdout.isatty():
        subprocess.run(["tmux", "attach", "-t", SESSION])
    else:
        print(f"attach with: tmux attach -t {SESSION}")


def _show() -> None:
    if not _session_exists():
        print(f"{SESSION}  state=missing")
        return

    print(f"{SESSION}  state=running")
    for name in (ARCHON_WINDOW, OPENCODE_WINDOW, GOOSE_WINDOW, SCRATCH_WINDOW):
        if not _window_exists(name):
            print(f"  {name} state=missing")
            continue
        r = _tmux("display-message", "-p", "-t", f"{SESSION}:{name}",
                  "#{window_name} active=#{window_active} panes=#{window_panes}")
        print(f"  {r.stdout.strip()}")


def _connect(name: str) -> None:
    windows = {"archon": ARCHON_WINDOW, "opencode": OPENCODE_WINDOW,
               "goose": GOOSE_WINDOW, "scratch": SCRATCH_WINDOW}
    win = windows.get(name)
    if win is None:
        print(f"error: unknown workspace '{name}' (expected: archon, opencode, goose, scratch)")
        sys.exit(1)
    if not _session_exists():
        print(f"error: session {SESSION} does not exist (run 'harnesses start' first)")
        sys.exit(1)
    if not _window_exists(win):
        print(f"error: workspace '{win}' does not exist (run 'harnesses start' first)")
        sys.exit(1)

    if _in_tmux():
        subprocess.run(["tmux", "switch-client", "-t", f"{SESSION}:{win}"])
    else:
        _tmux("select-window", "-t", f"{SESSION}:{win}")
        if sys.stdout.isatty():
            subprocess.run(["tmux", "attach", "-t", SESSION])
        else:
            print(f"selected: {SESSION}:{win}")
            print(f"attach with: tmux attach -t {SESSION}")


def _stop() -> None:
    if _in_tmux():
        print("error: run 'stop' from a normal shell, not from inside tmux")
        sys.exit(1)
    if _session_exists():
        _tmux("kill-session", "-t", SESSION)
        print(f"stopped: {SESSION}")
    else:
        print(f"missing: {SESSION}")


def _check_tmux() -> None:
    try:
        subprocess.run(["tmux", "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("error: tmux is not installed or not on PATH")
        sys.exit(1)


def run(args) -> None:
    _check_tmux()
    actions = {"start": _start, "show": _show, "connect": _connect, "stop": _stop}
    fn = actions[args.action]
    if args.action == "connect":
        fn(args.name)
    else:
        fn()
