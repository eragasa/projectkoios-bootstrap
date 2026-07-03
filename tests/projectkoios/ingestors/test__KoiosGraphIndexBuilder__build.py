from __future__ import annotations

from projectkoios.ingestors import JsonSchemaLoader, JsonSchemaValidator, ConfigLoader, GraphIndexBuilder, SourceResolver

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__GraphIndexBuilder__build(tmp_path):
    config = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path)))).load(write_config(tmp_path))
    source_set = SourceResolver().resolve(config)
    index = GraphIndexBuilder().build(source_set)
    assert index.sections
