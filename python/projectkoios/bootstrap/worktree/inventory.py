"""Stable, read-only inventory of registered Git worktrees."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from projectkoios.bootstrap.git.client import (
    GitClient,
    GitCommandError,
    parse_worktree_records,
)


class InventoryError(RuntimeError):
    pass


class RepositoryChanged(InventoryError):
    pass


_GIT = GitClient(
    disable_optional_locks=True,
    preserve_global_config=False,
)


def git(
    repo: str, *args: str, allowed: Iterable[int] = (0,)
) -> subprocess.CompletedProcess[bytes]:
    try:
        return _GIT.run(repo, *args, allowed=allowed)
    except GitCommandError as error:
        raise InventoryError(str(error)) from error


def decode(value: bytes) -> str:
    return os.fsdecode(value)


def one_line(result: subprocess.CompletedProcess[bytes]) -> str:
    return decode(result.stdout.rstrip(b"\n"))


def dirty_count(status: bytes) -> int:
    fields = status.split(b"\0")
    count = 0
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if not field:
            continue
        kind = field[:1]
        if kind in (b"1", b"u", b"?"):
            count += 1
        elif kind == b"2":
            count += 1
            if index >= len(fields):
                raise InventoryError("Malformed porcelain-v2 rename record")
            index += 1  # The second path in a rename/copy record.
        elif kind == b"!":
            continue
        else:
            raise InventoryError("Unrecognized porcelain-v2 status record")
    return count


def tagged_paths(raw: bytes, wanted: str) -> list[str]:
    paths: list[str] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        tag, separator, path = record.partition(b" ")
        if not separator or len(tag) != 1:
            raise InventoryError("Malformed ls-files tag record")
        character = decode(tag)
        if (wanted == "skip" and character == "S") or (
            wanted == "assume" and character.islower()
        ):
            paths.append(decode(path))
    return sorted(paths)


def _file_signature(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def filesystem_digest(worktree: str) -> str:
    """Hash tracked and non-ignored untracked entries without filters."""
    listed = git(
        worktree,
        "ls-files",
        "-z",
        "--cached",
        "--others",
        "--exclude-standard",
    ).stdout
    relative_paths = sorted({item for item in listed.split(b"\0") if item})
    root = os.fsencode(worktree)
    digest = hashlib.sha256()
    for relative in relative_paths:
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        full_path = os.path.join(root, relative)
        try:
            before = os.lstat(full_path)
        except FileNotFoundError:
            digest.update(b"missing\0")
            continue
        mode = before.st_mode
        before_signature = _file_signature(before)
        digest.update(stat.S_IFMT(mode).to_bytes(8, "big"))
        digest.update((mode & 0o7777).to_bytes(4, "big"))
        if stat.S_ISLNK(mode):
            try:
                target = os.readlink(full_path)
            except OSError as exc:
                raise RepositoryChanged(
                    f"Symlink changed during inspection: {decode(relative)}"
                ) from exc
            target_bytes = (
                os.fsencode(target) if isinstance(target, str) else target
            )
            digest.update(b"symlink\0" + target_bytes)
        elif stat.S_ISREG(mode):
            digest.update(b"file\0")
            flags = (
                os.O_RDONLY
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
                | getattr(os, "O_NONBLOCK", 0)
            )
            try:
                descriptor = os.open(full_path, flags)
            except OSError as exc:
                raise RepositoryChanged(
                    f"Path could not be opened safely: {decode(relative)}"
                ) from exc
            try:
                opened = os.fstat(descriptor)
                if (
                    not stat.S_ISREG(opened.st_mode)
                    or _file_signature(opened) != before_signature
                ):
                    raise RepositoryChanged(
                        f"Path changed before reading: {decode(relative)}"
                    )
                while True:
                    block = os.read(descriptor, 1024 * 1024)
                    if not block:
                        break
                    digest.update(block)
                descriptor_after = os.fstat(descriptor)
                if _file_signature(descriptor_after) != before_signature:
                    raise RepositoryChanged(
                        f"Path changed while reading: {decode(relative)}"
                    )
            finally:
                os.close(descriptor)
        elif stat.S_ISDIR(mode):
            # Normally a gitlink; its Git-observable state is in status.
            digest.update(b"directory\0")
        else:
            digest.update(b"special\0")
        try:
            after = os.lstat(full_path)
        except FileNotFoundError as exc:
            raise RepositoryChanged(
                f"Path disappeared during inspection: {decode(relative)}"
            ) from exc
        if before_signature != _file_signature(after):
            raise RepositoryChanged(
                f"Path changed during inspection: {decode(relative)}"
            )
    return digest.hexdigest()


def resolve_default_remote_ref(repo: str) -> dict[str, Any]:
    ref_name = "refs/remotes/origin/HEAD"
    symbolic = git(repo, "symbolic-ref", "-q", ref_name, allowed=(0, 1))
    target = one_line(symbolic) if symbolic.returncode == 0 else None
    resolved = git(
        repo,
        "rev-parse",
        "--verify",
        f"{ref_name}^{{commit}}",
        allowed=(0, 128),
    )
    oid = one_line(resolved) if resolved.returncode == 0 else None
    return {
        "available": oid is not None,
        "oid": oid,
        "ref": ref_name,
        "symbolic_target": target,
    }


def upstream_details(worktree: str, head: str) -> dict[str, Any] | None:
    full = git(
        worktree,
        "rev-parse",
        "--symbolic-full-name",
        "@{upstream}",
        allowed=(0, 128),
    )
    if full.returncode != 0:
        return None
    full_name = one_line(full)
    short_result = git(
        worktree,
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{upstream}",
    )
    short_name = one_line(short_result)
    oid_result = git(
        worktree,
        "rev-parse",
        "--verify",
        f"{full_name}^{{commit}}",
        allowed=(0, 128),
    )
    if oid_result.returncode != 0:
        return {
            "ahead": None,
            "behind": None,
            "comparable": False,
            "oid": None,
            "ref": full_name,
            "short": short_name,
        }
    oid = one_line(oid_result)
    counts = git(
        worktree,
        "rev-list",
        "--left-right",
        "--count",
        f"{head}...{oid}",
        allowed=(0, 128),
    )
    if counts.returncode != 0:
        ahead = behind = None
        comparable = False
    else:
        parts = counts.stdout.split()
        if len(parts) != 2:
            raise InventoryError("Malformed ahead/behind count")
        ahead, behind = (int(parts[0]), int(parts[1]))
        comparable = True
    return {
        "ahead": ahead,
        "behind": behind,
        "comparable": comparable,
        "oid": oid,
        "ref": full_name,
        "short": short_name,
    }


def inspect_worktree(
    metadata: dict[str, Any], default_ref: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    path = metadata.get("worktree")
    if not isinstance(path, str) or not os.path.isabs(path):
        raise InventoryError("Git reported a non-absolute worktree path")
    exists = os.path.exists(path)
    branch_ref = (
        metadata.get("branch")
        if isinstance(metadata.get("branch"), str)
        else None
    )
    listed_head = (
        metadata.get("HEAD") if isinstance(metadata.get("HEAD"), str) else None
    )
    is_bare = bool(metadata.get("bare", False))
    is_detached = bool(metadata.get("detached", False))
    state = (
        "bare"
        if is_bare
        else "detached"
        if is_detached
        else "branch"
        if branch_ref
        else "unknown"
    )
    item: dict[str, Any] = {
        "branch": branch_ref.removeprefix("refs/heads/")
        if branch_ref
        else None,
        "branch_ref": branch_ref,
        "default_remote_ancestry": {
            "default_ref": default_ref["ref"],
            "head_is_ancestor": None,
            "reason": "worktree_not_inspectable" if not exists else None,
        },
        "dirty_entry_count": None,
        "exists": exists,
        "head": listed_head,
        "index_flags": {
            "assume_unchanged_count": None,
            "assume_unchanged_paths": None,
            "skip_worktree_count": None,
            "skip_worktree_paths": None,
        },
        "inspectable": False,
        "locked": "locked" in metadata,
        "locked_reason": metadata.get("locked")
        if isinstance(metadata.get("locked"), str)
        else None,
        "missing": not exists,
        "path": path,
        "prunable": "prunable" in metadata,
        "prunable_reason": metadata.get("prunable")
        if isinstance(metadata.get("prunable"), str)
        else None,
        "state": state,
        "upstream": None,
    }
    witness: dict[str, Any] = {"metadata": metadata}
    if not exists:
        return item, witness
    probe = git(path, "rev-parse", "--git-dir", allowed=(0, 128))
    if probe.returncode != 0:
        item["default_remote_ancestry"]["reason"] = "git_probe_failed"
        return item, witness
    if is_bare:
        bare_head_result = git(
            path, "rev-parse", "--verify", "HEAD^{commit}", allowed=(0, 128)
        )
        actual_oid = (
            one_line(bare_head_result)
            if bare_head_result.returncode == 0
            else None
        )
        if listed_head and actual_oid != listed_head:
            raise RepositoryChanged(f"HEAD changed during inspection: {path}")
        item["inspectable"] = True
        item["default_remote_ancestry"]["reason"] = "bare_worktree"
        witness["actual_head"] = actual_oid
        return item, witness

    actual_head_result = git(
        path, "rev-parse", "--verify", "HEAD^{commit}", allowed=(0, 128)
    )
    actual_head = (
        one_line(actual_head_result)
        if actual_head_result.returncode == 0
        else None
    )
    if listed_head and actual_head != listed_head:
        raise RepositoryChanged(f"HEAD changed during inspection: {path}")
    symbolic = git(path, "symbolic-ref", "-q", "HEAD", allowed=(0, 1))
    actual_branch = one_line(symbolic) if symbolic.returncode == 0 else None
    if branch_ref != actual_branch:
        raise RepositoryChanged(
            f"Branch attachment changed during inspection: {path}"
        )

    status = git(
        path,
        "status",
        "--porcelain=v2",
        "-z",
        "--untracked-files=all",
        "--ignore-submodules=none",
    ).stdout
    tags_t = git(path, "ls-files", "-t", "-z", "--cached").stdout
    tags_v = git(path, "ls-files", "-v", "-z", "--cached").stdout
    skip_paths = tagged_paths(tags_t, "skip")
    assume_paths = tagged_paths(tags_v, "assume")
    item["dirty_entry_count"] = dirty_count(status)
    item["index_flags"] = {
        "assume_unchanged_count": len(assume_paths),
        "assume_unchanged_paths": assume_paths,
        "skip_worktree_count": len(skip_paths),
        "skip_worktree_paths": skip_paths,
    }
    item["inspectable"] = True
    item["upstream"] = (
        upstream_details(path, actual_head)
        if actual_head and branch_ref
        else None
    )

    ancestry = item["default_remote_ancestry"]
    if not actual_head:
        ancestry["reason"] = "head_unavailable"
    elif not default_ref["available"]:
        ancestry["reason"] = "default_remote_ref_unavailable"
    else:
        comparison = git(
            path,
            "merge-base",
            "--is-ancestor",
            actual_head,
            str(default_ref["oid"]),
            allowed=(0, 1, 128),
        )
        if comparison.returncode == 0:
            ancestry["head_is_ancestor"] = True
            ancestry["reason"] = None
        elif comparison.returncode == 1:
            ancestry["head_is_ancestor"] = False
            ancestry["reason"] = None
        else:
            ancestry["reason"] = "comparison_failed"

    witness.update(
        {
            "actual_branch": actual_branch,
            "actual_head": actual_head,
            "filesystem_digest": filesystem_digest(path),
            "status_digest": hashlib.sha256(status).hexdigest(),
            "tag_t_digest": hashlib.sha256(tags_t).hexdigest(),
            "tag_v_digest": hashlib.sha256(tags_v).hexdigest(),
        }
    )
    return item, witness


def collect(repo: str) -> tuple[dict[str, Any], dict[str, Any]]:
    worktree_raw = git(
        repo, "worktree", "list", "--porcelain", "-z", "--expire=now"
    ).stdout
    try:
        metadata = parse_worktree_records(worktree_raw)
    except GitCommandError as error:
        raise InventoryError(str(error)) from error
    default_ref = resolve_default_remote_ref(repo)
    origin = git(
        repo,
        "config",
        "-z",
        "--local",
        "--get-all",
        "remote.origin.url",
        allowed=(0, 1),
    )
    origin_urls = [
        decode(value) for value in origin.stdout.split(b"\0") if value
    ]
    refs = git(
        repo,
        "for-each-ref",
        "--format=%(refname)%00%(objectname)%00%(symref)",
    ).stdout

    worktrees: list[dict[str, Any]] = []
    worktree_witnesses: list[dict[str, Any]] = []
    for record in metadata:
        item, witness = inspect_worktree(record, default_ref)
        worktrees.append(item)
        worktree_witnesses.append(witness)
    paired = sorted(
        zip(worktrees, worktree_witnesses, strict=True),
        key=lambda pair: pair[0]["path"],
    )
    worktrees = [pair[0] for pair in paired]
    worktree_witnesses = [pair[1] for pair in paired]

    inventory = {
        "contract": {
            "deletion_safety_assessed": False,
            "purpose": "Evidence-only inventory of registered Git worktrees",
            "statement": (
                "This inventory does not claim that any worktree is safe "
                "to delete."
            ),
        },
        "repository": {
            "default_remote_ref": default_ref,
            "origin_urls": origin_urls,
            "path": repo,
        },
        "schema_version": 1,
        "worktrees": worktrees,
    }
    witness = {
        "inventory": inventory,
        "refs_digest": hashlib.sha256(refs).hexdigest(),
        "worktree_list_digest": hashlib.sha256(worktree_raw).hexdigest(),
        "worktrees": worktree_witnesses,
    }
    return inventory, witness


def inventory(argv: list[str]) -> int:
    if len(argv) != 2:
        raise InventoryError(
            "Usage: inventory-git-worktrees /absolute/path/to/repository"
        )
    supplied = argv[1]
    if not os.path.isabs(supplied):
        raise InventoryError("Repository path must be absolute")
    if not os.path.isdir(supplied):
        raise InventoryError("Repository path must name an existing directory")
    try:
        repo = str(Path(supplied).resolve(strict=True))
    except OSError as error:
        raise RepositoryChanged(
            "Repository path changed during inspection"
        ) from error
    top = git(
        repo,
        "rev-parse",
        "--path-format=absolute",
        "--show-toplevel",
        allowed=(0, 128),
    )
    if top.returncode != 0:
        raise InventoryError("Path is not inside a non-bare Git working tree")
    repository_root = one_line(top)
    if repo != repository_root:
        raise InventoryError("Repository path must be the worktree root")

    first_inventory, first_witness = collect(repo)
    second_inventory, second_witness = collect(repo)
    if first_witness != second_witness:
        raise RepositoryChanged(
            "Repository state changed during inspection; no inventory emitted"
        )
    json.dump(
        first_inventory, sys.stdout, ensure_ascii=True, indent=2, sort_keys=True
    )
    sys.stdout.write("\n")
    return 0


def main(argv: list[str]) -> int:
    try:
        return inventory(argv)
    except InventoryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
