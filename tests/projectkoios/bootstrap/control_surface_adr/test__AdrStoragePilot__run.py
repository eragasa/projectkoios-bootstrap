from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from projectkoios.bootstrap.control_surface.adr import (
    AdrStoragePilot,
    AdrMarkdownRecordParser,
    AdrRecordValidator,
    AdrStorageAdapter,
    DocumentStoreAdrStorageAdapter,
    PilotPaths,
    PilotResult,
)
from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.documents import DocumentRecord, DocumentType
from projectkoios.bootstrap.control_surface.storage import MemoryDocumentStore
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
    record, mapping = AdrMarkdownRecordParser().parse_source_record(markdown)
    return record


def test__AdrMarkdownRecordParser__parse_source_record__uses_status_free_identity() -> None:
    """Parse pilot source ADR while keeping lifecycle status out of identity."""
    # Record proves the status-free canonical identity rule.
    record: JsonObject = source_record()
    assert record["id"] == "adr.json-database-for-adr-storage"
    assert record["slug"] == "json-database-for-adr-storage"
    assert record["status"] == "draft"
    assert "routing" not in record


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


def test__DocumentStoreAdrStorageAdapter__protocol__conforms_to_adr_storage_adapter() -> None:
    """Verify ADR wrapper conforms to the ADR storage adapter protocol."""
    # Document store avoids SQLite for the protocol check.
    document_store: MemoryDocumentStore = MemoryDocumentStore(records={})
    # Adapter must satisfy the ADR-facing storage boundary.
    adapter: DocumentStoreAdrStorageAdapter = DocumentStoreAdrStorageAdapter(
        document_store=document_store,
        timestamp="20260711.034817Z",
    )
    assert isinstance(adapter, AdrStorageAdapter)


def test__DocumentStoreAdrStorageAdapter__export__proves_storage_boundary_without_sqlite() -> None:
    """Exercise the ADR storage adapter contract without SQLite."""
    # Record is stored through the ADR adapter contract.
    record: JsonObject = source_record()
    # Document store avoids SQLite to prove backend-independent behavior.
    document_store: MemoryDocumentStore = MemoryDocumentStore(records={})
    # Adapter delegates persistence to the generic document store.
    adapter: DocumentStoreAdrStorageAdapter = DocumentStoreAdrStorageAdapter(
        document_store=document_store,
        timestamp="20260711.034817Z",
    )
    adapter.store(record)
    # Exported record must match the input record.
    exported: JsonObject = adapter.export("adr.json-database-for-adr-storage")
    assert exported == record
    assert adapter.list_document_ids() == ("adr.json-database-for-adr-storage",)
    assert document_store.list_by_kind(DocumentType.ADR) == ("adr.json-database-for-adr-storage",)


def test__AdrStoragePilot__run__writes_pilot_artifacts(tmp_path: Path) -> None:
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
    result: PilotResult = AdrStoragePilot(paths=paths).run()
    # Checkpoint is the committed JSON review surface.
    checkpoint: JsonObject = json.loads(paths.json_checkpoint.read_text(encoding="utf-8"))
    # Manifest is the pilot-local config and evidence index.
    manifest: JsonObject = json.loads(paths.manifest.read_text(encoding="utf-8"))
    # Mapping preserves source status suffix and inferred-field evidence.
    mapping: JsonObject = json.loads(paths.mapping.read_text(encoding="utf-8"))
    # Migration evidence records the intentional storage-substrate break.
    migration_evidence: JsonObject = json.loads(paths.migration_evidence.read_text(encoding="utf-8"))
    assert checkpoint == result.exported_record
    assert "routing" not in checkpoint
    assert manifest["pilot"]["status"] == "non-authoritative-pilot"
    assert manifest["storage_adapter"]["selected"] == "sqlite"
    assert manifest["document_store"]["document_kind_enum"] == "DocumentType.ADR"
    assert manifest["sqlite_operational_store"]["committed_database_file"] is False
    assert manifest["source_adr"]["content_hash"] == PilotManifestBuilder.hash_text(
        SOURCE_ADR.read_text(encoding="utf-8")
    )
    assert manifest["json_checkpoint"]["content_hash"] == PilotManifestBuilder.hash_text(
        DocumentRecord.canonical_payload_text(checkpoint)
    )
    assert mapping["source_filename_status_suffix"] == ".draft"
    assert migration_evidence["new_surfaces"]["document_kind_enum"] == "DocumentType.ADR"
    assert migration_evidence["old_surfaces"]["table"] == "adr_records"
    assert migration_evidence["new_surfaces"]["table"] == "json_documents"
    assert not list(paths.pilot_dir.rglob("*.sqlite"))
    assert not list(paths.pilot_dir.rglob("*.db"))
    assert "GENERATED PILOT PROJECTION" in paths.markdown_projection.read_text(encoding="utf-8")
