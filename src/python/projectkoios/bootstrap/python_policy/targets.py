from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess


EXCLUDED_PARTS: frozenset[str] = frozenset({".git", ".venv", "__pycache__", "build", "dist"})


@dataclass(frozen=True, slots=True)
class ValidationTarget:
    """A Python file selected for policy validation.

    Args:
        path: Python file path.
        source: Selection mode that produced the target.
    """

    path: Path
    source: str


@dataclass(frozen=True, slots=True)
class TargetSelector:
    """Select Python files for policy validation.

    Args:
        repo_root: Repository root for relative target resolution and git commands.
    """

    repo_root: Path

    def explicit_targets(self, paths: tuple[Path, ...]) -> tuple[ValidationTarget, ...]:
        """Return Python targets from explicit file or directory paths.

        Args:
            paths: Explicit file or directory paths.

        Returns:
            Deduplicated validation targets.
        """
        # Targets collected from every explicit path.
        targets: list[ValidationTarget] = []
        path: Path
        for path in paths:
            targets.extend(self.path_targets(path, source="explicit"))
        return tuple(dict.fromkeys(targets))

    def all_targets(self) -> tuple[ValidationTarget, ...]:
        """Return all repository Python validation targets.

        Returns:
            Python files under source and test directories.
        """
        return self.explicit_targets((self.repo_root / "src" / "python", self.repo_root / "tests"))

    def changed_targets(self) -> tuple[ValidationTarget, ...]:
        """Return Python files changed relative to HEAD.

        Returns:
            Changed Python validation targets.

        Raises:
            subprocess.CalledProcessError: If git diff fails.
        """
        # Git command lists staged and unstaged changed file names.
        command: list[str] = ["git", "diff", "--name-only", "HEAD"]
        # Completed process contains changed paths relative to repo root.
        completed: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            cwd=self.repo_root,
            check=True,
            text=True,
            capture_output=True,
        )
        # Candidate changed Python paths.
        paths: list[Path] = []
        line: str
        for line in completed.stdout.splitlines():
            if line.endswith(".py"):
                paths.append(self.repo_root / line)
        return tuple(ValidationTarget(path=path.resolve(), source="changed") for path in paths if self.included(path))

    def path_targets(self, path: Path, *, source: str) -> tuple[ValidationTarget, ...]:
        """Return validation targets for one path.

        Args:
            path: File or directory path.
            source: Selection mode label.

        Returns:
            Python file targets contained in the path.
        """
        # Resolved path makes output stable across caller working directories.
        resolved: Path = path.resolve()
        if resolved.is_file():
            if self.included(resolved):
                return (ValidationTarget(path=resolved, source=source),)
            return ()
        if resolved.is_dir():
            # Directory targets recurse into Python files.
            targets: list[ValidationTarget] = []
            child: Path
            for child in sorted(resolved.rglob("*.py")):
                if self.included(child):
                    targets.append(ValidationTarget(path=child.resolve(), source=source))
            return tuple(targets)
        return ()

    def included(self, path: Path) -> bool:
        """Return whether a path should be validated.

        Args:
            path: Candidate Python path.

        Returns:
            True when the path is a non-excluded Python file.
        """
        if path.suffix != ".py":
            return False
        part: str
        for part in path.parts:
            if part in EXCLUDED_PARTS:
                return False
        return True
