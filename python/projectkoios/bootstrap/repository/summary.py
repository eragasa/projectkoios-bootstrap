"""Deterministic factual summary across an explicit repository set."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from projectkoios.bootstrap.worktree.inventory import (
    InventoryError,
    inventory_repository,
)

_WORKTREE_STATES = frozenset({"bare", "branch", "detached", "unknown"})


class RepositorySummaryError(RuntimeError):
    """A repository-set summary could not be produced safely."""


def _required(mapping: Mapping[str, Any], key: str, label: str) -> Any:
    try:
        return mapping[key]
    except KeyError as error:
        raise RepositorySummaryError(
            f"{label} is missing required field {key!r}"
        ) from error


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RepositorySummaryError(f"{label} must be a mapping")
    return value


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise RepositorySummaryError(f"{label} must be a sequence")
    return value


def _boolean(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise RepositorySummaryError(f"{label} must be a boolean")
    return value


def _optional_count(value: Any, label: str) -> int | None:
    if value is None:
        return None
    return _count(value, label)


def _count(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RepositorySummaryError(f"{label} must be a non-negative integer")
    return value


def summarize_repository(inventory: Mapping[str, Any]) -> dict[str, Any]:
    schema_version = _required(inventory, "schema_version", "inventory")
    if isinstance(schema_version, bool) or schema_version != 1:
        raise RepositorySummaryError("inventory.schema_version must equal 1")
    repository = _mapping(
        _required(inventory, "repository", "inventory"),
        "inventory.repository",
    )
    worktree_values = _sequence(
        _required(inventory, "worktrees", "inventory"),
        "inventory.worktrees",
    )
    worktrees = tuple(
        _mapping(value, f"inventory.worktrees[{index}]")
        for index, value in enumerate(worktree_values)
    )

    path = _required(repository, "path", "inventory.repository")
    if not isinstance(path, str):
        raise RepositorySummaryError("inventory.repository.path must be text")
    origin_values = _sequence(
        _required(repository, "origin_urls", "inventory.repository"),
        "inventory.repository.origin_urls",
    )
    if not all(isinstance(value, str) for value in origin_values):
        raise RepositorySummaryError(
            "inventory.repository.origin_urls must contain text"
        )
    default_ref_value = _mapping(
        _required(
            repository,
            "default_remote_ref",
            "inventory.repository",
        ),
        "inventory.repository.default_remote_ref",
    )
    default_available = _boolean(
        _required(default_ref_value, "available", "default_remote_ref"),
        "default_remote_ref.available",
    )
    default_ref = _required(default_ref_value, "ref", "default_remote_ref")
    default_symbolic = _required(
        default_ref_value,
        "symbolic_target",
        "default_remote_ref",
    )
    default_oid = _required(default_ref_value, "oid", "default_remote_ref")
    for value, label in (
        (default_ref, "default_remote_ref.ref"),
        (default_symbolic, "default_remote_ref.symbolic_target"),
        (default_oid, "default_remote_ref.oid"),
    ):
        if value is not None and not isinstance(value, str):
            raise RepositorySummaryError(f"{label} must be text or null")
    if not isinstance(default_ref, str):
        raise RepositorySummaryError("default_remote_ref.ref must be text")
    default_remote_ref = {
        "available": default_available,
        "oid": default_oid,
        "ref": default_ref,
        "symbolic_target": default_symbolic,
    }

    branches: set[str] = set()
    dirty_count = 0
    unknown_dirty_count = 0
    hidden_flag_count = 0
    locked_count = 0
    missing_count = 0
    non_branch_count = 0
    prunable_count = 0
    uninspectable_count = 0
    upstream_ahead_count = 0
    upstream_behind_count = 0
    upstream_diverged_count = 0
    upstream_comparison_unavailable_count = 0

    for index, worktree in enumerate(worktrees):
        label = f"inventory.worktrees[{index}]"
        branch = _required(worktree, "branch", label)
        if branch is not None:
            if not isinstance(branch, str):
                raise RepositorySummaryError(
                    f"{label}.branch must be text or null"
                )
            branches.add(branch)
        state = _required(worktree, "state", label)
        if not isinstance(state, str) or state not in _WORKTREE_STATES:
            raise RepositorySummaryError(
                f"{label}.state must be one of {sorted(_WORKTREE_STATES)}"
            )
        non_branch_count += state != "branch"

        inspectable = _boolean(
            _required(worktree, "inspectable", label),
            f"{label}.inspectable",
        )
        uninspectable_count += not inspectable
        locked_count += _boolean(
            _required(worktree, "locked", label),
            f"{label}.locked",
        )
        missing_count += _boolean(
            _required(worktree, "missing", label),
            f"{label}.missing",
        )
        prunable_count += _boolean(
            _required(worktree, "prunable", label),
            f"{label}.prunable",
        )

        dirty = _optional_count(
            _required(worktree, "dirty_entry_count", label),
            f"{label}.dirty_entry_count",
        )
        if dirty is None:
            unknown_dirty_count += 1
        elif dirty:
            dirty_count += 1

        flags = _mapping(
            _required(worktree, "index_flags", label),
            f"{label}.index_flags",
        )
        for field in ("skip_worktree_count", "assume_unchanged_count"):
            count = _optional_count(
                _required(flags, field, f"{label}.index_flags"),
                f"{label}.index_flags.{field}",
            )
            hidden_flag_count += count or 0

        upstream_value = _required(worktree, "upstream", label)
        if upstream_value is None:
            upstream_comparison_unavailable_count += 1
            continue
        upstream = _mapping(upstream_value, f"{label}.upstream")
        comparable = _boolean(
            _required(upstream, "comparable", f"{label}.upstream"),
            f"{label}.upstream.comparable",
        )
        if not comparable:
            upstream_comparison_unavailable_count += 1
            continue
        ahead = _count(
            _required(upstream, "ahead", f"{label}.upstream"),
            f"{label}.upstream.ahead",
        )
        behind = _count(
            _required(upstream, "behind", f"{label}.upstream"),
            f"{label}.upstream.behind",
        )
        upstream_ahead_count += bool(ahead)
        upstream_behind_count += bool(behind)
        upstream_diverged_count += bool(ahead and behind)

    return {
        "branches": sorted(branches),
        "default_remote_ref": default_remote_ref,
        "dirty_worktree_count": dirty_count,
        "hidden_index_flag_count": hidden_flag_count,
        "locked_worktree_count": locked_count,
        "missing_worktree_count": missing_count,
        "name": Path(path).name,
        "non_branch_worktree_count": non_branch_count,
        "origin_urls": list(origin_values),
        "path": path,
        "prunable_worktree_count": prunable_count,
        "registered_worktree_count": len(worktrees),
        "uninspectable_worktree_count": uninspectable_count,
        "unknown_dirty_state_count": unknown_dirty_count,
        "upstream_ahead_worktree_count": upstream_ahead_count,
        "upstream_behind_worktree_count": upstream_behind_count,
        "upstream_diverged_worktree_count": upstream_diverged_count,
        "upstream_comparison_unavailable_worktree_count": (
            upstream_comparison_unavailable_count
        ),
    }


def summarize_repository_set(paths: Sequence[Path]) -> dict[str, Any]:
    if not paths:
        raise RepositorySummaryError(
            "at least one absolute repository path is required"
        )
    canonical_paths: list[Path] = []
    for path in paths:
        if not path.is_absolute():
            raise RepositorySummaryError(
                f"repository path must be absolute: {path}"
            )
        try:
            canonical = path.resolve(strict=True)
        except OSError as error:
            raise RepositorySummaryError(
                f"repository path is unavailable: {path}"
            ) from error
        if canonical != path:
            raise RepositorySummaryError(
                f"repository path must be canonical: {canonical}"
            )
        canonical_paths.append(canonical)
    if len(set(canonical_paths)) != len(canonical_paths):
        raise RepositorySummaryError("repository paths must be unique")

    summaries: list[dict[str, Any]] = []
    for path in sorted(canonical_paths, key=str):
        try:
            summaries.append(summarize_repository(inventory_repository(path)))
        except InventoryError as error:
            raise RepositorySummaryError(
                f"inventory failed for {path}: {error}"
            ) from error

    count_fields = (
        "dirty_worktree_count",
        "hidden_index_flag_count",
        "locked_worktree_count",
        "missing_worktree_count",
        "non_branch_worktree_count",
        "prunable_worktree_count",
        "registered_worktree_count",
        "uninspectable_worktree_count",
        "unknown_dirty_state_count",
        "upstream_ahead_worktree_count",
        "upstream_behind_worktree_count",
        "upstream_diverged_worktree_count",
        "upstream_comparison_unavailable_worktree_count",
    )
    totals = {
        field: sum(summary[field] for summary in summaries)
        for field in count_fields
    }
    totals["repository_count"] = len(summaries)
    return {
        "contract": {
            "deletion_safety_assessed": False,
            "github_state_assessed": False,
            "migration_safety_assessed": False,
            "purpose": (
                "Factual worktree summary for an explicit repository set"
            ),
        },
        "repositories": summaries,
        "schema_version": 1,
        "totals": totals,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "repositories",
        nargs="+",
        type=Path,
        help="absolute canonical repository roots",
    )
    arguments = parser.parse_args(argv)
    try:
        result = summarize_repository_set(arguments.repositories)
    except RepositorySummaryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=True, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0
