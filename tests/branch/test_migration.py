from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import cast

from projectkoios.bootstrap.branch import (
    GitBranch,
    GitBranchMigrator,
    GitDevBranch,
    GitFeatureBranch,
    GitMainBranch,
    GitReleaseBranch,
    GitRepository,
)


class GitBranchTypesTests(unittest.TestCase):
    def test_long_lived_branch_names_are_fixed(self) -> None:
        commit = "a" * 40

        self.assertEqual(GitMainBranch(commit).name, "main")
        self.assertEqual(GitDevBranch(commit).name, "dev")
        self.assertEqual(GitReleaseBranch(commit).name, "release")

    def test_feature_branch_requires_main_or_dev_base(self) -> None:
        commit = "a" * 40
        main = GitMainBranch(commit)
        dev = GitDevBranch(commit)

        self.assertEqual(
            GitFeatureBranch("feature/main-work", commit, main).base,
            main,
        )
        self.assertEqual(
            GitFeatureBranch("feature/dev-work", commit, dev).base,
            dev,
        )
        invalid_base = cast(
            GitMainBranch | GitDevBranch,
            GitReleaseBranch(commit),
        )
        with self.assertRaisesRegex(ValueError, "base must be main or dev"):
            GitFeatureBranch("feature/release-work", commit, invalid_base)

    def test_feature_branch_rejects_long_lived_names(self) -> None:
        commit = "a" * 40
        base = GitDevBranch(commit)

        for name in ("main", "dev", "release"):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, "conflicts"):
                    GitFeatureBranch(name, commit, base)


class GitBranchMigratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        root = Path(self.temporary_directory.name).resolve()
        subprocess.run(
            ["git", "init", "-q", str(root)],
            check=True,
            timeout=10,
        )
        self.repository = GitRepository(
            root=root,
            github_repository="owner/repository",
            remote="origin",
        )
        self.source = GitBranch(name="master", commit="a" * 40)

    def test_from_branches_builds_immutable_migration(self) -> None:
        target = GitMainBranch(self.source.commit)

        migrator = GitBranchMigrator.from_branches(
            self.repository,
            self.source,
            target,
        )

        self.assertEqual(migrator.migration.repository, self.repository)
        self.assertEqual(migrator.migration.source, self.source)
        self.assertEqual(migrator.migration.target, target)
        self.assertFalse(migrator.migration.apply)

    def test_rejects_same_source_and_target_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "must differ"):
            GitBranchMigrator.from_branches(
                self.repository,
                self.source,
                GitBranch(
                    name=self.source.name,
                    commit=self.source.commit,
                ),
            )

    def test_rejects_commit_change_during_branch_migration(self) -> None:
        with self.assertRaisesRegex(ValueError, "commits must match"):
            GitBranchMigrator.from_branches(
                self.repository,
                self.source,
                GitMainBranch("b" * 40),
            )

    def test_rejects_invalid_branch_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid target branch"):
            GitBranchMigrator.from_branches(
                self.repository,
                self.source,
                GitBranch(name="bad..name", commit=self.source.commit),
            )


if __name__ == "__main__":
    unittest.main()
