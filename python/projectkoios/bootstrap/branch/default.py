from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Never

from projectkoios.bootstrap.branch.base import GitBranchChange
from projectkoios.bootstrap.git.client import (
    GitClient,
    GitCommandError,
    decode,
    parse_worktree_records,
)

_GITHUB_TIMEOUT_SECONDS = 30


class DefaultBranchError(RuntimeError):
    """Default-branch evidence or mutation failed."""


class DefaultBranchService:
    """Inspect and change one GitHub repository's default branch."""

    def __init__(self) -> None:
        self._inspect = GitClient(
            disable_optional_locks=True,
            preserve_global_config=True,
        )

    def assert_preflight(self, change: GitBranchChange) -> None:
        self._assert_remote_identity(change)
        self._assert_clean_single_worktree(change)
        self._assert_no_pre_push_hook(change)
        self._assert_source_exact(change)
        self._assert_target_absent(change)
        self._assert_default_branch(change, change.source.name)
        self._assert_no_open_pull_requests(change)

    def assert_post_push(self, change: GitBranchChange) -> str | None:
        self._assert_remote_identity(change)
        self._assert_clean_single_worktree(change)
        self._assert_source_exact(change)
        tracking = self._assert_target_exact(change)
        self._assert_default_branch(change, change.source.name)
        self._assert_no_open_pull_requests(change)
        return tracking

    def change_default_branch(self, change: GitBranchChange) -> None:
        self._github(
            "repo",
            "edit",
            change.repository.github_repository,
            "--default-branch",
            change.target.name,
        )

    def assert_final(self, change: GitBranchChange) -> str | None:
        self._assert_remote_identity(change)
        self._assert_clean_single_worktree(change)
        self._assert_source_exact(change)
        tracking = self._assert_target_exact(change)
        self._assert_default_branch(change, change.target.name)
        self._assert_remote_head(change)
        self._assert_no_open_pull_requests(change)
        return tracking

    def _assert_remote_identity(
        self,
        request: GitBranchChange,
    ) -> None:
        fetch_urls = self._git_lines(
            request,
            "remote",
            "get-url",
            "--all",
            request.repository.remote,
        )
        push_urls = self._git_lines(
            request,
            "remote",
            "get-url",
            "--push",
            "--all",
            request.repository.remote,
        )
        if len(fetch_urls) != 1:
            self._fail(
                f"{request.repository.remote} must have exactly one fetch URL, "
                f"found {len(fetch_urls)}"
            )
        if len(push_urls) != 1:
            self._fail(
                f"{request.repository.remote} must have exactly one push URL, "
                f"found {len(push_urls)}"
            )
        accepted = {
            f"https://github.com/{request.repository.github_repository}.git",
            f"https://github.com/{request.repository.github_repository}",
            f"git@github.com:{request.repository.github_repository}.git",
            f"ssh://git@github.com/{request.repository.github_repository}.git",
        }
        for url in (*fetch_urls, *push_urls):
            if url not in accepted:
                self._fail(
                    "remote URL does not identify "
                    f"{request.repository.github_repository}: {url}"
                )
        payload = self._github_json(
            "repo",
            "view",
            request.repository.github_repository,
            "--json",
            "nameWithOwner",
        )
        if payload.get("nameWithOwner") != request.repository.github_repository:
            self._fail(
                "GitHub identity mismatch: expected "
                f"{request.repository.github_repository}, got "
                f"{payload.get('nameWithOwner')!r}"
            )

    def _assert_clean_single_worktree(
        self,
        request: GitBranchChange,
    ) -> None:
        status = self._inspect.run(
            request.repository.root,
            "-c",
            "status.showUntrackedFiles=all",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--ignore-submodules=none",
        ).stdout
        if status:
            self._fail("checkout is dirty")
        flagged = self._flagged_index_paths(request)
        if flagged:
            rendered = ", ".join(flagged)
            self._fail(
                "tracked paths use skip-worktree or assume-unchanged: "
                f"{rendered}"
            )
        worktree_payload = self._inspect.run(
            request.repository.root,
            "worktree",
            "list",
            "--porcelain",
            "-z",
        ).stdout
        try:
            records = parse_worktree_records(worktree_payload)
        except GitCommandError as error:
            self._fail(str(error))
        paths = [
            value
            for record in records
            if isinstance((value := record.get("worktree")), str)
        ]
        if len(paths) != 1:
            self._fail(
                f"expected exactly one registered worktree, found {len(paths)}"
            )
        if Path(paths[0]).resolve() != request.repository.root:
            self._fail(
                f"sole registered worktree is not --repo-path: {paths[0]}"
            )

    def _flagged_index_paths(
        self,
        request: GitBranchChange,
    ) -> tuple[str, ...]:
        payload = self._inspect.run(
            request.repository.root,
            "ls-files",
            "-v",
            "-z",
            "--",
        ).stdout
        if payload and not payload.endswith(b"\0"):
            self._fail("Git returned an invalid index flag list")
        flagged: list[str] = []
        for record in payload[:-1].split(b"\0") if payload else ():
            if len(record) < 3 or record[1:2] != b" ":
                self._fail("Git returned an invalid index flag record")
            tag = decode(record[:1], "index flag")
            path = decode(record[2:], "index path")
            if tag == "S" or tag.islower():
                flagged.append(path)
        return tuple(sorted(flagged))

    def _assert_no_pre_push_hook(self, request: GitBranchChange) -> None:
        hook = self._git_text(
            request,
            "rev-parse",
            "--path-format=absolute",
            "--git-path",
            "hooks/pre-push",
        )
        hook_path = Path(hook)
        if hook_path.is_file() and os.access(hook_path, os.X_OK):
            self._fail(f"executable pre-push hook is not supported: {hook}")

    def _assert_source_exact(
        self,
        request: GitBranchChange,
    ) -> None:
        symbolic = self._git_text(
            request,
            "symbolic-ref",
            "-q",
            "HEAD",
        )
        expected_ref = f"refs/heads/{request.source.name}"
        if symbolic != expected_ref:
            self._fail(
                f"checkout must be on {request.source.name}; found {symbolic}"
            )
        comparisons = {
            "HEAD": self._local_commit(request, "HEAD"),
            "local source": self._local_commit(request, expected_ref),
            "source tracking ref": self._local_commit(
                request,
                f"refs/remotes/{request.repository.remote}/{request.source.name}",
            ),
            "canonical remote source": self._remote_ref_oid(
                request,
                request.source.name,
            ),
        }
        for label, actual in comparisons.items():
            if actual != request.source.commit:
                self._fail(
                    f"{label} changed: expected {request.source.commit}, "
                    f"got {actual or 'ABSENT'}"
                )
        self._inspect.run(
            request.repository.root,
            "cat-file",
            "-e",
            f"{request.source.commit}^{{commit}}",
        )

    def _assert_target_absent(
        self,
        request: GitBranchChange,
    ) -> None:
        local_ref = f"refs/heads/{request.target.name}"
        tracking_ref = (
            f"refs/remotes/{request.repository.remote}/{request.target.name}"
        )
        if self._ref_exists(request, local_ref):
            self._fail(f"local target already exists: {local_ref}")
        if self._ref_exists(request, tracking_ref):
            self._fail(f"target tracking ref already exists: {tracking_ref}")
        remote = self._remote_ref_oid(request, request.target.name)
        if remote is not None:
            self._fail(f"canonical remote target already exists at {remote}")

    def _assert_target_exact(
        self,
        request: GitBranchChange,
    ) -> str | None:
        local = self._local_commit(
            request,
            f"refs/heads/{request.target.name}",
        )
        remote = self._remote_ref_oid(request, request.target.name)
        if local != request.source.commit:
            self._fail(
                "local target mismatch: expected "
                f"{request.source.commit}, got {local or 'ABSENT'}"
            )
        if remote != request.source.commit:
            self._fail(
                "canonical remote target mismatch: expected "
                f"{request.source.commit}, got {remote or 'ABSENT'}"
            )
        tracking_ref = (
            f"refs/remotes/{request.repository.remote}/{request.target.name}"
        )
        tracking = (
            self._local_commit(request, tracking_ref)
            if self._ref_exists(request, tracking_ref)
            else None
        )
        if tracking is not None and tracking != request.source.commit:
            self._fail(
                "target tracking ref mismatch: expected "
                f"{request.source.commit}, got {tracking}"
            )
        return tracking

    def _assert_no_open_pull_requests(
        self,
        request: GitBranchChange,
    ) -> None:
        payload = self._github_json(
            "pr",
            "list",
            "--repo",
            request.repository.github_repository,
            "--state",
            "open",
            "--limit",
            "1",
            "--json",
            "number",
        )
        if not isinstance(payload, list):
            self._fail("GitHub returned an invalid pull-request list")
        if payload:
            self._fail("repository has one or more open pull requests")

    def _assert_default_branch(
        self,
        request: GitBranchChange,
        expected: str,
    ) -> None:
        payload = self._github_json(
            "repo",
            "view",
            request.repository.github_repository,
            "--json",
            "defaultBranchRef",
        )
        default = payload.get("defaultBranchRef")
        actual = default.get("name") if isinstance(default, dict) else None
        if actual != expected:
            self._fail(
                f"GitHub default branch mismatch: expected {expected}, "
                f"got {actual or 'NONE'}"
            )

    def _assert_remote_head(
        self,
        request: GitBranchChange,
    ) -> None:
        lines = self._git_lines(
            request,
            "ls-remote",
            "--symref",
            request.repository.remote,
            "HEAD",
        )
        expected_symbolic = f"ref: refs/heads/{request.target.name}\tHEAD"
        if not lines or lines[0] != expected_symbolic:
            self._fail(
                "canonical remote HEAD does not point to "
                f"refs/heads/{request.target.name}"
            )
        oid = next(
            (
                line.split("\t", 1)[0]
                for line in lines
                if line.endswith("\tHEAD") and not line.startswith("ref: ")
            ),
            None,
        )
        if oid != request.source.commit:
            self._fail(
                "canonical remote HEAD mismatch: expected "
                f"{request.source.commit}, got {oid or 'NONE'}"
            )

    def _remote_ref_oid(
        self,
        request: GitBranchChange,
        branch: str,
    ) -> str | None:
        reference = f"refs/heads/{branch}"
        lines = self._git_lines(
            request,
            "ls-remote",
            "--heads",
            request.repository.remote,
            reference,
        )
        if not lines:
            return None
        if len(lines) != 1:
            self._fail(
                f"remote ref query returned {len(lines)} rows for {reference}"
            )
        fields = lines[0].split("\t")
        if len(fields) != 2 or fields[1] != reference:
            self._fail(f"unexpected remote ref returned for {branch}")
        return fields[0]

    def _ref_exists(
        self,
        request: GitBranchChange,
        reference: str,
    ) -> bool:
        result = self._inspect.run(
            request.repository.root,
            "show-ref",
            "--verify",
            "--quiet",
            reference,
            allowed=(0, 1),
        )
        return result.returncode == 0

    def _local_commit(
        self,
        request: GitBranchChange,
        reference: str,
    ) -> str:
        return self._git_text(
            request,
            "rev-parse",
            "--verify",
            reference,
        )

    def _git_lines(
        self,
        request: GitBranchChange,
        *arguments: str,
    ) -> list[str]:
        payload = self._inspect.run(
            request.repository.root,
            *arguments,
        ).stdout
        text = decode(payload, "Git output")
        return [line for line in text.splitlines() if line]

    def _git_text(
        self,
        request: GitBranchChange,
        *arguments: str,
    ) -> str:
        lines = self._git_lines(request, *arguments)
        if len(lines) != 1:
            self._fail(
                "Git returned an unexpected number of lines for "
                f"{' '.join(arguments[:2])}"
            )
        return lines[0]

    def _github_json(self, *arguments: str) -> Any:
        output = self._github(*arguments)
        try:
            return json.loads(output)
        except json.JSONDecodeError as error:
            raise DefaultBranchError("GitHub returned invalid JSON") from error

    def _github(self, *arguments: str) -> str:
        try:
            result = subprocess.run(
                ["gh", *arguments],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                check=False,
                env=self._inspect.environment(),
                text=True,
                timeout=_GITHUB_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise DefaultBranchError(
                "GitHub command could not complete"
            ) from error
        if result.returncode != 0:
            raise DefaultBranchError(
                f"GitHub command failed with exit {result.returncode}"
            )
        return result.stdout

    def _fail(self, message: str) -> Never:
        raise DefaultBranchError(message)
