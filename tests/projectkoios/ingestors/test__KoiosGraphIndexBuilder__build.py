from __future__ import annotations

from pathlib import Path

from projectkoios.ingestors import Config, ConfigLoader, GraphIndex, GraphIndexBuilder, GraphIndexJsonSerializer, JsonSchema, JsonSchemaLoader, JsonSchemaValidator, SourceResolver, SourceSet

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def load_fixture_config(tmp_path: Path) -> Config:
    """Load a typed ingestion config from test fixtures."""
    # Schema fixture validates the generated YAML config.
    schema: JsonSchema = JsonSchemaLoader().load(write_schema(tmp_path))
    # Loader produces the typed ingestion config under test.
    loader: ConfigLoader = ConfigLoader(JsonSchemaValidator(schema))
    return loader.load(write_config(tmp_path))


def test__GraphIndexBuilder__build(tmp_path: Path) -> None:
    """Validate that graph index builder creates sections from ADR sources."""
    # Config controls source resolution for the fixture ADR.
    config: Config = load_fixture_config(tmp_path)
    # Source set contains resolved ADR Markdown documents.
    source_set: SourceSet = SourceResolver().resolve(config)
    # Index contains extracted sections from resolved documents.
    index: GraphIndex = GraphIndexBuilder().build(source_set)
    assert index.sections


def test__GraphIndexJsonSerializer__to_json__is_deterministic(tmp_path: Path) -> None:
    """Validate that graph index JSON serialization is deterministic."""
    # Config controls source resolution for the fixture ADR.
    config: Config = load_fixture_config(tmp_path)
    # Source set contains resolved ADR Markdown documents.
    source_set: SourceSet = SourceResolver().resolve(config)
    # Index contains extracted sections from resolved documents.
    index: GraphIndex = GraphIndexBuilder().build(source_set)
    # Serializer converts the index to stable JSON text.
    serializer: GraphIndexJsonSerializer = GraphIndexJsonSerializer()

    # First serialization establishes the expected deterministic text.
    first: str = serializer.to_json(index)
    # Second serialization should match exactly.
    second: str = serializer.to_json(index)

    assert first == second
    assert '"citation": "docs/adr/adr.example.md:' in first
    assert '"relative_path": "docs/adr/adr.example.md"' in first


def test__GraphIndexJsonSerializer__write__is_stable(tmp_path: Path) -> None:
    """Validate that graph index file writes are stable across runs."""
    # Config controls source resolution and index output path.
    config: Config = load_fixture_config(tmp_path)
    # Source set contains resolved ADR Markdown documents.
    source_set: SourceSet = SourceResolver().resolve(config)
    # Index contains extracted sections from resolved documents.
    index: GraphIndex = GraphIndexBuilder().build(source_set)
    # Serializer writes the index to disk.
    serializer: GraphIndexJsonSerializer = GraphIndexJsonSerializer()

    serializer.write(index, config.index_path)
    # First file content establishes the expected deterministic output.
    first: str = config.index_path.read_text(encoding="utf-8")
    serializer.write(index, config.index_path)
    # Second file content should match exactly.
    second: str = config.index_path.read_text(encoding="utf-8")

    assert first == second
