from __future__ import annotations

import json

from projectkoios.ingestors import ConfigLoader, GraphIndexBuilder, GraphIndexJsonSerializer, JsonSchemaLoader, JsonSchemaValidator, Retriever, SourceResolver

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__Retriever__retrieve(tmp_path):
    config = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path)))).load(write_config(tmp_path))
    source_set = SourceResolver().resolve(config)
    index = GraphIndexBuilder().build(source_set)
    result = Retriever().retrieve(index, "ADR Example", depth=1)
    assert result.evidence
    assert ":" in result.evidence[0].citation


def test__Retriever__retrieve__evidence_is_traceable_to_persisted_index(tmp_path):
    config = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path)))).load(write_config(tmp_path))
    source_set = SourceResolver().resolve(config)
    index = GraphIndexBuilder().build(source_set)
    result = Retriever().retrieve(index, "ADR Example", depth=1)
    assert result.evidence

    GraphIndexJsonSerializer().write(index, config.index_path)
    artifact = json.loads(config.index_path.read_text(encoding="utf-8"))
    sections = [section for document in artifact["documents"] for section in document["sections"]]
    evidence = result.evidence[0]

    assert any(
        section["relative_path"] == evidence.relative_path
        and section["title"] == evidence.title
        and section["line_start"] == evidence.line_start
        and section["line_end"] == evidence.line_end
        for section in sections
    )
