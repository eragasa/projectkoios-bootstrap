from __future__ import annotations

from argparse import ArgumentParser, Namespace
import os
from pathlib import Path
import shutil

from projectkoios.bootstrap.models import RUNTIMES, REPO_ROOT, Runtime


def register(subparsers) -> None:
    parser: ArgumentParser = subparsers.add_parser("install", help="Symlink global configs and materialize skills")
    parser.set_defaults(func=run)


def ensure_symlink(source: str, target: str) -> None:
    if os.path.islink(target):
        os.remove(target)
    elif os.path.exists(target):
        print(f"  skip (non-symlink exists): {target}")
        return
    os.symlink(source, target)
    print(f"  link: {target} → {source}")


def materialize_skills(runtime: Runtime) -> None:
    source_dir: Path = runtime.skills_dir
    if not source_dir.exists() or not any(source_dir.iterdir()):
        return
    destination_dir: Path = runtime.runtime_skills_dir
    destination_dir.mkdir(parents=True, exist_ok=True)
    skill_dir: Path
    for skill_dir in source_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        target: Path = destination_dir / skill_dir.name
        if target.exists():
            print(f"  skip skill: {target}")
            continue
        shutil.copytree(skill_dir, target)
        print(f"  skill: {target}")


def run(args: Namespace) -> None:
    pi_source_home: Path = Path.home() / "pi"
    pi_source_agent: Path = pi_source_home / "agent"
    pi_pi_agent: Path = Path.home() / ".pi" / "agent"

    pi_source_agent.mkdir(parents=True, exist_ok=True)
    pi_pi_agent.mkdir(parents=True, exist_ok=True)

    source: str = str(REPO_ROOT / "pi" / "AGENTS.md")
    target1: str = str(pi_source_agent / "AGENTS.md")
    target2: str = str(pi_pi_agent / "AGENTS.md")
    ensure_symlink(source, target1)
    ensure_symlink(target1, target2)

    name: str
    for name in ("settings.json", "models.json", "trust.json"):
        config_source: Path = REPO_ROOT / "pi" / "agent" / name
        if config_source.exists():
            ensure_symlink(str(config_source), str(pi_source_agent / name))
            ensure_symlink(str(pi_source_agent / name), str(pi_pi_agent / name))

    system_md: Path = REPO_ROOT / "pi" / "SYSTEM.md"
    if system_md.exists():
        ensure_symlink(str(system_md), str(pi_source_home / "SYSTEM.md"))
        ensure_symlink(str(pi_source_home / "SYSTEM.md"), str(pi_pi_agent / "SYSTEM.md"))

    print("done: pi config synced")
    print("note: auth.json is intentionally not managed by install")

    runtime: Runtime
    for runtime in RUNTIMES:
        materialize_skills(runtime)
