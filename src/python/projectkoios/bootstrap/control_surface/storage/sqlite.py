from __future__ import annotations

from dataclasses import dataclass, fields
from enum import StrEnum
from pathlib import Path
import json
import sqlite3

from projectkoios.bootstrap.control_surface.documents.models import DocumentRecord, DocumentType
from projectkoios.bootstrap.schema.models import JsonObject


class SqliteColumnType(StrEnum):
    """SQLite column types used by the generic document store."""

    TEXT = "TEXT"


@dataclass(frozen=True, slots=True)
class SqliteColumn:
    """SQLite column generated from a document record field.

    Args:
        name: SQLite column name.
        column_type: SQLite column type.
        primary_key: Whether this column is the primary key.
        not_null: Whether this column rejects null values.
    """

    name: str
    column_type: SqliteColumnType
    primary_key: bool
    not_null: bool

    def ddl(self) -> str:
        """Return the column DDL fragment.

        Returns:
            SQLite column definition.
        """
        # Parts are assembled explicitly so key/null flags cannot drift from the schema.
        parts: list[str] = [self.name, self.column_type.value]
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if self.not_null:
            parts.append("NOT NULL")
        return " ".join(parts)


@dataclass(frozen=True, slots=True)
class DocumentStoreSqlSchema:
    """Generate SQLite schema from the generic document record model.

    Args:
        table_name: SQLite table name for generic documents.
    """

    table_name: str = "json_documents"

    def columns(self) -> tuple[SqliteColumn, ...]:
        """Return SQLite columns generated from `DocumentRecord` fields.

        Returns:
            SQLite column definitions.
        """
        # Record field names are the source for the SQLite table shape.
        record_field_names: tuple[str, ...] = tuple(field.name for field in fields(DocumentRecord))
        return tuple(self.column_for_record_field(field_name) for field_name in record_field_names)

    def column_for_record_field(self, field_name: str) -> SqliteColumn:
        """Return a SQLite column for one document record field.

        Args:
            field_name: `DocumentRecord` field name.

        Returns:
            SQLite column definition.
        """
        # Payload is stored as canonical JSON text, so the storage column is explicit.
        column_name: str = "payload_json" if field_name == "payload" else field_name
        # Document ID is the stable storage key for one document.
        primary_key: bool = field_name == "document_id"
        return SqliteColumn(
            name=column_name,
            column_type=SqliteColumnType.TEXT,
            primary_key=primary_key,
            not_null=True,
        )

    def column_names(self) -> tuple[str, ...]:
        """Return generated SQLite column names.

        Returns:
            SQLite column names.
        """
        return tuple(column.name for column in self.columns())

    def placeholders(self) -> str:
        """Return SQL placeholders for all columns.

        Returns:
            Comma-separated SQL placeholders.
        """
        # Placeholder count follows generated columns.
        return ", ".join("?" for column in self.columns())

    def create_table_sql(self) -> str:
        """Return generated table DDL.

        Returns:
            SQLite `CREATE TABLE` statement.
        """
        # Column DDL follows the generated document-store columns.
        column_ddl: str = ",\n  ".join(column.ddl() for column in self.columns())
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} (\n  {column_ddl}\n)"

    def create_kind_index_sql(self) -> str:
        """Return generated document-kind index DDL.

        Returns:
            SQLite `CREATE INDEX` statement.
        """
        return f"CREATE INDEX IF NOT EXISTS idx_{self.table_name}_kind\nON {self.table_name} (document_kind, document_id)"

    def insert_sql(self) -> str:
        """Return generated insert/update SQL.

        Returns:
            SQLite insert statement.
        """
        # Insert columns follow the schema-generated column order.
        columns: str = ", ".join(self.column_names())
        return f"INSERT OR REPLACE INTO {self.table_name} ({columns}) VALUES ({self.placeholders()})"

    def select_by_id_sql(self) -> str:
        """Return generated lookup SQL.

        Returns:
            SQLite select statement.
        """
        # Select columns follow the schema-generated column order.
        columns: str = ", ".join(self.column_names())
        return f"SELECT {columns} FROM {self.table_name} WHERE document_id = ?"

    def list_by_kind_sql(self) -> str:
        """Return generated kind query SQL.

        Returns:
            SQLite select statement.
        """
        return f"SELECT document_id FROM {self.table_name} WHERE document_kind = ? ORDER BY document_id"


