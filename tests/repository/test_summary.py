from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from projectkoios.bootstrap.repository import summary

_REPOSITORY = Path(__file__).parents[2]
_SCRIPT = _REPOSITORY / "scripts/summarize-project-worktrees"


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ("git", "-C", str(repository), *arguments),
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return completed.stdout.strip()


def _create_repository(path: Path) -> Path:
    path.mkdir()
    _git(path, "init", "--quiet", "--initial-branch=main")
    (path / "tracked.txt").write_text("tracked\n", encoding="utf-8")
    _git(path, "add", "tracked.txt")
    _git(
        path,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "--quiet",
        "-m",
        "initial",
    )
    return path


def _inventory(
    path: Path,
    worktrees: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "repository": {
            "default_remote_ref": {
                "available": True,
                "oid": "a" * 40,
                "ref": "refs/remotes/origin/HEAD",
                "symbolic_target": "refs/remotes/origin/main",
            },
            "origin_urls": [f"https://github.com/example/{path.name}.git"],
            "path": str(path),
        },
        "worktrees": worktrees,
    }


def _worktree(**overrides: object) -> dict[str, object]:
    result: dict[str, object] = {
        "branch": "main",
        "dirty_entry_count": 0,
        "index_flags": {
            "assume_unchanged_count": 0,
            "skip_worktree_count": 0,
        },
        "inspectable": True,
        "locked": False,
        "missing": False,
        "prunable": False,
        "state": "branch",
        "upstream": {
            "ahead": 0,
            "behind": 0,
            "comparable": True,
        },
    }
    result.update(overrides)
    return result


