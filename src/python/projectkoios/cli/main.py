from __future__ import annotations

import argparse
from argparse import Namespace

from projectkoios.bootstrap.commands import handoff, harnesses, ingestion, init, install, validate_harnesses, workspaces
from projectkoios.cli import koios


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="projectkoios", description="Project Koios bootstrap CLI")
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(dest="command")
    subparsers.required = True

    bootstrap_parser: argparse.ArgumentParser = subparsers.add_parser("bootstrap", help="Bootstrap commands")
    bootstrap_subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = bootstrap_parser.add_subparsers(dest="action")
    bootstrap_subparsers.required = True

    handoff.register(bootstrap_subparsers)
    init.register(bootstrap_subparsers)
    install.register(bootstrap_subparsers)
    validate_harnesses.register(bootstrap_subparsers)
    workspaces.register(bootstrap_subparsers)
    harnesses.register(subparsers)
    ingestion.register(subparsers)
    koios.register(subparsers)

    args: Namespace = parser.parse_args()
    args.func(args)
