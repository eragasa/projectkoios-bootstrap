from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
import json
import sqlite3

from projectkoios.bootstrap.control_surface.adr.hashing import canonical_json_text, hash_json
from projectkoios.bootstrap.schema.models import JsonObject


class AdrStorageAdapter(Protocol):
    """Minimal ADR storage adapter boundary for the one-ADR pilot."""

    def store(self, record: JsonObject) -> None:
        """Store a schema-backed ADR record.

        Args:
            record: ADR record to store.
        """

    def get(self, record_id: str) -> JsonObject:
        """Return one stored ADR record by canonical ID.

        Args:
            record_id: Canonical ADR record ID.

        Returns:
            Stored ADR record.
        """

    def export(self, record_id: str) -> JsonObject:
        """Export one stored ADR record as schema-backed JSON.

        Args:
            record_id: Canonical ADR record ID.

        Returns:
            Exported ADR record.
        """

    def list_by_status(self, status: str) -> tuple[str, ...]:
        """Return stored record IDs with a lifecycle status.

        Args:
            status: ADR lifecycle status.

        Returns:
            Matching record IDs.
        """


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS adr_records (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  routing_owner TEXT NOT NULL,
  routing_next_phase TEXT NOT NULL,
  schema_id TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  record_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
)
""".strip()


@dataclass(frozen=True, slots=True)
class SqliteAdrStorageAdapter:
    """SQLite implementation of the minimal pilot storage adapter.

    Args:
        database_path: Local generated SQLite database path.
        schema_id: ADR schema identifier.
        timestamp: Deterministic pilot timestamp.
    """

    database_path: Path
    schema_id: str
    timestamp: str

    def initialize(self) -> None:
        """Create the SQLite table when needed."""
        # Parent directory is generated local state for the pilot adapter.
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        # Connection initializes the local generated SQLite adapter database.
        connection: sqlite3.Connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(CREATE_TABLE_SQL)
            connection.commit()
        finally:
            connection.close()

    def store(self, record: JsonObject) -> None:
        """Store a schema-backed ADR record in SQLite.

        Args:
            record: ADR record to store.
        """
        self.initialize()
        # Deterministic JSON is the backend payload and hash source.
        record_json: str = canonical_json_text(record)
        # Routing data is copied into query columns for pilot evidence.
        routing: object = record["routing"]
        if not isinstance(routing, dict):
            raise TypeError("ADR routing must be an object")
        # Connection writes the schema-backed payload through the SQLite adapter.
        connection: sqlite3.Connection = sqlite3.connect(self.database_path)
        try:
            connection.execute(
                """
                INSERT OR REPLACE INTO adr_records (
                  id, slug, title, status, routing_owner, routing_next_phase,
                  schema_id, content_hash, record_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(record["id"]),
                    str(record["slug"]),
                    str(record["title"]),
                    str(record["status"]),
                    str(routing["owner"]),
                    str(routing["next_phase"]),
                    self.schema_id,
                    hash_json(record),
                    record_json,
                    self.timestamp,
                    self.timestamp,
                ),
            )
            connection.commit()
        finally:
            connection.close()

    def get(self, record_id: str) -> JsonObject:
        """Return one stored ADR record by canonical ID.

        Args:
            record_id: Canonical ADR record ID.

        Returns:
            Stored ADR record.
        """
        self.initialize()
        # Connection reads the stored JSON payload through the adapter boundary.
        connection: sqlite3.Connection = sqlite3.connect(self.database_path)
        try:
            # Cursor fetches the one canonical ADR record payload.
            cursor: sqlite3.Cursor = connection.execute(
                "SELECT record_json FROM adr_records WHERE id = ?",
                (record_id,),
            )
            # Row is absent when the requested canonical ID was never stored.
            row: tuple[str] | None = cursor.fetchone()
        finally:
            connection.close()
        if row is None:
            raise KeyError(f"ADR record not found: {record_id}")
        # Stored payload is decoded back to a JSON object.
        payload: object = json.loads(row[0])
        if not isinstance(payload, dict):
            raise TypeError("Stored ADR record JSON must be an object")
        return payload

    def export(self, record_id: str) -> JsonObject:
        """Export one stored ADR record as schema-backed JSON.

        Args:
            record_id: Canonical ADR record ID.

        Returns:
            Exported ADR record.
        """
        return self.get(record_id)

    def list_by_status(self, status: str) -> tuple[str, ...]:
        """Return stored record IDs with a lifecycle status.

        Args:
            status: ADR lifecycle status.

        Returns:
            Matching record IDs.
        """
        self.initialize()
        # Connection reads query evidence through the SQLite adapter.
        connection: sqlite3.Connection = sqlite3.connect(self.database_path)
        try:
            # Cursor returns stable IDs matching the requested lifecycle status.
            cursor: sqlite3.Cursor = connection.execute(
                "SELECT id FROM adr_records WHERE status = ? ORDER BY id",
                (status,),
            )
            # Rows are converted to an immutable tuple for callers.
            rows: list[tuple[str]] = cursor.fetchall()
        finally:
            connection.close()
        return tuple(row[0] for row in rows)


@dataclass(frozen=True, slots=True)
class MemoryAdrStorageAdapter:
    """In-memory adapter used to test the storage boundary without SQLite."""

    records: dict[str, JsonObject]

    def store(self, record: JsonObject) -> None:
        """Store a schema-backed ADR record in memory.

        Args:
            record: ADR record to store.
        """
        self.records[str(record["id"])] = json.loads(canonical_json_text(record))

    def get(self, record_id: str) -> JsonObject:
        """Return one stored ADR record by canonical ID.

        Args:
            record_id: Canonical ADR record ID.

        Returns:
            Stored ADR record.
        """
        if record_id not in self.records:
            raise KeyError(f"ADR record not found: {record_id}")
        return json.loads(canonical_json_text(self.records[record_id]))

    def export(self, record_id: str) -> JsonObject:
        """Export one stored ADR record as schema-backed JSON.

        Args:
            record_id: Canonical ADR record ID.

        Returns:
            Exported ADR record.
        """
        return self.get(record_id)

    def list_by_status(self, status: str) -> tuple[str, ...]:
        """Return stored record IDs with a lifecycle status.

        Args:
            status: ADR lifecycle status.

        Returns:
            Matching record IDs.
        """
        # Sorted IDs make adapter behavior deterministic for tests.
        return tuple(sorted(record_id for record_id, record in self.records.items() if record["status"] == status))
