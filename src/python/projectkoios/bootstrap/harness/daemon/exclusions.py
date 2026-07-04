"""Exclusion policy for the Graphify ingestion daemon."""

from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path


BUILTIN_EXCLUDES: tuple[str, ...] = (
    ".git",
    "graphify-out",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "node_modules",
    ".DS_Store",
    "*.egg-info",
    "*.pyc",
    "*.pyo",
    ".pi/koios-ingestion",
    "*.swp",
    "*.swo",
    "*~",
)


@dataclass(frozen=True)
class ExclusionPolicy:
    """Path exclusion policy combining .gitignore-style and built-in rules."""

    repo_root: Path
    builtin: tuple[str, ...] = BUILTIN_EXCLUDES
    gitignore_patterns: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def for_repo(cls, repo_root: Path) -> ExclusionPolicy:
        """Build an exclusion policy for *repo_root*, loading ``.gitignore``."""
        # Root is normalized before matching repository-relative paths.
        root: Path = repo_root.resolve()
        # Patterns are loaded once so every policy check uses the same gitignore view.
        patterns: tuple[str, ...] = load_gitignore(root)
        return cls(repo_root=root, gitignore_patterns=patterns)

    def is_excluded(self, path: Path) -> bool:
        """True if *path* should be excluded from ingestion."""
        try:
            # Relative path rejects inputs outside the repository root.
            rel: Path = path.resolve().relative_to(self.repo_root)
        except ValueError:
            return True

        # Parts allow built-in patterns to match any path component.
        parts: tuple[str, ...] = rel.parts
        part: str
        pattern: str
        for part in parts:
            for pattern in self.builtin:
                if fnmatch(part, pattern):
                    return True

        # Rel-posix is the normalized string used for gitignore-style matching.
        rel_posix: str = rel.as_posix()
        for pattern in self.gitignore_patterns:
            if gitignore_match(pattern, rel_posix):
                return True

        return False

    def filter_eligible(self, paths: list[Path]) -> list[Path]:
        """Return only the paths that are not excluded."""
        return [path for path in paths if not self.is_excluded(path)]


def load_gitignore(repo_root: Path) -> tuple[str, ...]:
    """Load patterns from ``.gitignore`` at *repo_root*."""
    # Gitignore is the repository-local ignore file read by the daemon policy.
    gitignore: Path = repo_root / ".gitignore"
    if not gitignore.exists():
        return ()
    # Patterns accumulates supported non-negated ignore lines.
    patterns: list[str] = []
    line: str
    for line in gitignore.read_text(encoding="utf-8").splitlines():
        # Stripped line removes comments and blank-line noise before matching.
        stripped: str = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("!"):
            continue
        patterns.append(stripped)
    return tuple(patterns)


def gitignore_match(pattern: str, rel_path: str) -> bool:
    """Match a .gitignore-style pattern against a repo-relative posix path."""
    # Clean pattern ignores a trailing slash while preserving the path prefix.
    clean: str = pattern.rstrip("/")
    if fnmatch(rel_path, clean):
        return True
    if fnmatch(rel_path, f"{clean}/*"):
        return True
    part: str
    for part in rel_path.split("/"):
        if fnmatch(part, clean):
            return True
    return False
