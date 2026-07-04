from __future__ import annotations

from pathlib import Path

import pytest

from projectkoios.ingestors import Config, ConfigLoader, JsonSchema, JsonSchemaLoader, JsonSchemaValidator

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__ConfigLoader__load__applies_preset_by_explicit_section_replacement(tmp_path: Path) -> None:
    """Validate that explicit preset selection replaces config sections."""
    # Config path is rewritten so only the preset points at an existing ADR source.
    config_path: Path = write_config(tmp_path)
    # Text holds editable YAML fixture content.
    text: str = config_path.read_text(encoding="utf-8")
    config_path.write_text(
        text.replace(
            "source:\n  include:\n    - docs/adr/**/*.md\n  exclude: []",
            "source:\n  include:\n    - docs/adr/*.missing.md\n  exclude: []",
            1,
        ),
        encoding="utf-8",
    )
    # Schema feeds the config validator used by the loader.
    schema: JsonSchema = JsonSchemaLoader().load(write_schema(tmp_path))
    # Loader applies schema validation and preset overlays.
    loader: ConfigLoader = ConfigLoader(JsonSchemaValidator(schema))
    # Config should use the explicit adr preset source include.
    config: Config = loader.load(config_path, preset="adr")
    assert config.source_includes() == ("docs/adr/**/*.md",)


def test__ConfigLoader__load__rejects_unknown_preset(tmp_path: Path) -> None:
    """Validate that unknown preset names fail explicitly."""
    # Schema feeds the config validator used by the loader.
    schema: JsonSchema = JsonSchemaLoader().load(write_schema(tmp_path))
    # Loader applies schema validation and preset overlays.
    loader: ConfigLoader = ConfigLoader(JsonSchemaValidator(schema))
    with pytest.raises(KeyError, match="unknown preset"):
        loader.load(write_config(tmp_path), preset="missing")
