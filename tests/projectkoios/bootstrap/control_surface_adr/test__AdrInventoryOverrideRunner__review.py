from __future__ import annotations

import json
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr import (
    AdrInventoryOverridePaths,
    AdrInventoryOverrideResult,
    AdrInventoryOverrideRunner,
)
from projectkoios.bootstrap.control_surface.documents import DocumentRecord
from projectkoios.bootstrap.schema.models import JsonObject


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_INVENTORY = REPO_ROOT / "dev" / "adr-json-authority-inventory-classification-slice-0" / "source-inventory.json"


def write_source_inventory(repo_root: Path, entries: list[JsonObject]) -> Path:
    """Write a minimal Slice 0 source inventory fixture."""
    # Source inventory path mirrors the accepted Slice 0 evidence location.
    source_inventory: Path = repo_root / "dev" / "adr-json-authority-inventory-classification-slice-0" / "source-inventory.json"
    source_inventory.parent.mkdir(parents=True)
    # Payload is sufficient for the Slice 1 override runner contract.
    payload: JsonObject = {
        "slice_name": "adr-json-authority-inventory-classification-slice-0",
        "mode": "review-only inventory/classification",
        "inspected_count": len(entries),
        "entries": entries,
    }
    source_inventory.write_text(DocumentRecord.canonical_payload_text(payload), encoding="utf-8")
    return source_inventory


def entry(
    source_path: str,
    category: str = "template_schema_contract",
    disposition: str = "json_authority_candidate",
    authority_effect: str = "proposed_authority",
    auto: bool = True,
) -> JsonObject:
    """Build one minimal Slice 0 inventory entry."""
    return {
        "source_path": source_path,
        "source_hash": f"hash-{source_path}",
        "category_candidate": category,
        "disposition_candidate": disposition,
        "authority_effect": authority_effect,
        "owner_domain_review_flags": {
            "owner_review_required": False,
            "domain_review_required": False,
            "manual_review_required": False,
        },
        "automatic_conversion_eligibility_candidate": auto,
        "exclusion_blocking_reasons": [],
    }


def test__AdrInventoryOverrideRunner__run__downgrades_authority_forward_labels(tmp_path: Path) -> None:
    """Review-only overrides downgrade proposed authority to candidate."""
    # Temp repo contains a minimal accepted Slice 0 inventory fixture.
    repo_root: Path = tmp_path / "repo"
    write_source_inventory(repo_root, [entry("docs/adr/adr.json-schemas.draft.md")])
    # Paths target the temp source inventory and output evidence directory.
    paths: AdrInventoryOverridePaths = AdrInventoryOverridePaths(repo_root=repo_root)

    # Result exposes reviewed inventory and manifest evidence.
    result: AdrInventoryOverrideResult = AdrInventoryOverrideRunner(paths=paths).run()
    # Decision is the single explicit keep/override record.
    decision: JsonObject = result.reviewed_inventory["entries"][0]

    assert decision["candidate_only"] is True
    assert decision["authority_change"] is False
    assert decision["source_mutation"] is False
    assert decision["original"]["authority_effect"] == "proposed_authority"
    assert decision["reviewed"]["authority_effect"] == "candidate"
    assert decision["reviewed"]["disposition_candidate"] == "json_authority_candidate"
    assert result.manifest["conversion_performed"] is False
    assert result.manifest["schema_change_allowed"] is False


