from __future__ import annotations

from pathlib import Path

from projectkoios.ingestors import JsonSchema, JsonSchemaLoader

from tests.projectkoios.ingestors._helpers import write_schema


def test__JsonSchemaLoader__load(tmp_path: Path) -> None:
    """Validate that JSON Schema loader reads schema fixture metadata."""
    # Schema path points at a generated local fixture schema.
    schema_path: Path = write_schema(tmp_path)
    # Schema is the typed loader result under test.
    schema: JsonSchema = JsonSchemaLoader().load(schema_path)
    assert schema.title == "projectkoios.ingestion.config"
