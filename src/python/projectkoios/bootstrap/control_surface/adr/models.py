from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class PilotPaths:
    """Filesystem paths for the bounded one-ADR pilot.

    Args:
        repo_root: Repository root.
    """

    repo_root: Path

    @property
    def source_adr(self) -> Path:
        """Return the legacy/source Markdown ADR path.

        Returns:
            Source Markdown path.
        """
        return self.repo_root / "docs" / "adr" / "adr.json-database-for-adr-storage.draft.md"

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


@dataclass(frozen=True, slots=True)
class PilotResult:
    """Result of running the one-ADR pilot.

    Args:
        record: Source-derived ADR record.
        exported_record: Adapter-exported ADR record.
        projection_record: Projection-derived ADR record.
        manifest: Pilot manifest/config JSON.
        mapping: Mapping evidence JSON.
    """

    record: JsonObject
    exported_record: JsonObject
    projection_record: JsonObject
    manifest: JsonObject
    mapping: JsonObject
