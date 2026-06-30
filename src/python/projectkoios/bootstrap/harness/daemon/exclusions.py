"""Exclusion policy for the Graphify ingestion daemon.

Implements ``.gitignore``-style path matching plus built-in excludes for
generated, runtime, sensitive, and daemon-output directories. The exclusion
policy determines which filesystem events trigger ingestion.
"""

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
"""Built-in excludes always applied regardless of .gitignore contents.

These cover generated, runtime, cache, dependency, sensitive, and daemon-output
paths. ``.pi/koios-ingestion`` is excluded so the daemon never watches its own
output even if the runtime directory happens to be inside the repo root.
"""


@dataclass(frozen=True)
class ExclusionPolicy:
    """Path exclusion policy combining .gitignore-style and built-in rules.

    A path is excluded if any component matches a built-in exclude pattern or
    a loaded .gitignore pattern. .gitignore parsing is intentionally minimal:
    it supports plain patterns and directory patterns (trailing ``/``). Negation
    (``!``), glob anchors (``/`` in middle), and ``**`` are not supported in
    the first slice — YAGNI. The built-in excludes cover the safety-critical
    cases.
    """

    repo_root: Path
    builtin: tuple[str, ...] = BUILTIN_EXCLUDES
    gitignore_patterns: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def for_repo(cls, repo_root: Path) -> ExclusionPolicy:
        """Build an exclusion policy for *repo_root*, loading ``.gitignore``."""
        root = repo_root.resolve()
        patterns = _load_gitignore(root)
        return cls(repo_root=root, gitignore_patterns=patterns)

    def is_excluded(self, path: Path) -> bool:
        """True if *path* should be excluded from ingestion.

        Tests each path component against built-in patterns and the full
        repo-relative path against .gitignore patterns. A path is excluded if
        any rule matches any component or the relative path.
        """
        try:
            rel = path.resolve().relative_to(self.repo_root)
        except ValueError:
            return True

        parts = rel.parts
        for part in parts:
            for pattern in self.builtin:
                if fnmatch(part, pattern):
                    return True

        rel_posix = rel.as_posix()
        for pattern in self.gitignore_patterns:
            if _gitignore_match(pattern, rel_posix):
                return True

        return False

    def filter_eligible(self, paths: list[Path]) -> list[Path]:
        """Return only the paths that are not excluded."""
        return [p for p in paths if not self.is_excluded(p)]


def _load_gitignore(repo_root: Path) -> tuple[str, ...]:
    """Load patterns from ``.gitignore`` at *repo_root*.

    Strips comments, blank lines, and negation patterns (not supported in the
    first slice). Directory patterns (trailing ``/``) are kept as-is; the
    match logic tests both the pattern and the pattern without the slash.
    """
    gitignore = repo_root / ".gitignore"
    if not gitignore.exists():
        return ()
    patterns: list[str] = []
    for line in gitignore.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("!"):
            continue
        patterns.append(stripped)
    return tuple(patterns)


def _gitignore_match(pattern: str, rel_path: str) -> bool:
    """Match a .gitignore-style pattern against a repo-relative posix path."""
    clean = pattern.rstrip("/")
    if fnmatch(rel_path, clean):
        return True
    if fnmatch(rel_path, f"{clean}/*"):
        return True
    for part in rel_path.split("/"):
        if fnmatch(part, clean):
            return True
    return False
