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
    read_selection_policy,
    render_manifest,
    restore_archive,
    stage_artifacts,
    verify_git_source,
    verify_staging,
)


class OfflineArtifactTests(unittest.TestCase):
    def test__stage__uses_declarative_policy_and_preserves_unselected_files(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            self._git_init(repository)
            (repository / ".gitignore").write_text(
                ".offline/\n",
                encoding="utf-8",
            )
            (repository / "docs/build").mkdir(parents=True)
            (repository / "docs/build/index.html").write_text(
                "generated documentation\n",
                encoding="utf-8",
            )
            (repository / "data").mkdir()
            (repository / "data/output.log").write_text(
                "generated log\n",
                encoding="utf-8",
            )
            (repository / "results_001.out").write_text(
                "generated result\n",
                encoding="utf-8",
            )
            retained = repository / "data/input.config"
            retained.write_text("authored input\n", encoding="utf-8")
            policy = repository / "offline-artifacts.toml"
            policy.write_text(
                "schema_version = 1\n"
                "\n"
                "[[rules]]\n"
                "kind = 'path-prefix'\n"
                "reason = 'generated-documentation'\n"
                "values = ['docs/build']\n"
                "\n"
                "[[rules]]\n"
                "kind = 'exact-name'\n"
                "reason = 'generated-log'\n"
                "values = ['output.log']\n"
                "\n"
                "[[rules]]\n"
                "kind = 'name-regex'\n"
                "reason = 'generated-result'\n"
                "values = ['^results_[0-9]+\\.out$']\n",
                encoding="utf-8",
            )
            self._git(repository, "add", ".")
            self._git(repository, "commit", "-qm", "source")

            staged = stage_artifacts(
                repository_root=repository,
                policy_path=Path("offline-artifacts.toml"),
                destination_relative=PurePosixPath(
                    ".offline/release-readiness"
                ),
                checksum_manifest_relative=PurePosixPath(
                    "OFFLINE_ARTIFACT_SHA256SUMS"
                ),
                remove_originals=True,
            )

            self.assertEqual(staged.artifact_count, 3)
            self.assertTrue(staged.removed_originals)
            self.assertTrue(retained.is_file())
            self.assertFalse((repository / "data/output.log").exists())
            manifest = staged.directory / "MANIFEST.tsv"
            records = read_manifest(manifest)
            self.assertEqual(verify_staging(staged.directory, records), 55)
            self.assertEqual(
                {record.classification for record in records},
                {
                    "generated-documentation",
                    "generated-log",
                    "generated-result",
                },
            )

    def test__selection_policy__rejects_invalid_regex(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            policy = Path(directory) / "policy.toml"
            policy.write_text(
                "schema_version = 1\n"
                "[[rules]]\n"
                "kind = 'name-regex'\n"
                "reason = 'generated'\n"
                "values = ['[']\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                OfflineArtifactError,
                "regex is invalid",
            ):
                read_selection_policy(policy)

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

    @classmethod
    def _git_init(cls, repository: Path) -> None:
        repository.mkdir(exist_ok=True)
        subprocess.run(
            ["git", "init", "-q", "-b", "main", str(repository)],
            check=True,
        )
        cls._git(repository, "config", "user.name", "Test User")
        cls._git(
            repository,
            "config",
            "user.email",
            "test@example.invalid",
        )

    @staticmethod
    def _git(repository: Path, *arguments: str) -> None:
        subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=True,
        )

    @classmethod
    def _source_repository(cls, workspace: Path) -> tuple[Path, str]:
        source = workspace / "source"
        cls._git_init(source)
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
