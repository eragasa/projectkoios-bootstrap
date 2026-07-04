from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys
from typing import Any, TypeAlias

from projectkoios.bootstrap.models import REPO_ROOT
from projectkoios.bootstrap.python_policy import PolicyFinding, PythonPolicyValidator, TargetSelector, ValidationResult, ValidationTarget


SubparserCollection: TypeAlias = Any


def register(subparsers: SubparserCollection) -> None:
    """Register the validate-python-policy subcommand.

    Args:
        subparsers: Parent argparse subparser collection receiving the command.
    """

    # Parser defines Python policy validation options and delegates execution to run().
    parser: ArgumentParser = subparsers.add_parser(
        "validate-python-policy",
        help="Validate Python files against Project Koios source policy",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Python files or directories to validate, relative to --root when not absolute",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root for target resolution and changed-file detection",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate source and test Python files instead of the default source tree",
    )
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Validate changed Python files relative to HEAD",
    )
    parser.set_defaults(func=run)


def run(args: Namespace) -> None:
    """Run Python policy validation and print findings plus a summary.

    Args:
        args: Parsed CLI namespace containing root, selection mode, and paths.
    """

    # Root anchors relative path arguments and git changed-file detection.
    root: Path = args.root.resolve()
    # Selector expands explicit, all, or changed targets into Python files.
    selector: TargetSelector = TargetSelector(root)
    # Targets are selected from exactly one validation mode.
    targets: tuple[ValidationTarget, ...] = select_targets(args, root, selector)
    # Result contains all AST-checkable policy findings for selected targets.
    result: ValidationResult = PythonPolicyValidator().validate_targets(targets)

    finding: PolicyFinding
    for finding in result.findings:
        print(finding.format())

    print(f"summary: {len(result.findings)} finding(s), {len(targets)} file(s)")
    sys.exit(0 if result.passed else 1)


def select_targets(args: Namespace, root: Path, selector: TargetSelector) -> tuple[ValidationTarget, ...]:
    """Select Python policy validation targets from parsed arguments.

    Args:
        args: Parsed CLI namespace containing mode flags and paths.
        root: Resolved repository root.
        selector: Target selector bound to the repository root.

    Returns:
        Python validation targets selected for this run.
    """

    if args.changed:
        return selector.changed_targets()
    if args.all:
        return selector.all_targets()
    if args.paths:
        # Explicit paths are resolved relative to the requested root for repeatable CLI behavior.
        paths: tuple[Path, ...] = tuple(resolve_cli_path(root, path) for path in args.paths)
        return selector.explicit_targets(paths)
    return selector.explicit_targets((root / "src" / "python",))


def resolve_cli_path(root: Path, path: Path) -> Path:
    """Resolve one CLI path relative to the requested repository root.

    Args:
        root: Resolved repository root.
        path: CLI path argument.

    Returns:
        Absolute path for target selection.
    """

    if path.is_absolute():
        return path
    return root / path
