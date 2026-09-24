from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path, PurePosixPath

from projectkoios.bootstrap.harness.offline_artifacts import (
    ArtifactLimits,
    ArtifactRecord,
    OfflineArtifactError,
    create_archive,
    read_manifest,
    render_manifest,
    restore_archive,
    verify_git_source,
    verify_staging,
)


class OfflineArtifactTests(unittest.TestCase):
    def test__archive__is_deterministic_and_provenance_complete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source, revision = self._source_repository(workspace)
            staging, manifest, records = self._staging(workspace, source)

            first = create_archive(
                staging_root=staging,
                manifest=manifest,
                destination_directory=workspace / "archive-one",
                archive_prefix="example-offline-artifacts",
                source_checkout=source,
                source_revision=revision,
                source_repository_url="https://example.invalid/source.git",
            )
            second = create_archive(
                staging_root=staging,
                manifest=manifest,
                destination_directory=workspace / "archive-two",
                archive_prefix="example-offline-artifacts",
                source_checkout=source,
                source_revision=revision,
                source_repository_url="https://example.invalid/source.git",
            )

            self.assertEqual(first.archive_sha256, second.archive_sha256)
            self.assertEqual(
                first.archive.read_bytes(),
                second.archive.read_bytes(),
            )
            self.assertEqual(first.artifact_count, 2)
            self.assertEqual(
                first.artifact_bytes,
                sum(record.byte_size for record in records),
            )
            source_evidence = json.loads(
                (first.directory / "SOURCE.json").read_text(encoding="utf-8")
            )
            self.assertEqual(source_evidence["source_commit"], revision)
            self.assertEqual(source_evidence["source_tree"], first.source.tree)

            with tarfile.open(first.archive, mode="r") as archive:
                members = archive.getmembers()
                files = {member.name for member in members if member.isfile()}
                self.assertEqual(
                    files,
                    {
                        "MANIFEST.tsv",
                        "nested/result.dat",
                        "plain.out",
                    },
                )
                for member in members:
                    self.assertEqual(member.uid, 0)
                    self.assertEqual(member.gid, 0)
                    self.assertEqual(member.mtime, 0)
                    if member.isdir():
                        self.assertEqual(member.mode, 0o700)
                    else:
                        self.assertEqual(member.mode, 0o600)

            recovered = restore_archive(
                archive=first.archive,
                archive_checksum=(
                    first.directory / f"{first.archive.name}.sha256"
                ),
                manifest=first.directory / "MANIFEST.tsv",
                destination_directory=workspace / "recovered",
            )
            self.assertEqual(recovered.artifact_count, len(records))
            self.assertEqual(recovered.artifact_bytes, first.artifact_bytes)
            for record in records:
                restored_file = recovered.directory.joinpath(*record.path.parts)
                original_file = staging.joinpath(*record.path.parts)
                self.assertEqual(
                    restored_file.read_bytes(),
                    original_file.read_bytes(),
                )
                self.assertEqual(restored_file.stat().st_mode & 0o777, 0o600)

    def test__restore__rejects_incorrect_archive_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source, revision = self._source_repository(workspace)
            staging, manifest, _records = self._staging(workspace, source)
            archived = create_archive(
                staging_root=staging,
                manifest=manifest,
                destination_directory=workspace / "archive",
                archive_prefix="example-offline-artifacts",
                source_checkout=source,
                source_revision=revision,
                source_repository_url="https://example.invalid/source.git",
            )
            incorrect = workspace / "incorrect.sha256"
            incorrect.write_text(
                f"{'0' * 64}  {archived.archive.name}\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                OfflineArtifactError,
                "archive SHA-256 does not match",
            ):
                restore_archive(
                    archive=archived.archive,
                    archive_checksum=incorrect,
                    manifest=archived.directory / "MANIFEST.tsv",
                    destination_directory=workspace / "recovered",
                )
            self.assertFalse((workspace / "recovered").exists())

    def test__verify__accepts_exact_staging_and_git_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source, revision = self._source_repository(workspace)
            staging, manifest, records = self._staging(workspace, source)

            artifact_bytes = verify_staging(staging, records)
            identity = verify_git_source(
                source,
                revision,
                "https://example.invalid/source.git",
                records,
            )

            self.assertEqual(
                artifact_bytes,
                sum(record.byte_size for record in records),
            )
            self.assertEqual(identity.commit, revision)
            self.assertEqual(read_manifest(manifest), records)

    def test__verify__rejects_extra_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source, _revision = self._source_repository(workspace)
            staging, _manifest, records = self._staging(workspace, source)
            (staging / "extra").write_text("unexpected", encoding="utf-8")

            with self.assertRaisesRegex(
                OfflineArtifactError,
                "staging file set mismatch",
            ):
                verify_staging(staging, records)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test__verify__rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source, _revision = self._source_repository(workspace)
            staging, _manifest, records = self._staging(workspace, source)
            os.symlink(staging / "plain.out", staging / "alias.out")

            with self.assertRaisesRegex(
                OfflineArtifactError,
                "contains a non-regular entry",
            ):
                verify_staging(staging, records)

    def test__verify__rejects_conflicting_staging_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            source, _revision = self._source_repository(workspace)
            staging, _manifest, records = self._staging(workspace, source)
            (staging / "MANIFEST.tsv").write_text(
                "not the selected manifest\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                OfflineArtifactError,
                "staging manifest exceeds its byte limit|does not match",
            ):
                verify_staging(staging, records)

    def test__manifest__rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "MANIFEST.tsv"
            manifest.write_text(
                "sha256\tbyte_size\treason\toriginal_path\n"
                f"{'0' * 64}\t1\tgenerated\t../outside\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                OfflineArtifactError,
                "not normalized",
            ):
                read_manifest(manifest)

    def test__manifest__enforces_resource_limits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "MANIFEST.tsv"
            manifest.write_text(
                "sha256\tbyte_size\treason\toriginal_path\n"
                f"{'0' * 64}\t2\tgenerated\tartifact\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                OfflineArtifactError,
                "max_artifact_bytes",
            ):
                read_manifest(
                    manifest,
                    limits=ArtifactLimits(max_artifact_bytes=1),
                )

    @staticmethod
    def _source_repository(workspace: Path) -> tuple[Path, str]:
        source = workspace / "source"
        source.mkdir()
        subprocess.run(
            ["git", "init", "-q", "-b", "main", str(source)],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(source), "config", "user.name", "Test User"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(source),
                "config",
                "user.email",
                "test@example.invalid",
            ],
            check=True,
        )
        (source / "nested").mkdir()
        (source / "nested/result.dat").write_bytes(b"result\x00data\n")
        (source / "plain.out").write_bytes(b"plain output\n")
        subprocess.run(
            ["git", "-C", str(source), "add", "."],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(source), "commit", "-qm", "source"],
            check=True,
        )
        revision = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return source, revision

    @staticmethod
    def _staging(
        workspace: Path,
        source: Path,
    ) -> tuple[Path, Path, tuple[ArtifactRecord, ...]]:
        staging = workspace / "staging"
        (staging / "nested").mkdir(parents=True)
        shutil.copyfile(
            source / "nested/result.dat",
            staging / "nested/result.dat",
        )
        shutil.copyfile(source / "plain.out", staging / "plain.out")
        records = tuple(
            ArtifactRecord(
                path=PurePosixPath(relative),
                sha256=hashlib.sha256(
                    source.joinpath(*PurePosixPath(relative).parts).read_bytes()
                ).hexdigest(),
                byte_size=source.joinpath(*PurePosixPath(relative).parts)
                .stat()
                .st_size,
                classification="generated-test-artifact",
            )
            for relative in ("nested/result.dat", "plain.out")
        )
        manifest = workspace / "MANIFEST.tsv"
        manifest.write_bytes(render_manifest(records))
        return staging, manifest, records


if __name__ == "__main__":
    unittest.main()
