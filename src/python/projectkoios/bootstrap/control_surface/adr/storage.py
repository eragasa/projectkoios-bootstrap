from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from projectkoios.bootstrap.control_surface.documents import DocumentRecord, DocumentType
from projectkoios.bootstrap.control_surface.storage import DocumentStore
from projectkoios.bootstrap.schema.models import JsonObject


@runtime_checkable
class AdrStorageAdapter(Protocol):
    """ADR-facing storage adapter boundary for the one-ADR pilot."""

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

    def list_document_ids(self) -> tuple[str, ...]:
        """Return stored ADR document IDs.

        Returns:
            Stored ADR document IDs.
        """


@dataclass(frozen=True, slots=True)
class DocumentStoreAdrStorageAdapter:
    """ADR-facing adapter that delegates persistence to a generic document store.

    Args:
        document_store: Generic JSON document store.
        timestamp: Deterministic pilot timestamp.
    """

    document_store: DocumentStore
    timestamp: str

    def store(self, record: JsonObject) -> None:
        """Store a schema-backed ADR record through the generic document store.

        Args:
            record: ADR record to store.
        """
        # Document ID remains ADR-owned while the generic store treats it as opaque.
        document_id: str = str(record["id"])
        # Generic record carries only document-store metadata and opaque payload.
        document_record: DocumentRecord = DocumentRecord(
            document_id=document_id,
            document_kind=DocumentType.ADR,
            payload=record,
            content_hash=DocumentRecord.payload_hash(record),
            created_at=self.timestamp,
            updated_at=self.timestamp,
        )
        self.document_store.store(document_record)

    def get(self, record_id: str) -> JsonObject:
        """Return one stored ADR record by canonical ID.

        Args:
            record_id: Canonical ADR record ID.

        Returns:
            Stored ADR record.
        """
        # Payload is validated as JSON object by the generic store implementation.
        return self.document_store.export(record_id)

    def export(self, record_id: str) -> JsonObject:
        """Export one stored ADR record as schema-backed JSON.

        Args:
            record_id: Canonical ADR record ID.

        Returns:
            Exported ADR record.
        """
        return self.get(record_id)

    def list_document_ids(self) -> tuple[str, ...]:
        """Return stored ADR document IDs.

        Returns:
            Stored ADR document IDs.
        """
        return self.document_store.list_by_kind(DocumentType.ADR)
