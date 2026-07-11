from __future__ import annotations

import argparse
from argparse import Namespace

from projectkoios.bootstrap.commands import handoff, harnesses, ingestion, init, install, operator_console, validate_harnesses, validate_python_policy, workspaces
from projectkoios.cli import koios, workflow


def main() -> None:
    """Run the Project Koios command-line interface."""
    # Parser owns the top-level projectkoios CLI command surface.
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="projectkoios", description="Project Koios bootstrap CLI")
    # Subparsers dispatch top-level command groups.
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(dest="command")
    subparsers.required = True

    # Bootstrap parser groups bootstrap repository operations.
    bootstrap_parser: argparse.ArgumentParser = subparsers.add_parser("bootstrap", help="Bootstrap commands")
    # Bootstrap subparsers dispatch individual bootstrap commands.
    bootstrap_subparsers: argparse._SubParsersAction[argparse.ArgumentParser] = bootstrap_parser.add_subparsers(dest="action")
    bootstrap_subparsers.required = True

    handoff.register(bootstrap_subparsers)
    init.register(bootstrap_subparsers)
    install.register(bootstrap_subparsers)
    validate_harnesses.register(bootstrap_subparsers)
    validate_python_policy.register(bootstrap_subparsers)
    workspaces.register(bootstrap_subparsers)
    harnesses.register(subparsers)
    ingestion.register(subparsers)
    operator_console.register(subparsers)
    workflow.register(subparsers)
    koios.register(subparsers)

    # Args contains the parsed command namespace and selected handler.
    args: Namespace = parser.parse_args()
    args.func(args)
