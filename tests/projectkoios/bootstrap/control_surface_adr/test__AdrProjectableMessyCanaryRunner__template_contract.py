from __future__ import annotations

import json
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr import (
    AdrProjectableMessyCanaryPaths,
    AdrProjectableMessyCanaryResult,
    AdrProjectableMessyCanaryRunner,
)
from projectkoios.bootstrap.schema.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_ADR = REPO_ROOT / "docs" / "adr" / "adr.adr-template-contract.md"
REVIEWED_INVENTORY = REPO_ROOT / "dev" / "adr-json-authority-inventory-review-overrides-slice-1" / "reviewed-inventory.json"
SLICE_2_ACCEPTANCE = REPO_ROOT / "docs" / "reviews" / "hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md"


def copy_canary_inputs(repo_root: Path) -> None:
    """Copy exact projectable messy canary source and required input evidence."""
    # Source target mirrors the repository ADR path for the one-source canary.
    source_target: Path = repo_root / "docs" / "adr" / "adr.adr-template-contract.md"
    source_target.parent.mkdir(parents=True)
    source_target.write_text(SOURCE_ADR.read_text(encoding="utf-8"), encoding="utf-8")
    # Review target mirrors the required Slice 1 reviewed inventory input path.
    review_target_dir: Path = repo_root / "dev" / "adr-json-authority-inventory-review-overrides-slice-1"
    review_target_dir.mkdir(parents=True)
    (review_target_dir / "reviewed-inventory.json").write_text(REVIEWED_INVENTORY.read_text(encoding="utf-8"), encoding="utf-8")
    # Slice 2 acceptance is preserved as input provenance/watchpoint evidence.
    acceptance_target: Path = repo_root / "docs" / "reviews" / SLICE_2_ACCEPTANCE.name
    acceptance_target.parent.mkdir(parents=True)
    acceptance_target.write_text(SLICE_2_ACCEPTANCE.read_text(encoding="utf-8"), encoding="utf-8")


def test__AdrProjectableMessyCanaryRunner__run__preserves_status_casing_and_review_blockers(tmp_path: Path) -> None:
    """Projectable canary preserves Accepted separately from normalized candidate."""
    # Temp repo isolates source and generated evidence.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Local value keeps this canary step explicit for validation.
    paths: AdrProjectableMessyCanaryPaths = AdrProjectableMessyCanaryPaths(repo_root=repo_root)

    # Result exposes candidate and conflict evidence for assertions.
    result: AdrProjectableMessyCanaryResult = AdrProjectableMessyCanaryRunner(paths=paths).run()
    # Local value keeps this canary step explicit for validation.
    candidate: JsonObject = result.candidate_object

    assert candidate["source_path"] == "docs/adr/adr.adr-template-contract.md"
    assert candidate["content_candidate"]["status"] == "Accepted"
    assert candidate["content_candidate"]["observed_status_text"] == "Accepted"
    assert candidate["content_candidate"]["normalized_status_candidate"] == "accepted"
    assert candidate["content_candidate"]["normalization_requires_review"] is True
    assert "Workflow-bound ADRs can render optional gate fields without losing schema consistency." in candidate[
        "content_candidate"
    ]["acceptance_criteria"]
    assert result.conflict_lossiness_report["template_schema_contract_ambiguity"] is True
    assert result.conflict_lossiness_report["manual_review_required"] is True
    assert result.conflict_lossiness_report["blocked_from_authority_promotion"] is True
    assert result.conflict_lossiness_report["outcome"] == "projectable_candidate_blocked_pending_template_contract_and_status_review"


