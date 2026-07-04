from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from projectkoios.ingestors.answers import Answer, AnswerComposer, AnswerFormat
from projectkoios.ingestors.backends import BackendAdapter, BackendFactory, BackendSelection
from projectkoios.ingestors.config import Config, ConfigLoader, RuntimeConfigValidator
from projectkoios.ingestors.index import GraphIndex, GraphIndexBuilder
from projectkoios.ingestors.retrieval import RetrievalResult, Retriever
from projectkoios.ingestors.schemas import JsonSchema, JsonSchemaLoader, JsonSchemaValidator
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
        self.schema_loader: JsonSchemaLoader = JsonSchemaLoader()
        self.runtime_validator: RuntimeConfigValidator = RuntimeConfigValidator()
        self.source_resolver: SourceResolver = SourceResolver()
        self.index_builder: GraphIndexBuilder = GraphIndexBuilder()
        self.retriever: Retriever = Retriever()
        self.answer_composer: AnswerComposer = AnswerComposer()
        self.backend_factory: BackendFactory = backend_factory or BackendFactory()

    def schema_validator_for(self, schema_path: Path | None) -> JsonSchemaValidator | None:
        if schema_path is None:
            return None
        schema: JsonSchema = self.schema_loader.load(schema_path)
        return JsonSchemaValidator(schema)

    def load_config(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> Config:
        schema_validator: JsonSchemaValidator | None = self.schema_validator_for(schema_path)
        loader: ConfigLoader = ConfigLoader(schema_validator=schema_validator)
        return loader.load(config_path, preset=preset)

    def validate_config(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> ValidationReport:
        issues: list[str] = []
        try:
            config: Config = self.load_config(config_path, schema_path=schema_path, preset=preset)
        except Exception as exc:
            return ValidationReport(
                config_path=config_path.resolve(),
                schema_valid=False,
                runtime_valid=False,
                sources=0,
                issues=(str(exc),),
            )
        try:
            self.runtime_validator.validate(config)
            source_set: SourceSet = self.source_resolver.resolve(config)
        except Exception as exc:
            return ValidationReport(
                config_path=config.path,
                schema_valid=True,
                runtime_valid=False,
                sources=0,
                issues=(str(exc),),
            )
        sources: int = len(source_set.documents)
        return ValidationReport(
            config_path=config.path,
            schema_valid=True,
            runtime_valid=True,
            sources=sources,
            issues=tuple(issues),
        )

    def build_index(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> tuple[Config, SourceSet, GraphIndex]:
        config: Config = self.load_config(config_path, schema_path=schema_path, preset=preset)
        self.runtime_validator.validate(config)
        source_set: SourceSet = self.source_resolver.resolve(config)
        index: GraphIndex = self.index_builder.build(source_set)
        return config, source_set, index

    def retrieve(self, config_path: Path, query: str, *, schema_path: Path | None = None, preset: str | None = None) -> RetrievalResult:
        build_result: tuple[Config, SourceSet, GraphIndex] = self.build_index(
            config_path,
            schema_path=schema_path,
            preset=preset,
        )
        config: Config = build_result[0]
        index: GraphIndex = build_result[2]
        return self.retriever.retrieve(index, query, depth=config.retrieval_depth)

    def answer(self, config_path: Path, query: str, *, schema_path: Path | None = None, format: AnswerFormat | None = None, preset: str | None = None) -> Answer:
        build_result: tuple[Config, SourceSet, GraphIndex] = self.build_index(
            config_path,
            schema_path=schema_path,
            preset=preset,
        )
        config: Config = build_result[0]
        index: GraphIndex = build_result[2]
        retrieval: RetrievalResult = self.retriever.retrieve(index, query, depth=config.retrieval_depth)
        backend: BackendAdapter = self.backend_factory.from_selection(
            BackendSelection(
                name=config.backend_name.value,
                endpoint=config.backend_endpoint,
                model=config.backend_model,
                timeout_seconds=config.backend_timeout_seconds,
            )
        )
        answer_format: AnswerFormat = format or AnswerFormat(config.answer_format)
        return self.answer_composer.compose(
            query,
            retrieval,
            format=answer_format,
            backend=backend,
            backend_on_failure=config.backend_on_failure.value,
        )
