from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import BinaryIO

_MANIFEST_HEADER = "sha256\tbyte_size\treason\toriginal_path"
_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_ARCHIVE_PREFIX = re.compile(r"[a-z0-9][a-z0-9._-]*")


class OfflineArtifactError(ValueError):
    """Raised when offline artifact evidence violates the bounded contract."""


@dataclass(frozen=True)
class ArtifactLimits:
    """Fixed resource bounds for verification and archive creation."""

    max_artifacts: int = 10_000
    max_artifact_bytes: int = 100_000_000_000
    max_total_bytes: int = 1_000_000_000_000
    max_manifest_bytes: int = 10_000_000
    max_path_bytes: int = 4_096

    def __post_init__(self) -> None:
        for field_name, value in vars(self).items():
            if value <= 0:
                raise OfflineArtifactError(f"{field_name} must be positive")


_DEFAULT_LIMITS = ArtifactLimits()


@dataclass(frozen=True)
class ArtifactRecord:
    """Expected identity and classification of one offline artifact."""

    path: PurePosixPath
    sha256: str
    byte_size: int
    classification: str


@dataclass(frozen=True)
class GitSourceIdentity:
    """Exact Git source identity associated with an artifact collection."""

    repository_url: str
    commit: str
    tree: str


@dataclass(frozen=True)
class ArchiveResult:
    """Identity and location of a completed external archive bundle."""

    directory: Path
    archive: Path
    archive_sha256: str
    source: GitSourceIdentity
    artifact_count: int
    artifact_bytes: int


@dataclass(frozen=True)
class RestoreResult:
    """Identity and location of one completed artifact recovery."""

    directory: Path
    archive_sha256: str
    artifact_count: int
    artifact_bytes: int


def read_manifest(
    manifest: Path,
    *,
    limits: ArtifactLimits = _DEFAULT_LIMITS,
) -> tuple[ArtifactRecord, ...]:
    """Read a strict, ordered offline artifact manifest."""
    payload = _read_regular_file(
        manifest,
        max_bytes=limits.max_manifest_bytes,
        label="manifest",
    )
    try:
        lines = payload.decode("utf-8", errors="strict").splitlines()
    except UnicodeDecodeError as error:
        raise OfflineArtifactError("manifest must be UTF-8") from error
    if not lines or lines[0] != _MANIFEST_HEADER:
        raise OfflineArtifactError("manifest header is invalid")

    records: list[ArtifactRecord] = []
    seen: set[PurePosixPath] = set()
    total_bytes = 0
    for line_number, line in enumerate(lines[1:], 2):
        fields = line.split("\t")
        if len(fields) != 4:
            raise OfflineArtifactError(
                f"invalid manifest record at line {line_number}"
            )
        digest, raw_size, classification, raw_path = fields
        if _SHA256.fullmatch(digest) is None:
            raise OfflineArtifactError(f"invalid SHA-256 at line {line_number}")
        if not raw_size.isascii() or not raw_size.isdigit():
            raise OfflineArtifactError(
                f"invalid byte size at line {line_number}"
            )
        byte_size = int(raw_size)
        if byte_size > limits.max_artifact_bytes:
            raise OfflineArtifactError(
                f"artifact exceeds max_artifact_bytes at line {line_number}"
            )
        if not classification or any(
            character in classification for character in "\r\n\t"
        ):
            raise OfflineArtifactError(
                f"invalid classification at line {line_number}"
            )
        path = _parse_relative_path(raw_path, limits=limits)
        if path == PurePosixPath("MANIFEST.tsv"):
            raise OfflineArtifactError(
                "MANIFEST.tsv is reserved for archive metadata"
            )
        if path in seen:
            raise OfflineArtifactError(f"duplicate manifest path: {path}")
        seen.add(path)
        total_bytes += byte_size
        if total_bytes > limits.max_total_bytes:
            raise OfflineArtifactError("manifest exceeds max_total_bytes")
        records.append(
            ArtifactRecord(
                path=path,
                sha256=digest,
                byte_size=byte_size,
                classification=classification,
            )
        )
        if len(records) > limits.max_artifacts:
            raise OfflineArtifactError("manifest exceeds max_artifacts")
    if not records:
        raise OfflineArtifactError("manifest contains no artifact records")
    if [record.path.as_posix() for record in records] != sorted(
        record.path.as_posix() for record in records
    ):
        raise OfflineArtifactError("manifest records must be path-sorted")
    return tuple(records)


