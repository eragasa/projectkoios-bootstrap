"""Materialize and verify the exact contents of a Git index."""

from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from projectkoios.bootstrap.git.client import (
    GitClient,
    GitCommandError,
    one_line,
)


class StagedSnapshotVerificationError(RuntimeError):
    """The staged repository snapshot could not be verified."""


@dataclass(frozen=True)
class VerificationCommand:
    """One explicit command executed inside the staged snapshot."""

    label: str
    arguments: tuple[str, ...]
    environment: tuple[tuple[str, str], ...] = ()
    timeout_seconds: int = 300

    def __post_init__(self) -> None:
        if not self.label:
            raise StagedSnapshotVerificationError(
                "command label must be nonempty"
            )
        if not self.arguments or not self.arguments[0]:
            raise StagedSnapshotVerificationError(
                "command arguments must identify an executable"
            )
        if self.timeout_seconds <= 0:
            raise StagedSnapshotVerificationError(
                "command timeout must be positive"
            )
        names = tuple(name for name, _value in self.environment)
        if any(not name for name in names) or len(set(names)) != len(names):
            raise StagedSnapshotVerificationError(
                "command environment names must be nonempty and unique"
            )


@dataclass(frozen=True)
class StagedSnapshotVerification:
    """Explicit repository and command sequence for staged verification."""

    repository_root: Path
    commands: tuple[VerificationCommand, ...]

    def __post_init__(self) -> None:
        if not self.commands:
            raise StagedSnapshotVerificationError(
                "at least one verification command is required"
            )
        labels = tuple(command.label for command in self.commands)
        if len(set(labels)) != len(labels):
            raise StagedSnapshotVerificationError(
                "verification command labels must be unique"
            )


@dataclass(frozen=True)
class StagedSnapshotVerificationResult:
    """Evidence that every command passed against one staged tree."""

    staged_tree: str
    completed_commands: tuple[str, ...]


@dataclass(frozen=True)
class StagedSnapshotVerifier:
    """Run explicit checks against a temporary checkout of the Git index."""

    git_timeout_seconds: int = 30

    def verify(
        self,
        verification: StagedSnapshotVerification,
    ) -> StagedSnapshotVerificationResult:
        root = verification.repository_root
        if not root.is_absolute() or root.resolve() != root:
            raise StagedSnapshotVerificationError(
                "repository root must be an absolute canonical path"
            )
        git = GitClient(
            disable_optional_locks=False,
            preserve_global_config=False,
            timeout_seconds=self.git_timeout_seconds,
        )
        observed_root = Path(
            self._git_line(git, root, "rev-parse", "--show-toplevel")
        ).resolve()
        if observed_root != root:
            raise StagedSnapshotVerificationError(
                f"repository root is not a Git worktree root: {root}"
            )

        staged_tree = self._git_line(git, root, "write-tree")
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory)
            self._git_line(
                git,
                root,
                "checkout-index",
                "--all",
                f"--prefix={snapshot}{os.sep}",
            )
            for command in verification.commands:
                environment = os.environ.copy()
                environment.update(command.environment)
                try:
                    completed = subprocess.run(
                        command.arguments,
                        cwd=snapshot,
                        env=environment,
                        check=False,
                        timeout=command.timeout_seconds,
                    )
                except (OSError, subprocess.TimeoutExpired) as error:
                    raise StagedSnapshotVerificationError(
                        f"verification command {command.label!r} "
                        "could not complete"
                    ) from error
                if completed.returncode != 0:
                    raise StagedSnapshotVerificationError(
                        f"verification command {command.label!r} failed "
                        f"with exit status {completed.returncode}"
                    )

        observed_tree = self._git_line(git, root, "write-tree")
        if observed_tree != staged_tree:
            raise StagedSnapshotVerificationError(
                "the Git index changed during staged verification"
            )
        try:
            git.run(root, "diff", "--cached", "--check")
        except GitCommandError as error:
            raise StagedSnapshotVerificationError(str(error)) from error
        return StagedSnapshotVerificationResult(
            staged_tree=staged_tree,
            completed_commands=tuple(
                command.label for command in verification.commands
            ),
        )

    @staticmethod
    def _git_line(
        git: GitClient,
        root: Path,
        *arguments: str,
    ) -> str:
        try:
            result = git.run(root, *arguments)
            return one_line(result)
        except GitCommandError as error:
            raise StagedSnapshotVerificationError(str(error)) from error
