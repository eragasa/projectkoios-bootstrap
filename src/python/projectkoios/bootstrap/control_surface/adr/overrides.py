from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.documents import DocumentRecord
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrInventoryOverridePaths:
    """Filesystem paths for review-only ADR inventory override evidence."""

    repo_root: Path

    @property
    def source_inventory(self) -> Path:
        """Return Slice 0 source inventory path."""
        return self.repo_root / "dev" / "adr-json-authority-inventory-classification-slice-0" / "source-inventory.json"

    @property
    def target_dir(self) -> Path:
        """Return Slice 1 override evidence directory."""
        return self.repo_root / "dev" / "adr-json-authority-inventory-review-overrides-slice-1"

    @property
    def manifest(self) -> Path:
        """Return manifest path."""
        return self.target_dir / "manifest.json"

    @property
    def reviewed_inventory(self) -> Path:
        """Return reviewed inventory path."""
        return self.target_dir / "reviewed-inventory.json"

    @property
    def overrides(self) -> Path:
        """Return overrides path."""
        return self.target_dir / "overrides.json"

    @property
    def review_summary(self) -> Path:
        """Return review summary path."""
        return self.target_dir / "review-summary.json"


@dataclass(frozen=True, slots=True)
class AdrInventoryOverrideResult:
    """Generated review-only override evidence."""

    manifest: JsonObject
    reviewed_inventory: JsonObject
    overrides: JsonObject
    review_summary: JsonObject