def render_manifest(records: Sequence[ArtifactRecord]) -> bytes:
    """Render records in the canonical tab-separated representation."""
    return (
        _MANIFEST_HEADER
        + "\n"
        + "".join(
            "\t".join(
                (
                    record.sha256,
                    str(record.byte_size),
                    record.classification,
                    record.path.as_posix(),
                )
            )
            + "\n"
            for record in records
        )
    ).encode("utf-8")


def verify_staging(
    staging_root: Path,
    records: Sequence[ArtifactRecord],
) -> int:
    """Verify an exact regular-file staging tree against manifest records."""
    root = _regular_directory(staging_root, label="staging root")
    expected = {record.path for record in records}
    actual = _inventory_regular_files(root)
    allowed_metadata = {PurePosixPath("MANIFEST.tsv")}
    if actual - allowed_metadata != expected:
        missing = sorted(path.as_posix() for path in expected - actual)
        extra = sorted(
            path.as_posix() for path in actual - expected - allowed_metadata
        )
        raise OfflineArtifactError(
            f"staging file set mismatch; missing={missing}; extra={extra}"
        )

    metadata = root / "MANIFEST.tsv"
    if metadata.exists() and _read_regular_file(
        metadata,
        max_bytes=len(render_manifest(records)),
        label="staging manifest",
    ) != render_manifest(records):
        raise OfflineArtifactError(
            "staging MANIFEST.tsv does not match canonical records"
        )

    total_bytes = 0
    for record in records:
        digest, byte_size = _regular_file_identity(
            root.joinpath(*record.path.parts)
        )
        if (digest, byte_size) != (record.sha256, record.byte_size):
            raise OfflineArtifactError(
                f"staged artifact identity mismatch: {record.path}"
            )
        total_bytes += byte_size
    return total_bytes


def verify_git_source(
    checkout: Path,
    revision: str,
    repository_url: str,
    records: Sequence[ArtifactRecord],
) -> GitSourceIdentity:
    """Verify every manifest record against one explicit local Git object."""
    root = _regular_directory(checkout, label="Git checkout")
    if _OBJECT_ID.fullmatch(revision) is None:
        raise OfflineArtifactError(
            "source revision must be an exact lowercase Git object ID"
        )
    if not repository_url:
        raise OfflineArtifactError("repository URL must not be empty")
    commit = _git_object_id(root, f"{revision}^{{commit}}")
    tree = _git_object_id(root, f"{commit}^{{tree}}")
    for record in records:
        digest, byte_size = _git_blob_identity(
            root,
            commit,
            record,
        )
        if (digest, byte_size) != (record.sha256, record.byte_size):
            raise OfflineArtifactError(
                f"Git artifact identity mismatch: {record.path}"
            )
    return GitSourceIdentity(
        repository_url=repository_url,
        commit=commit,
        tree=tree,
    )


