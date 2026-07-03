from __future__ import annotations

from projectkoios.ingestors import JsonSchemaLoader, JsonSchemaValidator, ConfigLoader, SourceResolver

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__SourceResolver__resolve(tmp_path):
    config = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path)))).load(write_config(tmp_path))
    source_set = SourceResolver().resolve(config)
    assert len(source_set.documents) == 1
    assert source_set.documents[0].relative_path.endswith("adr.example.md")
