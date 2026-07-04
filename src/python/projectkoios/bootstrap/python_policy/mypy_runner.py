from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

from projectkoios.bootstrap.python_policy.targets import ValidationTarget


@dataclass(frozen=True, slots=True)
class MypyResult:
    exit_code: int
    output: str


@dataclass(frozen=True, slots=True)
class MypyRunner:
    repo_root: Path

    def run(self, targets: tuple[ValidationTarget, ...]) -> MypyResult:
        if not targets:
            return MypyResult(exit_code=0, output="")
        command: list[str] = [sys.executable, "-m", "mypy"]
        target: ValidationTarget
        for target in targets:
            command.append(str(target.path))
        completed: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            cwd=self.repo_root,
            check=False,
            text=True,
            capture_output=True,
        )
        output: str = "\n".join(part for part in (completed.stdout.strip(), completed.stderr.strip()) if part)
        return MypyResult(exit_code=completed.returncode, output=output)
