from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

from projectkoios.bootstrap.control_surface.adr.evidence import AdrPilotEvidenceBuilder
from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.adr.markdown import AdrMarkdownRecordParser, AdrProjectionRenderer
from projectkoios.bootstrap.control_surface.adr.models import PilotPaths, PilotResult
from projectkoios.bootstrap.control_surface.adr.storage import AdrStorageAdapter, DocumentStoreAdrStorageAdapter
from projectkoios.bootstrap.control_surface.documents import DocumentRecord
from projectkoios.bootstrap.control_surface.storage import SqliteDocumentStore
from projectkoios.bootstrap.control_surface.adr.validation import AdrRecordValidator
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrStoragePilot:
    """Run the bounded one-ADR JSON/database pilot.

    Args:
        paths: Pilot filesystem paths.
        timestamp: Deterministic timestamp for generated evidence.
    """

    paths: PilotPaths
    timestamp: str = "20260711.034817Z"

    def run(self) -> PilotResult:
        """Run the pilot and write committed evidence artifacts.

        Returns:
            Pilot run result.
        """
        self.paths.pilot_dir.mkdir(parents=True, exist_ok=True)
        # Source Markdown remains read-only migration evidence.
        source_markdown: str = self.paths.source_adr.read_text(encoding="utf-8")
        # Mapper is storage-independent by design.
        parser: AdrMarkdownRecordParser = AdrMarkdownRecordParser(source_config=self.paths.source_config)
        record: JsonObject
        mapping: JsonObject
        record, mapping = parser.parse_source_record(source_markdown)
        # Schema validation is storage-independent by design.
        validator: AdrRecordValidator = AdrRecordValidator()
        validator.validate(record)
        # Invalid record captures inspectable schema failure evidence.
        invalid_record: JsonObject = dict(record)
        invalid_record["status"] = "invalid-status"
        mapping["invalid_schema_error"] = validator.invalid_record_error(invalid_record)
        # Adapter selection is isolated from mapping/validation/projection/equality.
        database_path: Path = self.paths.pilot_dir / "generated-local" / "pilot.sqlite"
        # Generic store owns SQLite persistence while the ADR wrapper owns ADR semantics.
        document_store: SqliteDocumentStore = SqliteDocumentStore(database_path=database_path)
        # Adapter stores the ADR record through the generic document-store boundary.
        adapter: AdrStorageAdapter = DocumentStoreAdrStorageAdapter(
            document_store=document_store,
            timestamp=self.timestamp,
        )
        adapter.store(record)
        # Exported record is the JSON checkpoint payload from storage.
        exported_record: JsonObject = adapter.export(str(record["id"]))
        self.assert_records_equal(record, exported_record)
        # Record JSON is deterministic for hash and review evidence.
        record_json: str = DocumentRecord.canonical_payload_text(exported_record)
        # Manifest indexes all pilot configuration and evidence artifacts.
        manifest: JsonObject = PilotManifestBuilder(self.paths, validator.schema_id()).build(
            exported_record,
            source_markdown,
            record_json,
        )
        # Projection is rendered from record plus manifest metadata, not from SQLite.
        projection: str = AdrProjectionRenderer().render(exported_record, manifest, record_json)
        # Projection record verifies generated Markdown can recover schema data.
        projection_record: JsonObject = parser.parse_projection_record(projection)
        validator.validate(projection_record)
        self.assert_records_equal(exported_record, projection_record)
        mapping["source_hash"] = manifest["source_adr"]["content_hash"]
        mapping["json_hash"] = manifest["json_checkpoint"]["content_hash"]
        mapping["projection_round_trip_equal"] = True
        # Evidence builder keeps migration/database evidence out of pilot orchestration.
        evidence_builder: AdrPilotEvidenceBuilder = AdrPilotEvidenceBuilder()
        # Migration evidence records the intentional storage-substrate break.
        migration_evidence: JsonObject = evidence_builder.migration_evidence(manifest, mapping)
        self.write_artifacts(
            record_json,
            projection,
            manifest,
            mapping,
            migration_evidence,
            evidence_builder,
            adapter,
            database_path,
        )
        self.remove_mutable_database(database_path)
        return PilotResult(
            record=record,
            exported_record=exported_record,
            projection_record=projection_record,
            manifest=manifest,
            mapping=mapping,
            migration_evidence=migration_evidence,
        )

    def write_artifacts(
        self,
        record_json: str,
        projection: str,
        manifest: JsonObject,
        mapping: JsonObject,
        migration_evidence: JsonObject,
        evidence_builder: AdrPilotEvidenceBuilder,
        adapter: AdrStorageAdapter,
        database_path: Path,
    ) -> None:
        """Write deterministic committed pilot evidence artifacts.

        Args:
            record_json: Deterministic JSON checkpoint text.
            projection: Generated Markdown projection.
            manifest: Pilot manifest/config JSON.
            mapping: Mapping evidence JSON.
            migration_evidence: Document-store migration evidence JSON.
            evidence_builder: Review evidence builder.
            adapter: Storage adapter used for query evidence.
            database_path: Local generated SQLite path.
        """
        self.paths.json_checkpoint.write_text(record_json, encoding="utf-8")
        self.paths.markdown_projection.write_text(projection, encoding="utf-8")
        self.paths.manifest.write_text(DocumentRecord.canonical_payload_text(manifest), encoding="utf-8")
        self.paths.mapping.write_text(DocumentRecord.canonical_payload_text(mapping), encoding="utf-8")
        self.paths.migration_evidence.write_text(DocumentRecord.canonical_payload_text(migration_evidence), encoding="utf-8")
        self.paths.database_evidence.write_text(evidence_builder.database_evidence(adapter, database_path), encoding="utf-8")

    def assert_records_equal(self, expected: JsonObject, actual: JsonObject) -> None:
        """Assert that two ADR JSON records are equal.

        Args:
            expected: Expected ADR JSON record.
            actual: Actual ADR JSON record.
        """
        if expected != actual:
            raise AssertionError("ADR records differ")

    def remove_mutable_database(self, database_path: Path) -> None:
        """Remove local generated SQLite state after evidence is written.

        Args:
            database_path: Local generated SQLite path.
        """
        if database_path.exists():
            database_path.unlink()
        if database_path.parent.exists():
            shutil.rmtree(database_path.parent)


def run_pilot(repo_root: Path) -> PilotResult:
    """Run the ADR JSON/database one-ADR pilot.

    Args:
        repo_root: Repository root path.

    Returns:
        Pilot run result.
    """
    # Pilot paths are derived from the repository root argument.
    paths: PilotPaths = PilotPaths(repo_root=repo_root)
    return AdrStoragePilot(paths=paths).run()
