from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from projectkoios.bootstrap.branch.base import (
    GitBranch,
    GitBranchChange,
    GitDevBranch,
    GitMainBranch,
    GitReleaseBranch,
    GitRepository,
)
from projectkoios.bootstrap.branch.default import (
    DefaultBranchError,
    DefaultBranchService,
)
from projectkoios.bootstrap.git.client import (
    GitClient,
    GitCommandError,
    decode,
)

_GITHUB_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_REMOTE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")


class MigrationError(RuntimeError):
    """A branch migration could not proceed safely."""

    def __init__(self, stage: str, message: str) -> None:
        super().__init__(message)
        self.stage = stage


@dataclass(frozen=True)
class GitBranchMigration(GitBranchChange):
    """Explicit authority and identity inputs for one migration."""

    apply: bool = False

    def __post_init__(self) -> None:
        if self.source.name == self.target.name:
            raise ValueError("source and target branches must differ")
        if self.source.commit != self.target.commit:
            raise ValueError("source and target commits must match")


@dataclass(frozen=True)
class GitBranchMigrationResult:
    """Terminal evidence from a dry run or applied migration."""

    request: GitBranchMigration
    applied: bool
    target_tracking_commit: str | None

    def render(self) -> str:
        request = self.request
        if not self.applied:
            return "\n".join(
                (
                    "Preflight passed.",
                    f"  repo path:       {request.repository.root}",
                    "  GitHub repo:     "
                    f"{request.repository.github_repository}",
                    f"  remote:          {request.repository.remote}",
                    "  source:          "
                    f"{request.source.name} @ {request.source.commit}",
                    "  target:          "
                    f"{request.target.name} (absent locally and remotely)",
                    f"  current default: {request.source.name}",
                    "DRY RUN ONLY: no refs or repository settings were "
                    "changed. Re-run with --apply to mutate.",
                )
            )
        tracking = self.target_tracking_commit or (
            "ABSENT (canonical remote target verified directly)"
        )
        return "\n".join(
            (
                "FINAL STATUS",
                f"HEAD:                  {request.source.commit}",
                f"local source:          {request.source.commit}",
                f"source tracking ref:   {request.source.commit}",
                f"local target:          {request.source.commit}",
                f"target tracking ref:   {tracking}",
                f"GitHub default branch: {request.target.name}",
                "Open pull requests:     0",
                "SUCCESS: source was preserved; target and default branch "
                "were verified.",
            )
        )


class GitBranchMigrator:
    """Fail-closed action that migrates one repository's default branch."""

    def __init__(self, migration: GitBranchMigration) -> None:
        _validate_migration(migration)
        self._migration = migration
        self._default_branch = DefaultBranchService()
        self._mutate = GitClient(
            disable_optional_locks=False,
            preserve_global_config=True,
        )
        self._stage = "preflight"

    @property
    def migration(self) -> GitBranchMigration:
        return self._migration

    @classmethod
    def from_branches(
        cls,
        repository: GitRepository,
        source: GitBranch,
        target: GitBranch,
        *,
        apply: bool = False,
    ) -> Self:
        return cls(
            GitBranchMigration(
                repository=repository,
                source=source,
                target=target,
                apply=apply,
            )
        )

    def execute(self) -> GitBranchMigrationResult:
        request = self._migration
        try:
            self._stage = "preflight"
            self._default_branch.assert_preflight(request)
            if not request.apply:
                return GitBranchMigrationResult(
                    request=request,
                    applied=False,
                    target_tracking_commit=None,
                )

            self._stage = "create local target"
            self._mutate.run(
                request.repository.root,
                "branch",
                "--",
                request.target.name,
                request.source.commit,
            )

            self._stage = "push target"
            self._mutate.run(
                request.repository.root,
                "push",
                "--porcelain",
                "--no-verify",
                "--recurse-submodules=no",
                f"--force-with-lease=refs/heads/{request.target.name}:",
                request.repository.remote,
                "refs/heads/"
                f"{request.target.name}:refs/heads/{request.target.name}",
                configuration={
                    "push.followTags": "false",
                    "push.pushOption": "",
                },
            )

            self._stage = "post-push gate before default-branch change"
            self._default_branch.assert_post_push(request)

            self._stage = "change GitHub default branch"
            self._default_branch.change_default_branch(request)

            self._stage = "final validation"
            target_tracking = self._default_branch.assert_final(request)
            return GitBranchMigrationResult(
                request=request,
                applied=True,
                target_tracking_commit=target_tracking,
            )
        except MigrationError:
            raise
        except (DefaultBranchError, GitCommandError) as error:
            raise MigrationError(self._stage, str(error)) from error


def _validate_migration(migration: GitBranchMigration) -> None:
    repository = migration.repository
    if not repository.root.is_absolute():
        raise ValueError("repository root must be absolute")
    if not repository.root.is_dir():
        raise ValueError(
            f"repository root is not a directory: {repository.root}"
        )
    if repository.root.resolve() != repository.root:
        raise ValueError(
            f"repository root must be canonical: {repository.root.resolve()}"
        )
    if not _GITHUB_REPOSITORY.fullmatch(repository.github_repository):
        raise ValueError("GitHub repository must be OWNER/REPO")
    if not _REMOTE_NAME.fullmatch(repository.remote):
        raise ValueError("remote contains unsupported characters")

    for command in ("git", "gh"):
        if shutil.which(command) is None:
            raise ValueError(f"required command not found: {command}")

    git = GitClient(disable_optional_locks=True, preserve_global_config=True)
    for branch, label in (
        (migration.source, "source"),
        (migration.target, "target"),
    ):
        try:
            git.run(None, "check-ref-format", f"refs/heads/{branch.name}")
        except GitCommandError as error:
            raise ValueError(
                f"invalid {label} branch: {branch.name}"
            ) from error
    try:
        top = decode(
            git.run(
                repository.root,
                "rev-parse",
                "--show-toplevel",
            ).stdout,
            "repository root",
        ).strip()
    except GitCommandError as error:
        raise ValueError(f"not a Git worktree: {repository.root}") from error
    if Path(top).resolve() != repository.root:
        raise ValueError(f"repository root is not the worktree root: {top}")


def parse_migrator(
    argv: Sequence[str] | None = None,
) -> GitBranchMigrator:
    parser = argparse.ArgumentParser(
        description="Fail-closed GitHub default-branch migration",
    )
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--github-repo", required=True)
    parser.add_argument("--remote", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--apply", action="store_true")
    arguments = parser.parse_args(argv)

    repository = GitRepository(
        root=Path(arguments.repo_path),
        github_repository=arguments.github_repo,
        remote=arguments.remote,
    )
    try:
        return GitBranchMigrator.from_branches(
            repository,
            _branch(arguments.source, arguments.expected_commit),
            _branch(arguments.target, arguments.expected_commit),
            apply=arguments.apply,
        )
    except ValueError as error:
        raise MigrationError("argument validation", str(error)) from error


def _branch(name: str, commit: str) -> GitBranch:
    branch_types = {
        "main": GitMainBranch,
        "dev": GitDevBranch,
        "release": GitReleaseBranch,
    }
    branch_type = branch_types.get(name)
    return (
        GitBranch(name, commit) if branch_type is None else branch_type(commit)
    )


def main(argv: Sequence[str] | None = None) -> int:
    try:
        result = parse_migrator(argv).execute()
    except MigrationError as error:
        print(f"ERROR [{error.stage}]: {error}", file=sys.stderr)
        print(
            "No automatic cleanup or rollback was attempted. "
            "Inspect live refs before any follow-up.",
            file=sys.stderr,
        )
        return 1
    print(result.render())
    return 0
