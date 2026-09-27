from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from projectkoios.bootstrap.git.client import (
    GitClient,
    GitCommandError,
    decode,
)

_COMMIT_ID = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_GIT_VERSION = re.compile(r"^git version (\d+)\.(\d+)(?:[.\s].*)?$")
_MINIMUM_GIT_VERSION = (2, 45)
_REMOTE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")
_REMOTE_CONFIGURATION = {"credential.interactive": "false"}


class BranchPushError(RuntimeError):
    """A branch push could not produce the required evidence."""

    def __init__(self, stage: str, message: str) -> None:
        super().__init__(message)
        self.stage = stage


@dataclass(frozen=True)
class BranchPush:
    """Explicit authority and identity for one ordinary branch push."""

    repository_root: Path
    remote: str
    branch: str
    expected_commit: str
    apply: bool = False
    replace_upstream: bool = False
    timeout_seconds: int = 120


@dataclass(frozen=True)
class BranchPushResult:
    """Preflight or applied evidence for an exact branch push."""

    request: BranchPush
    remote_commit_before: str | None
    remote_commit_after: str | None
    applied: bool

    def render(self) -> str:
        request = self.request
        before = self.remote_commit_before or "ABSENT"
        if not self.applied:
            return "\n".join(
                (
                    "Preflight passed.",
                    f"  repository:      {request.repository_root}",
                    f"  remote:          {request.remote}",
                    f"  branch:          {request.branch}",
                    f"  expected commit: {request.expected_commit}",
                    f"  remote before:   {before}",
                    "DRY RUN ONLY: no ref or upstream configuration was "
                    "changed. Re-run with --apply to push.",
                )
            )
        return "\n".join(
            (
                "FINAL STATUS",
                f"repository:    {request.repository_root}",
                f"remote:        {request.remote}",
                f"branch:        {request.branch}",
                f"local commit:  {request.expected_commit}",
                f"remote before: {before}",
                f"remote after:  {self.remote_commit_after}",
                f"upstream:      {request.remote}/{request.branch}",
                "SUCCESS: the exact expected commit was pushed and verified.",
            )
        )


