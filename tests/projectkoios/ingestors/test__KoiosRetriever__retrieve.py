from __future__ import annotations

from pathlib import Path
import json
from typing import cast

from projectkoios.ingestors import Config, ConfigLoader, Evidence, GraphIndex, GraphIndexBuilder, GraphIndexJsonSerializer, JsonSchema, JsonSchemaLoader, JsonSchemaValidator, RetrievalResult, Retriever, SourceResolver, SourceSet
from projectkoios.ingestors.schemas import JsonObject

from tests.projectkoios.ingestors._helpers import write_config, write_schema


def load_fixture_index(tmp_path: Path) -> tuple[Config, GraphIndex]:
    """Load a fixture config and build its graph index."""
    # Schema fixture validates the generated YAML config.
    schema: JsonSchema = JsonSchemaLoader().load(write_schema(tmp_path))
    # Config controls source resolution for the fixture ADR.
    config: Config = ConfigLoader(JsonSchemaValidator(schema)).load(write_config(tmp_path))
    # Source set contains resolved ADR Markdown documents.
    source_set: SourceSet = SourceResolver().resolve(config)
    # Index contains extracted sections from resolved documents.
    index: GraphIndex = GraphIndexBuilder().build(source_set)
    return config, index


def test__Retriever__retrieve(tmp_path: Path) -> None:
    """Validate that retriever returns traceable evidence for a query."""
    # Index fixture contains the ADR source sections for retrieval.
    fixture: tuple[Config, GraphIndex] = load_fixture_index(tmp_path)
    # Index is the graph searched by the retriever.
    index: GraphIndex = fixture[1]
    # Result contains ranked evidence for the query.
    result: RetrievalResult = Retriever().retrieve(index, "ADR Example", depth=1)
    assert result.evidence
    assert ":" in result.evidence[0].citation


def test__Retriever__retrieve__evidence_is_traceable_to_persisted_index(tmp_path: Path) -> None:
    """Validate that retrieved evidence maps to the persisted index artifact."""
    # Index fixture contains the ADR source sections for retrieval.
    fixture: tuple[Config, GraphIndex] = load_fixture_index(tmp_path)
    # Config contains the persisted index output path.
    config: Config = fixture[0]
    # Index is the graph searched by the retriever.
    index: GraphIndex = fixture[1]
    # Result contains ranked evidence for the query.
    result: RetrievalResult = Retriever().retrieve(index, "ADR Example", depth=1)
    assert result.evidence

    GraphIndexJsonSerializer().write(index, config.index_path)
    # Artifact is the persisted JSON index loaded for traceability checks.
    artifact: JsonObject = cast(JsonObject, json.loads(config.index_path.read_text(encoding="utf-8")))
    # Documents are cast from JSON value form after loading the known index shape.
    documents: list[JsonObject] = cast(list[JsonObject], artifact["documents"])
    # Sections flatten persisted document sections for evidence matching.
    sections: list[JsonObject] = []
    document: JsonObject
    for document in documents:
        sections.extend(cast(list[JsonObject], document["sections"]))
    # Evidence is the first retriever hit to trace against persisted sections.
    evidence: Evidence = result.evidence[0]

    assert any(
        section["relative_path"] == evidence.relative_path
        and section["title"] == evidence.title
        and section["line_start"] == evidence.line_start
        and section["line_end"] == evidence.line_end
        for section in sections
    )
