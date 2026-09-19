#!/usr/bin/env python3
"""Read-only open-issue inventory for mapped Project Koios repositories.

This is an observed, unvalidated harness candidate. GitHub remains authoritative;
the command does not record or cache issue state.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence, TextIO
from urllib.parse import urlparse

SCHEMA_VERSION = 1
EXIT_COMPLETE = 0
EXIT_SETUP_ERROR = 2
EXIT_INCOMPLETE = 3

MAP_HEADER_PATTERN = re.compile(
    r"^\|\s*Repository\s*\|\s*GitHub identity\s*\|"
    r"\s*Coordination purpose\s*\|\s*$",
    re.IGNORECASE,
)
MAP_SEPARATOR_PATTERN = re.compile(
    r"^\|\s*:?-{3,}:?\s*\|\s*:?-{3,}:?\s*\|\s*:?-{3,}:?\s*\|\s*$"
)
MAP_ROW_PATTERN = re.compile(
    r"^\|\s*`(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)`\s*\|"
    r"\s*`(?P<host>[A-Za-z0-9.-]+)/(?P<owner>[A-Za-z0-9_.-]+)/"
    r"(?P<repository>[A-Za-z0-9_.-]+)`\s*\|[^|]+\|\s*$"
)
SCP_REMOTE_PATTERN = re.compile(
    r"^(?:[^@/\s]+@)?(?P<host>[A-Za-z0-9.-]+):"
    r"(?P<owner>[A-Za-z0-9_.-]+)/(?P<repository>[A-Za-z0-9_.-]+?)(?:\.git)?$"
)
GITHUB_COMPONENT_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")
OBSERVED_AT_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PAGE_SIZE = 100
MAX_OPEN_ISSUES_PER_REPOSITORY = 10_000
MAX_PAGES = MAX_OPEN_ISSUES_PER_REPOSITORY // PAGE_SIZE
MAX_REPLAY_BYTES = 16 * 1024 * 1024
MAX_TITLE_BYTES = 1_024
MAX_URL_BYTES = 2_048
REPLAY_TOP_LEVEL_FIELDS = frozenset({"observed_at", "repositories", "schema_version"})
REPLAY_REPOSITORY_FIELDS = frozenset({"github_host", "github_repository", "repository"})
ISSUE_FIELDS = frozenset({"number", "title", "url"})
ISSUES_QUERY = """
query($endCursor: String, $owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    issues(
      first: 100
      after: $endCursor
      states: OPEN
      orderBy: {field: CREATED_AT, direction: ASC}
    ) {
      totalCount
      nodes { number title url }
      pageInfo { hasNextPage endCursor }
    }
  }
}
""".strip()

ERROR_KINDS = frozenset(
    {
        "api_failed",
        "auth_failed",
        "command_timeout",
        "gh_unavailable",
        "inconsistent_response",
        "invalid_response",
        "limit_exceeded",
        "missing_checkout",
        "missing_origin",
        "rate_limited",
        "remote_mismatch",
        "repository_not_found",
        "unsupported_remote",
    }
)

CommandRunner = Callable[[Sequence[str], float], subprocess.CompletedProcess[str]]


class SetupError(Exception):
    """A fatal local or replay configuration error."""

    def __init__(self, kind: str, message: str) -> None:
        super().__init__(message)
        self.kind = kind


class ResponseError(Exception):
    """A malformed GitHub response."""


@dataclass(frozen=True)
class RepositorySpec:
    name: str
    path: Path
    identity: GitHubIdentity


@dataclass(frozen=True)
class GitHubIdentity:
    host: str
    owner: str
    repository: str

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.repository}"


@dataclass(frozen=True)
class Issue:
    number: int
    title: str
    url: str


@dataclass(frozen=True)
class RepositoryResult:
    repository: str
    identity: GitHubIdentity | None
    status: str
    issues: tuple[Issue, ...] = ()
    error_kind: str | None = None

    @classmethod
    def ok(
        cls,
        repository: str,
        identity: GitHubIdentity,
        issues: Sequence[Issue],
    ) -> RepositoryResult:
        return cls(repository, identity, "ok", tuple(issues), None)

    @classmethod
    def error(
        cls,
        repository: str,
        error_kind: str,
        identity: GitHubIdentity | None = None,
    ) -> RepositoryResult:
        if error_kind not in ERROR_KINDS:
            raise ValueError(f"unsupported error kind: {error_kind}")
        return cls(repository, identity, "error", (), error_kind)


def default_runner(
    args: Sequence[str], timeout: float
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        capture_output=True,
        check=False,
        text=True,
        timeout=timeout,
    )


def observed_at_now() -> str:
    value = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return value.replace("+00:00", "Z")


def validate_observed_at(value: Any) -> str:
    if not isinstance(value, str) or OBSERVED_AT_PATTERN.fullmatch(value) is None:
        raise ValueError("observation time must be canonical UTC")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValueError("observation time is invalid") from exc
    return value


def _object_without_duplicate_fields(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ResponseError(f"duplicate JSON field: {key}")
        value[key] = item
    return value


def parse_json_document(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_object_without_duplicate_fields)


def read_bounded_utf8(path: Path, byte_limit: int) -> str:
    try:
        with path.open("rb") as stream:
            raw = stream.read(byte_limit + 1)
    except OSError as exc:
        raise SetupError("replay_unreadable", f"cannot read {path}") from exc
    if len(raw) > byte_limit:
        raise SetupError("replay_invalid", "replay file exceeds its byte limit")
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SetupError("replay_invalid", "replay file is not UTF-8") from exc


def require_exact_fields(value: dict[str, Any], expected: frozenset[str]) -> None:
    if set(value) != expected:
        raise ResponseError("object contains missing or unknown fields")


def utf8_length(value: str, field: str) -> int:
    try:
        return len(value.encode("utf-8", errors="strict"))
    except UnicodeEncodeError as exc:
        raise ResponseError(f"{field} is not valid UTF-8") from exc


def parse_repository_map(map_path: Path, workspace: Path) -> list[RepositorySpec]:
    try:
        text = map_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SetupError("map_unreadable", f"cannot read {map_path}") from exc
    except UnicodeDecodeError as exc:
        raise SetupError("map_invalid", "repository map is not UTF-8") from exc

    lines = text.splitlines()
    header_index = next(
        (index for index, line in enumerate(lines) if MAP_HEADER_PATTERN.match(line)),
        None,
    )
    if header_index is None or header_index + 1 >= len(lines):
        raise SetupError("map_invalid", "repository map table is missing")
    if not MAP_SEPARATOR_PATTERN.match(lines[header_index + 1]):
        raise SetupError("map_invalid", "repository map table separator is invalid")

    specs: list[RepositorySpec] = []
    seen_names: set[str] = set()
    seen_identities: set[tuple[str, str, str]] = set()
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        match = MAP_ROW_PATTERN.match(line)
        if match is None:
            raise SetupError("map_invalid", "repository map contains an invalid row")
        name = match.group("name")
        try:
            identity = _validated_identity(
                match.group("host"),
                match.group("owner"),
                match.group("repository"),
            )
        except ValueError as exc:
            raise SetupError(
                "map_invalid", f"invalid GitHub identity for {name}"
            ) from exc
        if identity.repository.casefold() != name.casefold():
            raise SetupError("map_invalid", f"GitHub repository mismatch for {name}")
        identity_key = (
            identity.host.casefold(),
            identity.owner.casefold(),
            identity.repository.casefold(),
        )
        if name in seen_names:
            raise SetupError("map_invalid", f"duplicate mapped repository: {name}")
        if identity_key in seen_identities:
            raise SetupError(
                "map_invalid", f"duplicate mapped GitHub identity: {identity.slug}"
            )
        specs.append(RepositorySpec(name, workspace / name, identity))
        seen_names.add(name)
        seen_identities.add(identity_key)

    if not specs:
        raise SetupError("map_invalid", "repository map contains no repository rows")

    return specs


def parse_github_remote(remote: str) -> GitHubIdentity:
    value = remote.strip()
    scp_match = SCP_REMOTE_PATTERN.match(value)
    if scp_match is not None and "://" not in value:
        return _validated_identity(
            scp_match.group("host"),
            scp_match.group("owner"),
            scp_match.group("repository"),
        )

    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https", "ssh", "git"} or not parsed.hostname:
        raise ValueError("unsupported GitHub remote URL")

    path_parts = [part for part in parsed.path.split("/") if part]
    if len(path_parts) != 2:
        raise ValueError("GitHub remote must contain exactly owner and repository")
    owner, repository = path_parts
    if repository.endswith(".git"):
        repository = repository[:-4]
    return _validated_identity(parsed.hostname, owner, repository)


def _validated_identity(host: str, owner: str, repository: str) -> GitHubIdentity:
    if not host or "." not in host:
        raise ValueError("invalid GitHub host")
    if not GITHUB_COMPONENT_PATTERN.fullmatch(owner):
        raise ValueError("invalid GitHub owner")
    if not GITHUB_COMPONENT_PATTERN.fullmatch(repository):
        raise ValueError("invalid GitHub repository")
    return GitHubIdentity(host.lower(), owner, repository)


def resolve_repository(
    spec: RepositorySpec, runner: CommandRunner = default_runner
) -> RepositoryResult | GitHubIdentity:
    if not spec.path.is_dir():
        return RepositoryResult.error(spec.name, "missing_checkout", spec.identity)

    try:
        completed = runner(
            ["git", "-C", str(spec.path), "remote", "get-url", "origin"], 10.0
        )
    except FileNotFoundError:
        raise SetupError("git_unavailable", "git executable is unavailable") from None
    except subprocess.TimeoutExpired:
        return RepositoryResult.error(spec.name, "command_timeout", spec.identity)

    if completed.returncode != 0 or not completed.stdout.strip():
        return RepositoryResult.error(spec.name, "missing_origin", spec.identity)

    try:
        identity = parse_github_remote(completed.stdout)
    except ValueError:
        return RepositoryResult.error(spec.name, "unsupported_remote", spec.identity)

    if (
        identity.host.casefold() != spec.identity.host.casefold()
        or identity.owner.casefold() != spec.identity.owner.casefold()
        or identity.repository.casefold() != spec.identity.repository.casefold()
    ):
        return RepositoryResult.error(spec.name, "remote_mismatch", spec.identity)
    return spec.identity


def validate_gh(runner: CommandRunner = default_runner) -> None:
    try:
        version = runner(["gh", "--version"], 10.0)
    except FileNotFoundError:
        raise SetupError("gh_unavailable", "gh executable is unavailable") from None
    except subprocess.TimeoutExpired:
        raise SetupError("gh_unavailable", "gh preflight timed out") from None

    if version.returncode != 0:
        raise SetupError("gh_unavailable", "gh version check failed")


def authenticated_hosts(
    hosts: Sequence[str], runner: CommandRunner = default_runner
) -> dict[str, bool]:
    statuses: dict[str, bool] = {}
    for host in sorted(set(hosts)):
        try:
            completed = runner(["gh", "auth", "status", "--hostname", host], 15.0)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            statuses[host] = False
        else:
            statuses[host] = completed.returncode == 0
    return statuses


def classify_gh_failure(stderr: str) -> str:
    lowered = stderr.casefold()
    if "rate limit" in lowered or "http 403" in lowered:
        return "rate_limited"
    if (
        "http 401" in lowered
        or "authentication" in lowered
        or "gh auth login" in lowered
    ):
        return "auth_failed"
    if "http 404" in lowered or "not found" in lowered:
        return "repository_not_found"
    return "api_failed"


def query_open_issues(
    identity: GitHubIdentity, runner: CommandRunner = default_runner
) -> tuple[Issue, ...] | str:
    pages: list[list[dict[str, Any]]] = []
    expected_total: int | None = None
    cursor: str | None = None
    seen_cursors: set[str] = set()
    received = 0

    for _ in range(MAX_PAGES):
        args = [
            "gh",
            "api",
            "graphql",
            "--hostname",
            identity.host,
            "-f",
            f"owner={identity.owner}",
            "-f",
            f"name={identity.repository}",
            "-f",
            f"query={ISSUES_QUERY}",
        ]
        if cursor is not None:
            args.extend(["-f", f"endCursor={cursor}"])

        try:
            completed = runner(args, 60.0)
        except FileNotFoundError:
            return "gh_unavailable"
        except subprocess.TimeoutExpired:
            return "command_timeout"

        if completed.returncode != 0:
            return classify_gh_failure(completed.stderr)

        try:
            payload = parse_json_document(completed.stdout)
            nodes, total, next_cursor = normalize_graphql_page(payload)
        except (json.JSONDecodeError, RecursionError, ResponseError):
            return "invalid_response"

        if expected_total is None:
            expected_total = total
            if expected_total > MAX_OPEN_ISSUES_PER_REPOSITORY:
                return "limit_exceeded"
        elif total != expected_total:
            return "inconsistent_response"

        received += len(nodes)
        if received > expected_total:
            return "inconsistent_response"
        if next_cursor is not None:
            if not nodes or received >= expected_total or next_cursor in seen_cursors:
                return "inconsistent_response"
            seen_cursors.add(next_cursor)
        pages.append(nodes)
        cursor = next_cursor

        if cursor is None:
            try:
                issues = normalize_issue_pages(pages, identity)
            except ResponseError:
                return "invalid_response"
            if len(issues) != expected_total:
                return "inconsistent_response"
            return issues

    return "limit_exceeded"


def normalize_graphql_page(
    payload: Any,
) -> tuple[list[dict[str, Any]], int, str | None]:
    if not isinstance(payload, dict) or payload.get("errors"):
        raise ResponseError("GraphQL response contains errors")
    data = payload.get("data")
    repository = data.get("repository") if isinstance(data, dict) else None
    connection = repository.get("issues") if isinstance(repository, dict) else None
    if not isinstance(connection, dict):
        raise ResponseError("GraphQL response has no issue connection")

    nodes = connection.get("nodes")
    total = connection.get("totalCount")
    page_info = connection.get("pageInfo")
    if (
        not isinstance(nodes, list)
        or not isinstance(total, int)
        or isinstance(total, bool)
        or total < 0
        or not isinstance(page_info, dict)
    ):
        raise ResponseError("GraphQL issue connection is malformed")

    has_next = page_info.get("hasNextPage")
    end_cursor = page_info.get("endCursor")
    if not isinstance(has_next, bool):
        raise ResponseError("GraphQL page information is malformed")
    if has_next and (not isinstance(end_cursor, str) or not end_cursor):
        raise ResponseError("GraphQL next page has no cursor")
    if not has_next:
        end_cursor = None
    return nodes, total, end_cursor


def normalize_issue_pages(pages: Any, identity: GitHubIdentity) -> tuple[Issue, ...]:
    if (
        not isinstance(pages, list)
        or not 1 <= len(pages) <= MAX_PAGES
        or any(not isinstance(page, list) or len(page) > PAGE_SIZE for page in pages)
    ):
        raise ResponseError("paginated response exceeds page bounds")

    issues: dict[int, Issue] = {}
    for page in pages:
        for item in page:
            if not isinstance(item, dict):
                raise ResponseError("issue entry must be an object")
            require_exact_fields(item, ISSUE_FIELDS)
            number = item.get("number")
            title = item.get("title")
            url = item.get("url")
            if (
                not isinstance(number, int)
                or isinstance(number, bool)
                or number <= 0
                or not isinstance(title, str)
                or utf8_length(title, "issue title") > MAX_TITLE_BYTES
                or not isinstance(url, str)
                or utf8_length(url, "issue URL") > MAX_URL_BYTES
            ):
                raise ResponseError("issue entry has invalid required fields")
            if number in issues:
                raise ResponseError("duplicate issue number across pages")
            validated_url = validate_issue_url(url, identity, number)
            issues[number] = Issue(number, safe_title(title), validated_url)

    return tuple(issues[number] for number in sorted(issues))


def validate_issue_url(value: str, identity: GitHubIdentity, issue_number: int) -> str:
    if any(unicodedata.category(character).startswith("C") for character in value):
        raise ResponseError("issue URL contains control or format characters")
    expected_path = f"/{identity.owner}/{identity.repository}/issues/{issue_number}"
    try:
        parsed = urlparse(value)
        valid = (
            parsed.scheme == "https"
            and parsed.hostname is not None
            and parsed.hostname.casefold() == identity.host.casefold()
            and parsed.username is None
            and parsed.password is None
            and parsed.port is None
            and parsed.path.casefold() == expected_path.casefold()
            and not parsed.params
            and not parsed.query
            and not parsed.fragment
        )
    except ValueError as exc:
        raise ResponseError("issue URL is malformed") from exc
    if not valid:
        raise ResponseError("issue URL does not match its GitHub identity")
    return f"https://{identity.host}{expected_path}"


def safe_title(title: str) -> str:
    cleaned = "".join(
        " " if unicodedata.category(character).startswith("C") else character
        for character in title
    )
    return " ".join(cleaned.split())


def collect_live(
    specs: Sequence[RepositorySpec],
    runner: CommandRunner = default_runner,
) -> list[RepositoryResult]:
    validate_gh(runner)

    resolved: list[RepositoryResult | GitHubIdentity] = [
        resolve_repository(spec, runner) for spec in specs
    ]
    hosts = [item.host for item in resolved if isinstance(item, GitHubIdentity)]
    auth = authenticated_hosts(hosts, runner)

    results: list[RepositoryResult] = []
    for spec, resolution in zip(specs, resolved, strict=True):
        if isinstance(resolution, RepositoryResult):
            results.append(resolution)
            continue
        if not auth.get(resolution.host, False):
            results.append(RepositoryResult.error(spec.name, "auth_failed", resolution))
            continue
        queried = query_open_issues(resolution, runner)
        if isinstance(queried, str):
            results.append(RepositoryResult.error(spec.name, queried, resolution))
        else:
            results.append(RepositoryResult.ok(spec.name, resolution, queried))
    return results


def load_replay(
    replay_path: Path, specs: Sequence[RepositorySpec]
) -> tuple[str, list[RepositoryResult]]:
    try:
        payload = parse_json_document(read_bounded_utf8(replay_path, MAX_REPLAY_BYTES))
    except (json.JSONDecodeError, RecursionError, ResponseError) as exc:
        raise SetupError("replay_invalid", "replay file is not valid JSON") from exc

    if not isinstance(payload, dict):
        raise SetupError("replay_invalid", "replay must be a JSON object")
    try:
        require_exact_fields(payload, REPLAY_TOP_LEVEL_FIELDS)
    except ResponseError as exc:
        raise SetupError("replay_invalid", "invalid replay top-level fields") from exc
    if (
        type(payload.get("schema_version")) is not int
        or payload.get("schema_version") != SCHEMA_VERSION
    ):
        raise SetupError("replay_invalid", "unsupported replay schema")
    observed_at = payload.get("observed_at")
    entries = payload.get("repositories")
    try:
        observed_at = validate_observed_at(observed_at)
    except ValueError as exc:
        raise SetupError("replay_invalid", "replay observed_at is invalid") from exc
    if not isinstance(entries, list):
        raise SetupError("replay_invalid", "replay repositories must be a list")

    by_name: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("repository"), str):
            raise SetupError("replay_invalid", "invalid replay repository entry")
        name = entry["repository"]
        if name in by_name:
            raise SetupError("replay_invalid", "duplicate replay repository entry")
        by_name[name] = entry

    expected = [spec.name for spec in specs]
    if set(by_name) != set(expected):
        raise SetupError(
            "replay_invalid",
            "replay repositories must exactly match the repository map",
        )

    results: list[RepositoryResult] = []
    for spec in specs:
        name = spec.name
        entry = by_name[name]
        has_pages = "pages" in entry
        has_error = "error_kind" in entry
        if has_pages == has_error:
            raise SetupError(
                "replay_invalid",
                f"{name} must contain exactly one of pages or error_kind",
            )
        expected_fields = REPLAY_REPOSITORY_FIELDS | frozenset(
            {"pages" if has_pages else "error_kind"}
        )
        try:
            require_exact_fields(entry, expected_fields)
        except ResponseError as exc:
            raise SetupError(
                "replay_invalid", f"invalid replay fields for {name}"
            ) from exc
        identity = _replay_identity(entry, spec)
        if has_error:
            error_kind = entry["error_kind"]
            if not isinstance(error_kind, str) or error_kind not in ERROR_KINDS:
                raise SetupError("replay_invalid", f"invalid error kind for {name}")
            results.append(RepositoryResult.error(name, error_kind, identity))
            continue
        try:
            issues = normalize_issue_pages(entry["pages"], identity)
        except ResponseError as exc:
            raise SetupError(
                "replay_invalid", f"invalid replay response for {name}"
            ) from exc
        results.append(RepositoryResult.ok(name, identity, issues))

    return observed_at, results


def _replay_identity(
    entry: dict[str, Any], expected_spec: RepositorySpec
) -> GitHubIdentity:
    host = entry.get("github_host")
    slug = entry.get("github_repository")
    if not isinstance(host, str) or not isinstance(slug, str):
        raise SetupError(
            "replay_invalid", f"missing GitHub identity for {expected_spec.name}"
        )
    parts = slug.split("/")
    if len(parts) != 2:
        raise SetupError(
            "replay_invalid", f"invalid GitHub slug for {expected_spec.name}"
        )
    try:
        identity = _validated_identity(host, parts[0], parts[1])
    except ValueError as exc:
        raise SetupError(
            "replay_invalid", f"invalid GitHub identity for {expected_spec.name}"
        ) from exc
    if (
        identity.host.casefold() != expected_spec.identity.host.casefold()
        or identity.owner.casefold() != expected_spec.identity.owner.casefold()
        or identity.repository.casefold()
        != expected_spec.identity.repository.casefold()
    ):
        raise SetupError(
            "replay_invalid",
            f"GitHub identity mismatch for {expected_spec.name}",
        )
    return expected_spec.identity


def build_report(
    observed_at: str,
    source_mode: str,
    results: Sequence[RepositoryResult],
) -> dict[str, Any]:
    successful = sum(result.status == "ok" for result in results)
    failed = len(results) - successful
    open_issues = sum(len(result.issues) for result in results if result.status == "ok")

    repositories: list[dict[str, Any]] = []
    for result in results:
        repositories.append(
            {
                "error_kind": result.error_kind,
                "github_host": result.identity.host if result.identity else None,
                "github_repository": result.identity.slug if result.identity else None,
                "issues": [
                    {"number": issue.number, "title": issue.title, "url": issue.url}
                    for issue in result.issues
                ],
                "open_issue_count": (
                    len(result.issues) if result.status == "ok" else None
                ),
                "repository": result.repository,
                "status": result.status,
            }
        )

    return {
        "complete": failed == 0,
        "observed_at": observed_at,
        "repositories": repositories,
        "schema_version": SCHEMA_VERSION,
        "source_mode": source_mode,
        "totals": {
            "failed": failed,
            "known_open_issues": open_issues,
            "repositories": len(results),
            "successful": successful,
        },
    }


def render_text(report: dict[str, Any], details: bool = False) -> str:
    lines = [
        "Project Koios open issue inventory",
        f"Observed (collection start; non-atomic): {report['observed_at']}",
        f"Source: {str(report['source_mode']).upper()}",
    ]
    if report["source_mode"] == "replay":
        lines.append("Warning: replay data is not current GitHub state.")
    lines.extend(["", "Repository                         Open  Status"])

    for repository in report["repositories"]:
        count = (
            str(repository["open_issue_count"])
            if repository["open_issue_count"] is not None
            else "?"
        )
        status = (
            "OK"
            if repository["status"] == "ok"
            else f"ERROR ({repository['error_kind']})"
        )
        lines.append(f"{repository['repository']:<34} {count:>4}  {status}")

    totals = report["totals"]
    lines.extend(
        [
            "",
            f"Known open issues: {totals['known_open_issues']}",
            f"Coverage: {totals['successful']}/{totals['repositories']} repositories",
            f"Inventory: {'COMPLETE' if report['complete'] else 'INCOMPLETE'}",
        ]
    )

    if not details and totals["known_open_issues"]:
        lines.append(
            "Issue details omitted; rerun with --details to list titles and URLs."
        )

    if details:
        lines.append("")
        lines.append("Issues")
        for repository in report["repositories"]:
            if repository["status"] != "ok" or not repository["issues"]:
                continue
            lines.append(f"\n{repository['repository']}")
            for issue in repository["issues"]:
                lines.append(f"  #{issue['number']} {issue['title']}")
                lines.append(f"     {issue['url']}")

    return "\n".join(lines)


def build_parser(repo_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory open issues across mapped Project Koios repositories."
    )
    parser.add_argument(
        "--map",
        dest="map_path",
        type=Path,
        default=repo_root / "maps" / "repositories.md",
        help="repository map (default: maps/repositories.md)",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=repo_root.parent,
        help="parent directory containing mapped repositories",
    )
    parser.add_argument(
        "--replay",
        type=Path,
        help="read a synthetic replay fixture instead of querying GitHub",
    )
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="emit normalized JSON")
    output.add_argument(
        "--details", action="store_true", help="include issue titles and URLs"
    )
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
    runner: CommandRunner = default_runner,
) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = build_parser(repo_root)
    args = parser.parse_args(argv)

    try:
        specs = parse_repository_map(args.map_path.resolve(), args.workspace.resolve())
        if args.replay is not None:
            observed_at, results = load_replay(args.replay.resolve(), specs)
            source_mode = "replay"
        else:
            observed_at = observed_at_now()
            results = collect_live(specs, runner)
            source_mode = "live"
        report = build_report(observed_at, source_mode, results)
    except SetupError as exc:
        print(f"issue inventory setup error [{exc.kind}]: {exc}", file=stderr)
        return EXIT_SETUP_ERROR

    if args.json:
        json.dump(report, stdout, ensure_ascii=False, indent=2, sort_keys=True)
        print(file=stdout)
    else:
        print(render_text(report, details=args.details), file=stdout)

    return EXIT_COMPLETE if report["complete"] else EXIT_INCOMPLETE


if __name__ == "__main__":
    raise SystemExit(main())
