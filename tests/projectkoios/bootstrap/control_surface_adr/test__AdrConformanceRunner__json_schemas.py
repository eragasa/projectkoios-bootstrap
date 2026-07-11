from __future__ import annotations

import json
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr import (
    AdrConformancePaths,
    AdrConformanceResult,
    AdrConformanceRunner,
    AdrMarkdownRecordParser,
    AdrRecordValidator,
)
from projectkoios.bootstrap.control_surface.adr.models import PilotAdrSourceConfig
from projectkoios.bootstrap.schema.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ADR = REPO_ROOT / "docs" / "adr" / "adr.json-schemas.draft.md"
SCHEMA = REPO_ROOT / "docs" / "schemas" / "adr.schema.json"


JSON_SCHEMAS_SOURCE_CONFIG = PilotAdrSourceConfig(
    source_path="docs/adr/adr.json-schemas.draft.md",
    legacy_filename_status_suffix=".draft",
    record_id="adr.json-schemas",
    slug="json-schemas",
    delegated_operator="pi",
    source_date="20260702.213000Z",
)


def source_record() -> tuple[JsonObject, JsonObject]:
    """Return the JSON schemas ADR source record and mapping."""
    # Markdown is the source fixture for parser-focused tests.
    markdown: str = SOURCE_ADR.read_text(encoding="utf-8")
    return AdrMarkdownRecordParser(source_config=JSON_SCHEMAS_SOURCE_CONFIG).parse_source_record(markdown)


def test__AdrMarkdownRecordParser__parse_source_record__accepts_stable_adr_heading() -> None:
    """Parse stable `# ADR: Title` heading without legacy timestamp stripping note."""
    # Legacy fixture body is reused while the heading exercises stable format.
    markdown: str = SOURCE_ADR.read_text(encoding="utf-8").replace(
        "# ADR 20260702.213000Z: JSON Schemas Namespace",
        "# ADR: JSON Schemas Namespace",
        1,
    )
    # Parser should accept stable heading and not record legacy heading stripping.
    record: JsonObject
    mapping: JsonObject
    record, mapping = AdrMarkdownRecordParser(source_config=JSON_SCHEMAS_SOURCE_CONFIG).parse_source_record(markdown)

    assert record["title"] == "JSON Schemas Namespace"
    assert "legacy_title_heading" not in mapping["normalized_fields"]


def test__AdrMarkdownRecordParser__parse_source_record__omits_routing_and_related() -> None:
    """Map JSON schemas ADR into the current schema without routing."""
    record: JsonObject
    mapping: JsonObject
    record, mapping = source_record()
    assert record["id"] == "adr.json-schemas"
    assert record["slug"] == "json-schemas"
    assert record["status"] == "draft"
    assert record["context"]["delegated_operator"] == "pi"
    assert mapping["normalized_fields"]["legacy_title_heading"] == "removed legacy ADR heading prefix before title"
    assert "routing" not in record
    assert "related" not in record["links"]
    assert mapping["preserved_outside_schema"]["routing"] == {
        "owner": "Athena",
        "next_phase": "proposed",
        "notes": "JSON schema/contract surface for the UI/core family.",
    }
    assert mapping["preserved_outside_schema"]["links.related"] == [
        {
            "label": "ADR 20260702.213000Z: Shared UI Core Namespace",
            "path": "adr.ui-core.draft.md",
        }
    ]


def test__AdrRecordValidator__validate__accepts_json_schemas_record() -> None:
    """Validate the conformed JSON schemas ADR against the ADR schema."""
    record: JsonObject
    _mapping: JsonObject
    record, _mapping = source_record()
    AdrRecordValidator().validate(record)


