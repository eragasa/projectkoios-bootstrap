"""Deterministic preservation evidence across an explicit repository set."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from projectkoios.bootstrap.repository.summary import (
    RepositorySummaryError,
    summarize_repository,
)
from projectkoios.bootstrap.worktree.preservation import (
    PreservationInspectionError,
    inspect_repository_preservation,
    preservation_signals,
    status_counts,
)

RepositoryInspector = Callable[[str | Path], object]

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_OBJECT_FORMAT_LENGTHS = {"sha1": 40, "sha256": 64}
_STATUS_CHARACTERS = frozenset(".MTADRCU")
_UNMERGED_STATUSES = frozenset({"DD", "AU", "UD", "UA", "DU", "AA", "UU"})
_SUBMODULE_PATTERN = re.compile(r"^(?:N\.\.\.|S[.C][.M][.U])$")
_REACHABILITY_REASONS = frozenset(
    {
        "comparison_failed",
        "head_unavailable",
        "remote_tracking_refs_unavailable",
    }
)


class RepositoryPreservationError(RuntimeError):
    """Repository-set preservation evidence could not be produced safely."""


def _required(mapping: Mapping[str, Any], key: str, label: str) -> Any:
    try:
        return mapping[key]
    except KeyError as error:
        raise RepositoryPreservationError(
            f"{label} is missing required field {key!r}"
        ) from error


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RepositoryPreservationError(f"{label} must be an object")
    return value


def _sequence(value: object, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise RepositoryPreservationError(f"{label} must be a sequence")
    return value


def _non_negative_count(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RepositoryPreservationError(
            f"{label} must be a non-negative integer"
        )
    return value


def _boolean(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise RepositoryPreservationError(f"{label} must be a boolean")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RepositoryPreservationError(f"{label} must be non-empty text")
    return value


def _nullable_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _text(value, label)


def _sha256(value: object, label: str) -> str:
    text = _text(value, label)
    if _SHA256_PATTERN.fullmatch(text) is None:
        raise RepositoryPreservationError(f"{label} must be a SHA-256 digest")
    return text


def _valid_oid(value: object, object_format: str) -> bool:
    length = _OBJECT_FORMAT_LENGTHS[object_format]
    return (
        isinstance(value, str)
        and len(value) == length
        and all(character in "0123456789abcdef" for character in value)
    )


def _validate_contract(evidence: Mapping[str, Any]) -> None:
    contract = _mapping(
        _required(evidence, "contract", "evidence"),
        "evidence.contract",
    )
    for field in (
        "content_semantics_assessed",
        "deletion_safety_assessed",
        "github_state_assessed",
        "migration_safety_assessed",
    ):
        if _boolean(
            _required(contract, field, "evidence.contract"),
            f"evidence.contract.{field}",
        ):
            raise RepositoryPreservationError(
                f"evidence.contract.{field} must be false"
            )
    _text(
        _required(contract, "purpose", "evidence.contract"),
        "evidence.contract.purpose",
    )
    scope = _text(
        _required(
            contract,
            "remote_reachability_scope",
            "evidence.contract",
        ),
        "evidence.contract.remote_reachability_scope",
    )
    if scope != "locally known remote-tracking refs; no fetch is performed":
        raise RepositoryPreservationError(
            "evidence.contract.remote_reachability_scope is invalid"
        )


def _validate_repository_refs(
    repository: Mapping[str, Any],
) -> tuple[str, int]:
    object_format = _text(
        _required(repository, "object_format", "evidence.repository"),
        "evidence.repository.object_format",
    )
    if object_format not in _OBJECT_FORMAT_LENGTHS:
        raise RepositoryPreservationError(
            "evidence.repository.object_format is unsupported"
        )
    refs_value = _sequence(
        _required(
            repository,
            "remote_tracking_refs",
            "evidence.repository",
        ),
        "evidence.repository.remote_tracking_refs",
    )
    refs: list[dict[str, object]] = []
    ref_names: list[str] = []
    for index, value in enumerate(refs_value):
        label = f"evidence.repository.remote_tracking_refs[{index}]"
        ref = _mapping(value, label)
        ref_name = _text(_required(ref, "ref", label), f"{label}.ref")
        if not ref_name.startswith("refs/remotes/"):
            raise RepositoryPreservationError(
                f"{label}.ref must be a remote-tracking ref"
            )
        oid = _required(ref, "oid", label)
        if not _valid_oid(oid, object_format):
            raise RepositoryPreservationError(
                f"{label}.oid must match the repository object format"
            )
        symbolic = _nullable_text(
            _required(ref, "symbolic_target", label),
            f"{label}.symbolic_target",
        )
        refs.append({"oid": oid, "ref": ref_name, "symbolic_target": symbolic})
        ref_names.append(ref_name)
    if ref_names != sorted(set(ref_names)):
        raise RepositoryPreservationError(
            "evidence.repository.remote_tracking_refs must be unique and sorted"
        )
    expected_count = _non_negative_count(
        _required(
            repository,
            "remote_tracking_ref_count",
            "evidence.repository",
        ),
        "evidence.repository.remote_tracking_ref_count",
    )
    if expected_count != len(refs):
        raise RepositoryPreservationError(
            "evidence.repository.remote_tracking_ref_count is inconsistent"
        )
    encoded = json.dumps(
        refs,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("ascii")
    observed_digest = _sha256(
        _required(
            repository,
            "remote_tracking_refs_digest",
            "evidence.repository",
        ),
        "evidence.repository.remote_tracking_refs_digest",
    )
    if observed_digest != hashlib.sha256(encoded).hexdigest():
        raise RepositoryPreservationError(
            "evidence.repository.remote_tracking_refs_digest is inconsistent"
        )
    return object_format, expected_count


def _validate_status_entry(value: object, label: str) -> Mapping[str, object]:
    entry = _mapping(value, label)
    kind = _text(_required(entry, "kind", label), f"{label}.kind")
    if kind not in {"ordinary", "renamed", "unmerged", "untracked"}:
        raise RepositoryPreservationError(f"{label}.kind is invalid")
    path = _text(_required(entry, "path", label), f"{label}.path")
    original = _required(entry, "original_path", label)
    index_status = _required(entry, "index_status", label)
    worktree_status = _required(entry, "worktree_status", label)
    submodule = _required(entry, "submodule", label)
    if kind == "untracked":
        if any(
            item is not None
            for item in (original, index_status, worktree_status, submodule)
        ):
            raise RepositoryPreservationError(
                f"{label} untracked fields must be null"
            )
    else:
        index_status = _text(index_status, f"{label}.index_status")
        worktree_status = _text(worktree_status, f"{label}.worktree_status")
        submodule = _text(submodule, f"{label}.submodule")
        if (
            len(index_status) != 1
            or len(worktree_status) != 1
            or index_status not in _STATUS_CHARACTERS
            or worktree_status not in _STATUS_CHARACTERS
        ):
            raise RepositoryPreservationError(
                f"{label} status fields are invalid"
            )
        if _SUBMODULE_PATTERN.fullmatch(submodule) is None:
            raise RepositoryPreservationError(f"{label}.submodule is invalid")
        if kind == "unmerged" and (
            index_status + worktree_status not in _UNMERGED_STATUSES
        ):
            raise RepositoryPreservationError(
                f"{label} unmerged status is invalid"
            )
        if kind == "ordinary" and any(
            value in "RCU" for value in (index_status, worktree_status)
        ):
            raise RepositoryPreservationError(
                f"{label} ordinary status is invalid"
            )
        if kind == "renamed" and (
            index_status not in "RC" or worktree_status in "RCU"
        ):
            raise RepositoryPreservationError(
                f"{label} renamed status is invalid"
            )
        if kind == "renamed":
            _text(original, f"{label}.original_path")
        elif original is not None:
            raise RepositoryPreservationError(
                f"{label}.original_path must be null"
            )
    return {
        "index_status": index_status,
        "kind": kind,
        "original_path": original,
        "path": path,
        "submodule": submodule,
        "worktree_status": worktree_status,
    }


def _validate_status(
    worktree: Mapping[str, Any],
    label: str,
) -> None:
    status = _mapping(
        _required(worktree, "status", label),
        f"{label}.status",
    )
    available = _boolean(
        _required(status, "available", f"{label}.status"),
        f"{label}.status.available",
    )
    reason = _required(status, "reason", f"{label}.status")
    expected_available = bool(worktree["inspectable"]) and (
        worktree["state"] != "bare"
    )
    if available != expected_available:
        raise RepositoryPreservationError(
            f"{label}.status availability contradicts worktree evidence"
        )
    if not available:
        if _text(reason, f"{label}.status.reason") not in {
            "bare_worktree",
            "worktree_not_inspectable",
        }:
            raise RepositoryPreservationError(
                f"{label}.status.reason is invalid"
            )
        if worktree["dirty_entry_count"] is not None:
            raise RepositoryPreservationError(
                f"{label}.dirty_entry_count must be null when unavailable"
            )
        for field in ("counts", "digest", "entries", "entry_count"):
            if _required(status, field, f"{label}.status") is not None:
                raise RepositoryPreservationError(
                    f"{label}.status.{field} must be null when unavailable"
                )
        return
    if reason is not None:
        raise RepositoryPreservationError(
            f"{label}.status.reason must be null when available"
        )
    digest = _sha256(
        _required(status, "digest", f"{label}.status"),
        f"{label}.status.digest",
    )
    assert digest
    entries_value = _sequence(
        _required(status, "entries", f"{label}.status"),
        f"{label}.status.entries",
    )
    entries = [
        _validate_status_entry(value, f"{label}.status.entries[{index}]")
        for index, value in enumerate(entries_value)
    ]
    keys = [
        (str(entry["path"]), str(entry["kind"]), str(entry["original_path"]))
        for entry in entries
    ]
    if keys != sorted(set(keys)):
        raise RepositoryPreservationError(
            f"{label}.status.entries must be unique and sorted"
        )
    entry_count = _non_negative_count(
        _required(status, "entry_count", f"{label}.status"),
        f"{label}.status.entry_count",
    )
    if entry_count != len(entries):
        raise RepositoryPreservationError(
            f"{label}.status.entry_count is inconsistent"
        )
    dirty_count = _required(worktree, "dirty_entry_count", label)
    if dirty_count != entry_count:
        raise RepositoryPreservationError(
            f"{label}.dirty_entry_count does not match status entries"
        )
    counts = _mapping(
        _required(status, "counts", f"{label}.status"),
        f"{label}.status.counts",
    )
    expected_counts = status_counts(entries)
    observed_counts = {
        field: _non_negative_count(
            _required(counts, field, f"{label}.status.counts"),
            f"{label}.status.counts.{field}",
        )
        for field in expected_counts
    }
    if observed_counts != expected_counts:
        raise RepositoryPreservationError(
            f"{label}.status.counts is inconsistent"
        )


def _validate_reachability(
    worktree: Mapping[str, Any],
    label: str,
    object_format: str,
    remote_ref_count: int,
) -> None:
    reachability = _mapping(
        _required(worktree, "remote_reachability", label),
        f"{label}.remote_reachability",
    )
    available = _boolean(
        _required(
            reachability,
            "available",
            f"{label}.remote_reachability",
        ),
        f"{label}.remote_reachability.available",
    )
    scope = _text(
        _required(reachability, "scope", f"{label}.remote_reachability"),
        f"{label}.remote_reachability.scope",
    )
    if scope != "locally_known_remote_tracking_refs":
        raise RepositoryPreservationError(
            f"{label}.remote_reachability.scope is invalid"
        )
    fields = ("oid_count", "oid_digest", "oids", "oids_truncated")
    if not available:
        reason = _text(
            _required(reachability, "reason", f"{label}.remote_reachability"),
            f"{label}.remote_reachability.reason",
        )
        if reason not in _REACHABILITY_REASONS:
            raise RepositoryPreservationError(
                f"{label}.remote_reachability.reason is invalid"
            )
        if reason == "head_unavailable" and worktree["head"] is not None:
            raise RepositoryPreservationError(
                f"{label}.remote_reachability reason contradicts HEAD"
            )
        if reason == "remote_tracking_refs_unavailable" and remote_ref_count:
            raise RepositoryPreservationError(
                f"{label}.remote_reachability reason contradicts ref evidence"
            )
        if reason == "comparison_failed" and (
            worktree["head"] is None or remote_ref_count == 0
        ):
            raise RepositoryPreservationError(
                f"{label}.remote_reachability reason lacks comparison inputs"
            )
        for field in fields:
            if (
                _required(
                    reachability,
                    field,
                    f"{label}.remote_reachability",
                )
                is not None
            ):
                raise RepositoryPreservationError(
                    f"{label}.remote_reachability.{field} must be null "
                    "when unavailable"
                )
        return
    if remote_ref_count == 0:
        raise RepositoryPreservationError(
            f"{label}.remote_reachability cannot be available without refs"
        )
    if (
        _required(reachability, "reason", f"{label}.remote_reachability")
        is not None
    ):
        raise RepositoryPreservationError(
            f"{label}.remote_reachability.reason must be null when available"
        )
    oid_count = _non_negative_count(
        _required(reachability, "oid_count", f"{label}.remote_reachability"),
        f"{label}.remote_reachability.oid_count",
    )
    oid_digest = _sha256(
        _required(reachability, "oid_digest", f"{label}.remote_reachability"),
        f"{label}.remote_reachability.oid_digest",
    )
    oids_value = _sequence(
        _required(reachability, "oids", f"{label}.remote_reachability"),
        f"{label}.remote_reachability.oids",
    )
    oids = list(oids_value)
    if any(not _valid_oid(oid, object_format) for oid in oids):
        raise RepositoryPreservationError(
            f"{label}.remote_reachability.oids contain an invalid object id"
        )
    if oids != sorted(set(oids)):
        raise RepositoryPreservationError(
            f"{label}.remote_reachability.oids must be unique and sorted"
        )
    truncated = _boolean(
        _required(
            reachability,
            "oids_truncated",
            f"{label}.remote_reachability",
        ),
        f"{label}.remote_reachability.oids_truncated",
    )
    if truncated != (oid_count > 100):
        raise RepositoryPreservationError(
            f"{label}.remote_reachability.oids_truncated is inconsistent"
        )
    expected_length = min(oid_count, 100)
    if len(oids) != expected_length:
        raise RepositoryPreservationError(
            f"{label}.remote_reachability.oids length is inconsistent"
        )
    if not truncated:
        digest_input = b"\n".join(str(oid).encode("ascii") for oid in oids)
        if oid_digest != hashlib.sha256(digest_input).hexdigest():
            raise RepositoryPreservationError(
                f"{label}.remote_reachability.oid_digest is inconsistent"
            )


def _validate_optional_string_sequence(
    value: object,
    label: str,
) -> list[str] | None:
    if value is None:
        return None
    sequence = _sequence(value, label)
    result: list[str] = []
    for item in sequence:
        if not isinstance(item, str):
            raise RepositoryPreservationError(f"{label} must contain text")
        result.append(item)
    if result != sorted(result):
        raise RepositoryPreservationError(f"{label} must be sorted")
    return result


def _validate_inventory_worktree(
    worktree: Mapping[str, Any],
    label: str,
    object_format: str,
) -> None:
    path = _text(_required(worktree, "path", label), f"{label}.path")
    if not Path(path).is_absolute():
        raise RepositoryPreservationError(f"{label}.path must be absolute")
    branch = _required(worktree, "branch", label)
    branch_ref = _required(worktree, "branch_ref", label)
    if branch is None:
        if branch_ref is not None:
            raise RepositoryPreservationError(
                f"{label}.branch_ref must be null without a branch"
            )
    else:
        branch_text = _text(branch, f"{label}.branch")
        if branch_ref != f"refs/heads/{branch_text}":
            raise RepositoryPreservationError(
                f"{label}.branch_ref does not match branch"
            )
    state = _required(worktree, "state", label)
    if (state == "branch") != (branch is not None):
        raise RepositoryPreservationError(
            f"{label}.state and branch evidence are inconsistent"
        )
    head = _required(worktree, "head", label)
    if head is not None and not _valid_oid(head, object_format):
        raise RepositoryPreservationError(
            f"{label}.head must match the repository object format"
        )
    exists = _boolean(_required(worktree, "exists", label), f"{label}.exists")
    missing = _boolean(
        _required(worktree, "missing", label), f"{label}.missing"
    )
    if exists == missing:
        raise RepositoryPreservationError(
            f"{label}.exists and missing are inconsistent"
        )
    for field in ("locked_reason", "prunable_reason"):
        _nullable_text(_required(worktree, field, label), f"{label}.{field}")
    ancestry = _mapping(
        _required(worktree, "default_remote_ancestry", label),
        f"{label}.default_remote_ancestry",
    )
    _text(
        _required(ancestry, "default_ref", f"{label}.default_remote_ancestry"),
        f"{label}.default_remote_ancestry.default_ref",
    )
    ancestor = _required(
        ancestry,
        "head_is_ancestor",
        f"{label}.default_remote_ancestry",
    )
    if ancestor is not None and not isinstance(ancestor, bool):
        raise RepositoryPreservationError(
            f"{label}.default_remote_ancestry.head_is_ancestor is invalid"
        )
    _nullable_text(
        _required(ancestry, "reason", f"{label}.default_remote_ancestry"),
        f"{label}.default_remote_ancestry.reason",
    )
    flags = _mapping(
        _required(worktree, "index_flags", label),
        f"{label}.index_flags",
    )
    for prefix in ("assume_unchanged", "skip_worktree"):
        count_value = _required(
            flags, f"{prefix}_count", f"{label}.index_flags"
        )
        paths = _validate_optional_string_sequence(
            _required(flags, f"{prefix}_paths", f"{label}.index_flags"),
            f"{label}.index_flags.{prefix}_paths",
        )
        if count_value is None:
            if paths is not None:
                raise RepositoryPreservationError(
                    f"{label}.index_flags.{prefix}_paths must be null"
                )
        else:
            count = _non_negative_count(
                count_value,
                f"{label}.index_flags.{prefix}_count",
            )
            if paths is None or count != len(paths):
                raise RepositoryPreservationError(
                    f"{label}.index_flags.{prefix} evidence is inconsistent"
                )
    upstream_value = _required(worktree, "upstream", label)
    if upstream_value is not None:
        upstream = _mapping(upstream_value, f"{label}.upstream")
        comparable = _boolean(
            _required(upstream, "comparable", f"{label}.upstream"),
            f"{label}.upstream.comparable",
        )
        for field in ("oid", "ref", "short"):
            value = _required(upstream, field, f"{label}.upstream")
            if field == "oid" and value is not None:
                if not _valid_oid(value, object_format):
                    raise RepositoryPreservationError(
                        f"{label}.upstream.oid is invalid"
                    )
            else:
                _nullable_text(value, f"{label}.upstream.{field}")
        for field in ("ahead", "behind"):
            value = _required(upstream, field, f"{label}.upstream")
            if comparable:
                _non_negative_count(value, f"{label}.upstream.{field}")
            elif value is not None:
                raise RepositoryPreservationError(
                    f"{label}.upstream.{field} must be null when incomparable"
                )


def _validated_repository_evidence(
    evidence: Mapping[str, Any],
    expected_path: Path,
) -> tuple[dict[str, object], dict[str, int], int]:
    schema_version = _required(evidence, "schema_version", "evidence")
    if isinstance(schema_version, bool) or schema_version != 1:
        raise RepositoryPreservationError(
            "evidence.schema_version must equal 1"
        )
    _validate_contract(evidence)
    try:
        summarize_repository(evidence)
    except RepositorySummaryError as error:
        raise RepositoryPreservationError(str(error)) from error
    repository = _mapping(
        _required(evidence, "repository", "evidence"),
        "evidence.repository",
    )
    object_format, remote_ref_count = _validate_repository_refs(repository)
    path = _required(repository, "path", "evidence.repository")
    if path != str(expected_path):
        raise RepositoryPreservationError(
            "evidence.repository.path does not match its requested repository"
        )
    worktrees = _sequence(
        _required(evidence, "worktrees", "evidence"),
        "evidence.worktrees",
    )

    signal_counts: dict[str, int] = {}
    commit_occurrences = 0
    worktree_paths: list[str] = []
    for index, value in enumerate(worktrees):
        label = f"evidence.worktrees[{index}]"
        worktree = _mapping(value, label)
        _validate_inventory_worktree(worktree, label, object_format)
        worktree_paths.append(str(worktree["path"]))
        _validate_status(worktree, label)
        _validate_reachability(
            worktree,
            label,
            object_format,
            remote_ref_count,
        )
        signals_value = _sequence(
            _required(worktree, "preservation_signals", label),
            f"{label}.preservation_signals",
        )
        signals: list[str] = []
        for signal in signals_value:
            if not isinstance(signal, str) or not signal:
                raise RepositoryPreservationError(
                    f"{label}.preservation_signals must contain non-empty text"
                )
            signals.append(signal)
        expected_signals = preservation_signals(worktree)
        if signals != expected_signals:
            raise RepositoryPreservationError(
                f"{label}.preservation_signals are inconsistent"
            )
        for signal in signals:
            signal_counts[signal] = signal_counts.get(signal, 0) + 1

        reachability = _mapping(
            _required(worktree, "remote_reachability", label),
            f"{label}.remote_reachability",
        )
        if reachability["available"]:
            commit_occurrences += _non_negative_count(
                reachability["oid_count"],
                f"{label}.remote_reachability.oid_count",
            )

    if worktree_paths != sorted(set(worktree_paths)):
        raise RepositoryPreservationError(
            "evidence.worktrees must have unique, sorted paths"
        )

    producer_signal_counts = _mapping(
        _required(evidence, "signal_counts", "evidence"),
        "evidence.signal_counts",
    )
    validated_producer_counts = {
        key: _non_negative_count(value, f"evidence.signal_counts.{key}")
        for key, value in producer_signal_counts.items()
        if isinstance(key, str) and key
    }
    if len(validated_producer_counts) != len(producer_signal_counts):
        raise RepositoryPreservationError(
            "evidence.signal_counts keys must be non-empty text"
        )
    if validated_producer_counts != dict(sorted(signal_counts.items())):
        raise RepositoryPreservationError(
            "evidence.signal_counts does not match its worktrees"
        )
    return dict(evidence), signal_counts, commit_occurrences


def inspect_repository_set_preservation(
    paths: Sequence[Path],
    *,
    inspector: RepositoryInspector = inspect_repository_preservation,
) -> dict[str, object]:
    """Inspect explicit repositories and aggregate only factual signals."""
    if not paths:
        raise RepositoryPreservationError(
            "at least one absolute repository path is required"
        )
    canonical_paths: list[Path] = []
    for path in paths:
        if not path.is_absolute():
            raise RepositoryPreservationError(
                f"repository path must be absolute: {path}"
            )
        try:
            canonical = path.resolve(strict=True)
        except OSError as error:
            raise RepositoryPreservationError(
                f"repository path is unavailable: {path}"
            ) from error
        if canonical != path:
            raise RepositoryPreservationError(
                f"repository path must be canonical: {canonical}"
            )
        canonical_paths.append(canonical)
    if len(set(canonical_paths)) != len(canonical_paths):
        raise RepositoryPreservationError("repository paths must be unique")

    repositories: list[dict[str, object]] = []
    combined_signal_counts: dict[str, int] = {}
    commit_occurrences = 0
    for path in sorted(canonical_paths, key=str):
        try:
            produced = inspector(path)
        except PreservationInspectionError as error:
            raise RepositoryPreservationError(
                f"preservation inspection failed for {path}: {error}"
            ) from error
        evidence = _mapping(produced, f"inspection result for {path}")
        validated, signal_counts, repository_commit_occurrences = (
            _validated_repository_evidence(evidence, path)
        )
        repositories.append(validated)
        commit_occurrences += repository_commit_occurrences
        for signal, count in signal_counts.items():
            combined_signal_counts[signal] = (
                combined_signal_counts.get(signal, 0) + count
            )

    registered_worktree_count = sum(
        len(_sequence(repository["worktrees"], "evidence.worktrees"))
        for repository in repositories
    )
    result: dict[str, object] = {
        "contract": {
            "content_semantics_assessed": False,
            "deletion_safety_assessed": False,
            "github_state_assessed": False,
            "migration_safety_assessed": False,
            "purpose": (
                "Read-only preservation evidence for an explicit repository set"
            ),
            "remote_reachability_scope": (
                "locally known remote-tracking refs; no fetch is performed"
            ),
        },
        "repositories": repositories,
        "schema_version": 1,
        "totals": {
            "commits_not_on_known_remotes_worktree_occurrence_count": (
                commit_occurrences
            ),
            "registered_worktree_count": registered_worktree_count,
            "repository_count": len(repositories),
            "signal_counts": dict(sorted(combined_signal_counts.items())),
            "worktree_with_preservation_signal_count": sum(
                bool(
                    _sequence(
                        worktree["preservation_signals"],
                        "worktree.preservation_signals",
                    )
                )
                for repository in repositories
                for worktree in _sequence(
                    repository["worktrees"], "evidence.worktrees"
                )
                if isinstance(worktree, Mapping)
            ),
        },
    }
    try:
        json.dumps(
            result,
            allow_nan=False,
            ensure_ascii=True,
            sort_keys=True,
        )
    except (TypeError, ValueError) as error:
        raise RepositoryPreservationError(
            "preservation evidence is not JSON-compatible"
        ) from error
    return result


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
        raise RepositoryPreservationError(
            "preservation evidence is not JSON-compatible"
        ) from error


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repositories",
        nargs="+",
        type=Path,
        help="absolute canonical repository roots",
    )
    arguments = parser.parse_args(sys.argv[1:] if argv is None else argv)
    try:
        result = inspect_repository_set_preservation(arguments.repositories)
        encoded = _encode_json(result)
    except RepositoryPreservationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
