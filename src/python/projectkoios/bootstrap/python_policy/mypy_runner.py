from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

from projectkoios.bootstrap.python_policy.targets import ValidationTarget


@dataclass(frozen=True, slots=True)
class MypyResult:
    """Result from running mypy.

    Args:
        exit_code: Process exit code.
        output: Combined stdout and stderr text.
    """

    exit_code: int
    output: str


@dataclass(frozen=True, slots=True)
class MypyRunner:
    """Run mypy against selected Python policy targets.

    Args:
        repo_root: Repository root used as the mypy working directory.
    """

    repo_root: Path

    def run(self, targets: tuple[ValidationTarget, ...]) -> MypyResult:
        """Run mypy for selected targets.

        Args:
            targets: Python files to type-check.

        Returns:
            Captured mypy result.
        """
        if not targets:
            return MypyResult(exit_code=0, output="")
        # Mypy command uses the current Python environment.
        command: list[str] = [sys.executable, "-m", "mypy"]
        target: ValidationTarget
        for target in targets:
            command.append(str(target.path))
        # Completed process captures mypy output without raising on type failures.
        completed: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            cwd=self.repo_root,
            check=False,
            text=True,
            capture_output=True,
        )
        # Combined output is easier to persist in implementation reports.
        output: str = "\n".join(part for part in (completed.stdout.strip(), completed.stderr.strip()) if part)
        return MypyResult(exit_code=completed.returncode, output=output)
