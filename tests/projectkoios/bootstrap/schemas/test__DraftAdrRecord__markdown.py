from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from projectkoios.bootstrap.schemas import (
    DraftAdrMarkdownIngester,
    DraftAdrMarkdownRenderer,
    DraftAdrRecord,
    MarkdownIngestError,
)
from tests.projectkoios.bootstrap.schemas.test__SchemaRegistry__validate import valid_draft_adr_record


def test__DraftAdrRecord__from_dict__is_immutable_and_preserves_metadata():
    record = DraftAdrRecord.from_dict(valid_draft_adr_record())
    assert record.metadata.to_dict()["origin"] == {"type": "role_output", "method": "manual", "actor": "ATHENA", "authority": "role"}
    with pytest.raises(FrozenInstanceError):
        record.content = record.content


def test__DraftAdrRecord__from_dict__fails_before_render_for_missing_metadata():
    source = valid_draft_adr_record()
    del source["metadata"]
    with pytest.raises(Exception):
        DraftAdrRecord.from_dict(source)


def test__DraftAdrMarkdownRenderer__render__uses_deterministic_section_and_concern_order():
    source = valid_draft_adr_record()
    source["content"]["context"]["concerns"] = [
        {"level": "MAY", "text": "Allow optional details."},
        {"level": "MUST NOT", "text": "Lose provenance."},
        {"level": "MUST", "text": "Preserve metadata."},
    ]
    markdown = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    assert markdown.index("## Context") < markdown.index("## Decision") < markdown.index("## Consequences")
    assert markdown.index("# ADR: Test Schema Record") < markdown.index('"title": "Test Schema Record"')
    assert markdown.index("- MUST Preserve metadata.") < markdown.index("- MUST NOT Lose provenance.") < markdown.index("- MAY Allow optional details.")


def test__DraftAdrMarkdownIngester__ingest__round_trips_metadata_and_content():
    source = valid_draft_adr_record()
    record = DraftAdrRecord.from_dict(source)
    markdown = DraftAdrMarkdownRenderer().render(record)
    ingested = DraftAdrMarkdownIngester().ingest(markdown)
    assert ingested == source
    assert DraftAdrRecord.from_dict(ingested).to_dict() == source


def test__DraftAdrMarkdownIngester__ingest__rejects_missing_metadata():
    markdown = "# ADR: Missing Metadata\n\n## Context\n"
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__rejects_missing_required_section():
    source = valid_draft_adr_record()
    markdown = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("## Decision", "## Skipped Decision", 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__rejects_section_order_violation():
    source = valid_draft_adr_record()
    markdown = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("## Context", "## TEMP", 1)
    markdown = markdown.replace("## Decision", "## Context", 1)
    markdown = markdown.replace("## TEMP", "## Decision", 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__rejects_malformed_concern_keyword():
    source = valid_draft_adr_record()
    markdown = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("- MUST Preserve context.", "- REQUIRED Preserve context.", 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__rejects_ambiguous_heading_depth():
    source = valid_draft_adr_record()
    markdown = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("## Decision", "#### Decision", 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)


def test__DraftAdrMarkdownIngester__ingest__captures_extra_section_as_rejected():
    source = valid_draft_adr_record()
    markdown = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = f"{markdown}\n## Extra Notes\n\nTransport-only note.\n"
    ingested = DraftAdrMarkdownIngester().ingest(markdown)
    assert ingested["content"]["rejected"] == [{"heading": "Extra Notes", "reason": "extra_section", "body": "Transport-only note."}]


def test__DraftAdrMarkdownIngester__ingest__rejects_description_over_600_characters():
    source = valid_draft_adr_record()
    markdown = DraftAdrMarkdownRenderer().render(DraftAdrRecord.from_dict(source))
    markdown = markdown.replace("Context description.", "x" * 601, 1)
    with pytest.raises(MarkdownIngestError):
        DraftAdrMarkdownIngester().ingest(markdown)