def create_table_sql() -> str:
    """Return generated generic JSON document-store table DDL.

    Returns:
        SQLite DDL for the generic JSON document table.
    """
    return DocumentStoreSqlSchema().create_table_sql()


def create_kind_index_sql() -> str:
    """Return generated generic JSON document-store kind index DDL.

    Returns:
        SQLite DDL for the generic document-kind index.
    """
    return DocumentStoreSqlSchema().create_kind_index_sql()


@dataclass(frozen=True, slots=True)
class SqliteDocumentStore:
    """SQLite implementation of the generic JSON document store.

    Args:
        database_path: Local generated SQLite database path.
        sql_schema: Generated SQLite schema for document records.
    """

    database_path: Path
    sql_schema: DocumentStoreSqlSchema = DocumentStoreSqlSchema()

    def initialize(self) -> None:
        """Create the generic SQLite table and indexes when needed."""
        # Parent directory is generated local state for the pilot store.
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        # Connection initializes the local generated SQLite document store.
        connection: sqlite3.Connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(self.sql_schema.create_table_sql())
            connection.execute(self.sql_schema.create_kind_index_sql())
            connection.commit()
        finally:
            connection.close()

    def store(self, record: DocumentRecord) -> None:
        """Store a generic JSON document record.

        Args:
            record: Generic document record to persist.
        """
        self.initialize()
        # Payload text is the storage payload and content-hash source.
        payload_json: str = record.canonical_text()
        # Content hash is recomputed by the store to enforce generic consistency.
        content_hash: str = record.computed_content_hash()
        # Row values follow `DocumentStoreSqlSchema.column_names()` order.
        row_values: tuple[str, str, str, str, str, str] = (
            record.document_id,
            record.document_kind.value,
            payload_json,
            content_hash,
            record.created_at,
            record.updated_at,
        )
        # Connection writes only generic columns and opaque payload content.
        connection: sqlite3.Connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(self.sql_schema.insert_sql(), row_values)
            connection.commit()
        finally:
            connection.close()

    def get(self, document_id: str) -> DocumentRecord:
        """Return a generic JSON document record by ID.

        Args:
            document_id: Stable opaque document ID.

        Returns:
            Stored document record.
        """
        self.initialize()
        # Connection reads generic metadata and opaque payload through the store.
        connection: sqlite3.Connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            # Cursor fetches one generic document row by stable identity.
            cursor: sqlite3.Cursor = connection.execute(self.sql_schema.select_by_id_sql(), (document_id,))
            # Row is absent when the requested document was never stored.
            row: sqlite3.Row | None = cursor.fetchone()
        finally:
            connection.close()
        if row is None:
            raise KeyError(f"Document not found: {document_id}")
        # Payload is decoded after storage lookup so callers receive JSON data.
        payload: object = json.loads(row["payload_json"])
        if not isinstance(payload, dict):
            raise TypeError("Stored document payload must be a JSON object")
        return DocumentRecord(
            document_id=str(row["document_id"]),
            document_kind=DocumentType(str(row["document_kind"])),
            payload=payload,
            content_hash=str(row["content_hash"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )

    def export(self, document_id: str) -> JsonObject:
        """Export one stored payload by document ID.

        Args:
            document_id: Stable opaque document ID.

        Returns:
            Stored JSON payload.
        """
        return self.get(document_id).payload

    def list_by_kind(self, document_kind: DocumentType) -> tuple[str, ...]:
        """Return document IDs for a generic document kind.

        Args:
            document_kind: Generic document family discriminator.

        Returns:
            Matching document IDs.
        """
        self.initialize()
        # Connection reads generic kind query evidence through the store.
        connection: sqlite3.Connection = sqlite3.connect(self.database_path)
        try:
            # Cursor returns stable IDs matching the requested generic kind.
            cursor: sqlite3.Cursor = connection.execute(self.sql_schema.list_by_kind_sql(), (document_kind.value,))
            # Rows are converted to an immutable tuple for callers.
            rows: list[tuple[str]] = cursor.fetchall()
        finally:
            connection.close()
        return tuple(row[0] for row in rows)
