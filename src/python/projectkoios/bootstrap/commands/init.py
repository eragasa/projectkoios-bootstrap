from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import shutil

from projectkoios.bootstrap.models import GLOBAL_DIR, RUNTIMES, Runtime


def register(subparsers) -> None:
    parser: ArgumentParser = subparsers.add_parser("init", help="Copy agents/global/*.example → ~/.<harness>/")
    parser.set_defaults(func=run)


def run(args: Namespace) -> None:
    if not GLOBAL_DIR.exists():
        print(f"error: global config directory not found: {GLOBAL_DIR}")
        return

    runtime: Runtime
    for runtime in RUNTIMES:
        source_dir: Path = GLOBAL_DIR / runtime.name
        if not source_dir.exists():
            print(f"skip: {runtime.name} — no global config at {source_dir}")
            continue

        destination_dir: Path = runtime.config_dir
        destination_dir.mkdir(parents=True, exist_ok=True)

        item: Path
        for item in source_dir.iterdir():
            if item.is_dir():
                continue
            name: str = item.name
            target_name: str = name.removesuffix(".example") if name.endswith(".example") else name
            target: Path = destination_dir / target_name
            if target.exists():
                print(f"  exist: {target}")
            else:
                shutil.copy2(item, target)
                print(f"  wrote: {target}")

    print("done: init complete")
