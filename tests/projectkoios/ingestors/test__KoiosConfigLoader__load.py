from __future__ import annotations

from pathlib import Path

from projectkoios.ingestors import BackendFailureMode, BackendName, Config, ConfigLoader, JsonSchema, JsonSchemaLoader, JsonSchemaValidator, PipelineMode, ValidationMode

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__ConfigLoader__load(tmp_path: Path) -> None:
    """Validate that ConfigLoader maps fixture YAML into typed config fields."""
    # Schema fixture validates the generated YAML config.
    schema: JsonSchema = JsonSchemaLoader().load(write_schema(tmp_path))
    # Loader produces the typed ingestion config under test.
    loader: ConfigLoader = ConfigLoader(JsonSchemaValidator(schema))
    # Config is loaded from the generated fixture file.
    config: Config = loader.load(write_config(tmp_path))
    assert config.project == "projectkoios"
    assert config.retrieval_depth == 1
    assert config.index_path == config.root / "graph" / "index.json"
    assert config.pipeline_mode is PipelineMode.DERIVED_INDEX
    assert config.validation_mode is ValidationMode.STRICT
    assert config.backend_name is BackendName.OLLAMA
    assert config.backend_endpoint == "http://localhost:11434"
    assert config.backend_model == "llama3.2"
    assert config.backend_timeout_seconds == 60
    assert config.backend_on_failure is BackendFailureMode.ERROR
