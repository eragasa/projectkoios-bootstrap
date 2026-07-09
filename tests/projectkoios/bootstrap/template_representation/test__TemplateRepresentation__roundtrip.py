from __future__ import annotations

from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from projectkoios.bootstrap.schema import SchemaRegistry
from projectkoios.bootstrap.template_representation import (
    TemplateMarkdownError,
    TemplateMarkdownParser,
    TemplateMarkdownRenderer,
    TemplateNamespace,
    TemplateRecord,
    TemplateRepresentationPaths,
)
from projectkoios.bootstrap.template_representation.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
ADR_TEMPLATE_PATH = REPO_ROOT / "docs" / "templates" / "ADR.proposal.template.md"


def test__TemplateMarkdownParser__parse_file__constructs_record_from_adr_template() -> None:
    """Validate construction of a canonical record from the first template fixture."""
    # Parser reads only the controlled docs/templates fixture.
    parser: TemplateMarkdownParser = TemplateMarkdownParser()

    # Record is the canonical model for the live ADR proposal template fixture.
    record: TemplateRecord = parser.parse_file(ADR_TEMPLATE_PATH)

    assert record.template_id == "ADR.proposal.template"
    assert record.source_path == "docs/templates/ADR.proposal.template.md"
    assert record.title == "ADR: <Title>"
    assert [section.heading for section in record.sections][:3] == ["Status", "Normative language", "Context"]
    assert record.sections[0].body == "<proposal | draft | accepted | active | superseded>"


def test__SchemaRegistry__validate__loads_template_record_schema() -> None:
    """Validate the canonical template record schema loads through registry."""
    # Registry validates the schema document before instance validation.
    SchemaRegistry().validator_for("template-record.schema.json")


def test__TemplateMarkdownParser__parse_file_schema_record__validates_live_fixture() -> None:
    """Validate live template parsing produces a schema-backed record."""
    # Parser emits a validated schema-backed record instance from the live fixture.
    schema_record: JsonObject = TemplateMarkdownParser().parse_file_schema_record(
        ADR_TEMPLATE_PATH,
        created_on="20260708.044531Z",
    )
    # Metadata is schema-backed and narrows the template record schema ID.
    metadata: JsonObject = schema_record["metadata"]
    # Content is schema-backed and carries parsed template fields.
    content: JsonObject = schema_record["content"]

    assert metadata["schema_id"] == "https://projectkoios.local/schemas/template-record.schema.json"
    assert content["source_path"] == "docs/templates/ADR.proposal.template.md"


def test__TemplateSchema__validate__rejects_missing_required_content_field() -> None:
    """Validate schema rejection for missing required template content."""
    # Schema-backed record fixture is valid before one required field is removed.
    schema_record: JsonObject = TemplateMarkdownParser().parse_file_schema_record(
        ADR_TEMPLATE_PATH,
        created_on="20260708.044531Z",
    )
    # Content is mutated to remove a schema-required field.
    content: JsonObject = schema_record["content"]
    del content["sections"]

    with pytest.raises(ValidationError):
        SchemaRegistry().validate("template-record.schema.json", schema_record)


def test__TemplateSchema__validate__rejects_additional_content_properties() -> None:
    """Validate schema rejection for additional controlled content fields."""
    # Schema-backed record fixture is valid before an extra field is added.
    schema_record: JsonObject = TemplateMarkdownParser().parse_file_schema_record(
        ADR_TEMPLATE_PATH,
        created_on="20260708.044531Z",
    )
    # Content is mutated to include a schema-forbidden field.
    content: JsonObject = schema_record["content"]
    content["extra"] = "not allowed"

    with pytest.raises(ValidationError):
        SchemaRegistry().validate("template-record.schema.json", schema_record)


def test__TemplateRecord__to_dict__round_trips_serialized_representation() -> None:
    """Validate JSON-compatible serialization and deserialization."""
    # Record is parsed from the live fixture before serialization.
    record: TemplateRecord = TemplateMarkdownParser().parse_file(ADR_TEMPLATE_PATH)

    # Serialized record is the JSON-compatible canonical representation.
    serialized: JsonObject = record.to_dict()
    # Restored record proves the dictionary shape is complete enough for round trips.
    restored: TemplateRecord = TemplateRecord.from_dict(serialized)

    assert restored.semantic_dict() == record.semantic_dict()
    assert "<Title>" in {marker.marker for marker in restored.markers}


def test__TemplateMarkdownRenderer__render__is_deterministic() -> None:
    """Validate deterministic Markdown rendering from canonical representation."""
    # Record is parsed from the live fixture before rendering.
    record: TemplateRecord = TemplateMarkdownParser().parse_file(ADR_TEMPLATE_PATH)
    # Renderer emits the canonical Markdown projection.
    renderer: TemplateMarkdownRenderer = TemplateMarkdownRenderer()

    assert renderer.render(record) == renderer.render(record)
    assert renderer.render(record).startswith("```json\n")
    assert "# ADR: <Title>" in renderer.render(record)


