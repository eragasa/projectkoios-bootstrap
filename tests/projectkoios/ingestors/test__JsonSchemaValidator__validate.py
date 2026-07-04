from __future__ import annotations

import pytest

from projectkoios.ingestors import JsonSchemaLoader, JsonSchemaValidator

from tests.projectkoios.ingestors._helpers import write_schema


def test__JsonSchemaValidator__validate(tmp_path):
    schema = JsonSchemaLoader().load(write_schema(tmp_path))
    validator = JsonSchemaValidator(schema)
    validator.validate({
        "version": 1,
        "project": "projectkoios",
        "pipeline": {"mode": "derived-index", "answer_format": "cited_summary", "retrieval_depth": 1},
        "validation": {"mode": "strict"},
        "source": {"include": ["docs/adr/**/*.md"], "exclude": []},
        "ontology": {},
        "extraction": {"backend": {"name": "ollama", "model": "llama3.2", "timeout_seconds": 60, "on_failure": "error"}}, 
        "retrieval": {"max_nodes": 1},
        "evaluation": {},
        "presets": {},
    })


def test__JsonSchemaValidator__validate__rejects_missing_key(tmp_path):
    schema = JsonSchemaLoader().load(write_schema(tmp_path))
    validator = JsonSchemaValidator(schema)
    with pytest.raises((TypeError, ValueError)):
        validator.validate({"version": 1})
