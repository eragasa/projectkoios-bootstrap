from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from projectkoios.bootstrap.git.client import GitClient, GitCommandError
from projectkoios.bootstrap.git.push import (
    BranchPush,
    BranchPushError,
    GitBranchPusher,
    main,
)

_BRANCH = "feature/shared-push"


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


@pytest.fixture
def repository(tmp_path: Path) -> tuple[Path, Path, str]:
    remote = tmp_path / "remote.git"
    root = tmp_path / "repository"
    subprocess.run(
        ["git", "init", "--bare", "--quiet", str(remote)],
        check=True,
        timeout=10,
    )
    subprocess.run(
        ["git", "init", "--quiet", "-b", _BRANCH, str(root)],
        check=True,
        timeout=10,
    )
    _git(root, "config", "user.name", "Test User")
    _git(root, "config", "user.email", "test@example.invalid")
    (root / "tracked.txt").write_text("first\n", encoding="utf-8")
    _git(root, "add", "tracked.txt")
    _git(root, "commit", "--quiet", "-m", "first")
    _git(root, "remote", "add", "origin", str(remote))
    return root.resolve(), remote.resolve(), _git(root, "rev-parse", "HEAD")


def _pusher(
    root: Path,
    expected: str,
    *,
    apply: bool,
    replace_upstream: bool = False,
    remote: str = "origin",
) -> GitBranchPusher:
    return GitBranchPusher(
        BranchPush(
            repository_root=root,
            remote=remote,
            branch=_BRANCH,
            expected_commit=expected,
            apply=apply,
            replace_upstream=replace_upstream,
        )
    )


