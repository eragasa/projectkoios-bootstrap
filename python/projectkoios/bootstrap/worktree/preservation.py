"""Read-only preservation evidence for registered Git worktrees.

The inspection extends the existing worktree inventory with structured status
paths and commit reachability against locally known remote-tracking refs. It
reports facts and preservation signals only. It never decides that a worktree
is safe to delete, classifies file contents, contacts a remote, or mutates Git.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from projectkoios.bootstrap.git.client import GitClient, GitCommandError
from projectkoios.bootstrap.worktree.inventory import InventoryError
from projectkoios.bootstrap.worktree.inventory import (
    collect as collect_inventory,
)

_MAX_REPORTED_UNPUBLISHED_OIDS = 100
_OBJECT_FORMAT_LENGTHS = {"sha1": 40, "sha256": 64}
_STATUS_KINDS = frozenset({b"1", b"2", b"?", b"u"})
_STATUS_CHARACTERS = frozenset(b".MTADRCU")
_UNMERGED_STATUSES = frozenset(
    {b"DD", b"AU", b"UD", b"UA", b"DU", b"AA", b"UU"}
)
_FILE_MODES = frozenset({b"000000", b"100644", b"100755", b"120000", b"160000"})
_SUBMODULE_PATTERN = re.compile(rb"^(?:N\.\.\.|S[.C][.M][.U])$")
_RENAME_SCORE_PATTERN = re.compile(rb"^[RC](?:100|[0-9]{1,2})$")
_GIT = GitClient(
    disable_optional_locks=True,
    preserve_global_config=False,
)


class PreservationInspectionError(RuntimeError):
    """Preservation evidence could not be produced safely."""


class RepositoryChanged(PreservationInspectionError):
    """Repository evidence changed during inspection."""


def _git(
    repository: str | Path,
    *arguments: str,
    allowed: Sequence[int] = (0,),
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return _GIT.run(
            repository,
            *arguments,
            allowed=allowed,
            input_bytes=input_bytes,
        )
    except GitCommandError as error:
        raise PreservationInspectionError(str(error)) from error


def _decode(value: bytes) -> str:
    return os.fsdecode(value)


def _object_format_length(object_format: str) -> int:
    try:
        return _OBJECT_FORMAT_LENGTHS[object_format]
    except KeyError as error:
        raise PreservationInspectionError(
            f"unsupported Git object format: {object_format!r}"
        ) from error


def _valid_oid_bytes(value: bytes, object_format: str) -> bool:
    length = _object_format_length(object_format)
    return len(value) == length and all(
        character in b"0123456789abcdef" for character in value
    )


def _valid_oid_text(value: object, object_format: str) -> bool:
    if not isinstance(value, str):
        return False
    try:
        encoded = value.encode("ascii", errors="strict")
    except UnicodeEncodeError:
        return False
    return _valid_oid_bytes(encoded, object_format)


def _status_entry(
    field: bytes,
    *,
    object_format: str,
    original_path: bytes | None = None,
) -> dict[str, object]:
    kind = field[:1]
    if kind not in _STATUS_KINDS:
        raise PreservationInspectionError(
            "unrecognized porcelain-v2 status record"
        )
    if kind == b"?":
        prefix, separator, path = field.partition(b" ")
        if prefix != b"?" or not separator or not path:
            raise PreservationInspectionError(
                "malformed porcelain-v2 untracked record"
            )
        return {
            "index_status": None,
            "kind": "untracked",
            "original_path": None,
            "path": _decode(path),
            "submodule": None,
            "worktree_status": None,
        }

    limits = {b"1": 8, b"2": 9, b"u": 10}
    parts = field.split(b" ", limits[kind])
    expected = limits[kind] + 1
    if len(parts) != expected or parts[0] != kind or not parts[-1]:
        raise PreservationInspectionError(
            "malformed porcelain-v2 tracked record"
        )
    xy = parts[1]
    submodule = parts[2]
    if len(xy) != 2 or any(value not in _STATUS_CHARACTERS for value in xy):
        raise PreservationInspectionError(
            "malformed porcelain-v2 tracked status"
        )
    if _SUBMODULE_PATTERN.fullmatch(submodule) is None:
        raise PreservationInspectionError(
            "malformed porcelain-v2 submodule status"
        )
    mode_fields = parts[3:7] if kind == b"u" else parts[3:6]
    oid_fields = parts[7:10] if kind == b"u" else parts[6:8]
    if any(mode not in _FILE_MODES for mode in mode_fields):
        raise PreservationInspectionError("malformed porcelain-v2 file mode")
    if any(not _valid_oid_bytes(oid, object_format) for oid in oid_fields):
        raise PreservationInspectionError("malformed porcelain-v2 object id")
    if kind == b"u" and xy not in _UNMERGED_STATUSES:
        raise PreservationInspectionError(
            "malformed porcelain-v2 unmerged status"
        )
    if kind == b"1" and any(value in b"RCU" for value in xy):
        raise PreservationInspectionError(
            "malformed porcelain-v2 ordinary status"
        )
    if kind == b"2" and xy[1:] in b"RCU":
        raise PreservationInspectionError(
            "malformed porcelain-v2 renamed status"
        )
    if kind != b"u" and xy == b"..":
        raise PreservationInspectionError(
            "malformed porcelain-v2 clean tracked record"
        )
    if kind == b"2" and (
        _RENAME_SCORE_PATTERN.fullmatch(parts[8]) is None
        or parts[8][:1] != xy[:1]
    ):
        raise PreservationInspectionError("malformed porcelain-v2 rename score")
    if kind == b"2" and not original_path:
        raise PreservationInspectionError(
            "malformed porcelain-v2 rename record"
        )
    if kind != b"2" and original_path is not None:
        raise PreservationInspectionError(
            "unexpected porcelain-v2 original path"
        )
    names = {b"1": "ordinary", b"2": "renamed", b"u": "unmerged"}
    return {
        "index_status": _decode(xy[:1]),
        "kind": names[kind],
        "original_path": _decode(original_path)
        if original_path is not None
        else None,
        "path": _decode(parts[-1]),
        "submodule": _decode(submodule),
        "worktree_status": _decode(xy[1:]),
    }


def parse_status(
    payload: bytes,
    *,
    object_format: str = "sha1",
) -> tuple[dict[str, object], ...]:
    """Parse NUL-delimited porcelain-v2 status without reading file content."""
    _object_format_length(object_format)
    if not payload:
        return ()
    if not payload.endswith(b"\0"):
        raise PreservationInspectionError(
            "porcelain-v2 status is missing terminal NUL"
        )
    fields = payload[:-1].split(b"\0")
    if any(not field for field in fields):
        raise PreservationInspectionError(
            "porcelain-v2 status contains an empty record"
        )
    entries: list[dict[str, object]] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if field[:1] == b"2":
            if index >= len(fields) or not fields[index]:
                raise PreservationInspectionError(
                    "malformed porcelain-v2 rename record"
                )
            original_path = fields[index]
            index += 1
            entries.append(
                _status_entry(
                    field,
                    object_format=object_format,
                    original_path=original_path,
                )
            )
        else:
            entries.append(_status_entry(field, object_format=object_format))
    return tuple(
        sorted(
            entries,
            key=lambda item: (
                str(item["path"]),
                str(item["kind"]),
                str(item["original_path"]),
            ),
        )
    )


def status_counts(entries: Sequence[Mapping[str, object]]) -> dict[str, int]:
    return {
        "conflicted": sum(entry["kind"] == "unmerged" for entry in entries),
        "staged": sum(
            entry["index_status"] not in (None, ".") for entry in entries
        ),
        "submodule": sum(
            isinstance(entry["submodule"], str) and entry["submodule"] != "N..."
            for entry in entries
        ),
        "tracked": sum(entry["kind"] != "untracked" for entry in entries),
        "unstaged": sum(
            entry["worktree_status"] not in (None, ".") for entry in entries
        ),
        "untracked": sum(entry["kind"] == "untracked" for entry in entries),
    }


def _parse_refs(
    payload: bytes,
    *,
    object_format: str,
) -> tuple[tuple[str, str, str], ...]:
    _object_format_length(object_format)
    if payload and not payload.endswith(b"\n"):
        raise PreservationInspectionError(
            "for-each-ref output is missing terminal newline"
        )
    refs: list[tuple[str, str, str]] = []
    for line in payload.splitlines():
        fields = line.split(b"\0")
        if len(fields) != 3 or not fields[0]:
            raise PreservationInspectionError("malformed for-each-ref output")
        if not _valid_oid_bytes(fields[1], object_format):
            raise PreservationInspectionError(
                "malformed for-each-ref object id"
            )
        refs.append(
            (_decode(fields[0]), _decode(fields[1]), _decode(fields[2]))
        )
    return tuple(refs)


def parse_revision_oids(
    payload: bytes,
    *,
    object_format: str,
) -> tuple[str, ...]:
    """Validate newline-delimited ``rev-list`` output."""
    _object_format_length(object_format)
    if not payload:
        return ()
    if not payload.endswith(b"\n"):
        raise PreservationInspectionError(
            "rev-list output is missing terminal newline"
        )
    lines = payload[:-1].split(b"\n")
    if any(not line for line in lines):
        raise PreservationInspectionError(
            "rev-list output contains an empty record"
        )
    if any(not _valid_oid_bytes(oid, object_format) for oid in lines):
        raise PreservationInspectionError("malformed rev-list object id")
    decoded = tuple(_decode(oid) for oid in lines)
    if len(set(decoded)) != len(decoded):
        raise PreservationInspectionError(
            "rev-list output contains a duplicate object id"
        )
    return decoded


def _remote_reachability(
    repository: Path,
    head: object,
    remote_ref_oids: Sequence[str],
    *,
    object_format: str,
) -> dict[str, object]:
    if head is None:
        return {
            "available": False,
            "oid_count": None,
            "oid_digest": None,
            "oids": None,
            "oids_truncated": None,
            "reason": "head_unavailable",
            "scope": "locally_known_remote_tracking_refs",
        }
    if not _valid_oid_text(head, object_format):
        raise PreservationInspectionError("malformed worktree HEAD object id")
    assert isinstance(head, str)
    if not remote_ref_oids:
        return {
            "available": False,
            "oid_count": None,
            "oid_digest": None,
            "oids": None,
            "oids_truncated": None,
            "reason": "remote_tracking_refs_unavailable",
            "scope": "locally_known_remote_tracking_refs",
        }
    if any(not _valid_oid_text(oid, object_format) for oid in remote_ref_oids):
        raise PreservationInspectionError(
            "malformed remote-tracking ref object id"
        )
    revision_input = (
        "\n".join(
            (head, *(f"^{oid}" for oid in sorted(set(remote_ref_oids))))
        ).encode("ascii")
        + b"\n"
    )
    result = _git(
        repository,
        "rev-list",
        "--stdin",
        allowed=(0, 128),
        input_bytes=revision_input,
    )
    if result.returncode != 0:
        return {
            "available": False,
            "oid_count": None,
            "oid_digest": None,
            "oids": None,
            "oids_truncated": None,
            "reason": "comparison_failed",
            "scope": "locally_known_remote_tracking_refs",
        }
    oids = sorted(
        parse_revision_oids(
            result.stdout,
            object_format=object_format,
        )
    )
    digest_input = b"\n".join(oid.encode("ascii") for oid in oids)
    return {
        "available": True,
        "oid_count": len(oids),
        "oid_digest": hashlib.sha256(digest_input).hexdigest(),
        "oids": oids[:_MAX_REPORTED_UNPUBLISHED_OIDS],
        "oids_truncated": len(oids) > _MAX_REPORTED_UNPUBLISHED_OIDS,
        "reason": None,
        "scope": "locally_known_remote_tracking_refs",
    }


def preservation_signals(worktree: Mapping[str, Any]) -> list[str]:
    signals: set[str] = set()
    status = worktree["status"]
    reachability = worktree["remote_reachability"]
    if not isinstance(status, Mapping) or not isinstance(reachability, Mapping):
        raise PreservationInspectionError("invalid internal worktree evidence")
    if status["available"] and status["entry_count"]:
        signals.add("dirty")
    if not reachability["available"]:
        signals.add("remote_reachability_unknown")
    elif reachability["oid_count"]:
        signals.add("commits_not_on_known_remotes")
    if worktree["missing"]:
        signals.add("missing")
    if worktree["prunable"]:
        signals.add("prunable")
    if worktree["locked"]:
        signals.add("locked")
    if not worktree["inspectable"]:
        signals.add("uninspectable")
    if worktree["state"] != "branch":
        signals.add("non_branch")
    index_flags = worktree["index_flags"]
    if not isinstance(index_flags, Mapping):
        raise PreservationInspectionError("invalid internal index flags")
    hidden_count = sum(
        value
        for key in ("assume_unchanged_count", "skip_worktree_count")
        if isinstance((value := index_flags[key]), int)
    )
    if hidden_count:
        signals.add("hidden_index_flags")
    upstream = worktree["upstream"]
    if not isinstance(upstream, Mapping) or not upstream.get("comparable"):
        signals.add("upstream_comparison_unknown")
    else:
        ahead = upstream.get("ahead")
        behind = upstream.get("behind")
        if isinstance(ahead, int) and ahead:
            signals.add("upstream_ahead")
        if isinstance(behind, int) and behind:
            signals.add("upstream_behind")
        if (
            isinstance(ahead, int)
            and isinstance(behind, int)
            and ahead
            and behind
        ):
            signals.add("upstream_diverged")
    return sorted(signals)


def _canonical_repository(supplied: str | Path) -> Path:
    path = Path(supplied)
    if not path.is_absolute():
        raise PreservationInspectionError("repository path must be absolute")
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise PreservationInspectionError(
            "repository path is unavailable"
        ) from error
    if resolved != path:
        raise PreservationInspectionError(
            f"repository path must be canonical: {resolved}"
        )
    top = _git(
        resolved,
        "rev-parse",
        "--path-format=absolute",
        "--show-toplevel",
        allowed=(0, 128),
    )
    if top.returncode != 0 or _decode(top.stdout.rstrip(b"\n")) != str(
        resolved
    ):
        raise PreservationInspectionError(
            "repository path must be a non-bare worktree root"
        )
    return resolved


def inspect_repository_preservation(
    supplied: str | Path,
) -> dict[str, object]:
    """Return stable preservation evidence for one repository."""
    repository = _canonical_repository(supplied)
    try:
        before_inventory, before_witness = collect_inventory(str(repository))
    except InventoryError as error:
        raise PreservationInspectionError(str(error)) from error

    object_format_payload = _git(
        repository, "rev-parse", "--show-object-format"
    ).stdout
    if (
        not object_format_payload.endswith(b"\n")
        or object_format_payload.count(b"\n") != 1
    ):
        raise PreservationInspectionError("malformed Git object-format output")
    object_format = _decode(object_format_payload[:-1])
    _object_format_length(object_format)
    refs = _git(
        repository,
        "for-each-ref",
        "--format=%(refname)%00%(objectname)%00%(symref)",
    ).stdout
    if hashlib.sha256(refs).hexdigest() != before_witness["refs_digest"]:
        raise RepositoryChanged("repository refs changed during inspection")
    parsed_refs = _parse_refs(refs, object_format=object_format)
    remote_refs = [
        {
            "oid": oid,
            "ref": ref_name,
            "symbolic_target": symbolic or None,
        }
        for ref_name, oid, symbolic in parsed_refs
        if ref_name.startswith("refs/remotes/")
    ]
    remote_refs.sort(key=lambda item: str(item["ref"]))
    remote_ref_oids = [str(item["oid"]) for item in remote_refs]
    remote_ref_count = len(remote_refs)
    remote_refs_encoded = json.dumps(
        remote_refs,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")

    witness_by_path = {
        item["metadata"]["worktree"]: item
        for item in before_witness["worktrees"]
    }
    worktrees: list[dict[str, object]] = []
    inventory_worktrees = before_inventory["worktrees"]
    if not isinstance(inventory_worktrees, list):
        raise PreservationInspectionError("inventory worktrees must be a list")
    for source in inventory_worktrees:
        if not isinstance(source, Mapping):
            raise PreservationInspectionError(
                "inventory worktree must be an object"
            )
        worktree: dict[str, Any] = dict(source)
        path_value = worktree.get("path")
        if not isinstance(path_value, str):
            raise PreservationInspectionError("worktree path must be text")
        witness = witness_by_path.get(path_value)
        if not isinstance(witness, Mapping):
            raise PreservationInspectionError("worktree witness is unavailable")

        if worktree.get("inspectable") and worktree.get("state") != "bare":
            status_payload = _git(
                path_value,
                "status",
                "--porcelain=v2",
                "-z",
                "--untracked-files=all",
                "--ignore-submodules=none",
            ).stdout
            if hashlib.sha256(status_payload).hexdigest() != witness.get(
                "status_digest"
            ):
                raise RepositoryChanged(
                    f"worktree status changed during inspection: {path_value}"
                )
            entries = parse_status(
                status_payload,
                object_format=object_format,
            )
            status: dict[str, object] = {
                "available": True,
                "counts": status_counts(entries),
                "digest": hashlib.sha256(status_payload).hexdigest(),
                "entries": list(entries),
                "entry_count": len(entries),
                "reason": None,
            }
        else:
            reason = (
                "bare_worktree"
                if worktree.get("state") == "bare"
                else ("worktree_not_inspectable")
            )
            status = {
                "available": False,
                "counts": None,
                "digest": None,
                "entries": None,
                "entry_count": None,
                "reason": reason,
            }
        worktree["status"] = status
        worktree["remote_reachability"] = _remote_reachability(
            repository,
            worktree.get("head"),
            remote_ref_oids,
            object_format=object_format,
        )
        worktree["preservation_signals"] = preservation_signals(worktree)
        worktrees.append(worktree)

    try:
        after_inventory, after_witness = collect_inventory(str(repository))
    except InventoryError as error:
        raise PreservationInspectionError(str(error)) from error
    if before_witness != after_witness or before_inventory != after_inventory:
        raise RepositoryChanged(
            "repository state changed during inspection; no evidence emitted"
        )

    signal_counts: dict[str, int] = {}
    for worktree in worktrees:
        signals = worktree["preservation_signals"]
        if not isinstance(signals, list):
            raise PreservationInspectionError(
                "preservation signals must be a list"
            )
        for signal in signals:
            if not isinstance(signal, str):
                raise PreservationInspectionError(
                    "preservation signal must be text"
                )
            signal_counts[signal] = signal_counts.get(signal, 0) + 1

    repository_value = before_inventory["repository"]
    if not isinstance(repository_value, Mapping):
        raise PreservationInspectionError(
            "inventory repository must be an object"
        )
    return {
        "contract": {
            "content_semantics_assessed": False,
            "deletion_safety_assessed": False,
            "github_state_assessed": False,
            "migration_safety_assessed": False,
            "purpose": (
                "Read-only preservation evidence for registered worktrees"
            ),
            "remote_reachability_scope": (
                "locally known remote-tracking refs; no fetch is performed"
            ),
        },
        "repository": {
            **dict(repository_value),
            "object_format": object_format,
            "remote_tracking_ref_count": remote_ref_count,
            "remote_tracking_refs": remote_refs,
            "remote_tracking_refs_digest": hashlib.sha256(
                remote_refs_encoded
            ).hexdigest(),
        },
        "schema_version": 1,
        "signal_counts": dict(sorted(signal_counts.items())),
        "worktrees": worktrees,
    }


def _encode_json(result: Mapping[str, object]) -> str:
    try:
        return (
            json.dumps(
                result,
                allow_nan=False,
                ensure_ascii=True,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
    except (TypeError, ValueError) as error:
        raise PreservationInspectionError(
            "preservation evidence is not JSON-compatible"
        ) from error


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        result = inspect_repository_preservation(arguments.repository)
        encoded = _encode_json(result)
    except PreservationInspectionError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
