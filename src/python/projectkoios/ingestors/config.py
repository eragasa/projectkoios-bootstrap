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
        return self._section("source")

    @property
    def pipeline(self) -> Mapping[str, Any]:
        return self._section("pipeline")

    @property
    def validation(self) -> Mapping[str, Any]:
        return self._section("validation")

    @property
    def retrieval(self) -> Mapping[str, Any]:
        return self._section("retrieval")

    @property
    def extraction(self) -> Mapping[str, Any]:
        return self._section("extraction")

    @property
    def evaluation(self) -> Mapping[str, Any]:
        return self._section("evaluation")

    @property
    def presets(self) -> Mapping[str, Any]:
        return self._section("presets")

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
        value = self.extraction.get("backend", {})
        if isinstance(value, Mapping):
            return value
        raise TypeError("extraction.backend must be a mapping")

    @property
    def backend_name(self) -> BackendName:
        return BackendName(str(self.backend.get("name", BackendName.OLLAMA.value)))

    @property
    def backend_endpoint(self) -> str | None:
        value = self.backend.get("endpoint")
        return str(value) if value is not None else None

    @property
    def backend_model(self) -> str | None:
        value = self.backend.get("model")
        return str(value) if value is not None else None

    @property
    def backend_timeout_seconds(self) -> int:
        return int(self.backend.get("timeout_seconds", 60))

    @property
    def backend_on_failure(self) -> BackendFailureMode:
        return BackendFailureMode(str(self.backend.get("on_failure", BackendFailureMode.ERROR.value)))

    def source_includes(self) -> tuple[str, ...]:
        include = self.source.get("include", [])
        return tuple(str(item) for item in include)

    def source_excludes(self) -> tuple[str, ...]:
        exclude = self.source.get("exclude", [])
        return tuple(str(item) for item in exclude)

    def preset(self, name: str) -> Mapping[str, Any]:
        value = self.presets.get(name, {})
        if not isinstance(value, Mapping):
            raise TypeError(f"preset '{name}' must be a mapping")
        return value

    def _section(self, name: str) -> Mapping[str, Any]:
        value = self.document.get(name, {})
        if not isinstance(value, Mapping):
            raise TypeError(f"section '{name}' must be a mapping")
        return value


class RuntimeConfigValidator:
    _ANSWER_FORMATS = {"cited_summary", "structured_json"}
    _BACKENDS = {item.value for item in BackendName}
    _PIPELINE_MODES = {item.value for item in PipelineMode}
    _VALIDATION_MODES = {item.value for item in ValidationMode}
    _BACKEND_FAILURE_MODES = {item.value for item in BackendFailureMode}

    def validate(self, config: Config) -> None:
        issues = self.issues(config)
        if issues:
            raise ValueError("invalid runtime config: " + "; ".join(issues))

    def issues(self, config: Config) -> tuple[str, ...]:
        issues: list[str] = []
        self._validate_enum("validation.mode", config.validation_mode.value, self._VALIDATION_MODES, issues)
        self._validate_enum("pipeline.mode", config.pipeline_mode.value, self._PIPELINE_MODES, issues)
        self._validate_enum("pipeline.answer_format", config.answer_format, self._ANSWER_FORMATS, issues)
        self._validate_enum("extraction.backend.name", config.backend_name.value, self._BACKENDS, issues)
        self._validate_enum("extraction.backend.on_failure", config.backend_on_failure.value, self._BACKEND_FAILURE_MODES, issues)
        if config.retrieval_depth < 1:
            issues.append("pipeline.retrieval_depth must be >= 1")
        if config.backend_timeout_seconds < 1:
            issues.append("extraction.backend.timeout_seconds must be >= 1")
        for pattern in config.source_includes():
            if not self._is_adr_markdown_pattern(pattern):
                issues.append(f"source include must be ADR-only markdown for v1: {pattern}")
        return tuple(issues)

    def _validate_enum(self, field: str, value: str, allowed: set[str], issues: list[str]) -> None:
        if value not in allowed:
            issues.append(f"{field} must be one of {sorted(allowed)!r}: {value}")

    def _is_adr_markdown_pattern(self, pattern: str) -> bool:
        normalized = pattern.replace("\\", "/")
        return normalized.startswith("docs/adr/") and normalized.endswith(".md")


class ConfigLoader:
    def __init__(self, schema_validator: JsonSchemaValidator | None = None) -> None:
        self._schema_validator = schema_validator

    def load(self, path: Path, *, preset: str | None = None) -> Config:
        resolved = path.resolve()
        document = yaml.safe_load(resolved.read_text(encoding="utf-8"))
        if document is None:
            document = {}
        if not isinstance(document, dict):
            raise TypeError(f"Config must be a mapping: {resolved}")
        if preset is not None:
            document = self._apply_preset(document, preset)
        if self._schema_validator is not None:
            self._schema_validator.validate(document)
        return Config(path=resolved, document=document)

    def _apply_preset(self, document: dict[str, Any], preset: str) -> dict[str, Any]:
        presets = document.get("presets", {})
        if not isinstance(presets, Mapping):
            raise TypeError("presets must be a mapping")
        overlay = presets.get(preset)
        if overlay is None:
            raise KeyError(f"unknown preset: {preset}")
        if not isinstance(overlay, Mapping):
            raise TypeError(f"preset '{preset}' must be a mapping")
        merged = dict(document)
        for section_name, replacement in overlay.items():
            if section_name == "presets":
                raise ValueError("presets may not replace the presets section")
            merged[str(section_name)] = replacement
        return merged
