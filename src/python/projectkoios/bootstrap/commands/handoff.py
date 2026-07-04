from __future__ import annotations

from argparse import ArgumentParser, Namespace
from dataclasses import asdict
import json
from pathlib import Path
import sys
from typing import Any, TypeAlias

from projectkoios.bootstrap.harness.data.violation import Violation
from projectkoios.bootstrap.harness.handoffs.appender import append_violations
from projectkoios.bootstrap.harness.handoffs.evaluator import HandoffEvaluator
from projectkoios.bootstrap.harness.handoffs.topics import TopicsView, build_topics_view
from projectkoios.bootstrap.models import REPO_ROOT


SubparserCollection: TypeAlias = Any


def register(subparsers: SubparserCollection) -> None:
    """Register handoff evaluation and topic-listing subcommands.

    Args:
        subparsers: Parent argparse subparser collection receiving the command group.
    """

    # Parser owns the top-level handoff command group.
    parser: ArgumentParser = subparsers.add_parser(
        "handoff",
        help="Handoff evaluation and management commands",
    )
    # Handoff subparsers dispatch concrete handoff actions.
    handoff_subparsers: SubparserCollection = parser.add_subparsers(dest="action")
    handoff_subparsers.required = True

    # Evaluate parser checks handoff artifacts and can append violation comments.
    eval_parser: ArgumentParser = handoff_subparsers.add_parser(
        "evaluate",
        help="Evaluate handoff artifacts for guard violations",
    )
    eval_parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to evaluate (default: current package repo)",
    )
    eval_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print violations without modifying files",
    )
    eval_parser.set_defaults(func=run_evaluate)

    # Topics parser prints current handoff topics in stable JSON form.
    topics_parser: ArgumentParser = handoff_subparsers.add_parser(
        "topics",
        help="Show all handoff topics with their current messages",
    )
    topics_parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to evaluate (default: current package repo)",
    )
    topics_parser.add_argument(
        "--json",
        action="store_true",
        default=True,
        help="Output as JSON (default: true)",
    )
    topics_parser.add_argument(
        "--with-timestamp",
        action="store_true",
        help="Include a generation timestamp (omit for byte-stable output)",
    )
    topics_parser.set_defaults(func=run_topics)


def run_topics(args: Namespace) -> None:
    """Print a JSON view of handoff topics.

    Args:
        args: Parsed CLI namespace containing root and timestamp options.
    """

    # Root is normalized before topic collection scans repository files.
    root: Path = args.root.resolve()
    # View contains all topic data in a dataclass shape suitable for JSON output.
    view: TopicsView = build_topics_view(root, include_timestamp=args.with_timestamp)
    print(json.dumps(asdict(view), indent=2, default=str, ensure_ascii=False))


def run_evaluate(args: Namespace) -> None:
    """Evaluate handoff artifacts and optionally append violation comments.

    Args:
        args: Parsed CLI namespace containing root and dry-run options.
    """

    # Root is normalized before evaluator scans handoff artifacts.
    root: Path = args.root.resolve()
    # Evaluator owns handoff parsing and violation detection.
    evaluator: HandoffEvaluator = HandoffEvaluator(repo_root=root)
    # Violations are kept in original evaluator order for stable grouping.
    violations: list[Violation] = evaluator.evaluate()

    if not violations:
        print("handoff evaluate: no violations found")
        sys.exit(0)

    # Grouped violations determine which files would be printed or mutated.
    by_file: dict[Path, list[Violation]] = evaluator.violations_by_file(violations)

    path: Path
    file_violations: list[Violation]
    if args.dry_run:
        for path, file_violations in sorted(by_file.items()):
            print(f"\n{path}:")
            violation: Violation
            for violation in file_violations:
                print(f"  [{violation.code.value}] {violation.reason}")
    else:
        for path, file_violations in sorted(by_file.items()):
            if path.exists():
                append_violations(path, file_violations)
                print(f"  appended {len(file_violations)} violation(s) to {path}")

    print(
        f"handoff evaluate: {len(violations)} violation(s) found "
        f"across {len(by_file)} file(s)"
    )
    sys.exit(1 if violations else 0)
