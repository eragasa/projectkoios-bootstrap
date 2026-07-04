from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from projectkoios.ingestors.answers import Answer, AnswerComposer, AnswerFormat
from projectkoios.ingestors.backends import BackendAdapter, BackendFactory, BackendSelection
from projectkoios.ingestors.config import Config, ConfigLoader, RuntimeConfigValidator
from projectkoios.ingestors.index import GraphIndex, GraphIndexBuilder, GraphIndexJsonSerializer
from projectkoios.ingestors.retrieval import RetrievalResult, Retriever
from projectkoios.ingestors.schemas import JsonSchema, JsonSchemaLoader, JsonSchemaValidator
from projectkoios.ingestors.sources import SourceResolver, SourceSet


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Validation result for a Koios GraphRAG config.

    Args:
        config_path: Resolved config path.
        schema_valid: Whether schema loading/validation passed.
        runtime_valid: Whether runtime validation and source resolution passed.
        sources: Number of resolved sources.
        issues: Validation issue messages.
    """

    config_path: Path
    schema_valid: bool
    runtime_valid: bool
    sources: int
    issues: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PersistedIndexReport:
    """Summary of a persisted-index build.

    Args:
        output_path: Persisted index output path.
        sources: Number of resolved sources.
        sections: Number of indexed sections.
    """

    output_path: Path
    sources: int
    sections: int


class App:
    """Application service for Koios GraphRAG ingestion operations."""

    def __init__(self, *, backend_factory: BackendFactory | None = None) -> None:
        self.schema_loader: JsonSchemaLoader = JsonSchemaLoader()
        self.runtime_validator: RuntimeConfigValidator = RuntimeConfigValidator()
        self.source_resolver: SourceResolver = SourceResolver()
        self.index_builder: GraphIndexBuilder = GraphIndexBuilder()
        self.index_serializer: GraphIndexJsonSerializer = GraphIndexJsonSerializer()
        self.retriever: Retriever = Retriever()
        self.answer_composer: AnswerComposer = AnswerComposer()
        self.backend_factory: BackendFactory = backend_factory or BackendFactory()

    def schema_validator_for(self, schema_path: Path | None) -> JsonSchemaValidator | None:
        """Build a schema validator when a schema path is provided."""
        if schema_path is None:
            return None
        # Schema is loaded from disk before constructing the validator.
        schema: JsonSchema = self.schema_loader.load(schema_path)
        return JsonSchemaValidator(schema)

    def load_config(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> Config:
        """Load an ingestion config with optional schema validation."""
        # Schema validator is optional and only present when a schema path is supplied.
        schema_validator: JsonSchemaValidator | None = self.schema_validator_for(schema_path)
        # Loader applies schema validation and preset selection.
        loader: ConfigLoader = ConfigLoader(schema_validator=schema_validator)
        return loader.load(config_path, preset=preset)

    def validate_config(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> ValidationReport:
        """Validate config, runtime settings, and source resolution."""
        # Issues accumulates validation messages for the final report.
        issues: list[str] = []
        try:
            # Config is the loaded ingestion configuration under validation.
            config: Config = self.load_config(config_path, schema_path=schema_path, preset=preset)
        except Exception:
            # Error preserves the validation failure message for CLI and tests.
            error: BaseException | None = sys.exception()
            return ValidationReport(
                config_path=config_path.resolve(),
                schema_valid=False,
                runtime_valid=False,
                sources=0,
                issues=(str(error),),
            )
        try:
            self.runtime_validator.validate(config)
            # Source set confirms source patterns resolve after runtime validation.
            source_set: SourceSet = self.source_resolver.resolve(config)
        except Exception:
            # Runtime error preserves the runtime/source failure message for callers.
            runtime_error: BaseException | None = sys.exception()
            return ValidationReport(
                config_path=config.path,
                schema_valid=True,
                runtime_valid=False,
                sources=0,
                issues=(str(runtime_error),),
            )
        # Sources records the number of source documents resolved successfully.
        sources: int = len(source_set.documents)
        return ValidationReport(
            config_path=config.path,
            schema_valid=True,
            runtime_valid=True,
            sources=sources,
            issues=tuple(issues),
        )

    def build_index(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> tuple[Config, SourceSet, GraphIndex]:
        """Load config, resolve sources, and build an in-memory graph index."""
        # Config controls source selection and indexing options.
        config: Config = self.load_config(config_path, schema_path=schema_path, preset=preset)
        self.runtime_validator.validate(config)
        # Source set contains resolved source documents for indexing.
        source_set: SourceSet = self.source_resolver.resolve(config)
        # Index is built from the resolved source set.
        index: GraphIndex = self.index_builder.build(source_set)
        return config, source_set, index

    def persist_index(self, config_path: Path, *, schema_path: Path | None = None, preset: str | None = None) -> PersistedIndexReport:
        """Build and persist a graph index for a config."""
        # Build result carries config, sources, and index for persistence reporting.
        build_result: tuple[Config, SourceSet, GraphIndex] = self.build_index(
            config_path,
            schema_path=schema_path,
            preset=preset,
        )
        # Config provides the configured index output path.
        config: Config = build_result[0]
        # Source set provides source count for reporting.
        source_set: SourceSet = build_result[1]
        # Index provides sections and serialized content.
        index: GraphIndex = build_result[2]
        self.index_serializer.write(index, config.index_path)
        return PersistedIndexReport(
            output_path=config.index_path,
            sources=len(source_set.documents),
            sections=len(index.sections),
        )

    def retrieve(self, config_path: Path, query: str, *, schema_path: Path | None = None, preset: str | None = None) -> RetrievalResult:
        """Build an index and retrieve evidence for a query."""
        # Build result provides the config and index needed for retrieval.
        build_result: tuple[Config, SourceSet, GraphIndex] = self.build_index(
            config_path,
            schema_path=schema_path,
            preset=preset,
        )
        # Config provides retrieval depth.
        config: Config = build_result[0]
        # Index provides sections for lexical retrieval.
        index: GraphIndex = build_result[2]
        return self.retriever.retrieve(index, query, depth=config.retrieval_depth)

    def answer(self, config_path: Path, query: str, *, schema_path: Path | None = None, format: AnswerFormat | None = None, preset: str | None = None) -> Answer:
        """Build an index, retrieve evidence, and compose an answer."""
        # Build result provides config and index for retrieval and answering.
        build_result: tuple[Config, SourceSet, GraphIndex] = self.build_index(
            config_path,
            schema_path=schema_path,
            preset=preset,
        )
        # Config provides backend and answer-format settings.
        config: Config = build_result[0]
        # Index provides sections for lexical retrieval.
        index: GraphIndex = build_result[2]
        # Retrieval contains evidence passed to answer composition.
        retrieval: RetrievalResult = self.retriever.retrieve(index, query, depth=config.retrieval_depth)
        # Backend is constructed from runtime config selection.
        backend: BackendAdapter = self.backend_factory.from_selection(
            BackendSelection(
                name=config.backend_name.value,
                endpoint=config.backend_endpoint,
                model=config.backend_model,
                timeout_seconds=config.backend_timeout_seconds,
            )
        )
        # Answer format uses the explicit override or config default.
        answer_format: AnswerFormat = format or AnswerFormat(config.answer_format)
        return self.answer_composer.compose(
            query,
            retrieval,
            format=answer_format,
            backend=backend,
            backend_on_failure=config.backend_on_failure.value,
        )
