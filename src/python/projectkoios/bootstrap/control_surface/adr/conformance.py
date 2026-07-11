from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.adr.markdown import AdrMarkdownRecordParser, AdrProjectionRenderer
from projectkoios.bootstrap.control_surface.adr.models import PilotAdrSourceConfig
from projectkoios.bootstrap.control_surface.adr.storage import AdrStorageAdapter, DocumentStoreAdrStorageAdapter
from projectkoios.bootstrap.control_surface.adr.validation import AdrRecordValidator
from projectkoios.bootstrap.control_surface.documents import DocumentRecord, DocumentType
from projectkoios.bootstrap.control_surface.storage import DocumentStoreSqlSchema, SqliteDocumentStore
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrConformancePaths:
    """Filesystem paths for one active ADR conformance slice.

    Args:
        repo_root: Repository root.
        source_config: Target ADR source configuration.
    """

    repo_root: Path
    source_config: PilotAdrSourceConfig = PilotAdrSourceConfig(
        source_path="docs/adr/adr.json-schemas.draft.md",
        legacy_filename_status_suffix=".draft",
        record_id="adr.json-schemas",
        slug="json-schemas",
        delegated_operator="pi",
        source_date="20260702.213000Z",
    )

    @property
    def source_adr(self) -> Path:
        """Return source Markdown ADR path."""
        return self.repo_root / self.source_config.source_path

    @property
    def target_dir(self) -> Path:
        """Return target conformance artifact directory."""
        return self.repo_root / "dev" / "adr-json-schemas-conformance"

    @property
    def json_checkpoint(self) -> Path:
        """Return active conformed ADR JSON checkpoint path."""
        return self.target_dir / "adr.json-schemas.json"

    @property
    def markdown_projection(self) -> Path:
        """Return generated Markdown projection path."""
        return self.target_dir / "adr.json-schemas.projected.md"

    @property
    def manifest(self) -> Path:
        """Return manifest path."""
        return self.target_dir / "manifest.json"

    @property
    def mapping(self) -> Path:
        """Return mapping evidence path."""
        return self.target_dir / "mapping.json"

    @property
    def conversion_evidence(self) -> Path:
        """Return conversion evidence path."""
        return self.target_dir / "conversion-evidence.json"

    @property
    def database_evidence(self) -> Path:
        """Return database evidence path."""
        return self.target_dir / "database-evidence.md"

    @property
    def generated_database(self) -> Path:
        """Return local generated SQLite database path."""
        return self.target_dir / "generated-local" / "conformance.sqlite"


@dataclass(frozen=True, slots=True)
class AdrConformanceResult:
    """Result of running one active ADR conformance slice."""

    record: JsonObject
    exported_record: JsonObject
    projection_record: JsonObject
    manifest: JsonObject
    mapping: JsonObject
    conversion_evidence: JsonObject


