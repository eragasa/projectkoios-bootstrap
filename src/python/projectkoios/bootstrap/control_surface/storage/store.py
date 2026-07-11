from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable
import json

from projectkoios.bootstrap.control_surface.documents.models import DocumentRecord, DocumentType
from projectkoios.bootstrap.schema.models import JsonObject


@runtime_checkable
class DocumentStore(Protocol):
    """Generic JSON document-store boundary."""

    def store(self, record: DocumentRecord) -> None:
        """Store a generic JSON document record.

        Args:
            record: Generic document record to persist.
        """

    def get(self, document_id: str) -> DocumentRecord:
        """Return a generic JSON document record by ID.

        Args:
            document_id: Stable opaque document ID.

        Returns:
            Stored document record.
        """

    def export(self, document_id: str) -> JsonObject:
        """Export one stored payload by document ID.

        Args:
            document_id: Stable opaque document ID.

        Returns:
            Stored JSON payload.
        """

    def list_by_kind(self, document_kind: DocumentType) -> tuple[str, ...]:
        """Return document IDs for a generic document kind.

        Args:
            document_kind: Generic document family discriminator.

        Returns:
            Matching document IDs.
        """


@dataclass(frozen=True, slots=True)
class MemoryDocumentStore:
    """In-memory generic document store for tests and adapter-boundary checks.

    Args:
        records: Mutable backing map keyed by document ID.
    """

    records: dict[str, DocumentRecord] = field(default_factory=dict)

    def store(self, record: DocumentRecord) -> None:
        """Store a generic JSON document record.

        Args:
            record: Generic document record to persist.
        """
        # Payload text round-trips through JSON to keep memory behavior storage-like.
        payload_text: str = record.canonical_text()
        # Payload copy prevents callers from mutating stored in-memory evidence.
        payload_copy: object = json.loads(payload_text)
        if not isinstance(payload_copy, dict):
            raise TypeError("Stored document payload must be a JSON object")
        # Stored record preserves generic metadata while copying payload content.
        stored_record: DocumentRecord = DocumentRecord(
            document_id=record.document_id,
            document_kind=record.document_kind,
            payload=payload_copy,
            content_hash=DocumentRecord.payload_hash(payload_copy),
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
        self.records[record.document_id] = stored_record

    def get(self, document_id: str) -> DocumentRecord:
        """Return a generic JSON document record by ID.

        Args:
            document_id: Stable opaque document ID.

        Returns:
            Stored document record.
        """
        if document_id not in self.records:
            raise KeyError(f"Document not found: {document_id}")
        # Stored record is copied through store mechanics to avoid exposing internals.
        stored_record: DocumentRecord = self.records[document_id]
        return DocumentRecord(
            document_id=stored_record.document_id,
            document_kind=stored_record.document_kind,
            payload=json.loads(stored_record.canonical_text()),
            content_hash=stored_record.content_hash,
            created_at=stored_record.created_at,
            updated_at=stored_record.updated_at,
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
        # Matching IDs are sorted for deterministic tests and evidence.
        matching_ids: list[str] = [
            document_id for document_id, record in self.records.items() if record.document_kind == document_kind
        ]
        return tuple(sorted(matching_ids))
