from __future__ import annotations

import io
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from projectkoios.bootstrap.worktree import inventory


class FilesystemDigestTests(unittest.TestCase):
    def test_rejects_symlink_removed_before_readlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            tracked = root / "tracked"
            tracked.symlink_to(root / "target")
            real_readlink = os.readlink

            def remove_then_readlink(path: str | bytes) -> str | bytes:
                tracked.unlink()
                if isinstance(path, bytes):
                    return real_readlink(path)
                return real_readlink(path)

            listing = subprocess.CompletedProcess(
                args=["git"],
                returncode=0,
                stdout=b"tracked\0",
                stderr=b"",
            )
            with (
                patch.object(inventory, "git", return_value=listing),
                patch.object(
                    inventory.os,
                    "readlink",
                    side_effect=remove_then_readlink,
                ),
            ):
                with self.assertRaisesRegex(
                    inventory.RepositoryChanged,
                    "Symlink changed during inspection",
                ):
                    inventory.filesystem_digest(str(root))

    def test_rejects_regular_file_replaced_by_symlink_before_open(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            tracked = root / "tracked"
            secret = root / "secret"
            tracked.write_text("tracked", encoding="utf-8")
            secret.write_text("secret", encoding="utf-8")
            real_open = os.open

            def replace_then_open(
                path: str | bytes,
                flags: int,
            ) -> int:
                tracked.unlink()
                tracked.symlink_to(secret)
                return real_open(path, flags)

            listing = subprocess.CompletedProcess(
                args=["git"],
                returncode=0,
                stdout=b"tracked\0",
                stderr=b"",
            )
            with (
                patch.object(inventory, "git", return_value=listing),
                patch.object(
                    inventory.os, "open", side_effect=replace_then_open
                ),
            ):
                with self.assertRaisesRegex(
                    inventory.RepositoryChanged,
                    "could not be opened safely",
                ):
                    inventory.filesystem_digest(str(root))


class InventoryCliTests(unittest.TestCase):
    def test_expected_repository_change_has_no_traceback(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch.object(
                inventory,
                "inventory",
                side_effect=inventory.RepositoryChanged("changed"),
            ),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = inventory.main(["inventory-git-worktrees", "/repo"])

        self.assertEqual(result, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "error: changed\n")
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
