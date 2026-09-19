from __future__ import annotations

import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from typing import Sequence

from scripts import koios_issues


FIXTURES = Path(__file__).parent / "fixtures" / "issues"
EXAMPLE_IDENTITY = koios_issues.GitHubIdentity("github.com", "example", "repo")
PROJECTKOIOS_IDENTITY = koios_issues.GitHubIdentity(
    "github.com", "example", "projectkoios"
)


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
        self.assertEqual(specs[1].identity.slug, "example/projectkoios-bootstrap")
        self.assertEqual(specs[1].identity.host, "github.com")

    def test_rejects_duplicate_repository_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            map_path = Path(directory) / "repositories.md"
            map_path.write_text(
                "| Repository | GitHub identity | Coordination purpose |\n"
                "|---|---|---|\n"
                "| `duplicate` | `github.com/example/duplicate` | one |\n"
                "| `duplicate` | `github.com/example/duplicate` | two |\n",
                encoding="utf-8",
            )

            with self.assertRaises(koios_issues.SetupError) as raised:
                koios_issues.parse_repository_map(map_path, Path(directory))

        self.assertEqual(raised.exception.kind, "map_invalid")

    def test_rejects_malformed_row_instead_of_silently_omitting_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            map_path = Path(directory) / "repositories.md"
            map_path.write_text(
                "| Repository | GitHub identity | Coordination purpose |\n"
                "|---|---|---|\n"
                "| `projectkoios` | `github.com/example/projectkoios` | valid |\n"
                "| projectkoios-missing-backticks | `github.com/example/projectkoios-missing-backticks` | invalid |\n",
                encoding="utf-8",
            )

            with self.assertRaises(koios_issues.SetupError) as raised:
                koios_issues.parse_repository_map(map_path, Path(directory))

        self.assertEqual(raised.exception.kind, "map_invalid")

    def test_rejects_map_identity_that_does_not_match_repository_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            map_path = Path(directory) / "repositories.md"
            map_path.write_text(
                "| Repository | GitHub identity | Coordination purpose |\n"
                "|---|---|---|\n"
                "| `projectkoios` | `github.com/example/another-repository` | invalid |\n",
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
        spec = koios_issues.RepositorySpec(
            "projectkoios", Path("/does-not-exist"), PROJECTKOIOS_IDENTITY
        )

        result = koios_issues.resolve_repository(spec)

        self.assertIsInstance(result, koios_issues.RepositoryResult)
        assert isinstance(result, koios_issues.RepositoryResult)
        self.assertEqual(result.error_kind, "missing_checkout")
        self.assertEqual(result.identity, PROJECTKOIOS_IDENTITY)

    def test_missing_origin_is_an_explicit_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            spec = koios_issues.RepositorySpec(
                "projectkoios", Path(directory), PROJECTKOIOS_IDENTITY
            )
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
            spec = koios_issues.RepositorySpec(
                "projectkoios", Path(directory), PROJECTKOIOS_IDENTITY
            )
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
        self.assertEqual(result.identity, PROJECTKOIOS_IDENTITY)

    def test_same_name_origin_under_wrong_owner_is_a_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            spec = koios_issues.RepositorySpec(
                "projectkoios", Path(directory), PROJECTKOIOS_IDENTITY
            )
            command = ("git", "-C", directory, "remote", "get-url", "origin")
            runner = FakeRunner(
                {
                    command: completed(
                        command,
                        stdout="https://github.com/other-owner/projectkoios.git\n",
                    )
                }
            )

            result = koios_issues.resolve_repository(spec, runner)

        self.assertIsInstance(result, koios_issues.RepositoryResult)
        assert isinstance(result, koios_issues.RepositoryResult)
        self.assertEqual(result.error_kind, "remote_mismatch")
        self.assertEqual(result.identity, PROJECTKOIOS_IDENTITY)


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

        issues = koios_issues.normalize_issue_pages(pages, EXAMPLE_IDENTITY)

        self.assertEqual([issue.number for issue in issues], [1, 4])
        self.assertEqual(issues[1].title, "Fourth synthetic issue")

    def test_rejects_duplicate_issue_across_pages(self) -> None:
        entry = {
            "number": 1,
            "title": "Synthetic issue",
            "url": "https://github.com/example/repo/issues/1",
        }

        with self.assertRaises(koios_issues.ResponseError):
            koios_issues.normalize_issue_pages([[entry], [entry]], EXAMPLE_IDENTITY)

    def test_rejects_issue_url_outside_resolved_repository(self) -> None:
        base = {
            "number": 1,
            "title": "Synthetic issue",
        }
        unsafe_urls = (
            "http://github.com/example/repo/issues/1",
            "https://github.com/example/other/issues/1",
            "https://github.com/example/repo/issues/2",
            "https://github.com/example/repo/issues/1#fragment",
            "https://user@github.com/example/repo/issues/1",
            "https://github.com:invalid/example/repo/issues/1",
            "https://[broken/example/repo/issues/1",
            "https://github.com/example/repo/issues/1\nInjected",
        )

        for url in unsafe_urls:
            with self.subTest(url=url), self.assertRaises(koios_issues.ResponseError):
                koios_issues.normalize_issue_pages(
                    [[{**base, "url": url}]], EXAMPLE_IDENTITY
                )

    def test_issue_url_is_reconstructed_from_validated_identity(self) -> None:
        issues = koios_issues.normalize_issue_pages(
            [
                [
                    {
                        "number": 1,
                        "title": "Synthetic issue",
                        "url": "https://GITHUB.COM/EXAMPLE/REPO/issues/1",
                    }
                ]
            ],
            EXAMPLE_IDENTITY,
        )

        self.assertEqual(issues[0].url, "https://github.com/example/repo/issues/1")

    def test_issue_pages_enforce_exact_fields_and_resource_bounds(self) -> None:
        issue = {
            "number": 1,
            "title": "Synthetic issue",
            "url": "https://github.com/example/repo/issues/1",
        }
        invalid_pages: tuple[list[list[dict[str, object]]], ...] = (
            [],
            [[{**issue, "extra": True}]],
            [[{**issue, "title": "x" * (koios_issues.MAX_TITLE_BYTES + 1)}]],
            [[issue] * (koios_issues.PAGE_SIZE + 1)],
            [[] for _ in range(koios_issues.MAX_PAGES + 1)],
        )

        for pages in invalid_pages:
            with (
                self.subTest(size=len(pages)),
                self.assertRaises(koios_issues.ResponseError),
            ):
                koios_issues.normalize_issue_pages(pages, EXAMPLE_IDENTITY)

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

    def test_pagination_invariants_fail_closed_with_bounded_calls(self) -> None:
        def page(
            *, total: int, numbers: list[int], has_next: bool, cursor: str | None
        ) -> str:
            return json.dumps(
                {
                    "data": {
                        "repository": {
                            "issues": {
                                "totalCount": total,
                                "nodes": [
                                    {
                                        "number": number,
                                        "title": f"Issue {number}",
                                        "url": f"https://github.com/example/projectkoios/issues/{number}",
                                    }
                                    for number in numbers
                                ],
                                "pageInfo": {
                                    "hasNextPage": has_next,
                                    "endCursor": cursor,
                                },
                            }
                        }
                    }
                }
            )

        scenarios = (
            ([page(total=1, numbers=[], has_next=True, cursor="next")], 1),
            ([page(total=1, numbers=[1], has_next=True, cursor="next")], 1),
            ([page(total=0, numbers=[1], has_next=False, cursor=None)], 1),
            (
                [
                    page(total=2, numbers=[1], has_next=True, cursor="next"),
                    page(total=3, numbers=[2], has_next=False, cursor=None),
                ],
                2,
            ),
            ([page(total=2, numbers=[1], has_next=False, cursor=None)], 1),
        )
        identity = koios_issues.GitHubIdentity("github.com", "example", "projectkoios")

        for responses, expected_calls in scenarios:
            with self.subTest(responses=responses):
                runner = SequenceRunner(responses)
                result = koios_issues.query_open_issues(identity, runner)
                self.assertEqual(result, "inconsistent_response")
                self.assertEqual(len(runner.calls), expected_calls)

    def test_repeated_pagination_cursor_is_inconsistent(self) -> None:
        page = {
            "data": {
                "repository": {
                    "issues": {
                        "totalCount": 3,
                        "nodes": [
                            {
                                "number": 1,
                                "title": "Synthetic issue",
                                "url": "https://github.com/example/projectkoios/issues/1",
                            }
                        ],
                        "pageInfo": {"hasNextPage": True, "endCursor": "cycle"},
                    }
                }
            }
        }
        runner = SequenceRunner([json.dumps(page), json.dumps(page)])
        identity = koios_issues.GitHubIdentity("github.com", "example", "projectkoios")

        result = koios_issues.query_open_issues(identity, runner)

        self.assertEqual(result, "inconsistent_response")
        self.assertEqual(len(runner.calls), 2)

    def test_duplicate_json_field_is_not_treated_as_zero(self) -> None:
        runner = SequenceRunner(['{"data":null,"data":null}'])
        identity = koios_issues.GitHubIdentity("github.com", "example", "projectkoios")

        result = koios_issues.query_open_issues(identity, runner)

        self.assertEqual(result, "invalid_response")

    def test_malformed_live_response_is_not_treated_as_zero(self) -> None:
        identity = koios_issues.GitHubIdentity("github.com", "example", "projectkoios")
        malformed_responses = (
            '{"not":"a GraphQL response"}',
            "[" * 2_000 + "0" + "]" * 2_000,
        )

        for response in malformed_responses:
            with self.subTest(response=response[:40]):
                result = koios_issues.query_open_issues(
                    identity, SequenceRunner([response])
                )
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

    def test_replay_rejects_boolean_schema_duplicate_fields_and_bad_time(self) -> None:
        specs = koios_issues.parse_repository_map(
            FIXTURES / "repositories.md", Path("/unused")
        )
        valid = json.loads((FIXTURES / "zero-replay.json").read_text(encoding="utf-8"))
        partial = json.loads(
            (FIXTURES / "partial-replay.json").read_text(encoding="utf-8")
        )
        invalid_error_kind = json.loads(json.dumps(partial))
        invalid_error_kind["repositories"][1]["error_kind"] = []
        unknown_repository_field = json.loads(json.dumps(valid))
        unknown_repository_field["repositories"][0]["errorKind"] = "api_failed"
        unknown_issue_field = json.loads(
            (FIXTURES / "mixed-replay.json").read_text(encoding="utf-8")
        )
        unknown_issue_field["repositories"][0]["pages"][0][0]["extra"] = True
        documents = [
            json.dumps({**valid, "schema_version": True}),
            json.dumps({**valid, "unknown": True}),
            json.dumps(invalid_error_kind),
            json.dumps(unknown_repository_field),
            json.dumps(unknown_issue_field),
            (FIXTURES / "zero-replay.json")
            .read_text(encoding="utf-8")
            .replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1'),
            json.dumps({**valid, "observed_at": "not-a-time\nInjected"}),
        ]

        for document in documents:
            with (
                self.subTest(document=document[:40]),
                tempfile.TemporaryDirectory() as directory,
            ):
                replay = Path(directory) / "replay.json"
                replay.write_text(document, encoding="utf-8")
                with self.assertRaises(koios_issues.SetupError) as raised:
                    koios_issues.load_replay(replay, specs)
                self.assertEqual(raised.exception.kind, "replay_invalid")

    def test_replay_diagnostic_does_not_echo_untrusted_repository_name(self) -> None:
        unsafe_name = "spoof\n\x1b[31m\u202e"
        valid = json.loads((FIXTURES / "zero-replay.json").read_text(encoding="utf-8"))
        valid["repositories"] = [
            {**valid["repositories"][0], "repository": unsafe_name},
            {**valid["repositories"][1], "repository": unsafe_name},
        ]
        with tempfile.TemporaryDirectory() as directory:
            replay = Path(directory) / "replay.json"
            replay.write_text(json.dumps(valid), encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            code = koios_issues.main(
                [
                    "--map",
                    str(FIXTURES / "repositories.md"),
                    "--replay",
                    str(replay),
                ],
                stdout=stdout,
                stderr=stderr,
            )

        self.assertEqual(code, koios_issues.EXIT_SETUP_ERROR)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("duplicate replay repository entry", stderr.getvalue())
        self.assertNotIn(unsafe_name, stderr.getvalue())
        self.assertNotIn("\x1b", stderr.getvalue())

    def test_deep_replay_and_invalid_utf8_map_use_setup_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            replay = root / "deep.json"
            replay.write_text("[" * 2_000 + "0" + "]" * 2_000, encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            replay_code = koios_issues.main(
                [
                    "--map",
                    str(FIXTURES / "repositories.md"),
                    "--replay",
                    str(replay),
                ],
                stdout=stdout,
                stderr=stderr,
            )

            invalid_map = root / "repositories.md"
            invalid_map.write_bytes(b"\xff\xfe")
            map_stderr = io.StringIO()
            map_code = koios_issues.main(
                ["--map", str(invalid_map), "--replay", str(replay)],
                stdout=io.StringIO(),
                stderr=map_stderr,
            )

        self.assertEqual(replay_code, koios_issues.EXIT_SETUP_ERROR)
        self.assertIn("replay_invalid", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())
        self.assertEqual(map_code, koios_issues.EXIT_SETUP_ERROR)
        self.assertIn("map_invalid", map_stderr.getvalue())
        self.assertNotIn("Traceback", map_stderr.getvalue())

    def test_replay_file_byte_limit_fails_closed(self) -> None:
        specs = koios_issues.parse_repository_map(
            FIXTURES / "repositories.md", Path("/unused")
        )
        with tempfile.TemporaryDirectory() as directory:
            replay = Path(directory) / "replay.json"
            replay.write_text("{}", encoding="utf-8")
            with mock.patch.object(koios_issues, "MAX_REPLAY_BYTES", 1):
                with self.assertRaises(koios_issues.SetupError) as raised:
                    koios_issues.load_replay(replay, specs)

        self.assertEqual(raised.exception.kind, "replay_invalid")

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


class TextReportTests(unittest.TestCase):
    def test_summary_points_to_details_without_hiding_completeness(self) -> None:
        result = koios_issues.RepositoryResult.ok(
            "repo",
            EXAMPLE_IDENTITY,
            [
                koios_issues.Issue(
                    1, "Synthetic issue", "https://github.com/example/repo/issues/1"
                )
            ],
        )
        report = koios_issues.build_report("2026-01-02T03:04:05Z", "live", [result])

        summary = koios_issues.render_text(report)
        details = koios_issues.render_text(report, details=True)

        self.assertIn("Observed (collection start; non-atomic):", summary)
        self.assertIn("Inventory: COMPLETE", summary)
        self.assertIn("rerun with --details", summary)
        self.assertNotIn("#1 Synthetic issue", summary)
        self.assertIn("#1 Synthetic issue", details)
        self.assertNotIn("rerun with --details", details)


if __name__ == "__main__":
    unittest.main()