def test__AdrProjectableMessyCanaryRunner__run__generates_projection_and_parseback_without_status_normalization(
    tmp_path: Path,
) -> None:
    """Generated projection lives under dev evidence and parse-back preserves status casing."""
    # Temp repo isolates projection evidence from repository files.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Local value keeps this canary step explicit for validation.
    paths: AdrProjectableMessyCanaryPaths = AdrProjectableMessyCanaryPaths(repo_root=repo_root)

    # Projection and parse-back evidence are generated from the candidate only.
    result: AdrProjectableMessyCanaryResult = AdrProjectableMessyCanaryRunner(paths=paths).run()
    # Local value keeps this canary step explicit for validation.
    parseback: JsonObject = result.projection_parseback_evidence

    assert paths.generated_projection.exists()
    assert "GENERATED SLICE 3 PROJECTION EVIDENCE" in paths.generated_projection.read_text(encoding="utf-8")
    assert result.candidate_object["projection"]["generated"] is True
    assert result.candidate_object["projection"]["path"].startswith(
        "dev/adr-json-authority-projectable-messy-canary-slice-3/"
    )
    assert parseback["parseback_source"] == "generated_projection_only"
    assert parseback["hand_authored_source_parsed_as_replacement"] is False
    assert parseback["semantic_equal_for_candidate_fields"] is True
    assert parseback["parseback_status_text"] == "Accepted"
    assert parseback["status_casing_preserved_in_projection_record"] is True
    assert parseback["status_normalized_by_projection_or_parseback"] is False
    assert parseback["projection_resolves_review_blockers"] is False


def test__AdrProjectableMessyCanaryRunner__run__preserves_sidecar_reviewed_inventory_and_source_non_mutation(
    tmp_path: Path,
) -> None:
    """Preserve Slice 1 reviewed values, routing sidecar, and source non-mutation proof."""
    # Temp repo isolates source mutation proof.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Local value keeps this canary step explicit for validation.
    paths: AdrProjectableMessyCanaryPaths = AdrProjectableMessyCanaryPaths(repo_root=repo_root)
    # Local value keeps this canary step explicit for validation.
    source_before: str = paths.source_adr.read_text(encoding="utf-8")

    # Sidecar records review blockers outside ADR content candidate.
    result: AdrProjectableMessyCanaryResult = AdrProjectableMessyCanaryRunner(paths=paths).run()
    # Local value keeps this canary step explicit for validation.
    sidecar: JsonObject = result.sidecar_provenance

    assert paths.source_adr.read_text(encoding="utf-8") == source_before
    assert result.candidate_object["validation"]["source_mutated"] is False
    assert result.candidate_object["validation"]["exactly_one_source"] is True
    assert sidecar["source_title"] == "Canonical ADR proposal template"
    assert sidecar["observed_source_status_text"] == "Accepted"
    assert sidecar["reviewed_inventory_reference"]["reviewed_category"] == "template_schema_contract"
    assert sidecar["reviewed_inventory_reference"]["reviewed_disposition"] == "manual_review_required"
    assert sidecar["reviewed_inventory_reference"]["automatic_conversion_eligibility_candidate"] is False
    assert sidecar["routing_preserved_outside_content_candidate"]["owner"] == "Athena"
    assert not list(paths.target_dir.rglob("*.sqlite"))
    assert not list(paths.target_dir.rglob("*.db"))


def test__AdrProjectableMessyCanaryRunner__run__writes_valid_stable_json_artifacts(tmp_path: Path) -> None:
    """Repeated canary generation is stable and writes valid JSON artifacts."""
    # Temp repo isolates deterministic evidence generation.
    repo_root: Path = tmp_path / "repo"
    copy_canary_inputs(repo_root)
    # Local value keeps this canary step explicit for validation.
    paths: AdrProjectableMessyCanaryPaths = AdrProjectableMessyCanaryPaths(repo_root=repo_root)

    # First run is the deterministic evidence baseline; second run must match.
    first: AdrProjectableMessyCanaryResult = AdrProjectableMessyCanaryRunner(paths=paths).run()
    # Local value keeps this canary step explicit for validation.
    second: AdrProjectableMessyCanaryResult = AdrProjectableMessyCanaryRunner(paths=paths).run()
    # Local value keeps this canary step explicit for validation.
    artifact_paths: tuple[Path, ...] = (
        paths.manifest,
        paths.candidate_object,
        paths.projection_parseback_evidence,
        paths.conversion_evidence,
        paths.conflict_lossiness_report,
        paths.sidecar_provenance,
    )

    assert first == second
    artifact_path: Path
    for artifact_path in artifact_paths:
        assert isinstance(json.loads(artifact_path.read_text(encoding="utf-8")), dict)
