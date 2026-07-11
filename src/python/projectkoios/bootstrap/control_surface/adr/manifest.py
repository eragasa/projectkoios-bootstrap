from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from projectkoios.bootstrap.control_surface.adr.models import PilotPaths, SourceOfTruthMode
from projectkoios.bootstrap.control_surface.documents import DocumentRecord, DocumentStoreBackend, DocumentType
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class PilotManifestBuilder:
    """Build the pilot-local manifest/config and evidence index.

    Args:
        paths: Pilot filesystem paths.
        schema_id: ADR schema identifier.
    """

    paths: PilotPaths
    schema_id: str

    @classmethod
    def hash_text(cls, text: str) -> str:
        """Return a SHA-256 hash for UTF-8 text.

        Args:
            text: Text to hash.

        Returns:
            Hex SHA-256 digest.
        """
        return sha256(text.encode("utf-8")).hexdigest()

    def build(self, record: JsonObject, source_markdown: str, json_text: str) -> JsonObject:
        """Build the pilot manifest/config JSON.

        Args:
            record: ADR record.
            source_markdown: Legacy/source ADR Markdown text.
            json_text: Deterministic JSON checkpoint text.

        Returns:
            Manifest JSON object.
        """
        return {
            "pilot": {
                "name": "adr-json-database-one-adr-pilot",
                "status": "non-authoritative-pilot",
            },
            "authority_mode": SourceOfTruthMode.DATABASE_OPERATIONAL_JSON_CHECKPOINTED.value,
            "source_adr": {
                "path": self.paths.source_config.source_path,
                "content_hash": self.hash_text(source_markdown),
                "legacy_filename_status_suffix": self.paths.source_config.legacy_filename_status_suffix,
            },
            "canonical_record": {
                "id": record["id"],
                "slug": record["slug"],
                "status": record["status"],
                "status_location_rule": "Lifecycle status belongs in record content, not filename or record identity.",
            },
            "json_checkpoint": {
                "path": "dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json",
                "content_hash": self.hash_text(json_text),
            },
            "markdown_projection": {
                "path": "dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md",
                "status": "generated-pilot-projection-non-authoritative",
            },
            "storage_adapter": {
                "policy": "ADR mapping, validation, projection, and equality use an ADR wrapper that delegates persistence to a generic document store.",
                "selected": DocumentStoreBackend.SQLITE.value,
                "adr_wrapper": "projectkoios.bootstrap.control_surface.adr.storage.DocumentStoreAdrStorageAdapter",
            },
            "document_store": {
                "documents_package": "projectkoios.bootstrap.control_surface.documents",
                "storage_package": "projectkoios.bootstrap.control_surface.storage",
                "sqlite_store": "SqliteDocumentStore",
                "memory_store": "MemoryDocumentStore",
                "table": "json_documents",
                "document_kind_enum": "DocumentType.ADR",
                "document_kind_value": DocumentType.ADR.value,
                "generic_columns": [
                    "document_id",
                    "document_kind",
                    "content_hash",
                    "payload_json",
                    "created_at",
                    "updated_at",
                ],
            },
            "sqlite_operational_store": {
                "policy": "Mutable .sqlite/.db files are local/generated and not committed.",
                "committed_database_file": False,
            },
            "schema": {
                "path": "docs/schemas/adr.schema.json",
                "id": self.schema_id,
            },
            "generation": {
                "method": "projectkoios.bootstrap.control_surface.adr.pilot.AdrStoragePilot.run",
            },
            "conflict_rule": "Source Markdown remains migration evidence; SQLite is local operational state behind the adapter; JSON checkpoint is committed review checkpoint; generated Markdown projection is non-authoritative pilot evidence.",
            "evidence": {
                "manifest": "dev/adr-json-database-one-adr-pilot/manifest.json",
                "mapping": "dev/adr-json-database-one-adr-pilot/mapping.json",
                "database": "dev/adr-json-database-one-adr-pilot/database-evidence.md",
                "migration": "dev/adr-json-database-one-adr-pilot/document-store-migration-evidence.json",
                "implementation_report": "docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md",
            },
            "architecture": {
                "blueprint": "docs/architecture/architecture.json-adr-storage-topology.md",
                "brief": "docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md",
                "plan": "docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md",
            },
            "watchpoints": {
                "no_docs_adr_mutation": True,
                "no_committed_sqlite_db": True,
                "source_hash_preserved": True,
                "json_hash_preserved": DocumentRecord.payload_hash(record) == self.hash_text(json_text),
                "pilot_derived_non_authoritative": True,
            },
        }
