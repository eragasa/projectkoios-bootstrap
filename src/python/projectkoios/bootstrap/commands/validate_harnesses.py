from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys
from typing import Any, TypeAlias

from projectkoios.bootstrap.models import REPO_ROOT
from projectkoios.bootstrap.validation.harnesses import Finding, Severity, ValidationResult, validate_harnesses


SubparserCollection: TypeAlias = Any


def register(subparsers: SubparserCollection) -> None:
    """Register the validate-harnesses subcommand.

    Args:
        subparsers: Parent argparse subparser collection receiving the command.
    """

    # Parser defines validation command arguments and delegates behavior to run().
    parser: ArgumentParser = subparsers.add_parser(
        "validate-harnesses",
        help="Validate repo-local harness configuration documents",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to validate (default: current package repo)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures",
    )
    parser.set_defaults(func=run)


def run(args: Namespace) -> None:
    """Run harness validation and print findings plus a summary.

    Args:
        args: Parsed CLI namespace containing root and strict options.
    """

    # Result captures all findings and computes the command exit code.
    result: ValidationResult = validate_harnesses(args.root, strict=args.strict)

    finding: Finding
    for finding in result.findings:
        # Location prefix is present only for findings tied to a repository path.
        location: str = f"{finding.path}: " if finding.path else ""
        print(f"{finding.severity.value}: {location}{finding.message}")

    print(
        "summary: "
        f"{result.count(Severity.ERROR)} error(s), "
        f"{result.count(Severity.WARNING)} warning(s), "
        f"{result.count(Severity.INFO)} info"
    )
    sys.exit(result.exit_code(strict=args.strict))
