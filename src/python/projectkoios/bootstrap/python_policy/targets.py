from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess


EXCLUDED_PARTS: frozenset[str] = frozenset({".git", ".venv", "__pycache__", "build", "dist"})


@dataclass(frozen=True, slots=True)
class ValidationTarget:
    path: Path
    source: str


@dataclass(frozen=True, slots=True)
class TargetSelector:
    repo_root: Path

    def explicit_targets(self, paths: tuple[Path, ...]) -> tuple[ValidationTarget, ...]:
        targets: list[ValidationTarget] = []
        path: Path
        for path in paths:
            targets.extend(self.path_targets(path, source="explicit"))
        return tuple(dict.fromkeys(targets))

    def all_targets(self) -> tuple[ValidationTarget, ...]:
        return self.explicit_targets((self.repo_root / "src" / "python", self.repo_root / "tests"))

    def changed_targets(self) -> tuple[ValidationTarget, ...]:
        command: list[str] = ["git", "diff", "--name-only", "HEAD"]
        completed: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            cwd=self.repo_root,
            check=True,
            text=True,
            capture_output=True,
        )
        paths: list[Path] = []
        line: str
        for line in completed.stdout.splitlines():
            if line.endswith(".py"):
                paths.append(self.repo_root / line)
        return tuple(ValidationTarget(path=path.resolve(), source="changed") for path in paths if self.included(path))

    def path_targets(self, path: Path, *, source: str) -> tuple[ValidationTarget, ...]:
        resolved: Path = path.resolve()
        if resolved.is_file():
            if self.included(resolved):
                return (ValidationTarget(path=resolved, source=source),)
            return ()
        if resolved.is_dir():
            targets: list[ValidationTarget] = []
            child: Path
            for child in sorted(resolved.rglob("*.py")):
                if self.included(child):
                    targets.append(ValidationTarget(path=child.resolve(), source=source))
            return tuple(targets)
        return ()

    def included(self, path: Path) -> bool:
        if path.suffix != ".py":
            return False
        part: str
        for part in path.parts:
            if part in EXCLUDED_PARTS:
                return False
        return True
