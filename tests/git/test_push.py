from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
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
) -> GitBranchPusher:
    return GitBranchPusher(
        BranchPush(
            repository_root=root,
            remote="origin",
            branch=_BRANCH,
            expected_commit=expected,
            apply=apply,
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


def test_request_accepts_full_sha256_object_id(
    repository: tuple[Path, Path, str],
) -> None:
    root, _, _ = repository

    request = BranchPush(
        repository_root=root,
        remote="origin",
        branch=_BRANCH,
        expected_commit="a" * 64,
    )

    assert request.expected_commit == "a" * 64