@dataclass(frozen=True, slots=True)
class AdrInventoryOverrideRunner:
    """Apply review-only candidate overrides to Slice 0 ADR inventory."""

    paths: AdrInventoryOverridePaths
    generated_at: str = "20260711.142700Z"

    def run(self) -> AdrInventoryOverrideResult:
        """Generate deterministic review-only override evidence."""
        self.paths.target_dir.mkdir(parents=True, exist_ok=True)
        # Source inventory is accepted Slice 0 evidence and is only read.
        source_inventory: JsonObject = json.loads(self.paths.source_inventory.read_text(encoding="utf-8"))
        # Entries are reviewed in source order from the deterministic inventory.
        entries: list[JsonObject] = list(source_inventory["entries"])
        # Review decisions include explicit keep and override records.
        decisions: list[JsonObject] = [self.review_entry(entry) for entry in entries]
        # Reviewed inventory presents reviewed values beside original evidence.
        reviewed_inventory: JsonObject = self.build_reviewed_inventory(decisions)
        # Overrides artifact lists every explicit keep/override decision.
        overrides: JsonObject = self.build_overrides(decisions)
        # Summary highlights changed labels and messy canary recommendation.
        review_summary: JsonObject = self.build_review_summary(decisions)
        # Manifest indexes artifacts, hashes, and review-only boundaries.
        manifest: JsonObject = self.build_manifest(source_inventory, reviewed_inventory, overrides, review_summary)
        self.write_artifacts(manifest, reviewed_inventory, overrides, review_summary)
        return AdrInventoryOverrideResult(
            manifest=manifest,
            reviewed_inventory=reviewed_inventory,
            overrides=overrides,
            review_summary=review_summary,
        )

    def review_entry(self, entry: JsonObject) -> JsonObject:
        """Return one explicit keep/override decision for a source entry."""
        # Source path selects deterministic KOIOS/HERMES override rules.
        source_path: str = str(entry["source_path"])
        # Original values are preserved for review comparison.
        original: JsonObject = self.original_values(entry)
        # Reviewed values start from original then become safer candidates.
        reviewed: JsonObject = dict(original)
        # Rationale records why a value was kept or changed.
        rationale: list[str] = []
        # Source basis identifies deterministic rule or KOIOS recommendation.
        source_basis: list[str] = []

        if original["authority_effect"] == "proposed_authority":
            reviewed["authority_effect"] = "candidate"
            rationale.append("proposed_authority downgraded to candidate for review-only planning")
            source_basis.append("KOIOS global override rule 3")

        if original["disposition_candidate"] == "json_authority_candidate":
            rationale.append("json_authority_candidate retained only as candidate conversion-planning evidence")
            source_basis.append("HERMES authority-forward label watchpoint")

        self.apply_specific_recommendations(source_path, reviewed, rationale, source_basis)
        self.apply_review_flags(reviewed)
        # Changed flag compares reviewed candidate values against Slice 0 values.
        changed: bool = reviewed != original
        if not rationale:
            rationale.append("explicit keep decision; value remains candidate-only review evidence")
            source_basis.append("deterministic keep rule")
        return {
            "source_path": source_path,
            "source_hash": entry["source_hash"],
            "original": original,
            "reviewed": reviewed,
            "changed": changed,
            "rationale": rationale,
            "source_basis": sorted(set(source_basis)),
            "candidate_only": True,
            "authority_change": False,
            "source_mutation": False,
        }

    def original_values(self, entry: JsonObject) -> JsonObject:
        """Return original Slice 0 values that Slice 1 reviews."""
        return {
            "category_candidate": entry["category_candidate"],
            "disposition_candidate": entry["disposition_candidate"],
            "authority_effect": entry["authority_effect"],
            "owner_domain_review_flags": entry["owner_domain_review_flags"],
            "automatic_conversion_eligibility_candidate": entry["automatic_conversion_eligibility_candidate"],
            "exclusion_blocking_reasons": entry["exclusion_blocking_reasons"],
        }

    def apply_specific_recommendations(
        self,
        source_path: str,
        reviewed: JsonObject,
        rationale: list[str],
        source_basis: list[str],
    ) -> None:
        """Apply KOIOS per-file and group recommendations."""
        if source_path in self.domain_review_paths():
            reviewed["category_candidate"] = "product_future_system_draft"
            reviewed["disposition_candidate"] = "domain_review_required"
            reviewed["authority_effect"] = "domain_review_required"
            reviewed["automatic_conversion_eligibility_candidate"] = False
            reviewed["exclusion_blocking_reasons"] = self.reasons(reviewed, "domain_review_required")
            rationale.append("domain/product owner review required before conversion planning")
            source_basis.append("KOIOS section B domain/product review recommendation")
        if source_path in self.source_provenance_paths():
            reviewed["disposition_candidate"] = "source_only_provenance_candidate"
            reviewed["authority_effect"] = "candidate"
            reviewed["automatic_conversion_eligibility_candidate"] = False
            reviewed["exclusion_blocking_reasons"] = self.reasons(reviewed, "source_provenance_review_required")
            rationale.append("source/provenance draft should not auto-promote to JSON authority planning")
            source_basis.append("KOIOS section C source/provenance recommendation")
        if source_path in self.manual_review_overrides():
            # Manual review overrides are targeted category/disposition corrections.
            override: JsonObject = self.manual_review_overrides()[source_path]
            reviewed.update(override)
            reviewed["automatic_conversion_eligibility_candidate"] = False
            reviewed["exclusion_blocking_reasons"] = self.reasons(reviewed, "manual_review_required")
            rationale.append("mixed document category or status ambiguity requires manual review")
            source_basis.append("KOIOS sections A/E mixed-document recommendation")
        if source_path == "docs/adr/README.md":
            reviewed["authority_effect"] = "none"
            reviewed["automatic_conversion_eligibility_candidate"] = False
            reviewed["exclusion_blocking_reasons"] = self.reasons(reviewed, "index_or_control_surface")
            rationale.append("index/control surface is not an ADR record")
            source_basis.append("KOIOS section A index/control recommendation")

    def apply_review_flags(self, reviewed: JsonObject) -> None:
        """Update owner/domain review flags after overrides."""
        # Existing flags are copied before conservative overrides are added.
        flags: JsonObject = dict(reviewed["owner_domain_review_flags"])
        if reviewed["disposition_candidate"] in {"manual_review_required", "source_only_provenance_candidate"}:
            flags["manual_review_required"] = True
            flags["owner_review_required"] = True
        if reviewed["disposition_candidate"] == "domain_review_required":
            flags["manual_review_required"] = True
            flags["owner_review_required"] = True
            flags["domain_review_required"] = True
        reviewed["owner_domain_review_flags"] = flags

    def reasons(self, reviewed: JsonObject, reason: str) -> list[str]:
        """Return sorted blocking reasons with one required reason added."""
        # Blocking reasons stay explicit so auto-conversion exclusions are auditable.
        reasons: list[str] = list(reviewed.get("exclusion_blocking_reasons", []))
        reasons.append(reason)
        return sorted(set(reasons))

    def domain_review_paths(self) -> set[str]:
        """Return KOIOS domain/product review watchpoint paths."""
        return {
            "docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md",
            "docs/adr/adr.agent-windows-on-message-triggers.draft.md",
            "docs/adr/adr.ui-core.draft.md",
            "docs/adr/adr.workflow-ui.draft.md",
            "docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md",
        }

    def source_provenance_paths(self) -> set[str]:
        """Return KOIOS source/provenance draft paths."""
        return {
            "docs/adr/adr.adr-lifecycle.draft.md",
            "docs/adr/adr.adr-lifecycle-promotion-mechanics.md",
            "docs/adr/adr.adr-names.draft.md",
            "docs/adr/adr.adr-title-naming-convention.draft.md",
            "docs/adr/adr.adr-filename-naming-convention.draft.md",
        }

    def manual_review_overrides(self) -> dict[str, JsonObject]:
        """Return KOIOS mixed-document/manual-review override values."""
        return {
            "docs/adr/adr.schema-base.md": {
                "category_candidate": "template_schema_contract",
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.adr-template-contract.md": {
                "category_candidate": "template_schema_contract",
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md": {
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.unified-diff-review-surface.draft.md": {
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.json-database-for-adr-storage.draft.md": {
                "category_candidate": "architecture_blueprint",
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.json-authoritative-adr-store.draft.md": {
                "category_candidate": "current_decision",
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.control-surfaces-and-ownership-boundaries.draft.md": {
                "category_candidate": "policy_process",
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.idea-spike-adr-implementation-workflow.draft.md": {
                "category_candidate": "policy_process",
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.implementation.draft.md": {
                "category_candidate": "implementation_workflow_support",
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.implementation-brief-verification-method.draft.md": {
                "category_candidate": "implementation_workflow_support",
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.brainstorm-capture-and-incubator-template.draft.md": {
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.kernel.md": {
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.adr.md": {
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.templates.md": {
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
            "docs/adr/adr.templates-adr.md": {
                "disposition_candidate": "manual_review_required",
                "authority_effect": "candidate",
            },
        }

    def build_reviewed_inventory(self, decisions: list[JsonObject]) -> JsonObject:
        """Build reviewed inventory evidence."""
        return {
            "slice_name": "adr-json-authority-inventory-review-overrides-slice-1",
            "mode": "review-only inventory override evidence",
            "authority_change": False,
            "entries": decisions,
            "candidate_only": True,
        }

    def build_overrides(self, decisions: list[JsonObject]) -> JsonObject:
        """Build explicit keep/override decisions artifact."""
        return {
            "slice_name": "adr-json-authority-inventory-review-overrides-slice-1",
            "mode": "review-only explicit keep and override decisions",
            "decisions": decisions,
            "changed_count": sum(1 for decision in decisions if decision["changed"] is True),
            "unchanged_count": sum(1 for decision in decisions if decision["changed"] is False),
            "candidate_only": True,
            "authority_change": False,
        }

    def build_review_summary(self, decisions: list[JsonObject]) -> JsonObject:
        """Build aggregate review summary and messy canary recommendation."""
        # Reviewed values are aggregated separately from original Slice 0 labels.
        reviewed_values: list[JsonObject] = [decision["reviewed"] for decision in decisions]
        return {
            "slice_name": "adr-json-authority-inventory-review-overrides-slice-1",
            "mode": "review-only override summary",
            "total_reviewed": len(decisions),
            "changed_count": sum(1 for decision in decisions if decision["changed"] is True),
            "unchanged_count": sum(1 for decision in decisions if decision["changed"] is False),
            "reviewed_counts": {
                "by_authority_effect": self.count_by(reviewed_values, "authority_effect"),
                "by_disposition_candidate": self.count_by(reviewed_values, "disposition_candidate"),
                "by_category_candidate": self.count_by(reviewed_values, "category_candidate"),
            },
            "automatic_conversion_eligibility_candidate_count": sum(
                1 for value in reviewed_values if value["automatic_conversion_eligibility_candidate"] is True
            ),
            "messy_canary_recommendations": [
                {
                    "rank": 1,
                    "source_path": "docs/adr/adr.schema-base.md",
                    "recommendation": "primary_messy_canary_candidate",
                    "rationale": "missing status and schema/implementation contract ambiguity without broader product-domain implications",
                    "candidate_only": True,
                },
                {
                    "rank": 2,
                    "source_path": "docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md",
                    "recommendation": "alternate_messy_canary_candidate",
                    "rationale": "status casing preservation and domain/training review flags",
                    "candidate_only": True,
                },
            ],
            "candidate_only": True,
            "authority_change": False,
        }

    def count_by(self, values: list[JsonObject], key: str) -> JsonObject:
        """Count reviewed values by one string key."""
        # Counts are stable and sorted for deterministic review summaries.
        counts: dict[str, int] = {}
        value: JsonObject
        for value in values:
            # Label is the reviewed candidate value counted for summary output.
            label: str = str(value.get(key, "missing"))
            counts[label] = counts.get(label, 0) + 1
        return dict(sorted(counts.items()))

    def build_manifest(
        self,
        source_inventory: JsonObject,
        reviewed_inventory: JsonObject,
        overrides: JsonObject,
        review_summary: JsonObject,
    ) -> JsonObject:
        """Build review-only override manifest."""
        # Source inventory text hash records exact Slice 0 evidence input.
        source_inventory_hash: str = PilotManifestBuilder.hash_text(
            self.paths.source_inventory.read_text(encoding="utf-8")
        )
        return {
            "slice_name": "adr-json-authority-inventory-review-overrides-slice-1",
            "mode": "review-only inventory override evidence",
            "authority_change": False,
            "source_mutation_allowed": False,
            "schema_change_allowed": False,
            "conversion_performed": False,
            "database_authority": False,
            "generated_at": self.generated_at,
            "source_inventory": {
                "path": "dev/adr-json-authority-inventory-classification-slice-0/source-inventory.json",
                "sha256": source_inventory_hash,
                "entry_count": source_inventory["inspected_count"],
            },
            "source_refs": {
                "source_brief": "docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md",
                "koios_recommendations": "workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md",
                "hermes_decision": "docs/reviews/hermes-decision.20260711.142700_adr-json-authority-inventory-review-overrides-slice-1.md",
                "slice_0_acceptance": "docs/reviews/hermes-acceptance.20260711.142000_adr-json-authority-inventory-classification-slice-0.md",
            },
            "artifacts": {
                "manifest": "dev/adr-json-authority-inventory-review-overrides-slice-1/manifest.json",
                "reviewed_inventory": "dev/adr-json-authority-inventory-review-overrides-slice-1/reviewed-inventory.json",
                "overrides": "dev/adr-json-authority-inventory-review-overrides-slice-1/overrides.json",
                "review_summary": "dev/adr-json-authority-inventory-review-overrides-slice-1/review-summary.json",
            },
            "artifact_hashes": {
                "reviewed_inventory": DocumentRecord.payload_hash(reviewed_inventory),
                "overrides": DocumentRecord.payload_hash(overrides),
                "review_summary": DocumentRecord.payload_hash(review_summary),
            },
            "validation_command_summary": {
                "json_validity": "pending closeout validation",
                "source_schema_non_mutation": "pending closeout validation",
                "no_database_files": "pending closeout validation",
                "deterministic_generation": "canonical JSON with stable generated_at and deterministic rule set",
            },
            "candidate_only": True,
        }

    def write_artifacts(
        self,
        manifest: JsonObject,
        reviewed_inventory: JsonObject,
        overrides: JsonObject,
        review_summary: JsonObject,
    ) -> None:
        """Write deterministic review-only JSON artifacts."""
        self.paths.manifest.write_text(DocumentRecord.canonical_payload_text(manifest), encoding="utf-8")
        self.paths.reviewed_inventory.write_text(DocumentRecord.canonical_payload_text(reviewed_inventory), encoding="utf-8")
        self.paths.overrides.write_text(DocumentRecord.canonical_payload_text(overrides), encoding="utf-8")
        self.paths.review_summary.write_text(DocumentRecord.canonical_payload_text(review_summary), encoding="utf-8")


def run_adr_json_authority_inventory_overrides(repo_root: Path) -> AdrInventoryOverrideResult:
    """Run review-only ADR authority inventory override evidence generation."""
    return AdrInventoryOverrideRunner(paths=AdrInventoryOverridePaths(repo_root=repo_root)).run()
