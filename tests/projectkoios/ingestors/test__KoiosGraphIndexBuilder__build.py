from __future__ import annotations

from projectkoios.ingestors import JsonSchemaLoader, JsonSchemaValidator, ConfigLoader, GraphIndexBuilder, GraphIndexJsonSerializer, SourceResolver

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__GraphIndexBuilder__build(tmp_path):
    config = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path)))).load(write_config(tmp_path))
    source_set = SourceResolver().resolve(config)
    index = GraphIndexBuilder().build(source_set)
    assert index.sections


def test__GraphIndexJsonSerializer__to_json__is_deterministic(tmp_path):
    config = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path)))).load(write_config(tmp_path))
    source_set = SourceResolver().resolve(config)
    index = GraphIndexBuilder().build(source_set)
    serializer = GraphIndexJsonSerializer()

    first = serializer.to_json(index)
    second = serializer.to_json(index)

    assert first == second
    assert '"citation": "docs/adr/adr.example.md:' in first
    assert '"relative_path": "docs/adr/adr.example.md"' in first


def test__GraphIndexJsonSerializer__write__is_stable(tmp_path):
    config = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path)))).load(write_config(tmp_path))
    source_set = SourceResolver().resolve(config)
    index = GraphIndexBuilder().build(source_set)
    serializer = GraphIndexJsonSerializer()

    serializer.write(index, config.index_path)
    first = config.index_path.read_text(encoding="utf-8")
    serializer.write(index, config.index_path)
    second = config.index_path.read_text(encoding="utf-8")

    assert first == second
