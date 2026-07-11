from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
import subprocess
from typing import Any, TypeAlias

from projectkoios.bootstrap.models import REPO_ROOT


SubparserCollection: TypeAlias = Any


OPERATOR_CONSOLE_PACKAGE_DIR: Path = REPO_ROOT / "src" / "typescript" / "projectkoios" / "ui" / "operator-console"


class OperatorConsolePreviewCommand:
    """Run the bootstrap-incubated Operator Console browser preview."""

    def run(self, args: Namespace) -> None:
        """Install, build, and serve the Operator Console preview from the package directory.

        Args:
            args: Parsed CLI namespace with preview host/install options.
        """

        package_dir: Path = Path(args.package_dir).resolve()
        if not package_dir.exists():
            raise SystemExit(f"error: operator console package not found: {package_dir}")

        print(f"operator-console package: {package_dir}")
        if not args.skip_install:
            self.run_step(["npm", "install", "--ignore-scripts"], package_dir)
        self.run_step(["npm", "run", "build"], package_dir)
        print(f"operator-console preview: http://{args.host}:{args.port}/")
        print("press Ctrl-C to stop preview")
        self.run_step(["npm", "run", "preview", "--", "--host", args.host, "--port", str(args.port)], package_dir)

    def run_step(self, command: list[str], cwd: Path) -> None:
        """Run one npm command in the Operator Console package directory.

        Args:
            command: Command argv to execute.
            cwd: Working directory for the command.
        """

        subprocess.run(command, cwd=cwd, check=True)


def register(subparsers: SubparserCollection) -> None:
    """Register the operator-console command group.

    Args:
        subparsers: Parent argparse subparser collection receiving the command group.
    """

    parser: ArgumentParser = subparsers.add_parser("operator-console", help="Operator Console incubation commands")
    action_subparsers: SubparserCollection = parser.add_subparsers(dest="action")
    action_subparsers.required = True

    preview_parser: ArgumentParser = action_subparsers.add_parser("preview", help="Install, build, and serve the local UI preview")
    preview_parser.add_argument("--host", default="127.0.0.1", help="Preview host passed to Vite")
    preview_parser.add_argument("--port", default=4173, type=int, help="Preview port passed to Vite")
    preview_parser.add_argument("--skip-install", action="store_true", help="Skip npm install and only build/preview")
    preview_parser.add_argument("--package-dir", default=str(OPERATOR_CONSOLE_PACKAGE_DIR), help="Operator Console package directory")
    preview_parser.set_defaults(func=OperatorConsolePreviewCommand().run)
