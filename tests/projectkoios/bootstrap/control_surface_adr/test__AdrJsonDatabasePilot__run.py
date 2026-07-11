from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from projectkoios.bootstrap.control_surface.adr import (
    AdrJsonDatabasePilot,
    AdrMarkdownMapper,
    AdrRecordValidator,
    AdrSemanticComparer,
    MemoryAdrStorageAdapter,
    PilotPaths,
    PilotResult,
)
from projectkoios.bootstrap.control_surface.adr.hashing import canonical_json_text, hash_text
from projectkoios.bootstrap.schema.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ADR = REPO_ROOT / "docs" / "adr" / "adr.json-database-for-adr-storage.draft.md"


def source_record() -> JsonObject:
    """Return the source-derived pilot ADR record fixture.

    Returns:
        Source-derived ADR record.
    """
    # Source Markdown remains read-only test fixture input.
    markdown: str = SOURCE_ADR.read_text(encoding="utf-8")
    record: JsonObject
    mapping: JsonObject
    record, mapping = AdrMarkdownMapper().map_source(markdown)
    return record


def test__AdrMarkdownMapper__map_source__uses_status_free_identity() -> None:
    """Map source ADR while keeping lifecycle status out of identity."""
    # Record proves the status-free canonical identity rule.
    record: JsonObject = source_record()
    assert record["id"] == "adr.json-database-for-adr-storage"
    assert record["slug"] == "json-database-for-adr-storage"
    assert record["status"] == "draft"


def test__AdrRecordValidator__validate__accepts_source_record() -> None:
    """Validate the mapped source ADR against the plain ADR schema."""
    # Record is the schema validation target.
    record: JsonObject = source_record()
    AdrRecordValidator().validate(record)


def test__AdrRecordValidator__validate__rejects_invalid_status() -> None:
    """Reject invalid ADR schema values with inspectable errors."""
    # Record is mutated to produce a schema validation failure.
    record: JsonObject = dict(source_record())
    record["status"] = "invalid-status"
    with pytest.raises(ValidationError):
        AdrRecordValidator().validate(record)


def test__MemoryAdrStorageAdapter__export__proves_storage_boundary_without_sqlite() -> None:
    """Exercise the storage adapter contract without SQLite."""
    # Record is stored through the adapter contract.
    record: JsonObject = source_record()
    # Adapter avoids SQLite to prove backend-independent behavior.
    adapter: MemoryAdrStorageAdapter = MemoryAdrStorageAdapter(records={})
    adapter.store(record)
    # Exported record must match the input under semantic equality.
    exported: JsonObject = adapter.export("adr.json-database-for-adr-storage")
    AdrSemanticComparer().assert_equal(record, exported)
    assert adapter.list_by_status("draft") == ("adr.json-database-for-adr-storage",)


def test__AdrJsonDatabasePilot__run__writes_pilot_artifacts(tmp_path: Path) -> None:
    """Run the one-ADR pilot and write deterministic evidence artifacts."""
    # Temporary repo copy isolates generated artifacts from the real working tree.
    repo_root: Path = tmp_path / "repo"
    # Source directory contains only the approved one-ADR fixture.
    source_dir: Path = repo_root / "docs" / "adr"
    # Schema directory mirrors the canonical ADR schema for the temp repo.
    schema_dir: Path = repo_root / "docs" / "schemas"
    source_dir.mkdir(parents=True)
    schema_dir.mkdir(parents=True)
    (source_dir / SOURCE_ADR.name).write_text(SOURCE_ADR.read_text(encoding="utf-8"), encoding="utf-8")
    (schema_dir / "adr.schema.json").write_text(
        (REPO_ROOT / "docs" / "schemas" / "adr.schema.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    # Pilot paths redirect generated evidence to the temporary repo.
    paths: PilotPaths = PilotPaths(repo_root=repo_root)
    # Result exposes generated records for equality assertions.
    result: PilotResult = AdrJsonDatabasePilot(paths=paths).run()
    # Checkpoint is the committed JSON review surface.
    checkpoint: JsonObject = json.loads(paths.json_checkpoint.read_text(encoding="utf-8"))
    # Manifest is the pilot-local config and evidence index.
    manifest: JsonObject = json.loads(paths.manifest.read_text(encoding="utf-8"))
    # Mapping preserves source status suffix and inferred-field evidence.
    mapping: JsonObject = json.loads(paths.mapping.read_text(encoding="utf-8"))
    assert checkpoint == result.exported_record
    assert manifest["pilot"]["status"] == "non-authoritative-pilot"
    assert manifest["storage_adapter"]["selected"] == "sqlite"
    assert manifest["sqlite_operational_store"]["committed_database_file"] is False
    assert manifest["source_adr"]["content_hash"] == hash_text(SOURCE_ADR.read_text(encoding="utf-8"))
    assert manifest["json_checkpoint"]["content_hash"] == hash_text(canonical_json_text(checkpoint))
    assert mapping["source_filename_status_suffix"] == ".draft"
    assert not list(paths.pilot_dir.rglob("*.sqlite"))
    assert not list(paths.pilot_dir.rglob("*.db"))
    assert "GENERATED PILOT PROJECTION" in paths.markdown_projection.read_text(encoding="utf-8")
