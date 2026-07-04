from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from projectkoios.bootstrap.schema import (
    DraftAdrMarkdownIngester,
    DraftAdrMarkdownRenderer,
    DraftAdrRecord,
    MarkdownIngestError,
)
from projectkoios.bootstrap.schema.models import JsonObject
from tests.projectkoios.bootstrap.schema.test__SchemaRegistry__validate import valid_draft_adr_record


def test__DraftAdrRecord__from_dict__is_immutable_and_preserves_metadata() -> None:
    """Validate that draft ADR records are immutable and retain metadata."""
    # Record is built from the reusable valid schema-record fixture.
    record: DraftAdrRecord = DraftAdrRecord.from_dict(valid_draft_adr_record())
    assert record.metadata.to_dict()["origin"] == {"type": "role_output", "method": "manual", "actor": "ATHENA", "authority": "role"}
    with pytest.raises(FrozenInstanceError):
        setattr(record, "content", record.content)


def test__DraftAdrRecord__from_dict__deep_freezes_metadata_from_source_mutation() -> None:
    """Validate that source mutations cannot affect frozen record metadata."""
    # Source is mutated after model construction to verify defensive copying.
    source: JsonObject = valid_draft_adr_record()
    # Record should retain the original metadata values.
    record: DraftAdrRecord = DraftAdrRecord.from_dict(source)
    source["metadata"]["origin"]["actor"] = "user"
    assert record.metadata.to_dict()["origin"]["actor"] == "ATHENA"
    with pytest.raises(TypeError):
        record.metadata.fields["origin"]["actor"] = "user"


def test__DraftAdrRecord__to_dict__returns_deep_mutable_copy() -> None:
    """Validate that to_dict returns a mutable copy without changing the record."""
    # Record provides the immutable source for the mutable serialization check.
    record: DraftAdrRecord = DraftAdrRecord.from_dict(valid_draft_adr_record())
    # Serialized data is mutated to prove it is detached from record internals.
    serialized: JsonObject = record.to_dict()
    serialized["metadata"]["origin"]["actor"] = "user"
    serialized["content"]["context"]["concerns"].append({"level": "MAY", "text": "Mutate copy only."})
    assert record.metadata.to_dict()["origin"]["actor"] == "ATHENA"
    assert len(record.to_dict()["content"]["context"]["concerns"]) == 1


def test__DraftAdrRecord__from_dict__fails_before_render_for_missing_metadata() -> None:
    """Validate that record construction fails before rendering without metadata."""
    # Source is invalid because the required metadata object is removed.
    source: JsonObject = valid_draft_adr_record()
    del source["metadata"]
    with pytest.raises(Exception):
        DraftAdrRecord.from_dict(source)


def test__DraftAdrMarkdownRenderer__render__uses_deterministic_section_and_concern_order() -> None:
    """Validate deterministic section and concern rendering order."""
    # Source concerns are intentionally out of desired rendered order.
    source: JsonObject = valid_draft_adr_record()
    source["content"]["context"]["concerns"] = [
        {"level": "MAY", "text": "Allow optional details."},
        {"level": "MUST NOT", "text": "Lose provenance."},
        {"level": "MUST", "text": "Preserve metadata."},
    ]
    # Markdown output should normalize sections and concern severity order.
    markdown: str = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    assert markdown.index("## Context") < markdown.index("## Decision") < markdown.index("## Consequences")
    assert markdown.index("# ADR: Test Schema Record") < markdown.index('"title": "Test Schema Record"')
    assert markdown.index("- MUST Preserve metadata.") < markdown.index("- MUST NOT Lose provenance.") < markdown.index("- MAY Allow optional details.")


def test__DraftAdrMarkdownIngester__ingest__round_trips_metadata_and_content() -> None:
    """Validate that rendered draft ADR Markdown round-trips to schema data."""
    # Source fixture is converted into a typed record for rendering.
    source: JsonObject = valid_draft_adr_record()
    # Record is the canonical model used by the Markdown renderer.
    record: DraftAdrRecord = DraftAdrRecord.from_dict(source)
    # Markdown is ingested back into schema-record dictionary form.
    markdown: str = DraftAdrMarkdownRenderer().render(record)
    # Ingested data should match the original fixture exactly.
    ingested: JsonObject = DraftAdrMarkdownIngester().ingest(markdown)
    assert ingested == source
    assert DraftAdrRecord.from_dict(ingested).to_dict() == source


def test__DraftAdrMarkdownIngester__ingest__rejects_missing_metadata() -> None:
    """Validate that Markdown ingest rejects missing metadata blocks."""
    # Markdown intentionally omits the metadata block required by the ingester.
    markdown: str = "# ADR: Missing Metadata\n\n## Context\n"
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__rejects_missing_required_section() -> None:
    """Validate that Markdown ingest rejects missing required sections."""
    # Source fixture renders a complete document before one required heading is changed.
    source: JsonObject = valid_draft_adr_record()
    # Markdown is mutated to remove the expected Decision heading.
    markdown: str = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("## Decision", "## Skipped Decision", 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__rejects_section_order_violation() -> None:
    """Validate that Markdown ingest rejects required section order changes."""
    # Source fixture renders a complete document before headings are swapped.
    source: JsonObject = valid_draft_adr_record()
    # Markdown is mutated through a temporary heading to swap required order.
    markdown: str = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("## Context", "## TEMP", 1)
    markdown = markdown.replace("## Decision", "## Context", 1)
    markdown = markdown.replace("## TEMP", "## Decision", 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__rejects_malformed_concern_keyword() -> None:
    """Validate that Markdown ingest rejects unknown concern keywords."""
    # Source fixture renders a complete document before a concern keyword is changed.
    source: JsonObject = valid_draft_adr_record()
    # Markdown is mutated to use a non-policy concern keyword.
    markdown: str = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("- MUST Preserve context.", "- REQUIRED Preserve context.", 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__rejects_ambiguous_heading_depth() -> None:
    """Validate that Markdown ingest rejects ambiguous heading depth."""
    # Source fixture renders a complete document before one heading depth is changed.
    source: JsonObject = valid_draft_adr_record()
    # Markdown is mutated to create an unsupported required heading level.
    markdown: str = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("## Decision", "#### Decision", 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__captures_extra_section_as_rejected() -> None:
    """Validate that extra Markdown sections are captured as rejected content."""
    # Source fixture renders a complete document before an extra section is appended.
    source: JsonObject = valid_draft_adr_record()
    # Markdown includes one unsupported top-level section after required content.
    markdown: str = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = f"{markdown}\n## Extra Notes\n\nTransport-only note.\n"
    # Ingested content should preserve the rejected extra section details.
    ingested: JsonObject = DraftAdrMarkdownIngester().ingest(markdown)
    assert ingested["content"]["rejected"] == [{"heading": "Extra Notes", "reason": "extra_section", "body": "Transport-only note."}]


def test__DraftAdrMarkdownIngester__ingest__rejects_description_over_600_characters() -> None:
    """Validate that Markdown ingest rejects overlong section descriptions."""
    # Source fixture renders a complete document before a description is expanded.
    source: JsonObject = valid_draft_adr_record()
    # Markdown is mutated to exceed the section description length bound.
    markdown: str = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("Context description.", "x" * 601, 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)
