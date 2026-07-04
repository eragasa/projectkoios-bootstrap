from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Mapping, cast

import yaml

from projectkoios.ingestors.schemas import JsonObject, JsonSchemaValidator, JsonValue


class BackendFailureMode(StrEnum):
    """Supported backend failure handling modes."""

    ERROR = "error"
    FALLBACK = "fallback"


class BackendName(StrEnum):
    """Supported answer-generation backend names."""

    OLLAMA = "ollama"


class PipelineMode(StrEnum):
    """Supported ingestion pipeline modes."""

    DERIVED_INDEX = "derived-index"


class ValidationMode(StrEnum):
    """Supported runtime validation modes."""

    STRICT = "strict"
    RELAXED = "relaxed"


@dataclass(frozen=True, slots=True)
class Config:
    """Loaded Koios ingestion configuration.

    Args:
        path: Resolved config file path.
        document: Parsed configuration document.
    """

    path: Path
    document: Mapping[str, JsonValue]

    @property
    def root(self) -> Path:
        """Return the config root directory."""
        return self.path.parent

    @property
    def version(self) -> int:
        """Return the config version."""
        return int(str(self.document.get("version", 1)))

    @property
    def project(self) -> str:
        """Return the configured project name."""
        return str(self.document.get("project", ""))

    @property
    def source(self) -> Mapping[str, JsonValue]:
        """Return the source config section."""
        return self.section("source")

    @property
    def pipeline(self) -> Mapping[str, JsonValue]:
        """Return the pipeline config section."""
        return self.section("pipeline")

    @property
    def validation(self) -> Mapping[str, JsonValue]:
        """Return the validation config section."""
        return self.section("validation")

    @property
    def retrieval(self) -> Mapping[str, JsonValue]:
        """Return the retrieval config section."""
        return self.section("retrieval")

    @property
    def extraction(self) -> Mapping[str, JsonValue]:
        """Return the extraction config section."""
        return self.section("extraction")

    @property
    def evaluation(self) -> Mapping[str, JsonValue]:
        """Return the evaluation config section."""
        return self.section("evaluation")

    @property
    def presets(self) -> Mapping[str, JsonValue]:
        """Return the presets config section."""
        return self.section("presets")

    @property
    def answer_format(self) -> str:
        """Return the configured answer format."""
        return str(self.pipeline.get("answer_format", "cited_summary"))

    @property
    def index_path(self) -> Path:
        """Return the resolved persisted index output path."""
        # Value is the configured index path or repository default.
        value: JsonValue = self.pipeline.get("index_path", "graph/index.json")
        # Path is resolved relative to the config root when not absolute.
        path: Path = Path(str(value))
        return path if path.is_absolute() else self.root / path

    @property
    def retrieval_depth(self) -> int:
        """Return the configured retrieval depth."""
        return int(str(self.pipeline.get("retrieval_depth", self.retrieval.get("max_nodes", 1))))

    @property
    def validation_mode(self) -> ValidationMode:
        """Return the configured validation mode."""
        return ValidationMode(str(self.validation.get("mode", ValidationMode.STRICT.value)))

    @property
    def pipeline_mode(self) -> PipelineMode:
        """Return the configured pipeline mode."""
        return PipelineMode(str(self.pipeline.get("mode", PipelineMode.DERIVED_INDEX.value)))

    @property
    def backend(self) -> Mapping[str, JsonValue]:
        """Return the extraction backend section."""
        # Value is the backend object nested under extraction.
        value: JsonValue = self.extraction.get("backend", {})
        if isinstance(value, Mapping):
            return value
        raise TypeError("extraction.backend must be a mapping")

    @property
    def backend_name(self) -> BackendName:
        """Return the configured backend name."""
        return BackendName(str(self.backend.get("name", BackendName.OLLAMA.value)))

    @property
    def backend_endpoint(self) -> str | None:
        """Return the optional configured backend endpoint."""
        # Value is the optional endpoint field from the backend section.
        value: JsonValue = self.backend.get("endpoint")
        return str(value) if value is not None else None

    @property
    def backend_model(self) -> str | None:
        """Return the optional configured backend model."""
        # Value is the optional model field from the backend section.
        value: JsonValue = self.backend.get("model")
        return str(value) if value is not None else None

    @property
    def backend_timeout_seconds(self) -> int:
        """Return the configured backend timeout in seconds."""
        return int(str(self.backend.get("timeout_seconds", 60)))

    @property
    def backend_on_failure(self) -> BackendFailureMode:
        """Return the configured backend failure handling mode."""
        return BackendFailureMode(str(self.backend.get("on_failure", BackendFailureMode.ERROR.value)))

    def source_includes(self) -> tuple[str, ...]:
        """Return configured source include patterns."""
        # Include is expected to be a sequence of glob patterns.
        include: JsonValue = self.source.get("include", [])
        return tuple(str(item) for item in include) if isinstance(include, list | tuple) else ()

    def source_excludes(self) -> tuple[str, ...]:
        """Return configured source exclude patterns."""
        # Exclude is expected to be a sequence of glob patterns.
        exclude: JsonValue = self.source.get("exclude", [])
        return tuple(str(item) for item in exclude) if isinstance(exclude, list | tuple) else ()

    def preset(self, name: str) -> Mapping[str, JsonValue]:
        """Return a named preset section."""
        # Value is the requested preset overlay object.
        value: JsonValue = self.presets.get(name, {})
        if not isinstance(value, Mapping):
            raise TypeError(f"preset '{name}' must be a mapping")
        return value

    def section(self, name: str) -> Mapping[str, JsonValue]:
        """Return a named top-level config section as a mapping."""
        # Value is the requested top-level section or an empty mapping fallback.
        value: JsonValue = self.document.get(name, {})
        if not isinstance(value, Mapping):
            raise TypeError(f"section '{name}' must be a mapping")
        return value


