from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

from projectkoios.bootstrap.control_surface.adr.equality import AdrSemanticComparer
from projectkoios.bootstrap.control_surface.adr.hashing import canonical_json_text, hash_json
from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.adr.markdown import AdrMarkdownMapper, AdrProjectionRenderer
from projectkoios.bootstrap.control_surface.adr.models import PilotPaths, PilotResult
from projectkoios.bootstrap.control_surface.adr.storage import CREATE_TABLE_SQL, AdrStorageAdapter, SqliteAdrStorageAdapter
from projectkoios.bootstrap.control_surface.adr.validation import AdrRecordValidator
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrJsonDatabasePilot:
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
        mapper: AdrMarkdownMapper = AdrMarkdownMapper()
        record: JsonObject
        mapping: JsonObject
        record, mapping = mapper.map_source(source_markdown)
        # Schema validation is storage-independent by design.
        validator: AdrRecordValidator = AdrRecordValidator()
        validator.validate(record)
        # Invalid record captures inspectable schema failure evidence.
        invalid_record: JsonObject = dict(record)
        invalid_record["status"] = "invalid-status"
        mapping["invalid_schema_error"] = validator.invalid_record_error(invalid_record)
        # Adapter selection is isolated from mapping/validation/projection/equality.
        database_path: Path = self.paths.pilot_dir / "generated-local" / "pilot.sqlite"
        # Adapter stores the record through the approved storage boundary.
        adapter: AdrStorageAdapter = SqliteAdrStorageAdapter(
            database_path=database_path,
            schema_id=validator.schema_id(),
            timestamp=self.timestamp,
        )
        adapter.store(record)
        # Exported record is the JSON checkpoint payload from storage.
        exported_record: JsonObject = adapter.export(str(record["id"]))
        AdrSemanticComparer().assert_equal(record, exported_record)
        # Record JSON is deterministic for hash and review evidence.
        record_json: str = canonical_json_text(exported_record)
        # Manifest indexes all pilot configuration and evidence artifacts.
        manifest: JsonObject = PilotManifestBuilder(self.paths, validator.schema_id()).build(
            exported_record,
            source_markdown,
            record_json,
        )
        # Projection is rendered from record plus manifest metadata, not from SQLite.
        projection: str = AdrProjectionRenderer().render(exported_record, manifest, record_json)
        # Projection record verifies generated Markdown can recover schema data.
        projection_record: JsonObject = mapper.map_projection(projection)
        validator.validate(projection_record)
        AdrSemanticComparer().assert_equal(exported_record, projection_record)
        mapping["source_hash"] = manifest["source_adr"]["content_hash"]
        mapping["json_hash"] = manifest["json_checkpoint"]["content_hash"]
        mapping["projection_round_trip_equal"] = True
        self.write_artifacts(record_json, projection, manifest, mapping, adapter, database_path)
        self.remove_mutable_database(database_path)
        return PilotResult(
            record=record,
            exported_record=exported_record,
            projection_record=projection_record,
            manifest=manifest,
            mapping=mapping,
        )

    def write_artifacts(
        self,
        record_json: str,
        projection: str,
        manifest: JsonObject,
        mapping: JsonObject,
        adapter: AdrStorageAdapter,
        database_path: Path,
    ) -> None:
        """Write deterministic committed pilot evidence artifacts.

        Args:
            record_json: Deterministic JSON checkpoint text.
            projection: Generated Markdown projection.
            manifest: Pilot manifest/config JSON.
            mapping: Mapping evidence JSON.
            adapter: Storage adapter used for query evidence.
            database_path: Local generated SQLite path.
        """
        self.paths.json_checkpoint.write_text(record_json, encoding="utf-8")
        self.paths.markdown_projection.write_text(projection, encoding="utf-8")
        self.paths.manifest.write_text(canonical_json_text(manifest), encoding="utf-8")
        self.paths.mapping.write_text(canonical_json_text(mapping), encoding="utf-8")
        self.paths.database_evidence.write_text(self.database_evidence(adapter, database_path), encoding="utf-8")

    def database_evidence(self, adapter: AdrStorageAdapter, database_path: Path) -> str:
        """Render inspectable database and adapter evidence.

        Args:
            adapter: Storage adapter used by the pilot.
            database_path: Local generated SQLite path.

        Returns:
            Markdown evidence text.
        """
        # Adapter query proves lookup behavior without exposing SQLite to callers.
        draft_ids: tuple[str, ...] = adapter.list_by_status("draft")
        # Evidence lines are deterministic Markdown for review.
        lines: list[str] = [
            "# ADR JSON/database pilot database evidence",
            "",
            "Status: pilot-derived/non-authoritative evidence.",
            "",
            "## Storage adapter policy",
            "",
            "ADR workflow logic uses a narrow storage adapter boundary. SQLite is the selected pilot adapter implementation only.",
            "",
            "## SQLite operational store policy",
            "",
            f"Generated database path during run: `{database_path}`",
            "",
            "Mutable `.sqlite`/`.db` files are local/generated and are not committed as repository authority.",
            "",
            "## SQLite adapter DDL",
            "",
            "```sql",
            CREATE_TABLE_SQL,
            "```",
            "",
            "## Adapter query evidence",
            "",
            f"`list_by_status('draft')` returned: `{', '.join(draft_ids)}`",
            "",
            "## JSON checkpoint hash",
            "",
            f"`{hash_json(adapter.export('adr.json-database-for-adr-storage'))}`",
            "",
        ]
        return "\n".join(lines)

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
    return AdrJsonDatabasePilot(paths=paths).run()