class GitBranchPusher:
    """Push one exact current branch without force or implicit ref selection."""

    def __init__(self, request: BranchPush) -> None:
        _validate_request(request)
        self._request = request
        self._read = GitClient(
            disable_optional_locks=True,
            preserve_global_config=True,
            timeout_seconds=request.timeout_seconds,
        )
        self._mutate = GitClient(
            disable_optional_locks=False,
            preserve_global_config=True,
            timeout_seconds=request.timeout_seconds,
        )
        self._stage = "preflight"
        self._initial_upstream: str | None = None

    @property
    def request(self) -> BranchPush:
        return self._request

    def execute(self) -> BranchPushResult:
        try:
            self._stage = "local preflight"
            self._assert_local_preflight(capture_upstream=True)
            self._stage = "remote preflight"
            before = self._remote_commit()
            if not self._request.apply:
                return BranchPushResult(
                    request=self._request,
                    remote_commit_before=before,
                    remote_commit_after=None,
                    applied=False,
                )

            request = self._request
            self._stage = "push exact commit"
            self._mutate.run(
                request.repository_root,
                "push",
                "--porcelain",
                "--no-verify",
                "--recurse-submodules=no",
                request.remote,
                f"{request.expected_commit}:refs/heads/{request.branch}",
                configuration={
                    **_REMOTE_CONFIGURATION,
                    "push.followTags": "false",
                    "push.gpgSign": "false",
                    "push.pushOption": "",
                },
            )

            self._stage = "verify remote commit"
            after = self._remote_commit()
            if after != request.expected_commit:
                raise BranchPushError(
                    self._stage,
                    "remote branch does not identify the expected commit",
                )

            self._stage = "verify unchanged local branch"
            self._assert_local_identity()

            self._stage = "recheck upstream authority"
            self._assert_upstream_unchanged()

            self._stage = "set upstream"
            self._mutate.run(
                request.repository_root,
                "branch",
                "--set-upstream-to",
                f"{request.remote}/{request.branch}",
                "--",
                request.branch,
            )

            self._stage = "final validation"
            self._assert_local_preflight(capture_upstream=False)
            upstream = self._line(
                "for-each-ref",
                "--format=%(upstream:short)",
                f"refs/heads/{request.branch}",
                label="branch upstream",
            )
            if upstream != f"{request.remote}/{request.branch}":
                raise BranchPushError(
                    self._stage,
                    "branch upstream does not match the pushed remote branch",
                )
            tracking = self._line(
                "rev-parse",
                "--verify",
                f"refs/remotes/{request.remote}/{request.branch}",
                label="remote-tracking commit",
            )
            if tracking != request.expected_commit:
                raise BranchPushError(
                    self._stage,
                    "remote-tracking branch does not identify the expected "
                    "commit",
                )
            return BranchPushResult(
                request=request,
                remote_commit_before=before,
                remote_commit_after=after,
                applied=True,
            )
        except BranchPushError:
            raise
        except GitCommandError as error:
            raise BranchPushError(self._stage, str(error)) from error

    def _assert_local_preflight(self, *, capture_upstream: bool) -> None:
        request = self._request
        root = self._line(
            "rev-parse",
            "--show-toplevel",
            label="repository root",
        )
        if Path(root).resolve() != request.repository_root:
            raise BranchPushError(
                self._stage,
                f"repository root is not the worktree root: {root}",
            )
        current = self._line(
            "symbolic-ref",
            "--quiet",
            "--short",
            "HEAD",
            label="current branch",
        )
        if current != request.branch:
            raise BranchPushError(
                self._stage,
                f"current branch is {current}, expected {request.branch}",
            )
        self._assert_local_identity()
        status = self._read.run(
            request.repository_root,
            "status",
            "--porcelain=v2",
            "-z",
            "--untracked-files=all",
        ).stdout
        if status:
            raise BranchPushError(self._stage, "worktree is not clean")
        self._assert_remote_configuration()
        if capture_upstream:
            self._capture_upstream_authority()

    def _assert_local_identity(self) -> None:
        request = self._request
        self._read.run(
            request.repository_root,
            "cat-file",
            "-e",
            f"{request.expected_commit}^{{commit}}",
        )
        head = self._line("rev-parse", "--verify", "HEAD", label="HEAD")
        branch = self._line(
            "rev-parse",
            "--verify",
            f"refs/heads/{request.branch}",
            label="local branch commit",
        )
        if head != request.expected_commit or branch != request.expected_commit:
            raise BranchPushError(
                self._stage,
                "HEAD and local branch must both identify the expected commit",
            )

    def _assert_remote_configuration(self) -> None:
        request = self._request
        fetch_urls = self._lines(
            "remote",
            "get-url",
            "--all",
            "--",
            request.remote,
            label="remote fetch URL set",
            configuration=_REMOTE_CONFIGURATION,
        )
        push_urls = self._lines(
            "remote",
            "get-url",
            "--push",
            "--all",
            "--",
            request.remote,
            label="remote push URL set",
            configuration=_REMOTE_CONFIGURATION,
        )
        if (
            len(fetch_urls) != 1
            or len(push_urls) != 1
            or fetch_urls != push_urls
        ):
            raise BranchPushError(
                self._stage,
                "remote must have one identical fetch and push endpoint",
            )

        result = self._read.run(
            request.repository_root,
            "config",
            "--get-all",
            f"remote.{request.remote}.fetch",
            allowed=(0, 1),
        )
        refspecs = _decode_lines(result.stdout, "remote fetch refspecs")
        source = f"refs/heads/{request.branch}"
        expected_tracking = f"refs/remotes/{request.remote}/{request.branch}"
        destinations: list[str] = []
        for refspec in refspecs:
            if refspec.startswith("^"):
                raise BranchPushError(
                    self._stage,
                    "negative remote fetch refspecs are unsupported",
                )
            destination = _map_fetch_refspec(refspec, source)
            if destination is not None:
                destinations.append(destination)
        if destinations != [expected_tracking]:
            raise BranchPushError(
                self._stage,
                "remote fetch refspec must map the branch to its standard "
                "remote-tracking ref",
            )

    def _upstream(self) -> str:
        request = self._request
        return self._line(
            "for-each-ref",
            "--format=%(upstream:short)",
            f"refs/heads/{request.branch}",
            label="branch upstream",
        )

    def _capture_upstream_authority(self) -> None:
        request = self._request
        upstream = self._upstream()
        target = f"{request.remote}/{request.branch}"
        if upstream and upstream != target and not request.replace_upstream:
            raise BranchPushError(
                self._stage,
                f"branch already tracks a different upstream: {upstream}",
            )
        self._initial_upstream = upstream

    def _assert_upstream_unchanged(self) -> None:
        if self._upstream() != self._initial_upstream:
            raise BranchPushError(
                self._stage,
                "branch upstream changed during push",
            )

    def _remote_commit(self) -> str | None:
        request = self._request
        result = self._read.run(
            request.repository_root,
            "ls-remote",
            "--refs",
            request.remote,
            f"refs/heads/{request.branch}",
            configuration=_REMOTE_CONFIGURATION,
        )
        if not result.stdout:
            return None
        lines = decode(result.stdout, "remote branch evidence").splitlines()
        expected_ref = f"refs/heads/{request.branch}"
        if len(lines) != 1:
            raise BranchPushError(
                self._stage,
                "remote returned an unexpected number of branch records",
            )
        fields = lines[0].split("\t")
        if (
            len(fields) != 2
            or fields[1] != expected_ref
            or not _COMMIT_ID.fullmatch(fields[0])
        ):
            raise BranchPushError(
                self._stage,
                "remote returned malformed branch evidence",
            )
        return fields[0]

    def _lines(
        self,
        *arguments: str,
        label: str,
        configuration: dict[str, str] | None = None,
    ) -> tuple[str, ...]:
        result = self._read.run(
            self._request.repository_root,
            *arguments,
            configuration=configuration,
        )
        return _decode_lines(result.stdout, label)

    def _line(self, *arguments: str, label: str) -> str:
        result = self._read.run(self._request.repository_root, *arguments)
        value = decode(result.stdout, label).rstrip("\n")
        if "\n" in value or "\0" in value:
            raise BranchPushError(self._stage, f"{label} is not one line")
        return value