def test__AdrConformanceRunner__run__round_trips_without_mutating_source(tmp_path: Path) -> None:
    """Round-trip conformed JSON through projection without source mutation."""
    # Repo root isolates generated conformance artifacts from the real repository.
    repo_root: Path = tmp_path / "repo"
    # Source directory holds the copied source ADR fixture.
    source_dir: Path = repo_root / "docs" / "adr"
    # Schema directory holds the copied current ADR schema fixture.
    schema_dir: Path = repo_root / "docs" / "schemas"
    source_dir.mkdir(parents=True)
    schema_dir.mkdir(parents=True)
    # Original source text is the non-destructive baseline.
    original_source_text: str = SOURCE_ADR.read_text(encoding="utf-8")
    (source_dir / SOURCE_ADR.name).write_text(original_source_text, encoding="utf-8")
    (schema_dir / SCHEMA.name).write_text(SCHEMA.read_text(encoding="utf-8"), encoding="utf-8")

    # Paths point the runner at the isolated fixture repository.
    paths: AdrConformancePaths = AdrConformancePaths(repo_root=repo_root)
    # Result exposes storage export and projection parse records.
    result: AdrConformanceResult = AdrConformanceRunner(paths=paths).run()
    # Checkpoint is the active conformed JSON record artifact.
    checkpoint: JsonObject = json.loads(paths.json_checkpoint.read_text(encoding="utf-8"))
    # Copied source path must remain byte-for-byte unchanged after generation.
    copied_source_text: str = paths.source_adr.read_text(encoding="utf-8")

    assert copied_source_text == original_source_text
    assert result.projection_record == result.exported_record
    assert checkpoint == result.projection_record
    assert "routing" not in result.projection_record
    assert not list(paths.target_dir.rglob("*.sqlite"))
    assert not list(paths.target_dir.rglob("*.db"))


def test__AdrConformanceRunner__run__writes_active_conformance_artifacts(tmp_path: Path) -> None:
    """Run the approved JSON schemas conformance slice."""
    # Repo root isolates generated conformance artifacts from the real repository.
    repo_root: Path = tmp_path / "repo"
    # Source directory holds the copied source ADR fixture.
    source_dir: Path = repo_root / "docs" / "adr"
    # Schema directory holds the copied current ADR schema fixture.
    schema_dir: Path = repo_root / "docs" / "schemas"
    source_dir.mkdir(parents=True)
    schema_dir.mkdir(parents=True)
    (source_dir / SOURCE_ADR.name).write_text(SOURCE_ADR.read_text(encoding="utf-8"), encoding="utf-8")
    (schema_dir / SCHEMA.name).write_text(SCHEMA.read_text(encoding="utf-8"), encoding="utf-8")

    # Paths point the runner at the isolated fixture repository.
    paths: AdrConformancePaths = AdrConformancePaths(repo_root=repo_root)
    # Result exposes in-memory records for comparison against written artifacts.
    result: AdrConformanceResult = AdrConformanceRunner(paths=paths).run()

    # Checkpoint is the active conformed JSON record artifact.
    checkpoint: JsonObject = json.loads(paths.json_checkpoint.read_text(encoding="utf-8"))
    # Manifest indexes generated artifacts and active-forward status.
    manifest: JsonObject = json.loads(paths.manifest.read_text(encoding="utf-8"))
    # Mapping preserves field-level source conversion details.
    mapping: JsonObject = json.loads(paths.mapping.read_text(encoding="utf-8"))
    # Conversion evidence preserves omitted source-only fields in sidecar form.
    conversion_evidence: JsonObject = json.loads(paths.conversion_evidence.read_text(encoding="utf-8"))

    assert checkpoint == result.exported_record
    assert "routing" not in checkpoint
    assert "related" not in checkpoint["links"]
    assert manifest["conformance"]["status"] == "active-conformance-record"
    assert manifest["json_checkpoint"]["active_going_forward"] is True
    assert manifest["watchpoints"]["no_docs_adr_mutation"] is True
    assert manifest["document_store"]["table"] == "json_documents"
    assert conversion_evidence["status"] == "active-conformance-record"
    assert conversion_evidence["record"]["active_going_forward"] is True
    assert conversion_evidence["field_treatment"]["omitted_from_record_preserved_in_sidecar"]["routing"]["owner"] == "Athena"
    assert conversion_evidence["field_treatment"]["omitted_from_record_preserved_in_sidecar"]["links.related"] == [
        {
            "label": "ADR 20260702.213000Z: Shared UI Core Namespace",
            "path": "adr.ui-core.draft.md",
        }
    ]
    assert mapping["source_path"] == "docs/adr/adr.json-schemas.draft.md"
    assert not list(paths.target_dir.rglob("*.sqlite"))
    assert not list(paths.target_dir.rglob("*.db"))