class RepositorySummaryTests(unittest.TestCase):
    def test_reports_only_factual_counts(self) -> None:
        path = Path("/repositories/example")

        result = summary.summarize_repository(_inventory(path, [_worktree()]))

        self.assertEqual(result["registered_worktree_count"], 1)
        self.assertEqual(result["dirty_worktree_count"], 0)
        self.assertEqual(result["branches"], ["main"])
        self.assertNotIn("local_migration_readiness", result)

    def test_counts_each_preservation_risk_independently(self) -> None:
        path = Path("/repositories/example")
        cases = (
            ("dirty_entry_count", 1, "dirty_worktree_count"),
            ("inspectable", False, "uninspectable_worktree_count"),
            ("locked", True, "locked_worktree_count"),
            ("missing", True, "missing_worktree_count"),
            ("prunable", True, "prunable_worktree_count"),
            ("state", "detached", "non_branch_worktree_count"),
        )

        for field, value, count_field in cases:
            with self.subTest(field=field):
                result = summary.summarize_repository(
                    _inventory(path, [_worktree(**{field: value})])
                )
                self.assertEqual(result[count_field], 1)

    def test_preserves_unknown_state_without_treating_it_as_clean(self) -> None:
        path = Path("/repositories/example")

        result = summary.summarize_repository(
            _inventory(
                path,
                [
                    _worktree(
                        dirty_entry_count=None,
                        index_flags={
                            "assume_unchanged_count": None,
                            "skip_worktree_count": None,
                        },
                        upstream=None,
                    )
                ],
            )
        )

        self.assertEqual(result["dirty_worktree_count"], 0)
        self.assertEqual(result["unknown_dirty_state_count"], 1)
        self.assertEqual(result["hidden_index_flag_count"], 0)
        self.assertEqual(
            result["upstream_comparison_unavailable_worktree_count"],
            1,
        )

    def test_upstream_relationship_counts_use_git_terminology(self) -> None:
        path = Path("/repositories/example")
        result = summary.summarize_repository(
            _inventory(
                path,
                [
                    _worktree(
                        upstream={"ahead": 1, "behind": 0, "comparable": True}
                    ),
                    _worktree(
                        upstream={"ahead": 0, "behind": 1, "comparable": True}
                    ),
                    _worktree(
                        upstream={"ahead": 1, "behind": 1, "comparable": True}
                    ),
                ],
            )
        )

        self.assertEqual(result["upstream_ahead_worktree_count"], 2)
        self.assertEqual(result["upstream_behind_worktree_count"], 2)
        self.assertEqual(result["upstream_diverged_worktree_count"], 1)

    def test_rejects_unknown_worktree_state(self) -> None:
        path = Path("/repositories/example")

        with self.assertRaisesRegex(
            summary.RepositorySummaryError,
            "state must be one of",
        ):
            summary.summarize_repository(
                _inventory(path, [_worktree(state="unexpected")])
            )

    def test_allows_additive_fields_within_the_same_schema_version(
        self,
    ) -> None:
        path = Path("/repositories/example")
        inventory = _inventory(path, [_worktree()])
        inventory["future_top_level_fact"] = True
        repository = inventory["repository"]
        assert isinstance(repository, dict)
        repository["future_repository_fact"] = True
        default_ref = repository["default_remote_ref"]
        assert isinstance(default_ref, dict)
        default_ref["future_default_ref_fact"] = True
        worktrees = inventory["worktrees"]
        assert isinstance(worktrees, list)
        worktree = worktrees[0]
        worktree["future_worktree_fact"] = True
        index_flags = worktree["index_flags"]
        assert isinstance(index_flags, dict)
        index_flags["future_index_fact"] = True
        upstream = worktree["upstream"]
        assert isinstance(upstream, dict)
        upstream["future_upstream_fact"] = True

        result = summary.summarize_repository(inventory)

        self.assertEqual(result["registered_worktree_count"], 1)

    def test_missing_required_producer_field_fails_closed(self) -> None:
        path = Path("/repositories/example")
        worktree = _worktree()
        del worktree["locked"]

        with self.assertRaisesRegex(
            summary.RepositorySummaryError,
            "missing required field 'locked'",
        ):
            summary.summarize_repository(_inventory(path, [worktree]))

    def test_rejects_missing_schema_version(self) -> None:
        path = Path("/repositories/example")
        inventory = _inventory(path, [_worktree()])
        del inventory["schema_version"]

        with self.assertRaisesRegex(
            summary.RepositorySummaryError,
            "missing required field 'schema_version'",
        ):
            summary.summarize_repository(inventory)

    def test_rejects_incomplete_default_remote_ref(self) -> None:
        path = Path("/repositories/example")
        inventory = _inventory(path, [_worktree()])
        repository = inventory["repository"]
        assert isinstance(repository, dict)
        default_ref = repository["default_remote_ref"]
        assert isinstance(default_ref, dict)
        del default_ref["oid"]

        with self.assertRaisesRegex(
            summary.RepositorySummaryError,
            "missing required field 'oid'",
        ):
            summary.summarize_repository(inventory)

    def test_comparable_upstream_requires_integer_counts(self) -> None:
        path = Path("/repositories/example")

        with self.assertRaisesRegex(
            summary.RepositorySummaryError,
            "upstream.ahead must be a non-negative integer",
        ):
            summary.summarize_repository(
                _inventory(
                    path,
                    [
                        _worktree(
                            upstream={
                                "ahead": None,
                                "behind": 0,
                                "comparable": True,
                            }
                        )
                    ],
                )
            )

    def test_repository_output_is_sorted_independently_of_input_order(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            first = root / "a"
            second = root / "b"
            first.mkdir()
            second.mkdir()
            inventories = {
                first: _inventory(first, [_worktree()]),
                second: _inventory(second, [_worktree()]),
            }

            with patch.object(
                summary,
                "inventory_repository",
                side_effect=lambda path: inventories[path],
            ):
                result = summary.summarize_repository_set([second, first])

        self.assertEqual(
            [item["path"] for item in result["repositories"]],
            [str(first), str(second)],
        )
        self.assertEqual(result["totals"]["repository_count"], 2)
        self.assertNotIn(
            "local_migration_candidate_count",
            result["totals"],
        )


class RepositorySummaryCliTests(unittest.TestCase):
    def test_cli_output_is_byte_identical_for_reversed_input_order(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            first = _create_repository(root / "a")
            second = _create_repository(root / "b")

            forward = subprocess.run(
                [str(_SCRIPT), str(first), str(second)],
                capture_output=True,
                check=False,
                timeout=30,
            )
            reverse = subprocess.run(
                [str(_SCRIPT), str(second), str(first)],
                capture_output=True,
                check=False,
                timeout=30,
            )

        self.assertEqual(forward.returncode, 0, forward.stderr)
        self.assertEqual(reverse.returncode, 0, reverse.stderr)
        self.assertEqual(forward.stdout, reverse.stdout)
        self.assertIsInstance(forward.stdout, bytes)
        payload = json.loads(forward.stdout)
        self.assertFalse(payload["contract"]["deletion_safety_assessed"])
        self.assertFalse(payload["contract"]["migration_safety_assessed"])
        self.assertFalse(payload["contract"]["github_state_assessed"])
        self.assertNotIn("statement", payload["contract"])

    def test_late_repository_failure_emits_no_partial_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            valid = _create_repository(root / "a-valid")
            invalid = root / "z-not-git"
            invalid.mkdir()

            result = subprocess.run(
                [str(_SCRIPT), str(valid), str(invalid)],
                capture_output=True,
                check=False,
                text=True,
                timeout=30,
            )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("inventory failed", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_script_rejects_relative_repository_without_traceback(self) -> None:
        result = subprocess.run(
            [str(_SCRIPT), "relative/repository"],
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("must be absolute", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