def _decode_lines(payload: bytes, label: str) -> tuple[str, ...]:
    if b"\0" in payload:
        raise GitCommandError(f"{label} contains NUL framing")
    lines = tuple(decode(payload, label).splitlines())
    if any(not line for line in lines):
        raise GitCommandError(f"{label} contains an empty line")
    return lines


def _map_fetch_refspec(refspec: str, source: str) -> str | None:
    value = refspec.removeprefix("+")
    if value.count(":") != 1:
        raise GitCommandError("remote fetch refspec is malformed")
    source_pattern, destination_pattern = value.split(":", 1)
    if source_pattern.count("*") != destination_pattern.count("*"):
        raise GitCommandError("remote fetch refspec wildcard is malformed")
    if "*" not in source_pattern:
        return destination_pattern if source_pattern == source else None
    if source_pattern.count("*") != 1:
        raise GitCommandError(
            "multiple fetch refspec wildcards are unsupported"
        )
    prefix, suffix = source_pattern.split("*", 1)
    if not source.startswith(prefix) or not source.endswith(suffix):
        return None
    end = len(source) - len(suffix) if suffix else len(source)
    wildcard = source[len(prefix) : end]
    return destination_pattern.replace("*", wildcard)


def _validate_request(request: BranchPush) -> None:
    root = request.repository_root
    if not root.is_absolute():
        raise ValueError("repository root must be absolute")
    if not root.is_dir():
        raise ValueError(f"repository root is not a directory: {root}")
    if root.resolve() != root:
        raise ValueError(f"repository root must be canonical: {root.resolve()}")
    if not _REMOTE_NAME.fullmatch(request.remote):
        raise ValueError("remote contains unsupported characters")
    if not request.branch or request.branch.startswith("-"):
        raise ValueError("branch must be nonempty and not start with '-'")
    if not _COMMIT_ID.fullmatch(request.expected_commit):
        raise ValueError(
            "expected commit must be a full lowercase 40- or 64-hex ID"
        )
    if not 1 <= request.timeout_seconds <= 300:
        raise ValueError("timeout seconds must be between 1 and 300")
    if shutil.which("git") is None:
        raise ValueError("required command not found: git")
    git = GitClient(disable_optional_locks=True, preserve_global_config=True)
    version = decode(git.run(None, "--version").stdout, "Git version").strip()
    match = _GIT_VERSION.fullmatch(version)
    if match is None or tuple(map(int, match.groups())) < _MINIMUM_GIT_VERSION:
        raise ValueError("Git 2.45 or newer is required")
    try:
        git.run(None, "check-ref-format", f"refs/heads/{request.branch}")
    except GitCommandError as error:
        raise ValueError(f"invalid branch: {request.branch}") from error


def parse_pusher(argv: Sequence[str] | None = None) -> GitBranchPusher:
    parser = argparse.ArgumentParser(
        description="Push one exact current Git branch and verify the remote",
    )
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--remote", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--replace-upstream", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        return GitBranchPusher(
            BranchPush(
                repository_root=Path(arguments.repo_path),
                remote=arguments.remote,
                branch=arguments.branch,
                expected_commit=arguments.expected_commit,
                apply=arguments.apply,
                replace_upstream=arguments.replace_upstream,
                timeout_seconds=arguments.timeout_seconds,
            )
        )
    except ValueError as error:
        raise BranchPushError("argument validation", str(error)) from error


def main(argv: Sequence[str] | None = None) -> int:
    try:
        result = parse_pusher(argv).execute()
    except BranchPushError as error:
        print(f"ERROR [{error.stage}]: {error}", file=sys.stderr)
        print(
            "No automatic cleanup, retry, force push, or rollback was "
            "attempted. Inspect live refs before any follow-up.",
            file=sys.stderr,
        )
        return 1
    print(result.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
