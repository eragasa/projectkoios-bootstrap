from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from projectkoios.ingestors.answering import AnswerComposer, AnswerFormat, Answer
from projectkoios.ingestors.backends import BackendFactory, BackendSelection
from projectkoios.ingestors.config import Config, ConfigLoader, RuntimeConfigValidator
from projectkoios.ingestors.index import GraphIndex, GraphIndexBuilder
from projectkoios.ingestors.retrieval import RetrievalResult, Retriever
from projectkoios.ingestors.schemas import JsonSchemaLoader, JsonSchemaValidator
from projectkoios.ingestors.sources import SourceResolver, SourceSet


@dataclass(frozen=True, slots=True)
class ValidationReport:
    config_path: Path
    schema_valid: bool
    runtime_valid: bool
    sources: int
    issues: tuple[str, ...]


class App:
    def __init__(self, *, backend_factory: BackendFactory | None = None) -> None:
        self._schema_loader = JsonSchemaLoader()
        self._runtime_validator = RuntimeConfigValidator()
        self._source_resolver = SourceResolver()
        self._index_builder = GraphIndexBuilder()
        self._retriever = Retriever()
        self._answer_composer = AnswerComposer()
        self._backend_factory = backend_factory or BackendFactory()

    def load_config(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> Config:
        schema_validator = None
        if schema_path is not None:
            schema = self._schema_loader.load(schema_path)
            schema_validator = JsonSchemaValidator(schema)
        loader = ConfigLoader(schema_validator=schema_validator)
        return loader.load(config_path, preset=preset)

    def validate_config(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> ValidationReport:
        issues: list[str] = []
        schema_valid = True
        runtime_valid = True
        source_set: SourceSet | None = None
        config = None
        try:
            config = self.load_config(config_path, schema_path=schema_path, preset=preset)
        except Exception as exc:
            schema_valid = False
            runtime_valid = False
            issues.append(str(exc))
        if config is not None:
            try:
                self._runtime_validator.validate(config)
                source_set = self._source_resolver.resolve(config)
            except Exception as exc:
                runtime_valid = False
                issues.append(str(exc))
        sources = len(source_set.documents) if source_set is not None else 0
        return ValidationReport(
            config_path=config.path if config is not None else config_path.resolve(),
            schema_valid=schema_valid,
            runtime_valid=runtime_valid,
            sources=sources,
            issues=tuple(issues),
        )

    def build_index(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> tuple[Config, SourceSet, GraphIndex]:
        config = self.load_config(config_path, schema_path=schema_path, preset=preset)
        self._runtime_validator.validate(config)
        source_set = self._source_resolver.resolve(config)
        index = self._index_builder.build(source_set)
        return config, source_set, index

    def retrieve(self, config_path: Path, query: str, *, schema_path: Path | None = None, preset: str | None = None) -> RetrievalResult:
        config, _, index = self.build_index(config_path, schema_path=schema_path, preset=preset)
        return self._retriever.retrieve(index, query, depth=config.retrieval_depth)

    def answer(self, config_path: Path, query: str, *, schema_path: Path | None = None, format: AnswerFormat | None = None, preset: str | None = None) -> Answer:
        config, _, index = self.build_index(config_path, schema_path=schema_path, preset=preset)
        retrieval = self._retriever.retrieve(index, query, depth=config.retrieval_depth)
        backend = self._backend_factory.from_selection(
            BackendSelection(
                name=config.backend_name.value,
                endpoint=config.backend_endpoint,
                model=config.backend_model,
                timeout_seconds=config.backend_timeout_seconds,
            )
        )
        answer_format = format or AnswerFormat(config.answer_format)
        return self._answer_composer.compose(
            query,
            retrieval,
            format=answer_format,
            backend=backend,
            backend_on_failure=config.backend_on_failure.value,
        )
