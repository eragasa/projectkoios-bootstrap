from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any

_REPOSITORY = Path(__file__).parents[2]
_SCRIPT = _REPOSITORY / "scripts/inventory-git-worktrees"


class InventoryGitWorktreesScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name).resolve()
        self.repository = self.root / "repository"
        self.linked_worktree = self.root / "linked"

        self.git(self.root, "init", "-b", "main", self.repository)
        self.git(self.repository, "config", "user.name", "Test User")
        self.git(
            self.repository,
            "config",
            "user.email",
            "test@example.invalid",
        )
        (self.repository / "assume.txt").write_text(
            "assume\n",
            encoding="utf-8",
        )
        (self.repository / "skip.txt").write_text("skip\n", encoding="utf-8")
        self.git(self.repository, "add", "assume.txt", "skip.txt")
        self.git(self.repository, "commit", "-m", "initial")
        self.git(
            self.repository,
            "remote",
            "add",
            "origin",
            "https://github.com/test-owner/test-repository.git",
        )
        self.git(
            self.repository,
            "update-ref",
            "refs/remotes/origin/main",
            "HEAD",
        )
        self.git(
            self.repository,
            "symbolic-ref",
            "refs/remotes/origin/HEAD",
            "refs/remotes/origin/main",
        )
        self.git(
            self.repository,
            "worktree",
            "add",
            "-b",
            "feature/test",
            self.linked_worktree,
        )
        self.git(
            self.repository,
            "update-index",
            "--assume-unchanged",
            "assume.txt",
        )
        self.git(
            self.linked_worktree,
            "update-index",
            "--skip-worktree",
            "skip.txt",
        )
        (self.linked_worktree / "untracked.txt").write_text(
            "dirty\n",
            encoding="utf-8",
        )

    def git(self, cwd: Path, *arguments: object) -> None:
        subprocess.run(
            ["git", "-C", str(cwd), *(str(value) for value in arguments)],
            capture_output=True,
            check=True,
            text=True,
            timeout=10,
        )

    def inventory(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(_SCRIPT), str(self.repository)],
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )

    def by_branch(self, payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {item["branch"]: item for item in payload["worktrees"]}

    def test_reports_dirty_state_index_flags_and_local_ancestry(self) -> None:
        result = self.inventory()

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["contract"]["deletion_safety_assessed"])
        self.assertEqual(
            payload["repository"]["default_remote_ref"]["symbolic_target"],
            "refs/remotes/origin/main",
        )
        branches = self.by_branch(payload)
        self.assertEqual(set(branches), {"main", "feature/test"})
        self.assertEqual(branches["main"]["dirty_entry_count"], 0)
        self.assertEqual(
            branches["main"]["index_flags"]["assume_unchanged_paths"],
            ["assume.txt"],
        )
        self.assertEqual(branches["feature/test"]["dirty_entry_count"], 1)
        self.assertEqual(
            branches["feature/test"]["index_flags"]["skip_worktree_paths"],
            ["skip.txt"],
        )
        self.assertTrue(
            branches["feature/test"]["default_remote_ancestry"][
                "head_is_ancestor"
            ]
        )

    def test_repeated_stable_inventory_is_byte_identical(self) -> None:
        first = self.inventory()
        second = self.inventory()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)

    def test_rejects_relative_path_without_stdout(self) -> None:
        result = subprocess.run(
            [str(_SCRIPT), "relative/path"],
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("must be absolute", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
