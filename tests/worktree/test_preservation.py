from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from projectkoios.bootstrap.worktree import preservation
from projectkoios.bootstrap.worktree.preservation import (
    PreservationInspectionError,
    inspect_repository_preservation,
    parse_status,
)


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        check=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def _init_repository(path: Path, *, remote: Path | None = None) -> Path:
    path.mkdir()
    _git(path, "init", "--quiet", "--initial-branch=main")
    _git(path, "config", "user.name", "Test")
    _git(path, "config", "user.email", "test@example.invalid")
    (path / "tracked.txt").write_text("initial\n", encoding="utf-8")
    _git(path, "add", "tracked.txt")
    _git(path, "commit", "--quiet", "-m", "initial")
    if remote is not None:
        subprocess.run(
            ("git", "init", "--bare", "--quiet", str(remote)),
            check=True,
            capture_output=True,
            timeout=10,
        )
        _git(path, "remote", "add", "origin", str(remote))
        _git(path, "push", "--quiet", "--set-upstream", "origin", "main")
    return path


def _oid(character: str) -> bytes:
    return character.encode("ascii") * 40


def test_parse_status_preserves_paths_and_status_categories() -> None:
    ordinary = b" ".join(
        (
            b"1",
            b"MM",
            b"N...",
            b"100644",
            b"100644",
            b"100644",
            _oid("a"),
            _oid("b"),
            b"tracked path.txt",
        )
    )
    renamed = b" ".join(
        (
            b"2",
            b"R.",
            b"N...",
            b"100644",
            b"100644",
            b"100644",
            _oid("c"),
            _oid("d"),
            b"R100",
            b"new name.txt",
        )
    )
    unmerged = b" ".join(
        (
            b"u",
            b"UU",
            b"N...",
            b"100644",
            b"100644",
            b"100644",
            b"100644",
            _oid("e"),
            _oid("f"),
            _oid("0"),
            b"conflict.txt",
        )
    )
    payload = (
        ordinary
        + b"\0"
        + renamed
        + b"\0old name.txt\0"
        + unmerged
        + b"\0? untracked file.txt\0"
    )

    result = parse_status(payload)

    assert result == (
        {
            "index_status": "U",
            "kind": "unmerged",
            "original_path": None,
            "path": "conflict.txt",
            "submodule": "N...",
            "worktree_status": "U",
        },
        {
            "index_status": "R",
            "kind": "renamed",
            "original_path": "old name.txt",
            "path": "new name.txt",
            "submodule": "N...",
            "worktree_status": ".",
        },
        {
            "index_status": "M",
            "kind": "ordinary",
            "original_path": None,
            "path": "tracked path.txt",
            "submodule": "N...",
            "worktree_status": "M",
        },
        {
            "index_status": None,
            "kind": "untracked",
            "original_path": None,
            "path": "untracked file.txt",
            "submodule": None,
            "worktree_status": None,
        },
    )


def test_parse_status_accepts_sha256_object_ids() -> None:
    oid = b"a" * 64
    record = b" ".join(
        (
            b"1",
            b"M.",
            b"N...",
            b"100644",
            b"100644",
            b"100644",
            oid,
            oid,
            b"tracked.txt",
        )
    )

    result = parse_status(record + b"\0", object_format="sha256")

    assert result[0]["path"] == "tracked.txt"


def test_parse_status_preserves_non_utf8_path_bytes_for_json() -> None:
    result = parse_status(b"? non-utf8-\xff\0")

    assert result[0]["path"] == os.fsdecode(b"non-utf8-\xff")
    assert "\\udcff" in json.dumps(result, ensure_ascii=True)


@pytest.mark.parametrize(
    ("field_index", "replacement", "message"),
    [
        (1, b"Z.", "tracked status"),
        (1, b"U.", "ordinary status"),
        (2, b"SXYZ", "submodule status"),
        (3, b"100600", "file mode"),
        (6, b"not-an-object-id", "object id"),
    ],
)
def test_parse_status_rejects_malformed_ordinary_fields(
    field_index: int,
    replacement: bytes,
    message: str,
) -> None:
    fields = [
        b"1",
        b"M.",
        b"N...",
        b"100644",
        b"100644",
        b"100644",
        _oid("a"),
        _oid("b"),
        b"tracked.txt",
    ]
    fields[field_index] = replacement

    with pytest.raises(PreservationInspectionError, match=message):
        parse_status(b" ".join(fields) + b"\0")


def test_parse_status_rejects_malformed_unmerged_status() -> None:
    record = b" ".join(
        (
            b"u",
            b"MM",
            b"N...",
            b"100644",
            b"100644",
            b"100644",
            b"100644",
            _oid("a"),
            _oid("b"),
            _oid("c"),
            b"conflict.txt",
        )
    )

    with pytest.raises(PreservationInspectionError, match="unmerged status"):
        parse_status(record + b"\0")


