from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from projectkoios.bootstrap.schema.models import JsonObject


class ArtifactDisposition(StrEnum):
    """Pilot artifact dispositions represented in migration evidence."""

    ADDED = "added"
    GENERATED_LOCAL_DELETED = "generated-local-deleted"
    REGENERATED = "regenerated"
    REPLACED = "replaced"
    REPLACED_WITH_PRIOR_PROVENANCE_RETAINED = "replaced-with-prior-provenance-retained"
    RETAINED_OR_REGENERATED_SAME_PAYLOAD = "retained-or-regenerated-same-payload"


class ReplacementAction(StrEnum):
    """Replacement actions represented in document-store migration evidence."""

    REMOVED_FROM_GENERIC_TABLE = "removed-from-generic-table"
    REPLACED_BY_GENERIC_DOCUMENT_STORE_PLUS_ADR_WRAPPER = "replaced-by-generic-document-store-plus-adr-wrapper"
    REPLACED_BY_JSON_DOCUMENTS = "replaced-by-json_documents"


class SourceOfTruthMode(StrEnum):
    """Source-of-truth modes represented in pilot evidence."""

    DATABASE_OPERATIONAL_JSON_CHECKPOINTED = "database-operational/json-checkpointed"


@dataclass(frozen=True, slots=True)
class PilotAdrSourceConfig:
    """Source ADR values used by the one-ADR pilot.

    Args:
        source_path: Source Markdown ADR path relative to repository root.
        legacy_filename_status_suffix: Legacy status suffix from the source filename.
        record_id: ADR record ID used for the pilot JSON record.
        slug: ADR slug used for the pilot JSON record.
        delegated_operator: Delegated operator inferred for source context.
        source_date: Source-authored date preserved outside the current ADR schema.
    """

    source_path: str = "docs/adr/adr.json-database-for-adr-storage.draft.md"
    legacy_filename_status_suffix: str = ".draft"
    record_id: str = "adr.json-database-for-adr-storage"
    slug: str = "json-database-for-adr-storage"
    delegated_operator: str = "HERMES"
    source_date: str = "20260702.121432Z"


@dataclass(frozen=True, slots=True)
class PilotPaths:
    """Filesystem paths for the bounded one-ADR pilot.

    Args:
        repo_root: Repository root.
    """

    repo_root: Path
    source_config: PilotAdrSourceConfig = PilotAdrSourceConfig()

    @property
    def source_adr(self) -> Path:
        """Return the legacy/source Markdown ADR path.

        Returns:
            Source Markdown path.
        """
        return self.repo_root / self.source_config.source_path

    @property
    def pilot_dir(self) -> Path:
        """Return the pilot artifact directory.

        Returns:
            Pilot artifact directory path.
        """
        return self.repo_root / "dev" / "adr-json-database-one-adr-pilot"

    @property
    def json_checkpoint(self) -> Path:
        """Return the schema-backed JSON checkpoint path.

        Returns:
            JSON checkpoint path.
        """
        return self.pilot_dir / "adr.json-database-for-adr-storage.json"

    @property
    def markdown_projection(self) -> Path:
        """Return the generated Markdown projection path.

        Returns:
            Markdown projection path.
        """
        return self.pilot_dir / "adr.json-database-for-adr-storage.projected.md"

    @property
    def manifest(self) -> Path:
        """Return the pilot manifest/config path.

        Returns:
            Manifest path.
        """
        return self.pilot_dir / "manifest.json"

    @property
    def mapping(self) -> Path:
        """Return the mapping evidence path.

        Returns:
            Mapping evidence path.
        """
        return self.pilot_dir / "mapping.json"

    @property
    def database_evidence(self) -> Path:
        """Return the database evidence path.

        Returns:
            Database evidence path.
        """
        return self.pilot_dir / "database-evidence.md"

    @property
    def migration_evidence(self) -> Path:
        """Return the document-store migration evidence path.

        Returns:
            Migration evidence path.
        """
        return self.pilot_dir / "document-store-migration-evidence.json"


@dataclass(frozen=True, slots=True)
class PilotResult:
    """Result of running the one-ADR pilot.

    Args:
        record: Source-derived ADR record.
        exported_record: Adapter-exported ADR record.
        projection_record: Projection-derived ADR record.
        manifest: Pilot manifest/config JSON.
        mapping: Mapping evidence JSON.
        migration_evidence: Document-store migration evidence JSON.
    """

    record: JsonObject
    exported_record: JsonObject
    projection_record: JsonObject
    manifest: JsonObject
    mapping: JsonObject
    migration_evidence: JsonObject
