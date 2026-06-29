import os
from pathlib import Path

from projectkoios.bootstrap.models import REPO_ROOT


def register(subparsers) -> None:
    parser = subparsers.add_parser("install", help="Symlink global configs into place")
    parser.set_defaults(func=run)


def _ensure_symlink(source: str, target: str) -> None:
    if os.path.islink(target):
        os.remove(target)
    elif os.path.exists(target):
        print(f"  skip (non-symlink exists): {target}")
        return
    os.symlink(source, target)
    print(f"  link: {target} → {source}")


def run(args) -> None:
    pi_source_home = Path.home() / "pi"
    pi_source_agent = pi_source_home / "agent"
    pi_pi_agent = Path.home() / ".pi" / "agent"

    pi_source_agent.mkdir(parents=True, exist_ok=True)
    pi_pi_agent.mkdir(parents=True, exist_ok=True)

    source = str(REPO_ROOT / "pi" / "AGENTS.md")
    target1 = str(pi_source_agent / "AGENTS.md")
    target2 = str(pi_pi_agent / "AGENTS.md")
    _ensure_symlink(source, target1)
    _ensure_symlink(target1, target2)

    for name in ("settings.json", "models.json", "trust.json"):
        src = REPO_ROOT / "pi" / "agent" / name
        if src.exists():
            _ensure_symlink(str(src), str(pi_source_agent / name))
            _ensure_symlink(str(pi_source_agent / name), str(pi_pi_agent / name))

    system_md = REPO_ROOT / "pi" / "SYSTEM.md"
    if system_md.exists():
        _ensure_symlink(str(system_md), str(pi_source_home / "SYSTEM.md"))
        _ensure_symlink(str(pi_source_home / "SYSTEM.md"), str(pi_pi_agent / "SYSTEM.md"))

    print("done: pi config synced")
    print("note: auth.json is intentionally not managed by install")