def test_parse_status_rejects_missing_terminal_nul() -> None:
    with pytest.raises(PreservationInspectionError, match="terminal NUL"):
        parse_status(b"? path")


@pytest.mark.parametrize("payload", [b"\0", b"? path\0\0"])
def test_parse_status_rejects_empty_records(payload: bytes) -> None:
    with pytest.raises(PreservationInspectionError, match="empty record"):
        parse_status(payload)


def test_revision_oid_parser_rejects_malformed_framing_and_duplicates() -> None:
    oid = _oid("a")

    assert preservation.parse_revision_oids(b"", object_format="sha1") == ()
    for payload, message in (
        (b"\n", "empty record"),
        (oid, "terminal newline"),
        (oid + b"\n\n", "empty record"),
        (oid + b"\n" + oid + b"\n", "duplicate"),
    ):
        with pytest.raises(PreservationInspectionError, match=message):
            preservation.parse_revision_oids(payload, object_format="sha1")


def test_parse_status_rejects_incomplete_rename() -> None:
    record = b" ".join(
        (
            b"2",
            b"R.",
            b"N...",
            b"100644",
            b"100644",
            b"100644",
            _oid("a"),
            _oid("b"),
            b"R100",
            b"new.txt",
        )
    )

    with pytest.raises(PreservationInspectionError, match="rename record"):
        parse_status(record + b"\0")


def test_parse_status_rejects_malformed_rename_score() -> None:
    record = b" ".join(
        (
            b"2",
            b"R.",
            b"N...",
            b"100644",
            b"100644",
            b"100644",
            _oid("a"),
            _oid("b"),
            b"R101",
            b"new.txt",
        )
    )

    with pytest.raises(PreservationInspectionError, match="rename score"):
        parse_status(record + b"\0old.txt\0")


def test_refs_and_head_require_hash_format_aware_object_ids(
    tmp_path: Path,
) -> None:
    repository = _init_repository(tmp_path / "repository")

    with pytest.raises(PreservationInspectionError, match="ref object id"):
        preservation._parse_refs(
            b"refs/remotes/origin/main\0bad\0\n",
            object_format="sha1",
        )
    with pytest.raises(PreservationInspectionError, match="terminal newline"):
        preservation._parse_refs(
            b"refs/remotes/origin/main\0" + _oid("a") + b"\0",
            object_format="sha1",
        )
    with pytest.raises(PreservationInspectionError, match="HEAD object id"):
        preservation._remote_reachability(
            repository,
            "--all",
            ["a" * 40],
            object_format="sha1",
        )


def test_reachability_uses_captured_ref_oids_not_live_ref_namespace(
    tmp_path: Path,
) -> None:
    repository = _init_repository(
        tmp_path / "repository",
        remote=tmp_path / "remote.git",
    )
    captured_remote_oid = _git(
        repository, "rev-parse", "refs/remotes/origin/main"
    )
    (repository / "local.txt").write_text("local\n", encoding="utf-8")
    _git(repository, "add", "local.txt")
    _git(repository, "commit", "--quiet", "-m", "local")
    local_head = _git(repository, "rev-parse", "HEAD")
    _git(
        repository,
        "update-ref",
        "refs/remotes/origin/main",
        local_head,
    )

    result = preservation._remote_reachability(
        repository,
        local_head,
        [captured_remote_oid],
        object_format="sha1",
    )

    assert result["available"] is True
    assert result["oid_count"] == 1
    assert result["oids"] == [local_head]


