from __future__ import annotations

from projectkoios.ingestors import BackendFailureMode, BackendName, ConfigLoader, JsonSchemaLoader, JsonSchemaValidator, PipelineMode, ValidationMode

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def test__ConfigLoader__load(tmp_path):
    schema = JsonSchemaLoader().load(write_schema(tmp_path))
    loader = ConfigLoader(JsonSchemaValidator(schema))
    config = loader.load(write_config(tmp_path))
    assert config.project == "projectkoios"
    assert config.retrieval_depth == 1
    assert config.pipeline_mode is PipelineMode.DERIVED_INDEX
    assert config.validation_mode is ValidationMode.STRICT
    assert config.backend_name is BackendName.OLLAMA
    assert config.backend_endpoint == "http://localhost:11434"
    assert config.backend_model == "llama3.2"
    assert config.backend_timeout_seconds == 60
    assert config.backend_on_failure is BackendFailureMode.ERROR
