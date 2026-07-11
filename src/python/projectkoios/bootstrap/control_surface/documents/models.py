from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
import json

from projectkoios.bootstrap.schema.models import JsonObject


class DocumentType(StrEnum):
    """Generic document families supported by the document store pilot."""

    ADR = "adr"


class DocumentStoreBackend(StrEnum):
    """Generic document-store backend implementations represented in evidence."""

    SQLITE = "sqlite"


@dataclass(frozen=True, slots=True)
class DocumentRecord:
    """Generic JSON document-store record.

    Args:
        document_id: Stable opaque document identity.
        document_kind: Generic document family discriminator.
        payload: Canonical JSON object payload.
        content_hash: Hash of the canonical JSON payload.
        created_at: Deterministic creation timestamp supplied by caller.
        updated_at: Deterministic update timestamp supplied by caller.
    """

    document_id: str
    document_kind: DocumentType
    payload: JsonObject
    content_hash: str
    created_at: str
    updated_at: str

    @classmethod
    def canonical_payload_text(cls, payload: JsonObject) -> str:
        """Return deterministic JSON text for a payload.

        Args:
            payload: JSON object payload.

        Returns:
            Canonical JSON text.
        """
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    @classmethod
    def payload_hash(cls, payload: JsonObject) -> str:
        """Return the SHA-256 hash for canonical JSON payload text.

        Args:
            payload: JSON object payload.

        Returns:
            Hex SHA-256 digest.
        """
        # Canonical text is the stable hash input for reviewable payload evidence.
        payload_text: str = cls.canonical_payload_text(payload)
        return sha256(payload_text.encode("utf-8")).hexdigest()

    def canonical_text(self) -> str:
        """Return deterministic JSON text for this record payload.

        Returns:
            Canonical JSON text.
        """
        return self.canonical_payload_text(self.payload)

    def computed_content_hash(self) -> str:
        """Return the computed hash for this record payload.

        Returns:
            Hex SHA-256 digest.
        """
        return self.payload_hash(self.payload)