def _remote_commit(remote: Path) -> str | None:
    result = subprocess.run(
        [
            "git",
            "--git-dir",
            str(remote),
            "rev-parse",
            "--verify",
            f"refs/heads/{_BRANCH}",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def test_dry_run_does_not_push(
    repository: tuple[Path, Path, str],
) -> None:
    root, remote, expected = repository

    result = _pusher(root, expected, apply=False).execute()

    assert not result.applied
    assert result.remote_commit_before is None
    assert _remote_commit(remote) is None
    assert "DRY RUN ONLY" in result.render()


def test_apply_pushes_exact_commit_and_sets_upstream(
    repository: tuple[Path, Path, str],
) -> None:
    root, remote, expected = repository
    hook = Path(_git(root, "rev-parse", "--git-path", "hooks/pre-push"))
    if not hook.is_absolute():
        hook = root / hook
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text("#!/bin/sh\nexit 91\n", encoding="utf-8")
    hook.chmod(0o755)
    _git(root, "tag", "-a", "unrelated-tag", "-m", "not pushed")
    _git(root, "config", "push.gpgSign", "true")

    result = _pusher(root, expected, apply=True).execute()

    assert result.applied
    assert result.remote_commit_after == expected
    assert _remote_commit(remote) == expected
    assert (
        _git(
            root,
            "for-each-ref",
            "--format=%(upstream:short)",
            f"refs/heads/{_BRANCH}",
        )
        == f"origin/{_BRANCH}"
    )
    tag = subprocess.run(
        [
            "git",
            "--git-dir",
            str(remote),
            "show-ref",
            "--verify",
            "--quiet",
            "refs/tags/unrelated-tag",
        ],
        check=False,
        timeout=10,
    )
    assert tag.returncode == 1


def test_dirty_worktree_stops_before_push(
    repository: tuple[Path, Path, str],
) -> None:
    root, remote, expected = repository
    (root / "untracked.txt").write_text("dirty\n", encoding="utf-8")

    with pytest.raises(BranchPushError, match="worktree is not clean"):
        _pusher(root, expected, apply=True).execute()

    assert _remote_commit(remote) is None


def test_expected_commit_must_match_head_and_branch(
    repository: tuple[Path, Path, str],
) -> None:
    root, remote, _ = repository

    with pytest.raises(BranchPushError, match="cat-file"):
        _pusher(root, "b" * 40, apply=True).execute()

    assert _remote_commit(remote) is None


@pytest.mark.parametrize(
    "configuration",
    ["missing", "custom"],
)
def test_unsupported_fetch_mapping_stops_before_push(
    repository: tuple[Path, Path, str],
    configuration: str,
) -> None:
    root, remote, expected = repository
    _git(root, "config", "--unset-all", "remote.origin.fetch")
    if configuration == "custom":
        _git(
            root,
            "config",
            "--add",
            "remote.origin.fetch",
            "+refs/heads/*:refs/remotes/cache/*",
        )

    with pytest.raises(BranchPushError, match="fetch refspec"):
        _pusher(root, expected, apply=True).execute()

    assert _remote_commit(remote) is None


def test_nonmatching_negative_fetch_refspec_is_allowed(
    repository: tuple[Path, Path, str],
) -> None:
    root, remote, expected = repository
    _git(
        root,
        "config",
        "--add",
        "remote.origin.fetch",
        "^refs/heads/archive/*",
    )

    result = _pusher(root, expected, apply=True).execute()

    assert result.remote_commit_after == expected
    assert _remote_commit(remote) == expected


def test_matching_negative_fetch_refspec_stops_before_push(
    repository: tuple[Path, Path, str],
) -> None:
    root, remote, expected = repository
    _git(
        root,
        "config",
        "--add",
        "remote.origin.fetch",
        "^refs/heads/feature/*",
    )

    with pytest.raises(BranchPushError, match="excludes the branch"):
        _pusher(root, expected, apply=True).execute()

    assert _remote_commit(remote) is None


def test_slash_containing_remote_name_is_supported(
    repository: tuple[Path, Path, str],
) -> None:
    root, remote, expected = repository
    _git(root, "remote", "rename", "origin", "team/origin")

    result = _pusher(
        root,
        expected,
        apply=True,
        remote="team/origin",
    ).execute()

    assert result.remote_commit_after == expected
    assert _remote_commit(remote) == expected


def test_distinct_push_endpoint_stops_before_push(
    repository: tuple[Path, Path, str],
    tmp_path: Path,
) -> None:
    root, remote, expected = repository
    other = tmp_path / "other.git"
    subprocess.run(
        ["git", "init", "--bare", "--quiet", str(other)],
        check=True,
        timeout=10,
    )
    _git(root, "remote", "set-url", "--add", "--push", "origin", str(other))

    with pytest.raises(BranchPushError, match="identical fetch and push"):
        _pusher(root, expected, apply=True).execute()

    assert _remote_commit(remote) is None
    assert _remote_commit(other) is None


def test_existing_different_upstream_stops_before_push(
    repository: tuple[Path, Path, str],
) -> None:
    root, remote, expected = repository
    backup = root.parent / "backup.git"
    subprocess.run(
        ["git", "init", "--bare", "--quiet", str(backup)],
        check=True,
        timeout=10,
    )
    _git(root, "remote", "add", "backup", str(backup))
    _git(root, "push", "--quiet", "-u", "backup", _BRANCH)

    with pytest.raises(BranchPushError, match="different upstream"):
        _pusher(root, expected, apply=True).execute()

    assert _remote_commit(remote) is None


def test_explicit_upstream_replacement_allows_new_feature_branch(
    repository: tuple[Path, Path, str],
    tmp_path: Path,
) -> None:
    root, remote, expected = repository
    base = tmp_path / "base.git"
    subprocess.run(
        ["git", "init", "--bare", "--quiet", str(base)],
        check=True,
        timeout=10,
    )
    _git(root, "remote", "add", "base", str(base))
    _git(root, "push", "--quiet", "-u", "base", _BRANCH)

    result = _pusher(
        root,
        expected,
        apply=True,
        replace_upstream=True,
    ).execute()

    assert result.remote_commit_after == expected
    assert _remote_commit(remote) == expected
    assert (
        _git(
            root,
            "for-each-ref",
            "--format=%(upstream:short)",
            f"refs/heads/{_BRANCH}",
        )
        == f"origin/{_BRANCH}"
    )


def test_upstream_race_stops_after_push_without_overwrite(
    repository: tuple[Path, Path, str],
    tmp_path: Path,
) -> None:
    root, remote, expected = repository
    backup = tmp_path / "backup-race.git"
    subprocess.run(
        ["git", "init", "--bare", "--quiet", str(backup)],
        check=True,
        timeout=10,
    )
    _git(root, "remote", "add", "backup-race", str(backup))
    _git(root, "push", "--quiet", "backup-race", _BRANCH)
    _git(root, "fetch", "--quiet", "backup-race")

    class RacingPusher(GitBranchPusher):
        remote_checks = 0

        def _remote_commit(self) -> str | None:
            result = super()._remote_commit()
            self.remote_checks += 1
            if self.remote_checks == 2:
                _git(
                    root,
                    "branch",
                    "--set-upstream-to",
                    f"backup-race/{_BRANCH}",
                    _BRANCH,
                )
            return result

    pusher = RacingPusher(
        BranchPush(
            repository_root=root,
            remote="origin",
            branch=_BRANCH,
            expected_commit=expected,
            apply=True,
        )
    )
    with pytest.raises(BranchPushError, match="upstream changed during push"):
        pusher.execute()

    assert _remote_commit(remote) == expected
    assert (
        _git(
            root,
            "for-each-ref",
            "--format=%(upstream:short)",
            f"refs/heads/{_BRANCH}",
        )
        == f"backup-race/{_BRANCH}"
    )


def test_non_fast_forward_is_not_forced(
    repository: tuple[Path, Path, str],
    tmp_path: Path,
) -> None:
    root, remote, first = repository
    _pusher(root, first, apply=True).execute()

    other = tmp_path / "other"
    subprocess.run(
        ["git", "clone", "--quiet", str(remote), str(other)],
        check=True,
        timeout=10,
    )
    _git(other, "config", "user.name", "Other User")
    _git(other, "config", "user.email", "other@example.invalid")
    _git(other, "switch", "--quiet", _BRANCH)
    (other / "remote.txt").write_text("remote\n", encoding="utf-8")
    _git(other, "add", "remote.txt")
    _git(other, "commit", "--quiet", "-m", "remote")
    _git(other, "push", "--quiet", "origin", _BRANCH)
    remote_commit = _git(other, "rev-parse", "HEAD")

    (root / "local.txt").write_text("local\n", encoding="utf-8")
    _git(root, "add", "local.txt")
    _git(root, "commit", "--quiet", "-m", "local")
    local_commit = _git(root, "rev-parse", "HEAD")

    with pytest.raises(BranchPushError, match="Git command failed"):
        _pusher(root, local_commit, apply=True).execute()

    assert _remote_commit(remote) == remote_commit


def test_request_rejects_noncanonical_root(
    repository: tuple[Path, Path, str],
) -> None:
    root, _, expected = repository
    alias = root.parent / "alias"
    alias.symlink_to(root, target_is_directory=True)

    with pytest.raises(ValueError, match="must be canonical"):
        _pusher(alias, expected, apply=False)


def test_cli_dry_run_reports_bounded_evidence(
    repository: tuple[Path, Path, str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    root, remote, expected = repository

    status = main(
        [
            "--repo-path",
            str(root),
            "--remote",
            "origin",
            "--branch",
            _BRANCH,
            "--expected-commit",
            expected,
        ]
    )

    captured = capsys.readouterr()
    assert status == 0
    assert "Preflight passed." in captured.out
    assert captured.err == ""
    assert _remote_commit(remote) is None


def test_cli_version_failure_has_no_traceback(
    repository: tuple[Path, Path, str],
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, _, expected = repository

    def fail_version(
        client: GitClient,
        repository_root: Path | None,
        *arguments: str,
        **kwargs: object,
    ) -> subprocess.CompletedProcess[bytes]:
        assert client
        assert repository_root is None
        assert arguments == ("--version",)
        assert not kwargs
        raise GitCommandError("synthetic version failure")

    monkeypatch.setattr(GitClient, "run", fail_version)
    status = main(
        [
            "--repo-path",
            str(root),
            "--remote",
            "origin",
            "--branch",
            _BRANCH,
            "--expected-commit",
            expected,
        ]
    )

    captured = capsys.readouterr()
    assert status == 1
    assert captured.out == ""
    assert "synthetic version failure" in captured.err
    assert "Traceback" not in captured.err


def test_cli_failure_has_no_traceback(
    repository: tuple[Path, Path, str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    root, _, expected = repository
    (root / "untracked.txt").write_text("dirty\n", encoding="utf-8")

    status = main(
        [
            "--repo-path",
            str(root),
            "--remote",
            "origin",
            "--branch",
            _BRANCH,
            "--expected-commit",
            expected,
            "--apply",
        ]
    )

    captured = capsys.readouterr()
    assert status == 1
    assert captured.out == ""
    assert "worktree is not clean" in captured.err
    assert "Traceback" not in captured.err


def test_sha256_repository_pushes_and_verifies(tmp_path: Path) -> None:
    remote = tmp_path / "sha256-remote.git"
    root = tmp_path / "sha256-repository"
    commands = (
        [
            "git",
            "init",
            "--bare",
            "--quiet",
            "--object-format=sha256",
            str(remote),
        ],
        [
            "git",
            "init",
            "--quiet",
            "--object-format=sha256",
            "-b",
            _BRANCH,
            str(root),
        ],
    )
    for command in commands:
        command_result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if command_result.returncode != 0:
            pytest.skip(
                "installed Git lacks SHA-256 repository support: "
                f"{command_result.stderr}"
            )
    root = root.resolve()
    remote = remote.resolve()
    _git(root, "config", "user.name", "Test User")
    _git(root, "config", "user.email", "test@example.invalid")
    (root / "tracked.txt").write_text("sha256\n", encoding="utf-8")
    _git(root, "add", "tracked.txt")
    _git(root, "commit", "--quiet", "-m", "sha256")
    _git(root, "remote", "add", "origin", str(remote))
    expected = _git(root, "rev-parse", "HEAD")

    push_result = _pusher(root, expected, apply=True).execute()

    assert len(expected) == 64
    assert push_result.remote_commit_after == expected
    assert _remote_commit(remote) == expected