@dataclass(frozen=True, slots=True)
class AdrConformanceRunner:
    """Run one active ADR conformance slice through the document store."""

    paths: AdrConformancePaths
    timestamp: str = "20260711.062654Z"
    sql_schema: DocumentStoreSqlSchema = DocumentStoreSqlSchema()

    def run(self) -> AdrConformanceResult:
        """Run conformance and write deterministic evidence artifacts."""
        self.paths.target_dir.mkdir(parents=True, exist_ok=True)
        # Source Markdown remains unmutated source material for this conformance run.
        source_markdown: str = self.paths.source_adr.read_text(encoding="utf-8")
        # Parser maps the approved source into the current ADR schema record shape.
        parser: AdrMarkdownRecordParser = AdrMarkdownRecordParser(source_config=self.paths.source_config)
        record: JsonObject
        mapping: JsonObject
        record, mapping = parser.parse_source_record(source_markdown)
        # Validator proves the generated record conforms before storage/projection.
        validator: AdrRecordValidator = AdrRecordValidator()
        validator.validate(record)
        # Document store exercises the generic SQLite substrate for this active record.
        document_store: SqliteDocumentStore = SqliteDocumentStore(database_path=self.paths.generated_database)
        # Adapter keeps ADR-specific behavior outside generic document storage.
        adapter: AdrStorageAdapter = DocumentStoreAdrStorageAdapter(document_store=document_store, timestamp=self.timestamp)
        adapter.store(record)
        # Exported record proves store/export round trip through the adapter.
        exported_record: JsonObject = adapter.export(str(record["id"]))
        self.assert_records_equal(record, exported_record)
        # Canonical record JSON is the checkpoint and hash source.
        record_json: str = DocumentRecord.canonical_payload_text(exported_record)
        # Manifest indexes the active record, source, storage, and validation evidence.
        manifest: JsonObject = self.build_manifest(exported_record, source_markdown, record_json, validator.schema_id())
        # Projection is generated review evidence and does not mutate source ADR Markdown.
        projection: str = AdrProjectionRenderer().render(exported_record, manifest, record_json)
        # Projection record confirms generated Markdown preserves schema content.
        projection_record: JsonObject = parser.parse_projection_record(projection)
        validator.validate(projection_record)
        self.assert_records_equal(exported_record, projection_record)
        # Projection hash lets sidecar evidence detect generated artifact drift.
        projection_hash: str = PilotManifestBuilder.hash_text(projection)
        mapping = self.enrich_mapping(mapping, source_markdown, record_json, projection_hash)
        # Conversion evidence preserves source-only fields outside the schema record.
        conversion_evidence: JsonObject = self.build_conversion_evidence(
            manifest=manifest,
            mapping=mapping,
            projection_hash=projection_hash,
        )
        self.write_artifacts(record_json, projection, manifest, mapping, conversion_evidence, adapter)
        self.remove_mutable_database()
        return AdrConformanceResult(
            record=record,
            exported_record=exported_record,
            projection_record=projection_record,
            manifest=manifest,
            mapping=mapping,
            conversion_evidence=conversion_evidence,
        )

    def build_manifest(self, record: JsonObject, source_markdown: str, record_json: str, schema_id: str) -> JsonObject:
        """Build target-local active conformance manifest."""
        return {
            "conformance": {
                "name": "adr-json-schemas-conformance",
                "status": "active-conformance-record",
                "active_going_forward": True,
            },
            "authority_mode": "active-json-checkpoint-with-sidecar-provenance",
            "source_adr": {
                "path": self.paths.source_config.source_path,
                "content_hash": PilotManifestBuilder.hash_text(source_markdown),
                "status": "draft",
                "date": self.paths.source_config.source_date,
                "legacy_filename_status_suffix": self.paths.source_config.legacy_filename_status_suffix,
                "mutated": False,
            },
            "canonical_record": {
                "id": record["id"],
                "slug": record["slug"],
                "status": record["status"],
                "document_type": DocumentType.ADR.value,
            },
            "json_checkpoint": {
                "path": "dev/adr-json-schemas-conformance/adr.json-schemas.json",
                "content_hash": PilotManifestBuilder.hash_text(record_json),
                "active_going_forward": True,
            },
            "markdown_projection": {
                "path": "dev/adr-json-schemas-conformance/adr.json-schemas.projected.md",
                "status": "generated-conformance-projection",
            },
            "schema": {
                "path": "docs/schemas/adr.schema.json",
                "id": schema_id,
                "content_hash": PilotManifestBuilder.hash_text(
                    (self.paths.repo_root / "docs" / "schemas" / "adr.schema.json").read_text(encoding="utf-8")
                ),
                "routing_allowed": False,
            },
            "storage_adapter": {
                "policy": "ADR conformance uses an ADR adapter wrapper over the generic JSON document store.",
                "selected": "sqlite",
                "adr_wrapper": "projectkoios.bootstrap.control_surface.adr.storage.DocumentStoreAdrStorageAdapter",
            },
            "document_store": {
                "documents_package": "projectkoios.bootstrap.control_surface.documents",
                "storage_package": "projectkoios.bootstrap.control_surface.storage",
                "sqlite_store": "SqliteDocumentStore",
                "memory_store": "MemoryDocumentStore",
                "table": self.sql_schema.table_name,
                "document_kind_enum": "DocumentType.ADR",
                "document_kind_value": DocumentType.ADR.value,
                "generic_columns": list(self.sql_schema.column_names()),
            },
            "sqlite_operational_store": {
                "policy": "Mutable .sqlite/.db files are local/generated and not committed.",
                "path": "dev/adr-json-schemas-conformance/generated-local/conformance.sqlite",
                "committed_database_file": False,
            },
            "generation": {
                "method": "projectkoios.bootstrap.control_surface.adr.conformance.AdrConformanceRunner.run",
            },
            "conflict_rule": "The JSON checkpoint is the active conformed record for this target ADR; source Markdown remains unmutated source evidence; sidecars preserve conversion provenance; SQLite is generated local operational state.",
            "evidence": {
                "manifest": "dev/adr-json-schemas-conformance/manifest.json",
                "mapping": "dev/adr-json-schemas-conformance/mapping.json",
                "conversion": "dev/adr-json-schemas-conformance/conversion-evidence.json",
                "database": "dev/adr-json-schemas-conformance/database-evidence.md",
                "plan": "docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md",
            },
            "watchpoints": {
                "no_docs_adr_mutation": True,
                "no_committed_sqlite_db": True,
                "routing_absent_from_record": "routing" not in record,
                "sidecar_preserves_routing": True,
                "sidecar_preserves_links_related": True,
                "active_conformed_record": True,
            },
        }

    def enrich_mapping(
        self,
        mapping: JsonObject,
        source_markdown: str,
        record_json: str,
        projection_hash: str,
    ) -> JsonObject:
        """Add target-specific conversion details to parser mapping notes."""
        # Enriched mapping records target-specific paths and hashes.
        enriched: JsonObject = dict(mapping)
        enriched["status"] = "active-conformance-record"
        enriched["source_hash"] = PilotManifestBuilder.hash_text(source_markdown)
        enriched["json_hash"] = PilotManifestBuilder.hash_text(record_json)
        enriched["projection_hash"] = projection_hash
        enriched["json_checkpoint_path"] = "dev/adr-json-schemas-conformance/adr.json-schemas.json"
        enriched["projection_path"] = "dev/adr-json-schemas-conformance/adr.json-schemas.projected.md"
        enriched["omitted_from_record"] = [
            "routing.owner",
            "routing.next_phase",
            "routing.notes",
            "links.related",
            "source.date",
        ]
        return enriched

    def build_conversion_evidence(self, manifest: JsonObject, mapping: JsonObject, projection_hash: str) -> JsonObject:
        """Build sidecar conversion evidence for the conformed record."""
        # Preserved source-only fields are copied from parser mapping evidence.
        preserved: object = mapping["preserved_outside_schema"]
        if not isinstance(preserved, dict):
            raise TypeError("preserved_outside_schema must be an object")
        return {
            "status": "active-conformance-record",
            "source": {
                "path": manifest["source_adr"]["path"],
                "sha256": manifest["source_adr"]["content_hash"],
                "date": manifest["source_adr"]["date"],
                "status": manifest["source_adr"]["status"],
                "mutated": False,
            },
            "schema": {
                "path": manifest["schema"]["path"],
                "sha256": manifest["schema"]["content_hash"],
                "routing_allowed": False,
            },
            "record": {
                "id": manifest["canonical_record"]["id"],
                "slug": manifest["canonical_record"]["slug"],
                "path": manifest["json_checkpoint"]["path"],
                "document_type": DocumentType.ADR.value,
                "content_hash": manifest["json_checkpoint"]["content_hash"],
                "schema_valid": True,
                "active_going_forward": True,
            },
            "projection": {
                "path": manifest["markdown_projection"]["path"],
                "sha256": projection_hash,
                "generated_from_record_hash": manifest["json_checkpoint"]["content_hash"],
            },
            "storage": {
                "documents_package": manifest["document_store"]["documents_package"],
                "storage_package": manifest["document_store"]["storage_package"],
                "adr_wrapper": "DocumentStoreAdrStorageAdapter",
                "sqlite_store": manifest["document_store"]["sqlite_store"],
                "memory_store": manifest["document_store"]["memory_store"],
                "table": manifest["document_store"]["table"],
                "generated_local_database": manifest["sqlite_operational_store"]["path"],
                "committed_sqlite_or_db_files": False,
            },
            "field_treatment": {
                "copied_fields": mapping["copied_fields"],
                "normalized_fields": mapping["normalized_fields"],
                "omitted_from_record": mapping["omitted_from_record"],
                "omitted_from_record_preserved_in_sidecar": {
                    "routing": preserved["routing"],
                    "links.related": preserved["links.related"],
                    "source_date": preserved["source_date"],
                },
            },
            "artifact_paths": {
                "old_source_markdown": manifest["source_adr"]["path"],
                "new_json_checkpoint": manifest["json_checkpoint"]["path"],
                "new_projection": manifest["markdown_projection"]["path"],
                "new_manifest": manifest["evidence"]["manifest"],
                "new_mapping": manifest["evidence"]["mapping"],
                "new_conversion_evidence": manifest["evidence"]["conversion"],
            },
        }

    def write_artifacts(
        self,
        record_json: str,
        projection: str,
        manifest: JsonObject,
        mapping: JsonObject,
        conversion_evidence: JsonObject,
        adapter: AdrStorageAdapter,
    ) -> None:
        """Write conformance artifacts."""
        self.paths.json_checkpoint.write_text(record_json, encoding="utf-8")
        self.paths.markdown_projection.write_text(projection, encoding="utf-8")
        self.paths.manifest.write_text(DocumentRecord.canonical_payload_text(manifest), encoding="utf-8")
        self.paths.mapping.write_text(DocumentRecord.canonical_payload_text(mapping), encoding="utf-8")
        self.paths.conversion_evidence.write_text(
            DocumentRecord.canonical_payload_text(conversion_evidence), encoding="utf-8"
        )
        self.paths.database_evidence.write_text(self.database_evidence(adapter), encoding="utf-8")

    def database_evidence(self, adapter: AdrStorageAdapter) -> str:
        """Render database evidence for the conformance run."""
        # Document IDs prove generic list-by-kind behavior through the ADR adapter.
        document_ids: tuple[str, ...] = adapter.list_document_ids()
        # Lines render human-readable database evidence for reviewers.
        lines: list[str] = [
            "# ADR JSON schemas conformance database evidence",
            "",
            "Status: active conformance record evidence.",
            "",
            "## Storage adapter policy",
            "",
            "ADR conformance logic uses an ADR adapter wrapper over a generic JSON document store. SQLite is the selected generated-local backend only.",
            "",
            "## SQLite operational store policy",
            "",
            f"Generated database path during run: `{self.paths.generated_database}`",
            "",
            "Mutable `.sqlite`/`.db` files are local/generated and are not committed as repository authority.",
            "",
            "## SQLite document-store DDL",
            "",
            "```sql",
            self.sql_schema.create_table_sql(),
            "```",
            "",
            "## SQLite document-store index",
            "",
            "```sql",
            self.sql_schema.create_kind_index_sql(),
            "```",
            "",
            "## Adapter query evidence",
            "",
            f"`list_by_kind(DocumentType.ADR)` returned: `{', '.join(document_ids)}`",
            "",
            "## JSON checkpoint hash",
            "",
            f"`{DocumentRecord.payload_hash(adapter.export('adr.json-schemas'))}`",
            "",
        ]
        return "\n".join(lines)

    def assert_records_equal(self, expected: JsonObject, actual: JsonObject) -> None:
        """Assert records are equal."""
        if expected != actual:
            raise AssertionError("ADR records differ")

    def remove_mutable_database(self) -> None:
        """Remove local generated SQLite state after evidence is written."""
        # Database path is generated local state and must not be committed.
        database_path: Path = self.paths.generated_database
        if database_path.exists():
            database_path.unlink()
        if database_path.parent.exists():
            shutil.rmtree(database_path.parent)


def run_json_schemas_conformance(repo_root: Path) -> AdrConformanceResult:
    """Run the JSON schemas ADR conformance slice."""
    return AdrConformanceRunner(paths=AdrConformancePaths(repo_root=repo_root)).run()

