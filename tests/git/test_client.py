from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from projectkoios.bootstrap.git.client import (
    GitClient,
    GitCommandError,
    parse_worktree_records,
)


class GitClientTests(unittest.TestCase):
    def test_inspection_environment_removes_side_effects_and_disables_locks(
        self,
    ) -> None:
        client = GitClient(
            disable_optional_locks=True,
            preserve_global_config=False,
        )

        environment = client.environment(
            {
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.fsmonitor",
                "GIT_CONFIG_VALUE_0": "true",
                "GIT_DIR": "/redirected",
                "GIT_OPTIONAL_LOCKS": "1",
                "GIT_TRACE": "1",
                "GIT_TRACE2_EVENT": "/tmp/trace.json",
                "PATH": "/test/bin",
            }
        )

        self.assertNotIn("GIT_CONFIG_COUNT", environment)
        self.assertNotIn("GIT_CONFIG_KEY_0", environment)
        self.assertNotIn("GIT_CONFIG_VALUE_0", environment)
        self.assertNotIn("GIT_DIR", environment)
        self.assertNotIn("GIT_TRACE", environment)
        self.assertNotIn("GIT_TRACE2_EVENT", environment)
        self.assertEqual(environment["GIT_CONFIG_GLOBAL"], os.devnull)
        self.assertEqual(environment["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
        self.assertEqual(environment["GIT_OPTIONAL_LOCKS"], "0")
        self.assertEqual(environment["PATH"], "/test/bin")

    def test_input_bytes_are_sent_without_an_interactive_stdin(self) -> None:
        client = GitClient(
            disable_optional_locks=True,
            preserve_global_config=False,
        )

        result = client.run(
            None,
            "hash-object",
            "--stdin",
            input_bytes=b"preservation evidence\n",
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stdout.strip()), 40)

    def test_lazy_fetch_is_disabled_for_promisor_repositories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repository = root / "repository"
            binary_directory = root / "bin"
            marker = root / "remote-helper-ran"
            repository.mkdir()
            binary_directory.mkdir()
            subprocess.run(
                ("git", "-C", str(repository), "init", "--quiet"),
                check=True,
                timeout=10,
            )
            for key, value in (
                ("extensions.partialClone", "origin"),
                ("remote.origin.promisor", "true"),
                ("remote.origin.url", "attempt::target"),
            ):
                subprocess.run(
                    (
                        "git",
                        "-C",
                        str(repository),
                        "config",
                        key,
                        value,
                    ),
                    check=True,
                    timeout=10,
                )
            helper = binary_directory / "git-remote-attempt"
            helper.write_text(
                f"#!/bin/sh\nprintf attempted > {str(marker)!r}\nexit 1\n",
                encoding="utf-8",
            )
            helper.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = (
                f"{binary_directory}{os.pathsep}{environment['PATH']}"
            )
            missing_oid = "f" * 40

            subprocess.run(
                (
                    "git",
                    "-C",
                    str(repository),
                    "cat-file",
                    "-e",
                    missing_oid,
                ),
                env={**environment, "GIT_NO_LAZY_FETCH": "0"},
                capture_output=True,
                check=False,
                timeout=10,
            )
            self.assertTrue(marker.is_file())
            marker.unlink()

            client = GitClient(
                disable_optional_locks=True,
                preserve_global_config=False,
            )
            result = client.run(
                repository,
                "cat-file",
                "-e",
                missing_oid,
                allowed=(1, 128),
                environment=environment,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(marker.exists())

    def test_mutating_environment_preserves_credentials_but_not_lock_override(
        self,
    ) -> None:
        client = GitClient(
            disable_optional_locks=False,
            preserve_global_config=True,
        )

        environment = client.environment(
            {
                "GIT_CONFIG_GLOBAL": "/credentials/config",
                "GIT_OPTIONAL_LOCKS": "0",
                "PATH": "/test/bin",
            }
        )

        self.assertEqual(
            environment["GIT_CONFIG_GLOBAL"],
            "/credentials/config",
        )
        self.assertNotIn("GIT_CONFIG_NOSYSTEM", environment)
        self.assertEqual(environment["GIT_NO_LAZY_FETCH"], "1")
        self.assertNotIn("GIT_OPTIONAL_LOCKS", environment)


class ParseWorktreeRecordsTests(unittest.TestCase):
    def test_parses_nul_delimited_porcelain(self) -> None:
        records = parse_worktree_records(
            b"worktree /repo\0HEAD abc\0branch refs/heads/main\0\0"
            b"worktree /linked\0HEAD def\0detached\0\0"
        )

        self.assertEqual(
            records,
            (
                {
                    "worktree": "/repo",
                    "HEAD": "abc",
                    "branch": "refs/heads/main",
                },
                {
                    "worktree": "/linked",
                    "HEAD": "def",
                    "detached": True,
                },
            ),
        )

    def test_rejects_duplicate_metadata(self) -> None:
        with self.assertRaisesRegex(
            GitCommandError,
            "duplicate worktree metadata field",
        ):
            parse_worktree_records(b"worktree /repo\0worktree /other\0\0")


if __name__ == "__main__":
    unittest.main()
