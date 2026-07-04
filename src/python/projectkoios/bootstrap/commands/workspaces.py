from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any

from projectkoios.bootstrap.models import REPO_ROOT
from projectkoios.bootstrap.workspaces import CANONICAL_WORKSPACES, ensure_workspaces


def register(subparsers) -> None:
    parser: ArgumentParser = subparsers.add_parser(
        "workspaces",
        help="Manage per-agent workspaces and handoff folders",
    )
    workspace_subparsers: Any = parser.add_subparsers(dest="workspace_action")
    workspace_subparsers.required = True

    init_parser: ArgumentParser = workspace_subparsers.add_parser(
        "init",
        help="Create local workspaces, handoff folders, and seed AGENT.md files",
    )
    init_parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to materialize workspaces in",
    )
    init_parser.add_argument(
        "--agents",
        nargs="*",
        choices=CANONICAL_WORKSPACES,
        default=list(CANONICAL_WORKSPACES),
        help="Optional subset of workspaces to create",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing seed files",
    )
    init_parser.set_defaults(func=run_init)


def run_init(args: Namespace) -> None:
    created: list[Path] = ensure_workspaces(
        args.root,
        agents=args.agents,
        force=args.force,
    )
    path: Path
    for path in created:
        print(f"wrote: {path}")
    print("done: workspaces initialized")
