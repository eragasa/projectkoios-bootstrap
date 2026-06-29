from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys

from projectkoios.bootstrap.harness.actions.appender import ViolationAppender
from projectkoios.bootstrap.harness.handoffs.evaluator import HandoffEvaluator
from projectkoios.bootstrap.models import REPO_ROOT


def register(subparsers) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "handoff",
        help="Handoff evaluation and management commands",
    )
    h_sub = parser.add_subparsers(dest="action")
    h_sub.required = True

    eval_parser: ArgumentParser = h_sub.add_parser(
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


def run_evaluate(args: Namespace) -> None:
    root = args.root.resolve()
    evaluator = HandoffEvaluator(repo_root=root)
    violations = evaluator.evaluate()

    if not violations:
        print("handoff evaluate: no violations found")
        sys.exit(0)

    by_file = evaluator.violations_by_file(violations)

    if args.dry_run:
        for path, file_violations in sorted(by_file.items()):
            print(f"\n{path}:")
            for v in file_violations:
                print(f"  [{v.code}] {v.reason}")
    else:
        appender = ViolationAppender(dry_run=False)
        for path, file_violations in sorted(by_file.items()):
            if path.exists():
                appender.append(path, file_violations)
                print(f"  appended {len(file_violations)} violation(s) to {path}")

    print(
        f"handoff evaluate: {len(violations)} violation(s) found "
        f"across {len(by_file)} file(s)"
    )
    sys.exit(1 if violations else 0)
