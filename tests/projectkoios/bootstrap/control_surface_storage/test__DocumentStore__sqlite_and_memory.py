from __future__ import annotations

from dataclasses import fields
import sqlite3
from pathlib import Path

from projectkoios.bootstrap.control_surface.documents import DocumentRecord, DocumentType
from projectkoios.bootstrap.control_surface.storage import (
    DocumentStore,
    DocumentStoreSqlSchema,
    MemoryDocumentStore,
    SqliteDocumentStore,
)
from projectkoios.bootstrap.schema.models import JsonObject


def sample_payload() -> JsonObject:
    """Return a generic JSON payload fixture.

    Returns:
        Generic JSON payload.
    """
    return {"id": "adr.example", "title": "Example"}


def sample_record() -> DocumentRecord:
    """Return a generic document record fixture.

    Returns:
        Generic document record.
    """
    # Payload is intentionally opaque to the generic document store.
    payload: JsonObject = sample_payload()
    return DocumentRecord(
        document_id="adr.example",
        document_kind=DocumentType.ADR,
        payload=payload,
        content_hash=DocumentRecord.payload_hash(payload),
        created_at="20260711.050606Z",
        updated_at="20260711.050606Z",
    )


def test__DocumentStore__protocol__accepts_memory_and_sqlite_implementations(tmp_path: Path) -> None:
    """Verify generic stores conform to the document-store protocol."""
    # Memory store should satisfy the protocol used by callers.
    memory_store: MemoryDocumentStore = MemoryDocumentStore(records={})
    # SQLite store should satisfy the same protocol used by callers.
    sqlite_store: SqliteDocumentStore = SqliteDocumentStore(database_path=tmp_path / "documents.sqlite")
    assert isinstance(memory_store, DocumentStore)
    assert isinstance(sqlite_store, DocumentStore)


def test__DocumentStoreSqlSchema__columns__are_generated_from_document_record() -> None:
    """Generate SQLite columns from the document record model."""
    # Schema object generates SQLite columns from DocumentRecord fields.
    sql_schema: DocumentStoreSqlSchema = DocumentStoreSqlSchema()
    # Expected columns translate the payload field into its storage representation.
    expected_columns: tuple[str, ...] = tuple(
        "payload_json" if field.name == "payload" else field.name for field in fields(DocumentRecord)
    )
    assert sql_schema.column_names() == expected_columns


def test__MemoryDocumentStore__store__round_trips_payload_by_kind() -> None:
    """Store and list a generic document with the in-memory store."""
    # Store uses an in-memory backend for non-SQLite boundary proof.
    store: MemoryDocumentStore = MemoryDocumentStore(records={})
    # Record is the generic payload and metadata fixture.
    record: DocumentRecord = sample_record()
    store.store(record)
    assert store.export("adr.example") == sample_payload()
    assert store.list_by_kind(DocumentType.ADR) == ("adr.example",)


def test__SqliteDocumentStore__store__uses_generic_columns_only(tmp_path: Path) -> None:
    """Store a generic document in SQLite without ADR-specific columns."""
    # Database path is generated local test state.
    database_path: Path = tmp_path / "documents.sqlite"
    # Store owns generic SQLite persistence.
    store: SqliteDocumentStore = SqliteDocumentStore(database_path=database_path)
    # Record is the generic payload and metadata fixture.
    record: DocumentRecord = sample_record()
    store.store(record)
    assert store.export("adr.example") == sample_payload()
    assert store.list_by_kind(DocumentType.ADR) == ("adr.example",)
    # Connection inspects DDL to prove generic columns only.
    connection: sqlite3.Connection = sqlite3.connect(database_path)
    try:
        # Cursor reads the generic table column names.
        cursor: sqlite3.Cursor = connection.execute("PRAGMA table_info(json_documents)")
        # Column names are compared as a stable set.
        columns: set[str] = {str(row[1]) for row in cursor.fetchall()}
    finally:
        connection.close()
    assert columns == {
        "document_id",
        "document_kind",
        "content_hash",
        "payload_json",
        "created_at",
        "updated_at",
    }
    assert "status" not in columns
    assert "routing_next_phase" not in columns
