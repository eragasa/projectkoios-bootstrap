from __future__ import annotations

import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Sequence

from scripts import koios_issues


FIXTURES = Path(__file__).parent / "fixtures" / "issues"


class FakeRunner:
    def __init__(
        self,
        responses: dict[tuple[str, ...], subprocess.CompletedProcess[str]],
    ) -> None:
        self.responses = responses
        self.calls: list[tuple[str, ...]] = []

    def __call__(
        self, args: Sequence[str], timeout: float
    ) -> subprocess.CompletedProcess[str]:
        del timeout
        key = tuple(args)
        self.calls.append(key)
        if key not in self.responses:
            raise AssertionError(f"unexpected command: {key}")
        return self.responses[key]


class SequenceRunner:
    def __init__(self, stdout_values: Sequence[str]) -> None:
        self.stdout_values = list(stdout_values)
        self.calls: list[tuple[str, ...]] = []

    def __call__(
        self, args: Sequence[str], timeout: float
    ) -> subprocess.CompletedProcess[str]:
        del timeout
        self.calls.append(tuple(args))
        if not self.stdout_values:
            raise AssertionError(f"unexpected command: {tuple(args)}")
        return completed(args, stdout=self.stdout_values.pop(0))


def completed(
    args: Sequence[str],
    *,
    returncode: int = 0,
    stdout: str = "",
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(list(args), returncode, stdout, stderr)


class RepositoryMapTests(unittest.TestCase):
    def test_parses_repository_rows_in_map_order(self) -> None:
        specs = koios_issues.parse_repository_map(
            FIXTURES / "repositories.md", Path("/w")
        )

        self.assertEqual(
            [spec.name for spec in specs],
            ["projectkoios", "projectkoios-bootstrap"],
        )
        self.assertEqual(specs[1].path, Path("/w/projectkoios-bootstrap"))

    def test_rejects_duplicate_repository_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            map_path = Path(directory) / "repositories.md"
            map_path.write_text(
                "| Repository | Purpose |\n"
                "|---|---|\n"
                "| `duplicate` | one |\n"
                "| `duplicate` | two |\n",
                encoding="utf-8",
            )

            with self.assertRaises(koios_issues.SetupError) as raised:
                koios_issues.parse_repository_map(map_path, Path(directory))

        self.assertEqual(raised.exception.kind, "map_invalid")

    def test_rejects_malformed_row_instead_of_silently_omitting_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            map_path = Path(directory) / "repositories.md"
            map_path.write_text(
                "| Repository | Purpose |\n"
                "|---|---|\n"
                "| `projectkoios` | valid |\n"
                "| projectkoios-missing-backticks | invalid |\n",
                encoding="utf-8",
            )

            with self.assertRaises(koios_issues.SetupError) as raised:
                koios_issues.parse_repository_map(map_path, Path(directory))

        self.assertEqual(raised.exception.kind, "map_invalid")


class RemoteTests(unittest.TestCase):
    def test_parses_common_github_remote_forms(self) -> None:
        remotes = [
            "https://github.com/example/projectkoios.git",
            "git@github.com:example/projectkoios.git",
            "ssh://git@github.com/example/projectkoios.git",
        ]

        identities = [koios_issues.parse_github_remote(remote) for remote in remotes]

        self.assertTrue(all(identity.host == "github.com" for identity in identities))
        self.assertTrue(
            all(identity.slug == "example/projectkoios" for identity in identities)
        )

    def test_rejects_non_repository_remote(self) -> None:
        with self.assertRaises(ValueError):
            koios_issues.parse_github_remote("file:///tmp/projectkoios")

    def test_missing_checkout_is_an_explicit_error(self) -> None:
        spec = koios_issues.RepositorySpec("projectkoios", Path("/does-not-exist"))

        result = koios_issues.resolve_repository(spec)

        self.assertIsInstance(result, koios_issues.RepositoryResult)
        assert isinstance(result, koios_issues.RepositoryResult)
        self.assertEqual(result.error_kind, "missing_checkout")

    def test_missing_origin_is_an_explicit_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            spec = koios_issues.RepositorySpec("projectkoios", Path(directory))
            command = (
                "git",
                "-C",
                directory,
                "remote",
                "get-url",
                "origin",
            )
            runner = FakeRunner({command: completed(command, returncode=2)})

            result = koios_issues.resolve_repository(spec, runner)

        self.assertIsInstance(result, koios_issues.RepositoryResult)
        assert isinstance(result, koios_issues.RepositoryResult)
        self.assertEqual(result.error_kind, "missing_origin")

    def test_mismatched_origin_is_an_explicit_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            spec = koios_issues.RepositorySpec("projectkoios", Path(directory))
            command = (
                "git",
                "-C",
                directory,
                "remote",
                "get-url",
                "origin",
            )
            runner = FakeRunner(
                {
                    command: completed(
                        command,
                        stdout="https://github.com/example/another-repository.git\n",
                    )
                }
            )

            result = koios_issues.resolve_repository(spec, runner)

        self.assertIsInstance(result, koios_issues.RepositoryResult)
        assert isinstance(result, koios_issues.RepositoryResult)
        self.assertEqual(result.error_kind, "remote_mismatch")


class ResponseTests(unittest.TestCase):
    def test_flattens_pages_sorts_issues_and_sanitizes_titles(self) -> None:
        pages = [
            [
                {
                    "number": 4,
                    "title": "Fourth\u202e synthetic issue",
                    "url": "https://github.com/example/repo/issues/4",
                }
            ],
            [
                {
                    "number": 1,
                    "title": "First synthetic issue",
                    "url": "https://github.com/example/repo/issues/1",
                }
            ],
        ]

        issues = koios_issues.normalize_issue_pages(pages)

        self.assertEqual([issue.number for issue in issues], [1, 4])
        self.assertEqual(issues[1].title, "Fourth synthetic issue")

    def test_rejects_duplicate_issue_across_pages(self) -> None:
        entry = {
            "number": 1,
            "title": "Synthetic issue",
            "url": "https://github.com/example/repo/issues/1",
        }

        with self.assertRaises(koios_issues.ResponseError):
            koios_issues.normalize_issue_pages([[entry], [entry]])

    def test_graphql_query_pages_only_the_issue_connection(self) -> None:
        first_page = {
            "data": {
                "repository": {
                    "issues": {
                        "totalCount": 2,
                        "nodes": [
                            {
                                "number": 1,
                                "title": "First synthetic issue",
                                "url": "https://github.com/example/projectkoios/issues/1",
                            }
                        ],
                        "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                    }
                }
            }
        }
        second_page = {
            "data": {
                "repository": {
                    "issues": {
                        "totalCount": 2,
                        "nodes": [
                            {
                                "number": 2,
                                "title": "Second synthetic issue",
                                "url": "https://github.com/example/projectkoios/issues/2",
                            }
                        ],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            }
        }
        runner = SequenceRunner([json.dumps(first_page), json.dumps(second_page)])
        identity = koios_issues.GitHubIdentity("github.com", "example", "projectkoios")

        result = koios_issues.query_open_issues(identity, runner)

        self.assertIsInstance(result, tuple)
        assert isinstance(result, tuple)
        self.assertEqual([issue.number for issue in result], [1, 2])
        self.assertEqual(len(runner.calls), 2)
        self.assertIn("graphql", runner.calls[0])
        self.assertTrue(any("issues(" in argument for argument in runner.calls[0]))
        self.assertFalse(
            any("pullRequests" in argument for argument in runner.calls[0])
        )
        self.assertIn("endCursor=cursor-1", runner.calls[1])

    def test_malformed_live_response_is_not_treated_as_zero(self) -> None:
        identity = koios_issues.GitHubIdentity("github.com", "example", "projectkoios")
        runner = SequenceRunner(['{"not":"a GraphQL response"}'])

        result = koios_issues.query_open_issues(identity, runner)

        self.assertEqual(result, "invalid_response")

    def test_safety_limit_returns_an_incomplete_error(self) -> None:
        oversized_page = {
            "data": {
                "repository": {
                    "issues": {
                        "totalCount": 10_001,
                        "nodes": [],
                        "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                    }
                }
            }
        }
        runner = SequenceRunner([json.dumps(oversized_page)])
        identity = koios_issues.GitHubIdentity("github.com", "example", "projectkoios")

        result = koios_issues.query_open_issues(identity, runner)

        self.assertEqual(result, "limit_exceeded")
        self.assertEqual(len(runner.calls), 1)


class ReplayTests(unittest.TestCase):
    def run_main(self, replay_name: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = koios_issues.main(
            [
                "--map",
                str(FIXTURES / "repositories.md"),
                "--workspace",
                "/unused",
                "--replay",
                str(FIXTURES / replay_name),
                "--json",
            ],
            stdout=stdout,
            stderr=stderr,
        )
        return code, stdout.getvalue(), stderr.getvalue()

    def test_zero_replay_is_complete_without_open_issues(self) -> None:
        code, output, error = self.run_main("zero-replay.json")

        report = json.loads(output)
        self.assertEqual(code, koios_issues.EXIT_COMPLETE)
        self.assertEqual(error, "")
        self.assertTrue(report["complete"])
        self.assertEqual(report["totals"]["known_open_issues"], 0)
        self.assertEqual(
            [item["open_issue_count"] for item in report["repositories"]], [0, 0]
        )

    def test_mixed_replay_is_complete_and_deterministic(self) -> None:
        first = self.run_main("mixed-replay.json")
        second = self.run_main("mixed-replay.json")

        self.assertEqual(first, second)
        code, output, error = first
        report = json.loads(output)
        self.assertEqual(code, koios_issues.EXIT_COMPLETE)
        self.assertEqual(error, "")
        self.assertTrue(report["complete"])
        self.assertEqual(report["source_mode"], "replay")
        self.assertEqual(report["totals"]["known_open_issues"], 2)
        self.assertEqual(report["repositories"][0]["open_issue_count"], 2)
        self.assertEqual(
            [issue["number"] for issue in report["repositories"][0]["issues"]],
            [1, 2],
        )

    def test_partial_replay_returns_incomplete_exit_and_nullable_count(self) -> None:
        code, output, error = self.run_main("partial-replay.json")

        report = json.loads(output)
        self.assertEqual(code, koios_issues.EXIT_INCOMPLETE)
        self.assertEqual(error, "")
        self.assertFalse(report["complete"])
        self.assertEqual(report["totals"]["known_open_issues"], 1)
        self.assertEqual(report["totals"]["failed"], 1)
        failed = report["repositories"][1]
        self.assertEqual(failed["status"], "error")
        self.assertEqual(failed["error_kind"], "auth_failed")
        self.assertIsNone(failed["open_issue_count"])

    def test_replay_must_exactly_cover_the_map(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            replay = Path(directory) / "incomplete.json"
            replay.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "observed_at": "2026-01-02T03:04:05Z",
                        "repositories": [],
                    }
                ),
                encoding="utf-8",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()

            code = koios_issues.main(
                [
                    "--map",
                    str(FIXTURES / "repositories.md"),
                    "--replay",
                    str(replay),
                    "--json",
                ],
                stdout=stdout,
                stderr=stderr,
            )

        self.assertEqual(code, koios_issues.EXIT_SETUP_ERROR)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("replay_invalid", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
