from __future__ import annotations

from pathlib import Path

from projectkoios.ingestors import Config, ConfigLoader, JsonSchema, JsonSchemaLoader, JsonSchemaValidator, SourceResolver, SourceSet

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__SourceResolver__resolve(tmp_path: Path) -> None:
    """Validate that source resolver discovers the fixture ADR document."""
    # Schema fixture validates the generated YAML config.
    schema: JsonSchema = JsonSchemaLoader().load(write_schema(tmp_path))
    # Config controls ADR source glob resolution.
    config: Config = ConfigLoader(JsonSchemaValidator(schema)).load(write_config(tmp_path))
    # Source set contains documents matched by the config include patterns.
    source_set: SourceSet = SourceResolver().resolve(config)
    assert len(source_set.documents) == 1
    assert source_set.documents[0].relative_path.endswith("adr.example.md")
