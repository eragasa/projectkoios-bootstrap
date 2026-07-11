from __future__ import annotations

import json
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr import (
    AdrBidirectionalCanaryPaths,
    AdrBidirectionalCanaryResult,
    AdrBidirectionalCanaryRunner,
    AdrMarkdownRecordParser,
    AdrRecordValidator,
)
from projectkoios.bootstrap.schema.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ADR = REPO_ROOT / "docs" / "adr" / "adr.json-schemas.draft.md"
SCHEMA = REPO_ROOT / "docs" / "schemas" / "adr.schema.json"


def copy_canary_inputs(repo_root: Path) -> None:
    """Copy the exact canary source and current schema into a fixture repo."""
    # Source fixture directory mirrors repository layout without mutating the repo.
    source_dir: Path = repo_root / "docs" / "adr"
    # Schema fixture directory mirrors repository layout without changing schemas.
    schema_dir: Path = repo_root / "docs" / "schemas"
    source_dir.mkdir(parents=True)
    schema_dir.mkdir(parents=True)
    (source_dir / SOURCE_ADR.name).write_text(SOURCE_ADR.read_text(encoding="utf-8"), encoding="utf-8")
    (schema_dir / SCHEMA.name).write_text(SCHEMA.read_text(encoding="utf-8"), encoding="utf-8")


def test__AdrBidirectionalCanaryRunner__run__writes_candidate_envelope(tmp_path: Path) -> None:
    """Generate candidate object evidence without publishing schema authority."""
    # Temp repo prevents canary generation from touching repository source files.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Paths point the runner at isolated source/schema fixtures.
    paths: AdrBidirectionalCanaryPaths = AdrBidirectionalCanaryPaths(repo_root=repo_root)

    # Result exposes the in-memory envelope for artifact comparison.
    result: AdrBidirectionalCanaryResult = AdrBidirectionalCanaryRunner(paths=paths).run()
    # Envelope artifact is the candidate AdrBidirectionalObject evidence.
    envelope: JsonObject = json.loads(paths.bidirectional_object.read_text(encoding="utf-8"))
    # Conversion evidence proves classification and sidecar separation.
    conversion_evidence: JsonObject = json.loads(paths.conversion_evidence.read_text(encoding="utf-8"))
    # Manifest records one-source canary boundaries and artifact paths.
    manifest: JsonObject = json.loads(paths.manifest.read_text(encoding="utf-8"))

    assert envelope == result.envelope
    assert envelope["object_type"] == "AdrBidirectionalObject"
    assert envelope["object_version"] == "candidate-0"
    assert envelope["authority_mode"] == "candidate-evidence-only-not-repository-authority"
    assert envelope["classification"] == {
        "category": "template_schema_contract",
        "secondary_aspect": "architecture_blueprint",
        "source_role": "canary_source",
        "source_authority_effect": "none",
        "disposition_note": "Envelope metadata only; does not change source status, filename, lifecycle authority, or schema authority.",
    }
    assert "classification" not in envelope["content"]
    assert conversion_evidence["classification_outside_content"] is True
    assert manifest["canary"]["source_count"] == 1
    assert manifest["boundaries"]["docs_schemas_mutation"] is False


def test__AdrBidirectionalCanaryRunner__run__preserves_unsupported_source_fields(tmp_path: Path) -> None:
    """Preserve routing and related link evidence outside ADR content."""
    # Temp repo isolates generated evidence artifacts.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Paths constrain the run to the canary fixture and dev evidence directory.
    paths: AdrBidirectionalCanaryPaths = AdrBidirectionalCanaryPaths(repo_root=repo_root)

    # Result contains sidecar evidence produced from the exact canary source.
    result: AdrBidirectionalCanaryResult = AdrBidirectionalCanaryRunner(paths=paths).run()
    # Envelope is inspected to ensure unsupported fields stayed out of content.
    envelope: JsonObject = result.envelope

    assert "routing" not in envelope["content"]
    assert "related" not in envelope["content"]["links"]
    assert envelope["sidecar"]["routing"] == {
        "owner": "Athena",
        "next_phase": "proposed",
        "notes": "JSON schema/contract surface for the UI/core family.",
    }
    assert envelope["sidecar"]["links.related"] == [
        {
            "label": "ADR 20260702.213000Z: Shared UI Core Namespace",
            "path": "adr.ui-core.draft.md",
        }
    ]
    assert envelope["conversion_evidence"]["omitted_from_content_preserved_in_sidecar"] == [
        "routing",
        "links.related",
        "source.date",
        "source.filename_status_suffix",
    ]


def test__AdrBidirectionalCanaryRunner__run__round_trips_generated_projection_only(tmp_path: Path) -> None:
    """Parse generated projection back to schema content with semantic equality."""
    # Temp repo isolates generated projection evidence.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Paths point projection generation at the isolated fixture repository.
    paths: AdrBidirectionalCanaryPaths = AdrBidirectionalCanaryPaths(repo_root=repo_root)

    # Result carries the parsed projection record returned by the runner.
    result: AdrBidirectionalCanaryResult = AdrBidirectionalCanaryRunner(paths=paths).run()
    # Projection text must be visibly generated-only evidence.
    projection: str = paths.markdown_projection.read_text(encoding="utf-8")
    # Projection record is parsed only from the generated Markdown artifact.
    projection_record: JsonObject = AdrMarkdownRecordParser().parse_projection_record(projection)

    assert "ADR BIDIRECTIONAL OBJECT CANARY: generated projection evidence only" in projection
    assert result.envelope["content"] == projection_record
    assert result.envelope["content"] == result.projection_record
    assert result.envelope["markdown_projection"]["hand_authored_markdown_ingest"] is False
    assert result.envelope["conflict_policy"]["json_vs_markdown"] == "projection_only_no_ingest"
    AdrRecordValidator().validate(projection_record)


def test__AdrBidirectionalCanaryRunner__run__does_not_mutate_source_or_create_database(tmp_path: Path) -> None:
    """Prove source Markdown is unchanged and no mutable database files exist."""
    # Temp repo source text is compared before and after generation.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Paths identify the copied source whose bytes must remain unchanged.
    paths: AdrBidirectionalCanaryPaths = AdrBidirectionalCanaryPaths(repo_root=repo_root)
    # Original source text is the source-mutation baseline.
    original_source_text: str = paths.source_adr.read_text(encoding="utf-8")

    # Result includes validation flags and the generated evidence directory.
    result: AdrBidirectionalCanaryResult = AdrBidirectionalCanaryRunner(paths=paths).run()

    assert paths.source_adr.read_text(encoding="utf-8") == original_source_text
    assert result.envelope["validation"]["source_mutation_proof"]["mutated"] is False
    assert result.envelope["validation"]["no_mutable_database_files_created"] is True
    assert not list(paths.target_dir.rglob("*.sqlite"))
    assert not list(paths.target_dir.rglob("*.db"))
