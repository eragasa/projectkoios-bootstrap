from __future__ import annotations

from projectkoios.ingestors import JsonSchemaLoader

from tests.projectkoios.ingestors._helpers import write_schema


def test__JsonSchemaLoader__load(tmp_path):
    schema_path = write_schema(tmp_path)
    schema = JsonSchemaLoader().load(schema_path)
    assert schema.title == "projectkoios.ingestion.config"
