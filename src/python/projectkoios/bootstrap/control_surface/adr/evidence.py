from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr.models import ArtifactDisposition, ReplacementAction
from projectkoios.bootstrap.control_surface.adr.storage import AdrStorageAdapter
from projectkoios.bootstrap.control_surface.documents import DocumentRecord, DocumentType
from projectkoios.bootstrap.control_surface.storage import DocumentStoreSqlSchema
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrPilotEvidenceBuilder:
    """Build review evidence for the one-ADR storage pilot."""

    sql_schema: DocumentStoreSqlSchema = DocumentStoreSqlSchema()

    def migration_evidence(self, manifest: JsonObject, mapping: JsonObject) -> JsonObject:
        """Build document-store migration evidence.

        Args:
            manifest: Pilot manifest/config JSON.
            mapping: Mapping evidence JSON.

        Returns:
            Migration evidence JSON object.
        """
        # Old surface records make the intentional break reviewable.
        old_surfaces: JsonObject = {
            "package": "projectkoios.bootstrap.control_surface.adr.storage",
            "sqlite_adapter": "SqliteAdrStorageAdapter",
            "memory_adapter": "MemoryAdrStorageAdapter",
            "table": "adr_records",
            "query_columns": [
                "slug",
                "title",
                "status",
                "routing_owner",
                "routing_next_phase",
                "schema_id",
            ],
            "json_checkpoint_path": "dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json",
            "json_checkpoint_hash": mapping["json_hash"],
            "source_path": mapping["source_path"],
            "source_hash": mapping["source_hash"],
            "old_pilot_identity": {
                "id": mapping["canonical_id"],
                "slug": mapping["canonical_slug"],
            },
        }
        # New surface records show the generic document/storage boundary.
        new_surfaces: JsonObject = {
            "documents_package": "projectkoios.bootstrap.control_surface.documents",
            "storage_package": "projectkoios.bootstrap.control_surface.storage",
            "sqlite_store": "SqliteDocumentStore",
            "memory_store": "MemoryDocumentStore",
            "table": self.sql_schema.table_name,
            "generic_columns": list(self.sql_schema.column_names()),
            "adr_wrapper_package": "projectkoios.bootstrap.control_surface.adr.storage",
            "adr_wrapper": "DocumentStoreAdrStorageAdapter",
            "document_kind_enum": "DocumentType.ADR",
            "document_kind_value": DocumentType.ADR.value,
            "json_checkpoint_hash": manifest["json_checkpoint"]["content_hash"],
        }
        return {
            "status": "pilot-derived-non-authoritative",
            "source_brief": "docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md",
            "source_plan": "docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md",
            "old_surfaces": old_surfaces,
            "new_surfaces": new_surfaces,
            "field_treatment": {
                "copied_fields": mapping["copied_fields"],
                "normalized_fields": mapping["normalized_fields"],
                "inferred_fields": mapping["inferred_fields"],
                "new_fields": [
                    "documents.package",
                    "storage.table",
                    "documents.document_kind_enum",
                    "migration_evidence",
                ],
                "retained_outside_schema": mapping["preserved_outside_schema"],
            },
            "provenance_preserved": {
                "mapping_json_prior_fields_retained": True,
                "source_draft_path_hash_retained": True,
                "old_pilot_identity_retained_as_evidence": True,
            },
            "artifact_dispositions": {
                "manifest.json": ArtifactDisposition.REPLACED.value,
                "mapping.json": ArtifactDisposition.REPLACED_WITH_PRIOR_PROVENANCE_RETAINED.value,
                "database-evidence.md": ArtifactDisposition.REPLACED.value,
                "document-store-migration-evidence.json": ArtifactDisposition.ADDED.value,
                "adr.json-database-for-adr-storage.json": ArtifactDisposition.RETAINED_OR_REGENERATED_SAME_PAYLOAD.value,
                "adr.json-database-for-adr-storage.projected.md": ArtifactDisposition.REGENERATED.value,
                "generated-local/pilot.sqlite": ArtifactDisposition.GENERATED_LOCAL_DELETED.value,
            },
            "replacement_actions": {
                "adr_specific_sqlite_adapter": ReplacementAction.REPLACED_BY_GENERIC_DOCUMENT_STORE_PLUS_ADR_WRAPPER.value,
                "adr_records_table": ReplacementAction.REPLACED_BY_JSON_DOCUMENTS.value,
                "adr_specific_query_columns": ReplacementAction.REMOVED_FROM_GENERIC_TABLE.value,
            },
            "commit_safety": {
                "docs_adr_modified": False,
                "committed_sqlite_or_db_files": False,
            },
        }

    def database_evidence(self, adapter: AdrStorageAdapter, database_path: Path) -> str:
        """Render inspectable database and adapter evidence.

        Args:
            adapter: Storage adapter used by the pilot.
            database_path: Local generated SQLite path.

        Returns:
            Markdown evidence text.
        """
        # Adapter query proves lookup behavior without exposing SQLite to callers.
        document_ids: tuple[str, ...] = adapter.list_document_ids()
        # Evidence lines are deterministic Markdown for review.
        lines: list[str] = [
            "# ADR JSON/document-store pilot database evidence",
            "",
            "Status: pilot-derived/non-authoritative evidence.",
            "",
            "## Storage adapter policy",
            "",
            "ADR workflow logic uses an ADR adapter wrapper over a generic JSON document store. SQLite is the selected pilot document-store backend only.",
            "",
            "## SQLite operational store policy",
            "",
            f"Generated database path during run: `{database_path}`",
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
            "## Replaced ADR-specific table",
            "",
            "The previous `adr_records` table and ADR-specific query columns are retained only as historical migration evidence.",
            "",
            "## Adapter query evidence",
            "",
            f"`list_by_kind(DocumentType.ADR)` returned: `{', '.join(document_ids)}`",
            "",
            "## JSON checkpoint hash",
            "",
            f"`{DocumentRecord.payload_hash(adapter.export('adr.json-database-for-adr-storage'))}`",
            "",
        ]
        return "\n".join(lines)