def create_archive(
    *,
    staging_root: Path,
    manifest: Path,
    destination_directory: Path,
    archive_prefix: str,
    source_checkout: Path,
    source_revision: str,
    source_repository_url: str,
    limits: ArtifactLimits = _DEFAULT_LIMITS,
) -> ArchiveResult:
    """Verify and atomically publish a deterministic external tar bundle."""
    if _ARCHIVE_PREFIX.fullmatch(archive_prefix) is None:
        raise OfflineArtifactError(
            "archive prefix must be a safe lowercase filename component"
        )
    records = read_manifest(manifest, limits=limits)
    artifact_bytes = verify_staging(staging_root, records)
    source = verify_git_source(
        source_checkout,
        source_revision,
        source_repository_url,
        records,
    )
    staging = _regular_directory(staging_root, label="staging root")
    checkout = _regular_directory(source_checkout, label="Git checkout")
    destination = destination_directory.expanduser().resolve(strict=False)
    if destination.is_relative_to(staging) or destination.is_relative_to(
        checkout
    ):
        raise OfflineArtifactError(
            "archive destination must be outside staging and source checkout"
        )
    if destination.exists() or destination.is_symlink():
        raise OfflineArtifactError(
            f"archive destination already exists: {destination}"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}-",
            dir=destination.parent,
        )
    )
    archive_name = f"{archive_prefix}-git-{source.commit[:12]}.tar"
    try:
        archive = temporary / archive_name
        canonical_manifest = render_manifest(records)
        _write_archive(
            archive,
            staging,
            records,
            canonical_manifest,
        )
        archive_digest, _archive_bytes = _regular_file_identity(archive)
        (temporary / "MANIFEST.tsv").write_bytes(canonical_manifest)
        (temporary / f"{archive_name}.sha256").write_text(
            f"{archive_digest}  {archive_name}\n",
            encoding="utf-8",
        )
        source_payload = {
            "archive": archive_name,
            "archive_sha256": archive_digest,
            "artifact_bytes": artifact_bytes,
            "artifact_count": len(records),
            "repository": source.repository_url,
            "source_commit": source.commit,
            "source_tree": source.tree,
            "status": "private-offline-preservation",
        }
        (temporary / "SOURCE.json").write_text(
            json.dumps(
                source_payload,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, destination)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    return ArchiveResult(
        directory=destination,
        archive=destination / archive_name,
        archive_sha256=archive_digest,
        source=source,
        artifact_count=len(records),
        artifact_bytes=artifact_bytes,
    )


def restore_archive(
    *,
    archive: Path,
    archive_checksum: Path,
    manifest: Path,
    destination_directory: Path,
    limits: ArtifactLimits = _DEFAULT_LIMITS,
) -> RestoreResult:
    """Recover and verify manifest-bound artifacts into one new directory."""
    archive_path = archive.expanduser()
    records = read_manifest(manifest, limits=limits)
    expected_archive_digest = _read_archive_checksum(
        archive_checksum,
        archive_path.name,
    )
    max_archive_bytes = (
        limits.max_total_bytes
        + limits.max_manifest_bytes
        + limits.max_artifacts * 2_048
        + 20 * 1_024
    )
    archive_digest, _archive_size = _regular_file_identity(
        archive_path,
        max_bytes=max_archive_bytes,
    )
    if archive_digest != expected_archive_digest:
        raise OfflineArtifactError("archive SHA-256 does not match checksum")

    evidence_directory = archive_path.parent.resolve(strict=True)
    destination = destination_directory.expanduser().resolve(strict=False)
    if destination.is_relative_to(evidence_directory):
        raise OfflineArtifactError(
            "recovery destination must be outside the evidence directory"
        )
    if destination.exists() or destination.is_symlink():
        raise OfflineArtifactError(
            f"recovery destination already exists: {destination}"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}-",
            dir=destination.parent,
        )
    )
    artifact_bytes = 0
    try:
        with _open_regular_file(archive_path) as archive_stream:
            before = os.fstat(archive_stream.fileno())
            with tarfile.open(fileobj=archive_stream, mode="r:") as tar:
                members = _verified_archive_members(tar, records)
                manifest_payload = render_manifest(records)
                manifest_stream = tar.extractfile(members["MANIFEST.tsv"])
                if manifest_stream is None:
                    raise OfflineArtifactError(
                        "archive manifest cannot be read"
                    )
                with manifest_stream:
                    archived_manifest = manifest_stream.read(
                        len(manifest_payload) + 1
                    )
                if archived_manifest != manifest_payload:
                    raise OfflineArtifactError(
                        "archive manifest does not match canonical records"
                    )
                for record in records:
                    source = tar.extractfile(members[record.path.as_posix()])
                    if source is None:
                        raise OfflineArtifactError(
                            f"archive member cannot be read: {record.path}"
                        )
                    target = temporary.joinpath(*record.path.parts)
                    target.parent.mkdir(
                        mode=0o700,
                        parents=True,
                        exist_ok=True,
                    )
                    digest = hashlib.sha256()
                    byte_size = 0
                    descriptor = os.open(
                        target,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                    )
                    with source, os.fdopen(descriptor, "wb") as output:
                        while chunk := source.read(1024 * 1024):
                            byte_size += len(chunk)
                            if byte_size > record.byte_size:
                                raise OfflineArtifactError(
                                    "recovered artifact exceeds manifest size: "
                                    f"{record.path}"
                                )
                            output.write(chunk)
                            digest.update(chunk)
                    target.chmod(0o600)
                    if (digest.hexdigest(), byte_size) != (
                        record.sha256,
                        record.byte_size,
                    ):
                        raise OfflineArtifactError(
                            "recovered artifact identity mismatch: "
                            f"{record.path}"
                        )
                    artifact_bytes += byte_size
            after = os.fstat(archive_stream.fileno())
            if _stat_identity(before) != _stat_identity(after):
                raise OfflineArtifactError("archive mutated during recovery")
        if _inventory_regular_files(temporary) != {
            record.path for record in records
        }:
            raise OfflineArtifactError(
                "recovered file set does not match manifest"
            )
        for path in temporary.rglob("*"):
            if path.is_dir():
                path.chmod(0o700)
        os.replace(temporary, destination)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    return RestoreResult(
        directory=destination,
        archive_sha256=archive_digest,
        artifact_count=len(records),
        artifact_bytes=artifact_bytes,
    )


