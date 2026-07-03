from __future__ import annotations

import argparse

from projectkoios.bootstrap.commands import handoff, harnesses, ingestion, init, install, validate_harnesses, workspaces
from projectkoios.cli import koios


def main() -> None:
    parser = argparse.ArgumentParser(prog="projectkoios", description="Project Koios bootstrap CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    boot = subparsers.add_parser("bootstrap", help="Bootstrap commands")
    boot_sub = boot.add_subparsers(dest="action")
    boot_sub.required = True

    handoff.register(boot_sub)
    init.register(boot_sub)
    install.register(boot_sub)
    validate_harnesses.register(boot_sub)
    workspaces.register(boot_sub)
    harnesses.register(subparsers)
    ingestion.register(subparsers)
    koios.register(subparsers)

    args = parser.parse_args()
    args.func(args)
