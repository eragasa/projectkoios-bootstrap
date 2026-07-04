from __future__ import annotations

from argparse import ArgumentParser, Namespace
import os
from pathlib import Path
import shutil
from typing import Any, TypeAlias

from projectkoios.bootstrap.models import RUNTIMES, REPO_ROOT, Runtime


SubparserCollection: TypeAlias = Any


def register(subparsers: SubparserCollection) -> None:
    """Register the install subcommand on an argparse subparser collection.

    Args:
        subparsers: Parent argparse subparser collection receiving the command.
    """

    # Parser defines the user-facing install command and delegates behavior to run().
    parser: ArgumentParser = subparsers.add_parser("install", help="Symlink global configs and materialize skills")
    parser.set_defaults(func=run)


def ensure_symlink(source: str, target: str) -> None:
    """Replace a symlink target with a symlink to the requested source.

    Args:
        source: Filesystem path the symlink should point to.
        target: Filesystem path where the symlink should be created.
    """

    if os.path.islink(target):
        os.remove(target)
    elif os.path.exists(target):
        print(f"  skip (non-symlink exists): {target}")
        return
    os.symlink(source, target)
    print(f"  link: {target} → {source}")


def materialize_skills(runtime: Runtime) -> None:
    """Copy shared skill examples into a runtime's local skill directory.

    Args:
        runtime: Harness runtime whose shared skills should be materialized.
    """

    # Source directory is the committed shared skill-example directory for the runtime.
    source_dir: Path = runtime.skills_dir
    if not source_dir.exists() or not any(source_dir.iterdir()):
        return
    # Destination directory is the runtime-specific local skill installation path.
    destination_dir: Path = runtime.runtime_skills_dir
    destination_dir.mkdir(parents=True, exist_ok=True)
    skill_dir: Path
    for skill_dir in source_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        # Target is the local skill directory copied from the shared example source.
        target: Path = destination_dir / skill_dir.name
        if target.exists():
            print(f"  skip skill: {target}")
            continue
        shutil.copytree(skill_dir, target)
        print(f"  skill: {target}")


def run(args: Namespace) -> None:
    """Install local symlinks and materialized skills for bootstrap harness config.

    Args:
        args: Parsed CLI namespace reserved for interface consistency.
    """

    # Pi source home is the compatibility path used by older local harness config.
    pi_source_home: Path = Path.home() / "pi"
    # Pi source agent directory receives repo-managed source symlinks.
    pi_source_agent: Path = pi_source_home / "agent"
    # Pi runtime agent directory is the current local Pi config path.
    pi_pi_agent: Path = Path.home() / ".pi" / "agent"

    pi_source_agent.mkdir(parents=True, exist_ok=True)
    pi_pi_agent.mkdir(parents=True, exist_ok=True)

    # Source is the repo-owned global Pi instruction file.
    source: str = str(REPO_ROOT / "pi" / "AGENTS.md")
    # First target preserves the historical local source path.
    target1: str = str(pi_source_agent / "AGENTS.md")
    # Second target links the current runtime config to the historical source path.
    target2: str = str(pi_pi_agent / "AGENTS.md")
    ensure_symlink(source, target1)
    ensure_symlink(target1, target2)

    name: str
    for name in ("settings.json", "models.json", "trust.json"):
        # Config source is the optional repo-owned Pi agent config file.
        config_source: Path = REPO_ROOT / "pi" / "agent" / name
        if config_source.exists():
            ensure_symlink(str(config_source), str(pi_source_agent / name))
            ensure_symlink(str(pi_source_agent / name), str(pi_pi_agent / name))

    # System prompt source is optional and only linked when committed locally.
    system_md: Path = REPO_ROOT / "pi" / "SYSTEM.md"
    if system_md.exists():
        ensure_symlink(str(system_md), str(pi_source_home / "SYSTEM.md"))
        ensure_symlink(str(pi_source_home / "SYSTEM.md"), str(pi_pi_agent / "SYSTEM.md"))

    print("done: pi config synced")
    print("note: auth.json is intentionally not managed by install")

    runtime: Runtime
    for runtime in RUNTIMES:
        materialize_skills(runtime)