def _read_archive_checksum(path: Path, archive_name: str) -> str:
    payload = _read_regular_file(
        path,
        max_bytes=1_024,
        label="archive checksum",
    )
    try:
        line = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise OfflineArtifactError("archive checksum must be UTF-8") from error
    expected_suffix = f"  {archive_name}\n"
    if not line.endswith(expected_suffix):
        raise OfflineArtifactError(
            "archive checksum does not name the selected archive"
        )
    digest = line[: -len(expected_suffix)]
    if _SHA256.fullmatch(digest) is None:
        raise OfflineArtifactError("archive checksum SHA-256 is invalid")
    return digest


def _verified_archive_members(
    archive: tarfile.TarFile,
    records: Sequence[ArtifactRecord],
) -> dict[str, tarfile.TarInfo]:
    expected_files = {record.path.as_posix() for record in records}
    expected_files.add("MANIFEST.tsv")
    expected_directories = {
        parent.as_posix()
        for record in records
        for parent in record.path.parents
        if parent.as_posix() != "."
    }
    members: dict[str, tarfile.TarInfo] = {}
    actual_files: set[str] = set()
    actual_directories: set[str] = set()
    records_by_path = {record.path.as_posix(): record for record in records}
    for member in archive.getmembers():
        path = PurePosixPath(member.name)
        if (
            not member.name
            or path.is_absolute()
            or path.as_posix() != member.name
            or "." in path.parts
            or ".." in path.parts
        ):
            raise OfflineArtifactError(
                f"archive contains an unsafe path: {member.name}"
            )
        if member.name in members:
            raise OfflineArtifactError(
                f"archive contains a duplicate path: {member.name}"
            )
        members[member.name] = member
        if member.isfile():
            actual_files.add(member.name)
            if member.name in records_by_path:
                expected_size = records_by_path[member.name].byte_size
                if member.size != expected_size:
                    raise OfflineArtifactError(
                        f"archive member size mismatch: {member.name}"
                    )
        elif member.isdir():
            actual_directories.add(member.name)
        else:
            raise OfflineArtifactError(
                f"archive contains a non-regular entry: {member.name}"
            )
    if actual_files != expected_files:
        raise OfflineArtifactError("archive file set does not match manifest")
    if actual_directories != expected_directories:
        raise OfflineArtifactError(
            "archive directory set does not match manifest"
        )
    return members


def _write_archive(
    destination: Path,
    staging_root: Path,
    records: Sequence[ArtifactRecord],
    manifest_payload: bytes,
) -> None:
    directories = {
        parent.as_posix()
        for record in records
        for parent in Path(record.path).parents
        if parent.as_posix() != "."
    }
    with tarfile.open(
        destination,
        mode="w",
        format=tarfile.PAX_FORMAT,
    ) as archive:
        _add_bytes(
            archive,
            "MANIFEST.tsv",
            manifest_payload,
            mode=0o600,
        )
        for directory in sorted(directories):
            info = tarfile.TarInfo(name=directory)
            info.type = tarfile.DIRTYPE
            info.mode = 0o700
            _normalize_tar_info(info)
            archive.addfile(info)
        for record in records:
            path = staging_root.joinpath(*record.path.parts)
            with _open_regular_file(path) as stream:
                before = os.fstat(stream.fileno())
                if before.st_size != record.byte_size:
                    raise OfflineArtifactError(
                        f"artifact size changed before archive: {record.path}"
                    )
                info = tarfile.TarInfo(name=record.path.as_posix())
                info.size = record.byte_size
                info.mode = 0o600
                _normalize_tar_info(info)
                hashing_stream = _HashingReader(stream)
                archive.addfile(info, hashing_stream)
                after = os.fstat(stream.fileno())
                if _stat_identity(before) != _stat_identity(after):
                    raise OfflineArtifactError(
                        f"artifact mutated during archive: {record.path}"
                    )
                if (
                    hashing_stream.byte_size != record.byte_size
                    or hashing_stream.hexdigest() != record.sha256
                ):
                    raise OfflineArtifactError(
                        f"artifact changed during archive: {record.path}"
                    )