def test__TemplateMarkdownParser__parse__round_trips_rendered_markdown() -> None:
    """Validate controlled Markdown render parses back to equivalent canonical data."""
    # Parser owns the controlled Markdown to record conversion.
    parser: TemplateMarkdownParser = TemplateMarkdownParser()
    # Record is parsed from the source fixture.
    record: TemplateRecord = parser.parse_file(ADR_TEMPLATE_PATH)
    # Markdown render is ingested back into the canonical representation.
    markdown: str = TemplateMarkdownRenderer().render(record)
    # Round-tripped record should preserve semantic representation fields.
    round_tripped: TemplateRecord = parser.parse(markdown, source_path=record.source_path)

    assert round_tripped.semantic_dict() == record.semantic_dict()


def test__TemplateMarkdownParser__schema_record_round_trip__preserves_semantic_equality() -> None:
    """Validate schema-backed record render and parse round-trip equivalence."""
    # Parser emits schema-backed record data from the live fixture.
    parser: TemplateMarkdownParser = TemplateMarkdownParser()
    # Schema record is the validated first parse result.
    schema_record: JsonObject = parser.parse_file_schema_record(ADR_TEMPLATE_PATH, created_on="20260708.044531Z")
    # Renderer consumes schema-backed record data for deterministic Markdown projection.
    markdown: str = TemplateMarkdownRenderer().render_schema_record(schema_record)
    # Round-tripped schema record is validated during parsing.
    round_tripped: JsonObject = parser.parse_schema_record(
        markdown,
        source_path="docs/templates/ADR.proposal.template.md",
        created_on="20260708.044531Z",
    )

    assert round_tripped["content"] == schema_record["content"]


def test__TemplateSchema__validate__distinguishes_schema_errors_from_parse_errors() -> None:
    """Validate schema validation errors remain distinct from Markdown parse errors."""
    # Invalid schema record keeps parse behavior out of this validation assertion.
    invalid_record: JsonObject = {"metadata": {}, "content": {}}

    with pytest.raises(ValidationError):
        SchemaRegistry().validate("template-record.schema.json", invalid_record)
    with pytest.raises(TemplateMarkdownError):
        TemplateMarkdownParser().parse("## Missing Title", source_path="docs/templates/missing-title.md")


def test__TemplateMarkdownParser__parse__allows_presentation_variance() -> None:
    """Validate presentation-only whitespace variance normalizes for equivalence."""
    # Markdown fixture includes extra surrounding blank lines and trailing spaces.
    markdown: str = "\n\n# Minimal Template  \n\n\nIntro text.  \n\n## Section  \n\nBody text.  \n\n"
    # Parser converts presentation variance into canonical body values.
    record: TemplateRecord = TemplateMarkdownParser().parse(markdown, source_path="docs/templates/minimal.template.md")

    assert record.title == "Minimal Template"
    assert record.lead_body == "Intro text."
    assert record.sections[0].body == "Body text."


def test__TemplateMarkdownParser__parse__rejects_missing_title() -> None:
    """Validate typed parse failure for missing required heading."""
    # Markdown fixture intentionally omits the required top-level title.
    markdown: str = "## Section\n\nBody text.\n"

    with pytest.raises(TemplateMarkdownError, match="Missing required top-level"):
        TemplateMarkdownParser().parse(markdown, source_path="docs/templates/missing-title.md")


def test__TemplateMarkdownParser__parse__rejects_ambiguous_heading_hierarchy() -> None:
    """Validate typed parse failure for ambiguous heading hierarchy."""
    # Markdown fixture includes an unsupported fourth-level heading.
    markdown: str = "# Template\n\n## Section\n\n#### Too Deep\n"

    with pytest.raises(TemplateMarkdownError, match="Ambiguous heading depth"):
        TemplateMarkdownParser().parse(markdown, source_path="docs/templates/ambiguous.md")


def test__TemplateRepresentationPaths__classify__distinguishes_document_namespaces() -> None:
    """Validate namespace classification boundaries for first-slice documents."""
    # Path helper classifies repository document paths without broad ingestion behavior.
    paths: TemplateRepresentationPaths = TemplateRepresentationPaths()

    assert paths.classify(REPO_ROOT / "docs" / "templates" / "ADR.proposal.template.md").namespace is TemplateNamespace.TEMPLATE
    assert paths.classify(REPO_ROOT / "docs" / "implementation" / "implementation.00.md").namespace is TemplateNamespace.IMPLEMENTATION
    assert paths.classify(REPO_ROOT / "docs" / "plans" / "implementation-brief.example.md").namespace is TemplateNamespace.PLAN


def test__TemplateMarkdownParser__parse_file__rejects_non_template_namespace() -> None:
    """Validate parser refuses files outside the template namespace by default."""
    # Non-template document path should not be parsed as a template fixture.
    path: Path = REPO_ROOT / "docs" / "implementation" / "implementation.00.md"

    with pytest.raises(ValueError, match="only supports docs/templates"):
        TemplateMarkdownParser().parse_file(path)
