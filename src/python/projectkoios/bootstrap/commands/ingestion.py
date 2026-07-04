"""``projectkoios ingestion daemon`` CLI subcommand."""

from __future__ import annotations

import asyncio
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, TypeAlias

from projectkoios.bootstrap.harness.daemon.daemon import print_result, run_daemon, run_once
from projectkoios.bootstrap.harness.daemon.data import DaemonRunResult
from projectkoios.bootstrap.models import REPO_ROOT


SubparserCollection: TypeAlias = Any


def register(subparsers: SubparserCollection) -> None:
    """Register Graphify ingestion daemon subcommands.

    Args:
        subparsers: Parent argparse subparser collection receiving the command group.
    """

    # Parser owns the top-level ingestion command group.
    parser: ArgumentParser = subparsers.add_parser(
        "ingestion",
        help="Graphify ingestion daemon commands",
    )
    # Ingestion subparsers dispatch concrete ingestion daemon actions.
    ingestion_subparsers: SubparserCollection = parser.add_subparsers(dest="action")
    ingestion_subparsers.required = True

    # Daemon parser configures one-shot and watch-mode ingestion runs.
    daemon_parser: ArgumentParser = ingestion_subparsers.add_parser(
        "daemon",
        help="Run the Graphify ingestion daemon for this repository",
    )
    daemon_parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to ingest (default: current package repo)",
    )
    daemon_parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single build cycle and exit (no watcher)",
    )
    daemon_parser.add_argument(
        "--poll-interval",
        type=float,
        default=2.0,
        help="Filesystem poll interval in seconds (default: 2.0)",
    )
    daemon_parser.set_defaults(func=run)


def run(args: Namespace) -> None:
    """Run the ingestion daemon command selected by parsed CLI options.

    Args:
        args: Parsed CLI namespace containing root, once, and poll-interval options.
    """

    # Repository root is normalized before daemon services receive it.
    repo_root: Path = args.root.resolve()
    if args.once:
        # Result is printed through the daemon's stable CLI formatter.
        result: DaemonRunResult = run_once(repo_root, trigger_kind="manual")
        print_result(result)
        return
    asyncio.run(run_watch(repo_root, args.poll_interval))


async def run_watch(repo_root: Path, poll_interval: float) -> None:
    """Run the ingestion daemon until interrupted.

    Args:
        repo_root: Repository root watched by the daemon.
        poll_interval: Filesystem polling interval in seconds.
    """

    # Stop event is passed to the daemon so interruption can request graceful shutdown.
    stop: asyncio.Event = asyncio.Event()
    try:
        await run_daemon(repo_root, poll_interval=poll_interval, stop_event=stop)
    except KeyboardInterrupt:
        stop.set()