def _add_bytes(
    archive: tarfile.TarFile,
    name: str,
    payload: bytes,
    *,
    mode: int,
) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = len(payload)
    info.mode = mode
    _normalize_tar_info(info)
    with tempfile.SpooledTemporaryFile() as stream:
        stream.write(payload)
        stream.seek(0)
        archive.addfile(info, stream)


def _normalize_tar_info(info: tarfile.TarInfo) -> None:
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0


class _HashingReader:
    def __init__(self, stream: BinaryIO) -> None:
        self._stream = stream
        self._digest = hashlib.sha256()
        self.byte_size = 0

    def read(self, size: int = -1) -> bytes:
        payload = self._stream.read(size)
        self._digest.update(payload)
        self.byte_size += len(payload)
        return payload

    def hexdigest(self) -> str:
        return self._digest.hexdigest()


def _inventory_regular_files(root: Path) -> set[PurePosixPath]:
    files: set[PurePosixPath] = set()
    for directory, directory_names, file_names in os.walk(
        root,
        topdown=True,
        followlinks=False,
    ):
        current = Path(directory)
        for name in directory_names:
            candidate = current / name
            if candidate.is_symlink():
                raise OfflineArtifactError(
                    f"staging contains a symlink: {candidate.relative_to(root)}"
                )
        for name in file_names:
            candidate = current / name
            if candidate.is_symlink() or not candidate.is_file():
                raise OfflineArtifactError(
                    "staging contains a non-regular entry: "
                    f"{candidate.relative_to(root)}"
                )
            files.add(PurePosixPath(candidate.relative_to(root).as_posix()))
    return files


def _regular_file_identity(
    path: Path,
    *,
    max_bytes: int | None = None,
) -> tuple[str, int]:
    with _open_regular_file(path) as stream:
        before = os.fstat(stream.fileno())
        if max_bytes is not None and before.st_size > max_bytes:
            raise OfflineArtifactError(f"file exceeds its byte limit: {path}")
        digest = hashlib.sha256()
        byte_size = 0
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            byte_size += len(chunk)
            if max_bytes is not None and byte_size > max_bytes:
                raise OfflineArtifactError(
                    f"file exceeds its byte limit: {path}"
                )
        after = os.fstat(stream.fileno())
    if _stat_identity(before) != _stat_identity(after):
        raise OfflineArtifactError(f"file mutated while reading: {path}")
    return digest.hexdigest(), byte_size


def _open_regular_file(path: Path) -> BinaryIO:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise OfflineArtifactError(
            f"cannot open regular artifact: {path}"
        ) from error
    status = os.fstat(descriptor)
    if not stat.S_ISREG(status.st_mode):
        os.close(descriptor)
        raise OfflineArtifactError(f"artifact is not a regular file: {path}")
    return os.fdopen(descriptor, "rb")


def _read_regular_file(path: Path, *, max_bytes: int, label: str) -> bytes:
    with _open_regular_file(path) as stream:
        status = os.fstat(stream.fileno())
        if status.st_size > max_bytes:
            raise OfflineArtifactError(f"{label} exceeds its byte limit")
        payload = stream.read(max_bytes + 1)
        after = os.fstat(stream.fileno())
    if len(payload) > max_bytes:
        raise OfflineArtifactError(f"{label} exceeds its byte limit")
    if _stat_identity(status) != _stat_identity(after):
        raise OfflineArtifactError(f"{label} mutated while reading")
    return payload


def _regular_directory(path: Path, *, label: str) -> Path:
    expanded = path.expanduser()
    try:
        status = expanded.lstat()
    except OSError as error:
        raise OfflineArtifactError(f"{label} is unavailable") from error
    if not stat.S_ISDIR(status.st_mode) or expanded.is_symlink():
        raise OfflineArtifactError(f"{label} must be a non-symlink directory")
    return expanded.resolve(strict=True)


def _parse_relative_path(
    raw_path: str,
    *,
    limits: ArtifactLimits,
) -> PurePosixPath:
    if (
        not raw_path
        or "\\" in raw_path
        or "\x00" in raw_path
        or len(raw_path.encode("utf-8")) > limits.max_path_bytes
    ):
        raise OfflineArtifactError("manifest path is invalid")
    path = PurePosixPath(raw_path)
    if (
        path.is_absolute()
        or path.as_posix() != raw_path
        or "." in path.parts
        or ".." in path.parts
    ):
        raise OfflineArtifactError(
            f"manifest path is not normalized: {raw_path}"
        )
    return path