def test__AdrInventoryOverrideRunner__run__applies_domain_and_provenance_recommendations(tmp_path: Path) -> None:
    """Apply KOIOS domain-review and source/provenance override groups."""
    # Temp repo contains watchpoint examples from KOIOS recommendations.
    repo_root: Path = tmp_path / "repo"
    write_source_inventory(
        repo_root,
        [
            entry("docs/adr/adr.ui-core.draft.md"),
            entry("docs/adr/adr.adr-lifecycle.draft.md"),
        ],
    )
    # Paths target the temp source inventory and output evidence directory.
    paths: AdrInventoryOverridePaths = AdrInventoryOverridePaths(repo_root=repo_root)

    # Decisions are keyed by source path for direct assertions.
    result: AdrInventoryOverrideResult = AdrInventoryOverrideRunner(paths=paths).run()
    # Decision lookup lets the test compare domain and provenance rules.
    decisions: dict[str, JsonObject] = {
        str(decision["source_path"]): decision for decision in result.overrides["decisions"]
    }

    assert decisions["docs/adr/adr.ui-core.draft.md"]["reviewed"]["disposition_candidate"] == "domain_review_required"
    assert decisions["docs/adr/adr.ui-core.draft.md"]["reviewed"]["authority_effect"] == "domain_review_required"
    assert decisions["docs/adr/adr.ui-core.draft.md"]["reviewed"]["automatic_conversion_eligibility_candidate"] is False
    assert decisions["docs/adr/adr.adr-lifecycle.draft.md"]["reviewed"]["disposition_candidate"] == "source_only_provenance_candidate"
    assert decisions["docs/adr/adr.adr-lifecycle.draft.md"]["reviewed"]["automatic_conversion_eligibility_candidate"] is False


def test__AdrInventoryOverrideRunner__run__recommends_schema_base_messy_canary(tmp_path: Path) -> None:
    """Review summary names schema-base as the primary messy canary."""
    # Temp repo contains the KOIOS primary messy canary candidate.
    repo_root: Path = tmp_path / "repo"
    write_source_inventory(
        repo_root,
        [entry("docs/adr/adr.schema-base.md", disposition="manual_review_required", authority_effect="candidate", auto=False)],
    )
    # Paths target the temp source inventory and output evidence directory.
    paths: AdrInventoryOverridePaths = AdrInventoryOverridePaths(repo_root=repo_root)

    # Summary includes the ranked messy canary recommendations.
    result: AdrInventoryOverrideResult = AdrInventoryOverrideRunner(paths=paths).run()
    # Primary recommendation should match KOIOS's schema-base guidance.
    primary: JsonObject = result.review_summary["messy_canary_recommendations"][0]

    assert primary["source_path"] == "docs/adr/adr.schema-base.md"
    assert primary["recommendation"] == "primary_messy_canary_candidate"
    assert primary["candidate_only"] is True


def test__AdrInventoryOverrideRunner__run__is_stable_and_writes_valid_artifacts(tmp_path: Path) -> None:
    """Repeated generation is stable and creates no mutable DB files."""
    # Temp repo uses the real Slice 0 source inventory as fixture input.
    repo_root: Path = tmp_path / "repo"
    # Target inventory is the copied accepted Slice 0 evidence fixture.
    target_inventory: Path = repo_root / "dev" / "adr-json-authority-inventory-classification-slice-0" / "source-inventory.json"
    target_inventory.parent.mkdir(parents=True)
    target_inventory.write_text(SOURCE_INVENTORY.read_text(encoding="utf-8"), encoding="utf-8")
    # Paths target copied Slice 0 evidence and generated Slice 1 evidence.
    paths: AdrInventoryOverridePaths = AdrInventoryOverridePaths(repo_root=repo_root)

    # First run is the deterministic baseline.
    first: AdrInventoryOverrideResult = AdrInventoryOverrideRunner(paths=paths).run()
    # Second run must match for unchanged input evidence.
    second: AdrInventoryOverrideResult = AdrInventoryOverrideRunner(paths=paths).run()
    # Artifact paths are parsed to prove valid JSON was written.
    artifact_paths: tuple[Path, ...] = (paths.manifest, paths.reviewed_inventory, paths.overrides, paths.review_summary)

    assert first == second
    artifact_path: Path
    for artifact_path in artifact_paths:
        assert isinstance(json.loads(artifact_path.read_text(encoding="utf-8")), dict)
    assert not list(paths.target_dir.rglob("*.sqlite"))
    assert not list(paths.target_dir.rglob("*.db"))
