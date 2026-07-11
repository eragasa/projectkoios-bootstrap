from __future__ import annotations

import json
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr import AdrMessyCanaryPaths, AdrMessyCanaryResult, AdrMessyCanaryRunner
from projectkoios.bootstrap.schema.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ADR = REPO_ROOT / "docs" / "adr" / "adr.schema-base.md"
REVIEWED_INVENTORY = REPO_ROOT / "dev" / "adr-json-authority-inventory-review-overrides-slice-1" / "reviewed-inventory.json"
REVIEW_SUMMARY = REPO_ROOT / "dev" / "adr-json-authority-inventory-review-overrides-slice-1" / "review-summary.json"


def copy_canary_inputs(repo_root: Path) -> None:
    """Copy exact messy canary source and Slice 1 review evidence."""
    # Source target mirrors the repository ADR path for the one-source canary.
    source_target: Path = repo_root / "docs" / "adr" / "adr.schema-base.md"
    source_target.parent.mkdir(parents=True)
    source_target.write_text(SOURCE_ADR.read_text(encoding="utf-8"), encoding="utf-8")
    # Review target mirrors the required Slice 1 reviewed inventory input path.
    review_target_dir: Path = repo_root / "dev" / "adr-json-authority-inventory-review-overrides-slice-1"
    review_target_dir.mkdir(parents=True)
    (review_target_dir / "reviewed-inventory.json").write_text(REVIEWED_INVENTORY.read_text(encoding="utf-8"), encoding="utf-8")
    (review_target_dir / "review-summary.json").write_text(REVIEW_SUMMARY.read_text(encoding="utf-8"), encoding="utf-8")


def test__AdrMessyCanaryRunner__run__preserves_missing_status_and_blocks_conversion(tmp_path: Path) -> None:
    """Messy canary preserves missing Markdown status without inventing draft."""
    # Temp repo isolates source and generated evidence.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Paths point the runner at copied canary inputs.
    paths: AdrMessyCanaryPaths = AdrMessyCanaryPaths(repo_root=repo_root)

    # Result exposes candidate object and conflict report for assertions.
    result: AdrMessyCanaryResult = AdrMessyCanaryRunner(paths=paths).run()
    # Candidate object must remain incomplete/review-only due missing status.
    candidate: JsonObject = result.candidate_object

    assert candidate["source_path"] == "docs/adr/adr.schema-base.md"
    assert candidate["content_candidate"]["status"] is None
    assert candidate["content_candidate"]["status_preservation"] == "missing in Markdown source; not invented"
    assert candidate["content_candidate"]["schema_validation_blocked"] is True
    assert result.conflict_lossiness_report["outcome"] == "conversion_candidate_blocked_pending_review"
    assert result.conflict_lossiness_report["status_inference"] == "blocked; no status invented to satisfy schema"
    assert result.conversion_evidence["status_invented"] is False


def test__AdrMessyCanaryRunner__run__preserves_sidecar_and_reviewed_inventory(tmp_path: Path) -> None:
    """Preserve embedded metadata and Slice 1 reviewed values as provenance."""
    # Temp repo isolates generated evidence from repository files.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Paths point the runner at copied canary inputs.
    paths: AdrMessyCanaryPaths = AdrMessyCanaryPaths(repo_root=repo_root)

    # Result sidecar contains ambiguous embedded metadata and reviewed labels.
    result: AdrMessyCanaryResult = AdrMessyCanaryRunner(paths=paths).run()
    # Sidecar evidence keeps schema-record metadata outside ADR content.
    sidecar: JsonObject = result.sidecar_provenance

    assert sidecar["source_title"] == "ADR: Schema Base Class for ADR Records"
    assert sidecar["embedded_metadata"]["record_id"] == "adr.schema-base"
    assert sidecar["embedded_metadata"]["status"] == "draft"
    assert sidecar["observed_markdown_status"] is None
    assert sidecar["reviewed_inventory_reference"]["reviewed_disposition"] == "manual_review_required"
    assert sidecar["reviewed_inventory_reference"]["automatic_conversion_eligibility_candidate"] is False
    assert sidecar["ambiguity"]["schema_implementation_contract"] is True


def test__AdrMessyCanaryRunner__run__does_not_mutate_source_or_create_projection_or_database(tmp_path: Path) -> None:
    """Canary generation leaves source unchanged and avoids DB/projection files."""
    # Temp repo isolates source mutation proof.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Paths identify copied source and evidence directory.
    paths: AdrMessyCanaryPaths = AdrMessyCanaryPaths(repo_root=repo_root)
    # Source text before generation is the non-mutation baseline.
    source_before: str = paths.source_adr.read_text(encoding="utf-8")

    # Result contains validation proof for one-source evidence generation.
    result: AdrMessyCanaryResult = AdrMessyCanaryRunner(paths=paths).run()

    assert paths.source_adr.read_text(encoding="utf-8") == source_before
    assert result.candidate_object["validation"]["source_mutated"] is False
    assert result.candidate_object["validation"]["exactly_one_source"] is True
    assert result.candidate_object["projection"]["generated"] is False
    assert not list(paths.target_dir.rglob("*.sqlite"))
    assert not list(paths.target_dir.rglob("*.db"))
    assert not list(paths.target_dir.rglob("*.projected.md"))


def test__AdrMessyCanaryRunner__run__writes_valid_stable_json_artifacts(tmp_path: Path) -> None:
    """Repeated canary generation is stable and writes JSON objects."""
    # Temp repo isolates deterministic evidence generation.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Paths identify copied canary input and output artifacts.
    paths: AdrMessyCanaryPaths = AdrMessyCanaryPaths(repo_root=repo_root)

    # First run is the deterministic evidence baseline.
    first: AdrMessyCanaryResult = AdrMessyCanaryRunner(paths=paths).run()
    # Second run must match for unchanged input evidence and source.
    second: AdrMessyCanaryResult = AdrMessyCanaryRunner(paths=paths).run()
    # Artifact paths are parsed to confirm JSON validity.
    artifact_paths: tuple[Path, ...] = (
        paths.manifest,
        paths.candidate_object,
        paths.conversion_evidence,
        paths.conflict_lossiness_report,
        paths.sidecar_provenance,
    )

    assert first == second
    artifact_path: Path
    for artifact_path in artifact_paths:
        assert isinstance(json.loads(artifact_path.read_text(encoding="utf-8")), dict)
