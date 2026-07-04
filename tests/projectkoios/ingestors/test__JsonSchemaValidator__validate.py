from __future__ import annotations

from pathlib import Path

import pytest

from projectkoios.ingestors import JsonSchema, JsonSchemaLoader, JsonSchemaValidator
from projectkoios.ingestors.schemas import JsonObject

from tests.projectkoios.ingestors._helpers import write_schema


def test__JsonSchemaValidator__validate(tmp_path: Path) -> None:
    """Validate that the local JSON schema validator accepts valid config data."""
    # Schema fixture defines the expected config object shape.
    schema: JsonSchema = JsonSchemaLoader().load(write_schema(tmp_path))
    # Validator enforces the local schema rules.
    validator: JsonSchemaValidator = JsonSchemaValidator(schema)
    # Instance contains all required ingestion config sections.
    instance: JsonObject = {
        "version": 1,
        "project": "projectkoios",
        "pipeline": {"mode": "derived-index", "answer_format": "cited_summary", "retrieval_depth": 1, "index_path": "graph/index.json"},
        "validation": {"mode": "strict"},
        "source": {"include": ["docs/adr/**/*.md"], "exclude": []},
        "ontology": {},
        "extraction": {"backend": {"name": "ollama", "model": "llama3.2", "timeout_seconds": 60, "on_failure": "error"}},
        "retrieval": {"max_nodes": 1},
        "evaluation": {},
        "presets": {},
    }
    validator.validate(instance)


def test__JsonSchemaValidator__validate__rejects_missing_key(tmp_path: Path) -> None:
    """Validate that missing required config keys fail validation."""
    # Schema fixture defines the expected config object shape.
    schema: JsonSchema = JsonSchemaLoader().load(write_schema(tmp_path))
    # Validator enforces required-key rules from the fixture schema.
    validator: JsonSchemaValidator = JsonSchemaValidator(schema)
    with pytest.raises((TypeError, ValueError)):
        validator.validate({"version": 1})
