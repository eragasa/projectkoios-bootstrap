from __future__ import annotations

import hashlib
import json

from projectkoios.bootstrap.schema.models import JsonObject


def hash_text(text: str) -> str:
    """Return a SHA-256 hash for UTF-8 text.

    Args:
        text: Text to hash.

    Returns:
        Hex SHA-256 digest.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json_text(data: JsonObject) -> str:
    """Serialize JSON deterministically for review artifacts.

    Args:
        data: JSON object to serialize.

    Returns:
        Stable JSON text with trailing newline.
    """
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def hash_json(data: JsonObject) -> str:
    """Return a SHA-256 hash for canonical JSON.

    Args:
        data: JSON object to hash.

    Returns:
        Hex SHA-256 digest.
    """
    return hash_text(canonical_json_text(data))
