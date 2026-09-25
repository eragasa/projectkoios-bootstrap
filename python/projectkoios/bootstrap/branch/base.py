from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_COMMIT_ID = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class GitRepository:
    """Canonical local, GitHub, and remote identity for one repository."""

    root: Path
    github_repository: str
    remote: str


@dataclass(frozen=True)
class GitBranch:
    """Immutable branch name and exact commit identity."""

    name: str
    commit: str

    def __post_init__(self) -> None:
        if not self.name or self.name.startswith("-"):
            raise ValueError(
                "branch name must be nonempty and not start with '-'"
            )
        if not _COMMIT_ID.fullmatch(self.commit):
            raise ValueError("branch commit must be a full lowercase 40-hex ID")


class GitMainBranch(GitBranch):
    """The fixed long-lived main branch."""

    def __init__(self, commit: str) -> None:
        super().__init__(name="main", commit=commit)


class GitDevBranch(GitBranch):
    """The fixed long-lived development branch."""

    def __init__(self, commit: str) -> None:
        super().__init__(name="dev", commit=commit)


class GitReleaseBranch(GitBranch):
    """The fixed long-lived release branch."""

    def __init__(self, commit: str) -> None:
        super().__init__(name="release", commit=commit)


@dataclass(frozen=True)
class GitFeatureBranch(GitBranch):
    """A feature branch rooted in main or dev."""

    base: GitMainBranch | GitDevBranch

    def __post_init__(self) -> None:
        super().__post_init__()
        if not isinstance(self.base, (GitMainBranch, GitDevBranch)):
            raise ValueError("feature branch base must be main or dev")
        if self.name in {"main", "dev", "release"}:
            raise ValueError(
                "feature branch name conflicts with a long-lived branch"
            )


@dataclass(frozen=True)
class GitBranchChange:
    """Repository plus source and target branch identities."""

    repository: GitRepository
    source: GitBranch
    target: GitBranch
