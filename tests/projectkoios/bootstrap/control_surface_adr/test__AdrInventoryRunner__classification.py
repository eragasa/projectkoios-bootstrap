from __future__ import annotations

import json
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr import AdrInventoryPaths, AdrInventoryResult, AdrInventoryRunner
from projectkoios.bootstrap.schema.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = REPO_ROOT / "docs" / "adr"


def copy_inventory_sources(repo_root: Path) -> None:
    """Copy ADR Markdown sources into an isolated fixture repository."""
    # Fixture source directory mirrors docs/adr without mutating real sources.
    target_source_dir: Path = repo_root / "docs" / "adr"
    target_source_dir.mkdir(parents=True)
    source_path: Path
    for source_path in sorted(SOURCE_DIR.glob("*.md")):
        # Each Markdown source is copied byte-for-byte for inventory tests.
        (target_source_dir / source_path.name).write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")


def test__AdrInventoryRunner__run__writes_review_only_manifest(tmp_path: Path) -> None:
    """Generate review-only inventory evidence with required markers."""
    # Temp repo isolates inventory evidence from repository sources.
    repo_root: Path = tmp_path / "repo"
    copy_inventory_sources(repo_root)
    # Paths direct the runner to copied ADR Markdown inputs.
    paths: AdrInventoryPaths = AdrInventoryPaths(repo_root=repo_root)

    # Result exposes generated evidence objects for artifact comparison.
    result: AdrInventoryResult = AdrInventoryRunner(paths=paths).run()
    # Manifest artifact records review-only authority boundaries.
    manifest: JsonObject = json.loads(paths.manifest.read_text(encoding="utf-8"))
    # Source inventory artifact records per-file classification evidence.
    source_inventory: JsonObject = json.loads(paths.source_inventory.read_text(encoding="utf-8"))
    # Summary artifact records aggregate candidate counts.
    classification_summary: JsonObject = json.loads(paths.classification_summary.read_text(encoding="utf-8"))

    assert manifest == result.manifest
    assert source_inventory == result.source_inventory
    assert classification_summary == result.classification_summary
    assert manifest["mode"] == "review-only inventory/classification"
    assert manifest["authority_change"] is False
    assert manifest["source_mutation_allowed"] is False
    assert manifest["schema_change_allowed"] is False
    assert manifest["database_authority"] is False
    assert source_inventory["inspected_count"] == len(list(SOURCE_DIR.glob("*.md")))
    assert classification_summary["review_only"] is True


def test__AdrInventoryRunner__run__records_required_per_file_fields(tmp_path: Path) -> None:
    """Every inspected source has required review fields."""
    # Temp repo isolates copied source inputs.
    repo_root: Path = tmp_path / "repo"
    copy_inventory_sources(repo_root)
    # Paths constrain inventory to copied docs/adr Markdown files.
    paths: AdrInventoryPaths = AdrInventoryPaths(repo_root=repo_root)

    # Inventory entries are inspected for required Phase 0 evidence fields.
    result: AdrInventoryResult = AdrInventoryRunner(paths=paths).run()
    # Required keys mirror the brief's per-file evidence contract.
    required_keys: set[str] = {
        "source_path",
        "source_hash",
        "file_kind",
        "source_title",
        "observed_status_text",
        "observed_status_casing",
        "normalized_status_candidate",
        "status_normalization_required",
        "parse_confidence",
        "warnings",
        "uncertainty_flags",
        "category_candidate",
        "disposition_candidate",
        "authority_effect",
        "owner_domain_review_flags",
        "automatic_conversion_eligibility_candidate",
        "exclusion_blocking_reasons",
        "review_only",
    }

    entry: JsonObject
    for entry in result.source_inventory["entries"]:
        assert required_keys.issubset(entry.keys())
        assert entry["review_only"] is True
        assert entry["authority_effect"] in {
            "none",
            "candidate",
            "proposed_authority",
            "accepted_authority",
            "excluded",
            "domain_review_required",
        }


def test__AdrInventoryRunner__run__classifies_control_and_status_evidence(tmp_path: Path) -> None:
    """Classify index/control files separately and preserve status evidence."""
    # Temp repo uses tiny fixtures to exercise control-surface behavior.
    repo_root: Path = tmp_path / "repo"
    # Source directory holds minimal index and ADR fixtures.
    source_dir: Path = repo_root / "docs" / "adr"
    source_dir.mkdir(parents=True)
    (source_dir / "README.md").write_text("# ADR index\n\nIndex text.\n", encoding="utf-8")
    (source_dir / "adr.sample.draft.md").write_text(
        "# ADR 20260711.000000Z: Sample\n\n## Status\n\nDraft\n\n## Context\n\nExample.\n",
        encoding="utf-8",
    )
    # Paths point the runner at the tiny fixture corpus.
    paths: AdrInventoryPaths = AdrInventoryPaths(repo_root=repo_root)

    # Entries are keyed by source path for direct assertions.
    result: AdrInventoryResult = AdrInventoryRunner(paths=paths).run()
    # Entry lookup lets the test compare control and ADR candidates directly.
    entries: dict[str, JsonObject] = {
        str(entry["source_path"]): entry for entry in result.source_inventory["entries"]
    }

    assert entries["docs/adr/README.md"]["file_kind"] == "index_or_control_surface"
    assert entries["docs/adr/README.md"]["authority_effect"] == "none"
    assert entries["docs/adr/adr.sample.draft.md"]["observed_status_text"] == "Draft"
    assert entries["docs/adr/adr.sample.draft.md"]["observed_status_casing"] == "Draft"
    assert entries["docs/adr/adr.sample.draft.md"]["normalized_status_candidate"] == "draft"
    assert entries["docs/adr/adr.sample.draft.md"]["status_normalization_required"] is True


def test__AdrInventoryRunner__run__is_stable_and_does_not_create_database(tmp_path: Path) -> None:
    """Repeated generation is stable and creates no mutable DB files."""
    # Temp repo isolates copied ADR corpus and generated evidence.
    repo_root: Path = tmp_path / "repo"
    copy_inventory_sources(repo_root)
    # Paths identify copied sources and review-only evidence directory.
    paths: AdrInventoryPaths = AdrInventoryPaths(repo_root=repo_root)
    # Source bytes before generation prove non-mutation after repeated runs.
    before_sources: dict[str, str] = {
        path.name: path.read_text(encoding="utf-8") for path in sorted(paths.source_dir.glob("*.md"))
    }

    # First run is the deterministic baseline.
    first: AdrInventoryResult = AdrInventoryRunner(paths=paths).run()
    # Second run must match the baseline for unchanged inputs.
    second: AdrInventoryResult = AdrInventoryRunner(paths=paths).run()
    # Source bytes after generation must match the copied baseline.
    after_sources: dict[str, str] = {
        path.name: path.read_text(encoding="utf-8") for path in sorted(paths.source_dir.glob("*.md"))
    }

    assert first == second
    assert before_sources == after_sources
    assert not list(paths.target_dir.rglob("*.sqlite"))
    assert not list(paths.target_dir.rglob("*.db"))
