from __future__ import annotations

from projectkoios.ingestors import ConfigLoader, JsonSchemaLoader, JsonSchemaValidator

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__ConfigLoader__load__applies_preset_by_explicit_section_replacement(tmp_path):
    config_path = write_config(tmp_path)
    text = config_path.read_text(encoding="utf-8")
    config_path.write_text(
        text.replace(
            "source:\n  include:\n    - docs/architecture/adr/**/*.md\n  exclude: []",
            "source:\n  include:\n    - docs/architecture/adr/*.missing.md\n  exclude: []",
            1,
        ),
        encoding="utf-8",
    )
    loader = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path))))
    config = loader.load(config_path, preset="adr")
    assert config.source_includes() == ("docs/architecture/adr/**/*.md",)


def test__ConfigLoader__load__rejects_unknown_preset(tmp_path):
    loader = ConfigLoader(JsonSchemaValidator(JsonSchemaLoader().load(write_schema(tmp_path))))
    try:
        loader.load(write_config(tmp_path), preset="missing")
    except KeyError as exc:
        assert "unknown preset" in str(exc)
    else:
        raise AssertionError("expected unknown preset to fail")