class RuntimeConfigValidator:
    """Validate config values that require runtime policy checks."""

    ANSWER_FORMATS: set[str] = {"cited_summary", "structured_json"}
    BACKENDS: set[str] = {item.value for item in BackendName}
    PIPELINE_MODES: set[str] = {item.value for item in PipelineMode}
    VALIDATION_MODES: set[str] = {item.value for item in ValidationMode}
    BACKEND_FAILURE_MODES: set[str] = {item.value for item in BackendFailureMode}

    def validate(self, config: Config) -> None:
        """Raise when runtime config validation finds issues."""
        # Issues are collected before raising so callers see all runtime problems.
        issues: tuple[str, ...] = self.issues(config)
        if issues:
            raise ValueError("invalid runtime config: " + "; ".join(issues))

    def issues(self, config: Config) -> tuple[str, ...]:
        """Return runtime config validation issues."""
        # Issues accumulates human-readable runtime validation failures.
        issues: list[str] = []
        self.validate_enum("validation.mode", config.validation_mode.value, self.VALIDATION_MODES, issues)
        self.validate_enum("pipeline.mode", config.pipeline_mode.value, self.PIPELINE_MODES, issues)
        self.validate_enum("pipeline.answer_format", config.answer_format, self.ANSWER_FORMATS, issues)
        self.validate_enum("extraction.backend.name", config.backend_name.value, self.BACKENDS, issues)
        self.validate_enum("extraction.backend.on_failure", config.backend_on_failure.value, self.BACKEND_FAILURE_MODES, issues)
        if config.retrieval_depth < 1:
            issues.append("pipeline.retrieval_depth must be >= 1")
        if config.backend_timeout_seconds < 1:
            issues.append("extraction.backend.timeout_seconds must be >= 1")
        if str(config.pipeline.get("index_path", "graph/index.json")).strip() == "":
            issues.append("pipeline.index_path must not be empty")
        pattern: str
        for pattern in config.source_includes():
            if not self.is_adr_markdown_pattern(pattern):
                issues.append(f"source include must be ADR-only markdown for v1: {pattern}")
        return tuple(issues)

    def validate_enum(self, field: str, value: str, allowed: set[str], issues: list[str]) -> None:
        """Append an issue when an enum-like field has an unsupported value."""
        if value not in allowed:
            issues.append(f"{field} must be one of {sorted(allowed)!r}: {value}")

    def is_adr_markdown_pattern(self, pattern: str) -> bool:
        """Return whether a source include is constrained to ADR Markdown."""
        # Normalized path uses POSIX separators for policy checks.
        normalized: str = pattern.replace("\\", "/")
        return normalized.startswith("docs/adr/") and normalized.endswith(".md")


class ConfigLoader:
    """Load YAML config files with optional schema validation and presets."""

    def __init__(self, schema_validator: JsonSchemaValidator | None = None) -> None:
        self.schema_validator: JsonSchemaValidator | None = schema_validator

    def load(self, path: Path, *, preset: str | None = None) -> Config:
        """Load a config file and apply an optional preset overlay."""
        # Resolved path is stored on the returned config object.
        resolved: Path = path.resolve()
        # Loaded document is the YAML parser output before shape validation.
        loaded_document: JsonValue = cast(JsonValue, yaml.safe_load(resolved.read_text(encoding="utf-8")))
        # Raw document treats an empty YAML file as an empty object.
        raw_document: JsonValue = {} if loaded_document is None else loaded_document
        if not isinstance(raw_document, dict):
            raise TypeError(f"Config must be a mapping: {resolved}")
        # Base document is the validated top-level config mapping.
        base_document: JsonObject = raw_document
        # Config document includes preset replacement when requested.
        config_document: JsonObject = self.apply_preset(base_document, preset) if preset is not None else base_document
        if self.schema_validator is not None:
            self.schema_validator.validate(config_document)
        return Config(path=resolved, document=config_document)

    def apply_preset(self, document: JsonObject, preset: str) -> JsonObject:
        """Apply a named preset overlay using replacement semantics."""
        # Presets is the top-level preset mapping from the config document.
        presets: JsonValue = document.get("presets", {})
        if not isinstance(presets, Mapping):
            raise TypeError("presets must be a mapping")
        # Overlay is the selected named preset mapping.
        overlay: JsonValue = presets.get(preset)
        if overlay is None:
            raise KeyError(f"unknown preset: {preset}")
        if not isinstance(overlay, Mapping):
            raise TypeError(f"preset '{preset}' must be a mapping")
        # Merged starts as a shallow copy of the base document before replacements.
        merged: JsonObject = dict(document)
        section_name: JsonValue
        replacement: JsonValue
        for section_name, replacement in overlay.items():
            if section_name == "presets":
                raise ValueError("presets may not replace the presets section")
            merged[str(section_name)] = replacement
        return merged
