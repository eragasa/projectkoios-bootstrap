from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping

import yaml

from projectkoios.ingestors.schemas import JsonSchemaValidator


class BackendFailureMode(StrEnum):
    ERROR = "error"
    FALLBACK = "fallback"


class BackendName(StrEnum):
    OLLAMA = "ollama"


class PipelineMode(StrEnum):
    DERIVED_INDEX = "derived-index"


class ValidationMode(StrEnum):
    STRICT = "strict"
    RELAXED = "relaxed"


@dataclass(frozen=True, slots=True)
class Config:
    path: Path
    document: Mapping[str, Any]

    @property
    def root(self) -> Path:
        return self.path.parent

    @property
    def version(self) -> int:
        return int(self.document.get("version", 1))

    @property
    def project(self) -> str:
        return str(self.document.get("project", ""))

    @property
    def source(self) -> Mapping[str, Any]:
        return self.section("source")

    @property
    def pipeline(self) -> Mapping[str, Any]:
        return self.section("pipeline")

    @property
    def validation(self) -> Mapping[str, Any]:
        return self.section("validation")

    @property
    def retrieval(self) -> Mapping[str, Any]:
        return self.section("retrieval")

    @property
    def extraction(self) -> Mapping[str, Any]:
        return self.section("extraction")

    @property
    def evaluation(self) -> Mapping[str, Any]:
        return self.section("evaluation")

    @property
    def presets(self) -> Mapping[str, Any]:
        return self.section("presets")

    @property
    def answer_format(self) -> str:
        return str(self.pipeline.get("answer_format", "cited_summary"))

    @property
    def retrieval_depth(self) -> int:
        return int(self.pipeline.get("retrieval_depth", self.retrieval.get("max_nodes", 1)))

    @property
    def validation_mode(self) -> ValidationMode:
        return ValidationMode(str(self.validation.get("mode", ValidationMode.STRICT.value)))

    @property
    def pipeline_mode(self) -> PipelineMode:
        return PipelineMode(str(self.pipeline.get("mode", PipelineMode.DERIVED_INDEX.value)))

    @property
    def backend(self) -> Mapping[str, Any]:
        value: object = self.extraction.get("backend", {})
        if isinstance(value, Mapping):
            return value
        raise TypeError("extraction.backend must be a mapping")

    @property
    def backend_name(self) -> BackendName:
        return BackendName(str(self.backend.get("name", BackendName.OLLAMA.value)))

    @property
    def backend_endpoint(self) -> str | None:
        value: object = self.backend.get("endpoint")
        return str(value) if value is not None else None

    @property
    def backend_model(self) -> str | None:
        value: object = self.backend.get("model")
        return str(value) if value is not None else None

    @property
    def backend_timeout_seconds(self) -> int:
        return int(self.backend.get("timeout_seconds", 60))

    @property
    def backend_on_failure(self) -> BackendFailureMode:
        return BackendFailureMode(str(self.backend.get("on_failure", BackendFailureMode.ERROR.value)))

    def source_includes(self) -> tuple[str, ...]:
        include: object = self.source.get("include", [])
        return tuple(str(item) for item in include) if isinstance(include, list | tuple) else ()

    def source_excludes(self) -> tuple[str, ...]:
        exclude: object = self.source.get("exclude", [])
        return tuple(str(item) for item in exclude) if isinstance(exclude, list | tuple) else ()

    def preset(self, name: str) -> Mapping[str, Any]:
        value: object = self.presets.get(name, {})
        if not isinstance(value, Mapping):
            raise TypeError(f"preset '{name}' must be a mapping")
        return value

    def section(self, name: str) -> Mapping[str, Any]:
        value: object = self.document.get(name, {})
        if not isinstance(value, Mapping):
            raise TypeError(f"section '{name}' must be a mapping")
        return value


class RuntimeConfigValidator:
    ANSWER_FORMATS: set[str] = {"cited_summary", "structured_json"}
    BACKENDS: set[str] = {item.value for item in BackendName}
    PIPELINE_MODES: set[str] = {item.value for item in PipelineMode}
    VALIDATION_MODES: set[str] = {item.value for item in ValidationMode}
    BACKEND_FAILURE_MODES: set[str] = {item.value for item in BackendFailureMode}

    def validate(self, config: Config) -> None:
        issues: tuple[str, ...] = self.issues(config)
        if issues:
            raise ValueError("invalid runtime config: " + "; ".join(issues))

    def issues(self, config: Config) -> tuple[str, ...]:
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
        pattern: str
        for pattern in config.source_includes():
            if not self.is_adr_markdown_pattern(pattern):
                issues.append(f"source include must be ADR-only markdown for v1: {pattern}")
        return tuple(issues)

    def validate_enum(self, field: str, value: str, allowed: set[str], issues: list[str]) -> None:
        if value not in allowed:
            issues.append(f"{field} must be one of {sorted(allowed)!r}: {value}")

    def is_adr_markdown_pattern(self, pattern: str) -> bool:
        normalized: str = pattern.replace("\\", "/")
        return normalized.startswith("docs/adr/") and normalized.endswith(".md")


class ConfigLoader:
    def __init__(self, schema_validator: JsonSchemaValidator | None = None) -> None:
        self.schema_validator: JsonSchemaValidator | None = schema_validator

    def load(self, path: Path, *, preset: str | None = None) -> Config:
        resolved: Path = path.resolve()
        loaded_document: Any = yaml.safe_load(resolved.read_text(encoding="utf-8"))
        raw_document: Any = {} if loaded_document is None else loaded_document
        if not isinstance(raw_document, dict):
            raise TypeError(f"Config must be a mapping: {resolved}")
        base_document: dict[str, Any] = raw_document
        config_document: dict[str, Any] = self.apply_preset(base_document, preset) if preset is not None else base_document
        if self.schema_validator is not None:
            self.schema_validator.validate(config_document)
        return Config(path=resolved, document=config_document)

    def apply_preset(self, document: dict[str, Any], preset: str) -> dict[str, Any]:
        presets: object = document.get("presets", {})
        if not isinstance(presets, Mapping):
            raise TypeError("presets must be a mapping")
        overlay: object = presets.get(preset)
        if overlay is None:
            raise KeyError(f"unknown preset: {preset}")
        if not isinstance(overlay, Mapping):
            raise TypeError(f"preset '{preset}' must be a mapping")
        merged: dict[str, Any] = dict(document)
        section_name: object
        replacement: object
        for section_name, replacement in overlay.items():
            if section_name == "presets":
                raise ValueError("presets may not replace the presets section")
            merged[str(section_name)] = replacement
        return merged
