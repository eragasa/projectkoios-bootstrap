from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest
from projectkoios.bootstrap.repository.preservation import (
    RepositoryPreservationError,
    inspect_repository_set_preservation,
)

_REPOSITORY = Path(__file__).parents[2]
_SCRIPT = _REPOSITORY / "scripts/inspect-project-preservation"


def _evidence(
    path: Path,
    *,
    signals: list[str] | None = None,
    oid_count: int | None = 0,
    reachability_available: bool = True,
) -> dict[str, object]:
    signal_values = [] if signals is None else signals
    dirty = "dirty" in signal_values
    status_entries = (
        [
            {
                "index_status": None,
                "kind": "untracked",
                "original_path": None,
                "path": "untracked.txt",
                "submodule": None,
                "worktree_status": None,
            }
        ]
        if dirty
        else []
    )
    status_payload = b"? untracked.txt\0" if dirty else b""
    counts = {
        "conflicted": 0,
        "staged": 0,
        "submodule": 0,
        "tracked": 0,
        "unstaged": 0,
        "untracked": int(dirty),
    }
    remote_oid = "a" * 40
    remote_refs = (
        [
            {
                "oid": remote_oid,
                "ref": "refs/remotes/origin/main",
                "symbolic_target": None,
            }
        ]
        if reachability_available
        else []
    )
    remote_refs_encoded = json.dumps(
        remote_refs,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")
    oids = [chr(ord("b") + index) * 40 for index in range(oid_count or 0)]
    oid_digest = hashlib.sha256("\n".join(oids).encode("ascii")).hexdigest()
    reachability = (
        {
            "available": True,
            "oid_count": oid_count,
            "oid_digest": oid_digest,
            "oids": oids,
            "oids_truncated": False,
            "reason": None,
            "scope": "locally_known_remote_tracking_refs",
        }
        if reachability_available
        else {
            "available": False,
            "oid_count": None,
            "oid_digest": None,
            "oids": None,
            "oids_truncated": None,
            "reason": "remote_tracking_refs_unavailable",
            "scope": "locally_known_remote_tracking_refs",
        }
    )
    return {
        "contract": {
            "content_semantics_assessed": False,
            "deletion_safety_assessed": False,
            "future": True,
            "github_state_assessed": False,
            "migration_safety_assessed": False,
            "purpose": "test preservation evidence",
            "remote_reachability_scope": (
                "locally known remote-tracking refs; no fetch is performed"
            ),
        },
        "future_top_level": {"accepted": True},
        "repository": {
            "default_remote_ref": {
                "available": reachability_available,
                "oid": remote_oid if reachability_available else None,
                "ref": "refs/remotes/origin/HEAD",
                "symbolic_target": (
                    "refs/remotes/origin/main"
                    if reachability_available
                    else None
                ),
            },
            "future_repository_field": True,
            "object_format": "sha1",
            "origin_urls": ["https://example.invalid/repository.git"],
            "path": str(path),
            "remote_tracking_ref_count": len(remote_refs),
            "remote_tracking_refs": remote_refs,
            "remote_tracking_refs_digest": hashlib.sha256(
                remote_refs_encoded
            ).hexdigest(),
        },
        "schema_version": 1,
        "signal_counts": {signal: 1 for signal in signal_values},
        "worktrees": [
            {
                "branch": "main",
                "branch_ref": "refs/heads/main",
                "default_remote_ancestry": {
                    "default_ref": "refs/remotes/origin/HEAD",
                    "head_is_ancestor": None,
                    "reason": "default_remote_ref_unavailable",
                },
                "dirty_entry_count": len(status_entries),
                "exists": True,
                "future_worktree_field": True,
                "head": remote_oid,
                "index_flags": {
                    "assume_unchanged_count": 0,
                    "assume_unchanged_paths": [],
                    "skip_worktree_count": 0,
                    "skip_worktree_paths": [],
                },
                "inspectable": True,
                "locked": False,
                "locked_reason": None,
                "missing": False,
                "path": str(path),
                "preservation_signals": signal_values,
                "prunable": False,
                "prunable_reason": None,
                "remote_reachability": reachability,
                "state": "branch",
                "status": {
                    "available": True,
                    "counts": counts,
                    "digest": hashlib.sha256(status_payload).hexdigest(),
                    "entries": status_entries,
                    "entry_count": len(status_entries),
                    "reason": None,
                },
                "upstream": {
                    "ahead": 0,
                    "behind": 0,
                    "comparable": True,
                    "oid": remote_oid,
                    "ref": "refs/remotes/origin/main",
                    "short": "origin/main",
                },
            }
        ],
    }


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        check=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def _init_repository(path: Path) -> Path:
    path.mkdir()
    _git(path, "init", "--quiet", "--initial-branch=main")
    _git(path, "config", "user.name", "Test")
    _git(path, "config", "user.email", "test@example.invalid")
    (path / "tracked.txt").write_text("tracked\n", encoding="utf-8")
    _git(path, "add", "tracked.txt")
    _git(path, "commit", "--quiet", "-m", "initial")
    return path


def test_aggregation_is_deterministic_and_counts_factual_signals(
    tmp_path: Path,
) -> None:
    first = tmp_path / "a"
    second = tmp_path / "b"
    first.mkdir()
    second.mkdir()
    evidence_by_path = {
        first: _evidence(
            first,
            signals=["commits_not_on_known_remotes", "dirty"],
            oid_count=2,
        ),
        second: _evidence(
            second,
            signals=["remote_reachability_unknown"],
            oid_count=None,
            reachability_available=False,
        ),
    }

    def inspect(path: str | Path) -> dict[str, object]:
        return evidence_by_path[Path(path)]

    normal = inspect_repository_set_preservation(
        [first, second],
        inspector=inspect,
    )
    reversed_result = inspect_repository_set_preservation(
        [second, first],
        inspector=inspect,
    )

    assert normal == reversed_result
    repositories = normal["repositories"]
    assert isinstance(repositories, list)
    repository_paths: list[str] = []
    for repository in repositories:
        assert isinstance(repository, dict)
        repository_identity = repository["repository"]
        assert isinstance(repository_identity, dict)
        path = repository_identity["path"]
        assert isinstance(path, str)
        repository_paths.append(path)
    assert repository_paths == [str(first), str(second)]
    assert normal["totals"] == {
        "commits_not_on_known_remotes_worktree_occurrence_count": 2,
        "registered_worktree_count": 2,
        "repository_count": 2,
        "signal_counts": {
            "commits_not_on_known_remotes": 1,
            "dirty": 1,
            "remote_reachability_unknown": 1,
        },
        "worktree_with_preservation_signal_count": 2,
    }


def test_aggregation_rejects_relative_duplicate_and_missing_inputs(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()

    with pytest.raises(RepositoryPreservationError, match="at least one"):
        inspect_repository_set_preservation([])
    with pytest.raises(RepositoryPreservationError, match="must be absolute"):
        inspect_repository_set_preservation([Path("relative")])
    with pytest.raises(RepositoryPreservationError, match="must be unique"):
        inspect_repository_set_preservation([repository, repository])


def test_aggregation_fails_closed_on_consumed_producer_fields(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    evidence = _evidence(repository, signals=["dirty"])
    del evidence["signal_counts"]

    with pytest.raises(RepositoryPreservationError, match="signal_counts"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: evidence,
        )


def test_aggregation_rejects_non_mapping_producer_result(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()

    with pytest.raises(RepositoryPreservationError, match="must be an object"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: [],
        )


def test_aggregation_rejects_reachability_signal_contradiction(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    evidence = _evidence(repository, signals=[], oid_count=2)

    with pytest.raises(RepositoryPreservationError, match="are inconsistent"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: evidence,
        )


def test_aggregation_rejects_missing_required_worktree_field(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    evidence = _evidence(repository)
    worktrees = evidence["worktrees"]
    assert isinstance(worktrees, list)
    worktree = worktrees[0]
    assert isinstance(worktree, dict)
    del worktree["status"]

    with pytest.raises(RepositoryPreservationError, match="status"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: evidence,
        )


def test_aggregation_rejects_non_json_additive_field(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    evidence = _evidence(repository)
    evidence["future_non_json_value"] = object()

    with pytest.raises(RepositoryPreservationError, match="JSON-compatible"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: evidence,
        )


def test_aggregation_rejects_duplicate_or_unsorted_worktrees(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()

    duplicate_evidence = _evidence(repository)
    duplicate_worktrees = duplicate_evidence["worktrees"]
    assert isinstance(duplicate_worktrees, list)
    duplicate_worktrees.append(copy.deepcopy(duplicate_worktrees[0]))
    with pytest.raises(RepositoryPreservationError, match="unique, sorted"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: duplicate_evidence,
        )

    unsorted_evidence = _evidence(repository)
    unsorted_worktrees = unsorted_evidence["worktrees"]
    assert isinstance(unsorted_worktrees, list)
    later = copy.deepcopy(unsorted_worktrees[0])
    assert isinstance(later, dict)
    later["path"] = str(repository / "later-worktree")
    unsorted_worktrees.insert(0, later)
    with pytest.raises(RepositoryPreservationError, match="unique, sorted"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: unsorted_evidence,
        )


def test_aggregation_rejects_duplicate_status_entries(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    evidence = _evidence(repository, signals=["dirty"])
    worktrees = evidence["worktrees"]
    assert isinstance(worktrees, list)
    worktree = worktrees[0]
    assert isinstance(worktree, dict)
    status = worktree["status"]
    assert isinstance(status, dict)
    entries = status["entries"]
    assert isinstance(entries, list)
    entries.append(copy.deepcopy(entries[0]))
    status["entry_count"] = 2
    worktree["dirty_entry_count"] = 2
    counts = status["counts"]
    assert isinstance(counts, dict)
    counts["untracked"] = 2

    with pytest.raises(RepositoryPreservationError, match="unique and sorted"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: evidence,
        )


def test_aggregation_rejects_inconsistent_signal_counts(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    evidence = _evidence(repository, signals=["dirty"])
    evidence["signal_counts"] = {}

    with pytest.raises(RepositoryPreservationError, match="does not match"):
        inspect_repository_set_preservation(
            [repository],
            inspector=lambda _path: evidence,
        )


def test_aggregation_tolerates_additive_fields_within_schema_one(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    evidence = _evidence(repository)

    result = inspect_repository_set_preservation(
        [repository],
        inspector=lambda _path: evidence,
    )

    repositories = result["repositories"]
    assert isinstance(repositories, list)
    first_result = repositories[0]
    assert isinstance(first_result, dict)
    assert first_result["future_top_level"] == {"accepted": True}


def test_executable_emits_json_and_is_input_order_deterministic(
    tmp_path: Path,
) -> None:
    first = _init_repository(tmp_path / "a")
    second = _init_repository(tmp_path / "b")

    normal = subprocess.run(
        [str(_SCRIPT), str(first), str(second)],
        env=os.environ.copy(),
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    reversed_result = subprocess.run(
        [str(_SCRIPT), str(second), str(first)],
        env=os.environ.copy(),
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )

    assert normal.returncode == 0, normal.stderr
    assert reversed_result.returncode == 0, reversed_result.stderr
    assert normal.stderr == ""
    assert reversed_result.stderr == ""
    assert normal.stdout == reversed_result.stdout
    payload = json.loads(normal.stdout)
    assert payload["schema_version"] == 1
    assert payload["totals"]["repository_count"] == 2
    assert payload["totals"]["registered_worktree_count"] == 2


def test_executable_expected_failure_has_no_partial_json_or_traceback(
    tmp_path: Path,
) -> None:
    result = subprocess.run(
        [str(_SCRIPT), str(tmp_path / "missing")],
        env=os.environ.copy(),
        capture_output=True,
        check=False,
        text=True,
        timeout=10,
    )

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.startswith("error: ")
    assert "Traceback" not in result.stderr
