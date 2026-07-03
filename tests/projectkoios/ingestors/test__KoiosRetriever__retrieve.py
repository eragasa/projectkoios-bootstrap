from __future__ import annotations

from projectkoios.ingestors import JsonSchemaLoader, JsonSchemaValidator, ConfigLoader, GraphIndexBuilder, Retriever, SourceResolver

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__Retriever__retrieve(tmp_path):
    config = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path)))).load(write_config(tmp_path))
    source_set = SourceResolver().resolve(config)
    index = GraphIndexBuilder().build(source_set)
    result = Retriever().retrieve(index, "ADR Example", depth=1)
    assert result.evidence
    assert ":" in result.evidence[0].citation
