from __future__ import annotations

import json
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr import AdrCorpusDryRunPaths, AdrCorpusDryRunResult, AdrCorpusDryRunRunner
from projectkoios.bootstrap.schema.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
SELECTED_SOURCES = (
    "docs/adr/adr.json-schemas.draft.md",
    "docs/adr/adr.petrinet.20260705.132740Z.md",
    "docs/adr/adr.adr-template-contract.md",
    "docs/adr/adr.schema-base.md",
    "docs/adr/adr.adr-lifecycle.draft.md",
    "docs/adr/README.md",
)
REVIEWED_INVENTORY = REPO_ROOT / "dev" / "adr-json-authority-inventory-review-overrides-slice-1" / "reviewed-inventory.json"


def copy_dry_run_inputs(repo_root: Path) -> None:
    """Copy exact Slice 4 selected sources and reviewed inventory evidence."""
    # Selected source path is copied into a temp repository mirror.
    source_path: str
    for source_path in SELECTED_SOURCES:
        # Source target mirrors the repository-selected source path.
        source_target: Path = repo_root / source_path
        source_target.parent.mkdir(parents=True, exist_ok=True)
        source_target.write_text((REPO_ROOT / source_path).read_text(encoding="utf-8"), encoding="utf-8")
    # Review target mirrors the required Slice 1 reviewed inventory input path.
    review_target_dir: Path = repo_root / "dev" / "adr-json-authority-inventory-review-overrides-slice-1"
    review_target_dir.mkdir(parents=True)
    (review_target_dir / "reviewed-inventory.json").write_text(REVIEWED_INVENTORY.read_text(encoding="utf-8"), encoding="utf-8")


def test__AdrCorpusDryRunRunner__run__uses_exact_six_source_subset(tmp_path: Path) -> None:
    """Dry run freezes exact six-source subset and does not add extra ADRs."""
    # Temp repo isolates dry-run evidence from repository files.
    repo_root: Path = tmp_path / "repo"
    copy_dry_run_inputs(repo_root)
    # Paths point the runner at copied Slice 4 inputs.
    paths: AdrCorpusDryRunPaths = AdrCorpusDryRunPaths(repo_root=repo_root)

    # Result exposes selected sources and per-source rows for assertions.
    result: AdrCorpusDryRunResult = AdrCorpusDryRunRunner(paths=paths).run()

    assert result.selected_sources["selected_entry_count"] == 6
    assert result.selected_sources["selected_sources"] == list(SELECTED_SOURCES)
    assert result.selected_sources["no_extra_sources"] is True
    assert result.per_source_results["selected_entry_count"] == 6
    assert [row["source_path"] for row in result.per_source_results["results"]] == list(SELECTED_SOURCES)


def test__AdrCorpusDryRunRunner__run__preserves_slice2_slice3_and_skip_watchpoints(tmp_path: Path) -> None:
    """Dry-run rows preserve missing status, Slice 3 wrapped list, source-only, and README skip behavior."""
    # Temp repo isolates generated evidence.
    repo_root: Path = tmp_path / "repo"
    copy_dry_run_inputs(repo_root)
    # Paths identify copied inputs and output artifacts.
    paths: AdrCorpusDryRunPaths = AdrCorpusDryRunPaths(repo_root=repo_root)

    # Result contains all six per-source outcome rows.
    result: AdrCorpusDryRunResult = AdrCorpusDryRunRunner(paths=paths).run()
    # Rows are keyed by source path for targeted assertions.
    rows: dict[str, JsonObject] = {row["source_path"]: row for row in result.per_source_results["results"]}

    assert rows["docs/adr/adr.schema-base.md"]["observed_status_text"] is None
    assert rows["docs/adr/adr.schema-base.md"]["final_outcome"] == "blocked_missing_status_pending_review"
    assert rows["docs/adr/adr.schema-base.md"]["projection_status"] == "blocked_missing_status"
    assert rows["docs/adr/adr.adr-template-contract.md"]["observed_status_text"] == "Accepted"
    assert rows["docs/adr/adr.adr-template-contract.md"]["normalized_status_candidate"] == "accepted"
    assert rows["docs/adr/adr.adr-template-contract.md"]["status_casing_or_text_would_normalize"] is True
    assert rows["docs/adr/adr.adr-lifecycle.draft.md"]["entry_type"] == "source_provenance_draft"
    assert rows["docs/adr/adr.adr-lifecycle.draft.md"]["candidate_object_path"] is None
    assert rows["docs/adr/README.md"]["entry_type"] == "index_control_surface"
    assert rows["docs/adr/README.md"]["attempted_candidate_conversion"] is False

    # Candidate object preserves Slice 3 wrapped-list continuation in multi-file mode.
    candidate_path: Path = repo_root / rows["docs/adr/adr.adr-template-contract.md"]["candidate_object_path"]
    # Candidate object is valid JSON evidence.
    candidate: JsonObject = json.loads(candidate_path.read_text(encoding="utf-8"))
    assert "Workflow-bound ADRs can render optional gate fields without losing schema consistency." in candidate[
        "content_candidate"
    ]["acceptance_criteria"]
    assert rows["docs/adr/adr.json-schemas.draft.md"]["source_to_candidate_complete"] is False
    assert "context" in rows["docs/adr/adr.json-schemas.draft.md"]["omitted_or_sidecar_preserved_source_sections"]
    assert "definitions" in rows["docs/adr/adr.json-schemas.draft.md"]["omitted_or_sidecar_preserved_source_sections"]


