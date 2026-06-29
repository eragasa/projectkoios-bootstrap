from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys

from projectkoios.bootstrap.models import REPO_ROOT
from projectkoios.bootstrap.validation.harnesses import Severity, validate_harnesses


def register(subparsers) -> None:
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
    result = validate_harnesses(args.root, strict=args.strict)

    for finding in result.findings:
        location = f"{finding.path}: " if finding.path else ""
        print(f"{finding.severity.value}: {location}{finding.message}")

    print(
        "summary: "
        f"{result.count(Severity.ERROR)} error(s), "
        f"{result.count(Severity.WARNING)} warning(s), "
        f"{result.count(Severity.INFO)} info"
    )
    sys.exit(result.exit_code(strict=args.strict))
