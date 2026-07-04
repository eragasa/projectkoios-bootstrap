from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import shutil
from typing import Any, TypeAlias

from projectkoios.bootstrap.models import GLOBAL_DIR, RUNTIMES, Runtime


SubparserCollection: TypeAlias = Any


def register(subparsers: SubparserCollection) -> None:
    """Register the init subcommand on an argparse subparser collection.

    Args:
        subparsers: Parent argparse subparser collection receiving the command.
    """

    # Parser defines the user-facing command and delegates behavior to run().
    parser: ArgumentParser = subparsers.add_parser("init", help="Copy agents/global/*.example → ~/.<harness>/")
    parser.set_defaults(func=run)


def run(args: Namespace) -> None:
    """Copy shared global example configs into local harness config directories.

    Args:
        args: Parsed CLI namespace reserved for interface consistency.
    """

    if not GLOBAL_DIR.exists():
        print(f"error: global config directory not found: {GLOBAL_DIR}")
        return

    runtime: Runtime
    for runtime in RUNTIMES:
        # Source directory contains committed example config files for one runtime.
        source_dir: Path = GLOBAL_DIR / runtime.name
        if not source_dir.exists():
            print(f"skip: {runtime.name} — no global config at {source_dir}")
            continue

        # Destination directory is the local machine config root for the runtime.
        destination_dir: Path = runtime.config_dir
        destination_dir.mkdir(parents=True, exist_ok=True)

        item: Path
        for item in source_dir.iterdir():
            if item.is_dir():
                continue
            # Name preserves non-example files and strips .example from templates.
            name: str = item.name
            # Target name is the local config filename that should be materialized.
            target_name: str = name.removesuffix(".example") if name.endswith(".example") else name
            # Target is the local config path that receives the copied example.
            target: Path = destination_dir / target_name
            if target.exists():
                print(f"  exist: {target}")
            else:
                shutil.copy2(item, target)
                print(f"  wrote: {target}")

    print("done: init complete")