def _git_object_id(checkout: Path, expression: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "--verify", expression],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    value = result.stdout.strip()
    if result.returncode != 0 or _OBJECT_ID.fullmatch(value) is None:
        raise OfflineArtifactError(
            f"cannot resolve exact Git object: {expression}"
        )
    return value


def _git_blob_identity(
    checkout: Path,
    commit: str,
    record: ArtifactRecord,
) -> tuple[str, int]:
    with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(checkout),
                    "cat-file",
                    "blob",
                    f"{commit}:{record.path.as_posix()}",
                ],
                check=False,
                stdout=output,
                stderr=errors,
                timeout=15,
            )
        except subprocess.TimeoutExpired as error:
            raise OfflineArtifactError(
                f"Git blob read timed out: {record.path}"
            ) from error
        if result.returncode != 0:
            raise OfflineArtifactError(
                f"Git cannot read artifact: {record.path}"
            )
        output.seek(0)
        digest = hashlib.sha256()
        byte_size = 0
        while chunk := output.read(1024 * 1024):
            byte_size += len(chunk)
            if byte_size > record.byte_size:
                raise OfflineArtifactError(
                    f"Git blob exceeds manifest size: {record.path}"
                )
            digest.update(chunk)
    return digest.hexdigest(), byte_size


def _stat_identity(status: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        status.st_dev,
        status.st_ino,
        status.st_size,
        status.st_mtime_ns,
        status.st_ctime_ns,
    )


def _verify_command(arguments: argparse.Namespace) -> dict[str, object]:
    records = read_manifest(arguments.manifest)
    artifact_bytes = verify_staging(arguments.staging_root, records)
    result: dict[str, object] = {
        "artifact_bytes": artifact_bytes,
        "artifact_count": len(records),
    }
    if arguments.source_checkout is not None:
        source = verify_git_source(
            arguments.source_checkout,
            arguments.source_revision,
            arguments.source_repository_url,
            records,
        )
        result["source"] = {
            "commit": source.commit,
            "repository": source.repository_url,
            "tree": source.tree,
        }
    return result


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Verify and archive manifest-bound offline artifacts."
    )
    commands = result.add_subparsers(dest="command", required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("--staging-root", type=Path, required=True)
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--source-checkout", type=Path)
    verify.add_argument("--source-revision")
    verify.add_argument("--source-repository-url")

    archive = commands.add_parser("archive")
    archive.add_argument("--staging-root", type=Path, required=True)
    archive.add_argument("--manifest", type=Path, required=True)
    archive.add_argument("--destination-directory", type=Path, required=True)
    archive.add_argument("--archive-prefix", required=True)
    archive.add_argument("--source-checkout", type=Path, required=True)
    archive.add_argument("--source-revision", required=True)
    archive.add_argument("--source-repository-url", required=True)

    restore = commands.add_parser("restore")
    restore.add_argument("--archive", type=Path, required=True)
    restore.add_argument("--archive-checksum", type=Path, required=True)
    restore.add_argument("--manifest", type=Path, required=True)
    restore.add_argument("--destination-directory", type=Path, required=True)
    return result


def main(arguments: Sequence[str] | None = None) -> int:
    args = parser().parse_args(arguments)
    if args.command == "verify":
        source_values = (
            args.source_checkout,
            args.source_revision,
            args.source_repository_url,
        )
        if any(value is not None for value in source_values) and not all(
            value is not None for value in source_values
        ):
            raise OfflineArtifactError(
                "Git verification requires checkout, revision, and URL"
            )
        payload = _verify_command(args)
    elif args.command == "archive":
        archived = create_archive(
            staging_root=args.staging_root,
            manifest=args.manifest,
            destination_directory=args.destination_directory,
            archive_prefix=args.archive_prefix,
            source_checkout=args.source_checkout,
            source_revision=args.source_revision,
            source_repository_url=args.source_repository_url,
        )
        payload = {
            "archive": str(archived.archive),
            "archive_sha256": archived.archive_sha256,
            "artifact_bytes": archived.artifact_bytes,
            "artifact_count": archived.artifact_count,
            "source_commit": archived.source.commit,
            "source_tree": archived.source.tree,
        }
    else:
        restored = restore_archive(
            archive=args.archive,
            archive_checksum=args.archive_checksum,
            manifest=args.manifest,
            destination_directory=args.destination_directory,
        )
        payload = {
            "archive_sha256": restored.archive_sha256,
            "artifact_bytes": restored.artifact_bytes,
            "artifact_count": restored.artifact_count,
            "destination": str(restored.directory),
        }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