def test__AdrCorpusDryRunRunner__run__aggregates_counts_and_projection_parsebacks(tmp_path: Path) -> None:
    """Aggregate counts match the six per-source records and generated projection parsebacks."""
    # Temp repo isolates aggregate evidence.
    repo_root: Path = tmp_path / "repo"
    copy_dry_run_inputs(repo_root)
    # Paths identify copied inputs and output artifacts.
    paths: AdrCorpusDryRunPaths = AdrCorpusDryRunPaths(repo_root=repo_root)

    # Result manifest carries aggregate counts derived from rows.
    result: AdrCorpusDryRunResult = AdrCorpusDryRunRunner(paths=paths).run()
    # Counts summarize candidate, blocked, skipped, and projection outcomes.
    counts: JsonObject = result.manifest["aggregate_counts"]

    assert counts["selected_entry_count"] == 6
    assert counts["generated_candidate_objects"] == 4
    assert counts["generated_projections"] == 3
    assert counts["parseback_comparisons_run"] == 3
    assert counts["missing_status_findings"] == 2
    assert counts["status_casing_normalization_sensitive_findings"] == 1
    assert counts["source_only_provenance_blockers"] == 1
    assert counts["index_control_surface_exclusions"] == 1
    assert counts["manual_review_blockers"] == 4
    assert counts["omitted_sidecar_preserved_source_sections_total"] > 0
    assert counts["by_omitted_sidecar_preserved_source_section"]["context"] >= 1
    assert result.projection_parseback_report["all_parsebacks_generated_projection_only"] is True
    assert result.projection_parseback_report["all_semantic_equal_for_candidate_fields"] is True


def test__AdrCorpusDryRunRunner__run__does_not_mutate_sources_or_create_db_and_writes_valid_json(tmp_path: Path) -> None:
    """Dry run leaves sources unchanged, creates no DB files, and writes valid JSON evidence."""
    # Temp repo isolates source mutation proof.
    repo_root: Path = tmp_path / "repo"
    copy_dry_run_inputs(repo_root)
    # Source text before generation is the non-mutation baseline.
    source_before: dict[str, str] = {
        source_path: (repo_root / source_path).read_text(encoding="utf-8") for source_path in SELECTED_SOURCES
    }
    # Paths identify copied inputs and output artifacts.
    paths: AdrCorpusDryRunPaths = AdrCorpusDryRunPaths(repo_root=repo_root)

    # Running the dry run writes all evidence artifacts.
    AdrCorpusDryRunRunner(paths=paths).run()
    # Artifact paths cover required root-level JSON evidence.
    artifact_paths: tuple[Path, ...] = (
        paths.manifest,
        paths.selected_sources,
        paths.per_source_results,
        paths.conflict_lossiness_report,
        paths.projection_parseback_report,
        paths.skipped_or_blocked_sources,
    )

    assert {source_path: (repo_root / source_path).read_text(encoding="utf-8") for source_path in SELECTED_SOURCES} == source_before
    assert not list(paths.target_dir.rglob("*.sqlite"))
    assert not list(paths.target_dir.rglob("*.db"))
    # Projection evidence remains under the Slice 4 dev path.
    assert all(str(path).startswith(str(paths.generated_projections_dir)) for path in paths.generated_projections_dir.glob("*.md"))
    # JSON artifacts can be parsed as JSON objects.
    artifact_path: Path
    for artifact_path in artifact_paths:
        assert isinstance(json.loads(artifact_path.read_text(encoding="utf-8")), dict)