def test_inspection_reports_dirty_paths_and_commits_not_on_known_remotes(
    tmp_path: Path,
) -> None:
    repository = _init_repository(
        tmp_path / "repository",
        remote=tmp_path / "remote.git",
    )
    (repository / "local.txt").write_text("local commit\n", encoding="utf-8")
    _git(repository, "add", "local.txt")
    _git(repository, "commit", "--quiet", "-m", "local")
    local_head = _git(repository, "rev-parse", "HEAD")
    (repository / "tracked.txt").write_text("staged\n", encoding="utf-8")
    _git(repository, "add", "tracked.txt")
    (repository / "tracked.txt").write_text("unstaged\n", encoding="utf-8")
    (repository / "untracked.txt").write_text("untracked\n", encoding="utf-8")
    status_before = _git(repository, "status", "--porcelain=v2")
    refs_before = _git(repository, "show-ref")

    evidence = inspect_repository_preservation(repository)

    assert _git(repository, "status", "--porcelain=v2") == status_before
    assert _git(repository, "show-ref") == refs_before
    assert evidence["schema_version"] == 1
    repository_evidence = evidence["repository"]
    assert isinstance(repository_evidence, dict)
    assert repository_evidence["remote_tracking_ref_count"] == 1
    assert repository_evidence["remote_tracking_refs"] == [
        {
            "oid": _git(repository, "rev-parse", "refs/remotes/origin/main"),
            "ref": "refs/remotes/origin/main",
            "symbolic_target": None,
        }
    ]
    assert isinstance(repository_evidence["remote_tracking_refs_digest"], str)
    contract = evidence["contract"]
    assert isinstance(contract, dict)
    assert contract["deletion_safety_assessed"] is False
    worktrees = evidence["worktrees"]
    assert isinstance(worktrees, list)
    assert len(worktrees) == 1
    worktree = worktrees[0]
    assert worktree["preservation_signals"] == [
        "commits_not_on_known_remotes",
        "dirty",
        "upstream_ahead",
    ]
    assert worktree["status"]["counts"] == {
        "conflicted": 0,
        "staged": 1,
        "submodule": 0,
        "tracked": 1,
        "unstaged": 1,
        "untracked": 1,
    }
    assert [entry["path"] for entry in worktree["status"]["entries"]] == [
        "tracked.txt",
        "untracked.txt",
    ]
    reachability = worktree["remote_reachability"]
    assert reachability["available"] is True
    assert reachability["oid_count"] == 1
    assert reachability["oids"] == [local_head]
    assert reachability["oids_truncated"] is False


def test_inspection_reports_unknown_reachability_without_remote_refs(
    tmp_path: Path,
) -> None:
    repository = _init_repository(tmp_path / "repository")

    evidence = inspect_repository_preservation(repository)

    worktrees = evidence["worktrees"]
    assert isinstance(worktrees, list)
    worktree = worktrees[0]
    assert isinstance(worktree, dict)
    assert worktree["remote_reachability"] == {
        "available": False,
        "oid_count": None,
        "oid_digest": None,
        "oids": None,
        "oids_truncated": None,
        "reason": "remote_tracking_refs_unavailable",
        "scope": "locally_known_remote_tracking_refs",
    }
    assert worktree["preservation_signals"] == [
        "remote_reachability_unknown",
        "upstream_comparison_unknown",
    ]


def test_inspection_preserves_missing_prunable_worktree_as_evidence(
    tmp_path: Path,
) -> None:
    repository = _init_repository(
        tmp_path / "repository",
        remote=tmp_path / "remote.git",
    )
    worktree_path = tmp_path / "worktree"
    _git(
        repository,
        "worktree",
        "add",
        "--quiet",
        "-b",
        "topic",
        str(worktree_path),
    )
    shutil.rmtree(worktree_path)

    evidence = inspect_repository_preservation(repository)

    worktrees = evidence["worktrees"]
    assert isinstance(worktrees, list)
    typed_worktrees = [item for item in worktrees if isinstance(item, dict)]
    assert len(typed_worktrees) == len(worktrees)
    missing = next(
        item for item in typed_worktrees if item["path"] == str(worktree_path)
    )
    assert missing["missing"] is True
    assert missing["prunable"] is True
    status = missing["status"]
    assert isinstance(status, dict)
    assert status["available"] is False
    assert status["reason"] == "worktree_not_inspectable"
    signals = missing["preservation_signals"]
    assert isinstance(signals, list)
    assert {"missing", "prunable", "uninspectable"}.issubset(signals)


def test_inspection_rejects_status_change_after_inventory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = _init_repository(tmp_path / "repository")
    real_git = preservation._git
    changed = False

    def mutate_after_refs(
        repository_path: str | Path,
        *arguments: str,
        allowed: tuple[int, ...] = (0,),
    ) -> subprocess.CompletedProcess[bytes]:
        nonlocal changed
        result = real_git(repository_path, *arguments, allowed=allowed)
        if arguments[:1] == ("for-each-ref",) and not changed:
            changed = True
            (repository / "tracked.txt").write_text(
                "changed\n", encoding="utf-8"
            )
        return result

    monkeypatch.setattr(preservation, "_git", mutate_after_refs)

    with pytest.raises(
        preservation.RepositoryChanged,
        match="status changed during inspection",
    ):
        inspect_repository_preservation(repository)


def test_json_evidence_round_trips_without_non_json_values(
    tmp_path: Path,
) -> None:
    repository = _init_repository(tmp_path / "repository")

    encoded = json.dumps(
        inspect_repository_preservation(repository), sort_keys=True
    )

    assert json.loads(encoded)["repository"]["path"] == str(repository)
