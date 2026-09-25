from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from projectkoios.bootstrap.git.staged_snapshot import (
    StagedSnapshotVerification,
    StagedSnapshotVerificationError,
    StagedSnapshotVerifier,
    VerificationCommand,
)


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ("git", "-C", str(repository), *arguments),
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return completed.stdout.strip()


class StagedSnapshotVerifierTests(unittest.TestCase):
    def test_verifies_index_without_copying_unstaged_or_untracked_content(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory).resolve()
            _git(repository, "init", "--quiet")
            tracked = repository / "tracked.txt"
            tracked.write_text("staged\n", encoding="utf-8")
            _git(repository, "add", "tracked.txt")
            tracked.write_text("unstaged\n", encoding="utf-8")
            (repository / "untracked.txt").write_text(
                "not staged\n",
                encoding="utf-8",
            )
            verification = StagedSnapshotVerification(
                repository_root=repository,
                commands=(
                    VerificationCommand(
                        label="inspect-index",
                        arguments=(
                            sys.executable,
                            "-c",
                            (
                                "from pathlib import Path; "
                                "assert Path('tracked.txt').read_text() "
                                "== 'staged\\n'; "
                                "assert not Path('untracked.txt').exists()"
                            ),
                        ),
                    ),
                ),
            )

            result = StagedSnapshotVerifier().verify(verification)

            self.assertEqual(result.completed_commands, ("inspect-index",))
            self.assertEqual(result.staged_tree, _git(repository, "write-tree"))
            self.assertEqual(tracked.read_text(encoding="utf-8"), "unstaged\n")

    def test_reports_failing_command(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory).resolve()
            _git(repository, "init", "--quiet")
            (repository / "tracked.txt").write_text(
                "staged\n",
                encoding="utf-8",
            )
            _git(repository, "add", "tracked.txt")
            verification = StagedSnapshotVerification(
                repository_root=repository,
                commands=(
                    VerificationCommand(
                        label="fails",
                        arguments=(
                            sys.executable,
                            "-c",
                            "raise SystemExit(7)",
                        ),
                    ),
                ),
            )

            with self.assertRaisesRegex(
                StagedSnapshotVerificationError,
                "'fails'.*exit status 7",
            ):
                StagedSnapshotVerifier().verify(verification)

    def test_requires_explicit_commands(self) -> None:
        with self.assertRaisesRegex(
            StagedSnapshotVerificationError,
            "at least one",
        ):
            StagedSnapshotVerification(
                repository_root=Path("/repository"),
                commands=(),
            )


if __name__ == "__main__":
    unittest.main()
