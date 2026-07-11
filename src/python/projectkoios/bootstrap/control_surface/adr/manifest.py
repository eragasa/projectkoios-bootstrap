from __future__ import annotations

from dataclasses import dataclass

from projectkoios.bootstrap.control_surface.adr.hashing import hash_json, hash_text
from projectkoios.bootstrap.control_surface.adr.models import PilotPaths
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
            "authority_mode": "database-operational/json-checkpointed",
            "source_adr": {
                "path": "docs/adr/adr.json-database-for-adr-storage.draft.md",
                "content_hash": hash_text(source_markdown),
                "legacy_filename_status_suffix": ".draft",
            },
            "canonical_record": {
                "id": record["id"],
                "slug": record["slug"],
                "status": record["status"],
                "status_location_rule": "Lifecycle status belongs in record content, not filename or record identity.",
            },
            "json_checkpoint": {
                "path": "dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json",
                "content_hash": hash_text(json_text),
            },
            "markdown_projection": {
                "path": "dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md",
                "status": "generated-pilot-projection-non-authoritative",
            },
            "storage_adapter": {
                "policy": "ADR mapping, validation, projection, and equality use a narrow adapter boundary and do not depend directly on SQLite.",
                "selected": "sqlite",
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
                "method": "projectkoios.bootstrap.control_surface.adr.pilot.AdrJsonDatabasePilot.run",
            },
            "conflict_rule": "Source Markdown remains migration evidence; SQLite is local operational state behind the adapter; JSON checkpoint is committed review checkpoint; generated Markdown projection is non-authoritative pilot evidence.",
            "evidence": {
                "manifest": "dev/adr-json-database-one-adr-pilot/manifest.json",
                "mapping": "dev/adr-json-database-one-adr-pilot/mapping.json",
                "database": "dev/adr-json-database-one-adr-pilot/database-evidence.md",
                "implementation_report": "docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md",
            },
            "architecture": {
                "blueprint": "docs/architecture/architecture.json-adr-storage-topology.md",
                "brief": "docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md",
                "plan": "docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md",
            },
            "watchpoints": {
                "no_docs_adr_mutation": True,
                "no_committed_sqlite_db": True,
                "source_hash_preserved": True,
                "json_hash_preserved": hash_json(record) == hash_text(json_text),
                "pilot_derived_non_authoritative": True,
            },
        }
