from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re

from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.documents import DocumentRecord
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrMessyCanaryPaths:
    """Filesystem paths for the ADR JSON authority messy canary."""

    repo_root: Path

    @property
    def source_adr(self) -> Path:
        """Return the exact messy canary source path."""
        return self.repo_root / "docs" / "adr" / "adr.schema-base.md"

    @property
    def reviewed_inventory(self) -> Path:
        """Return Slice 1 reviewed inventory evidence path."""
        return self.repo_root / "dev" / "adr-json-authority-inventory-review-overrides-slice-1" / "reviewed-inventory.json"

    @property
    def review_summary(self) -> Path:
        """Return Slice 1 review summary evidence path."""
        return self.repo_root / "dev" / "adr-json-authority-inventory-review-overrides-slice-1" / "review-summary.json"

    @property
    def target_dir(self) -> Path:
        """Return Slice 2 messy canary evidence directory."""
        return self.repo_root / "dev" / "adr-json-authority-messy-canary-slice-2"

    @property
    def manifest(self) -> Path:
        """Return manifest path."""
        return self.target_dir / "manifest.json"

    @property
    def candidate_object(self) -> Path:
        """Return candidate object path."""
        return self.target_dir / "adr.schema-base.candidate-object.json"

    @property
    def conversion_evidence(self) -> Path:
        """Return conversion evidence path."""
        return self.target_dir / "conversion-evidence.json"

    @property
    def conflict_lossiness_report(self) -> Path:
        """Return conflict/lossiness report path."""
        return self.target_dir / "conflict-lossiness-report.json"

    @property
    def sidecar_provenance(self) -> Path:
        """Return sidecar provenance path."""
        return self.target_dir / "sidecar-provenance.json"


@dataclass(frozen=True, slots=True)
class AdrMessyCanaryResult:
    """Generated messy canary evidence result."""

    manifest: JsonObject
    candidate_object: JsonObject
    conversion_evidence: JsonObject
    conflict_lossiness_report: JsonObject
    sidecar_provenance: JsonObject


@dataclass(frozen=True, slots=True)
class AdrMessyCanaryRunner:
    """Generate evidence for the one-source missing-status ADR messy canary."""

    paths: AdrMessyCanaryPaths
    generated_at: str = "20260711.144200Z"

    def run(self) -> AdrMessyCanaryResult:
        """Generate deterministic messy canary evidence artifacts."""
        self.paths.target_dir.mkdir(parents=True, exist_ok=True)
        # Source text before generation is the non-mutation baseline.
        source_before: str = self.paths.source_adr.read_text(encoding="utf-8")
        # Source hash proves the exact canary source inspected.
        source_hash_before: str = PilotManifestBuilder.hash_text(source_before)
        # Reviewed entry carries Slice 1 candidate-only disposition evidence.
        reviewed_entry: JsonObject = self.reviewed_entry()
        # Source title is parseable even though lifecycle status is missing.
        title: str | None = self.parse_title(source_before)
        # Embedded metadata is preserved as sidecar/provenance, not authority.
        embedded_metadata: JsonObject | None = self.parse_embedded_metadata(source_before)
        # Conflict report records missing status and schema gap findings.
        conflict_lossiness_report: JsonObject = self.build_conflict_lossiness_report(
            source_hash_before=source_hash_before,
            reviewed_entry=reviewed_entry,
            embedded_metadata=embedded_metadata,
        )
        # Sidecar provenance keeps ambiguous source metadata outside content.
        sidecar_provenance: JsonObject = self.build_sidecar_provenance(
            source_hash=source_hash_before,
            title=title,
            embedded_metadata=embedded_metadata,
            reviewed_entry=reviewed_entry,
        )
        # Candidate object is evidence-only and intentionally incomplete.
        candidate_object: JsonObject = self.build_candidate_object(
            source_hash=source_hash_before,
            title=title,
            reviewed_entry=reviewed_entry,
            conflict_lossiness_report=conflict_lossiness_report,
            sidecar_provenance=sidecar_provenance,
        )
        # Conversion evidence summarizes the blocked-pending-review outcome.
        conversion_evidence: JsonObject = self.build_conversion_evidence(candidate_object, conflict_lossiness_report)
        # Source text after generation must be byte-for-byte identical.
        source_after: str = self.paths.source_adr.read_text(encoding="utf-8")
        # Source hash after generation is recorded as mutation proof.
        source_hash_after: str = PilotManifestBuilder.hash_text(source_after)
        if source_before != source_after:
            raise AssertionError("Messy canary source ADR was mutated")
        candidate_object["validation"]["source_hash_after"] = source_hash_after
        candidate_object["validation"]["source_mutated"] = source_hash_before != source_hash_after
        conversion_evidence["source_non_mutation_proof"]["source_hash_after"] = source_hash_after
        conversion_evidence["source_non_mutation_proof"]["source_mutated"] = source_hash_before != source_hash_after
        # Manifest indexes all evidence artifacts and hashes.
        manifest: JsonObject = self.build_manifest(
            candidate_object=candidate_object,
            conversion_evidence=conversion_evidence,
            conflict_lossiness_report=conflict_lossiness_report,
            sidecar_provenance=sidecar_provenance,
            source_hash=source_hash_before,
        )
        self.write_artifacts(manifest, candidate_object, conversion_evidence, conflict_lossiness_report, sidecar_provenance)
        return AdrMessyCanaryResult(
            manifest=manifest,
            candidate_object=candidate_object,
            conversion_evidence=conversion_evidence,
            conflict_lossiness_report=conflict_lossiness_report,
            sidecar_provenance=sidecar_provenance,
        )

    def reviewed_entry(self) -> JsonObject:
        """Return the Slice 1 reviewed entry for the exact canary source."""
        # Reviewed inventory is read-only input evidence.
        reviewed_inventory: JsonObject = json.loads(self.paths.reviewed_inventory.read_text(encoding="utf-8"))
        entry: JsonObject
        for entry in reviewed_inventory["entries"]:
            if entry["source_path"] == "docs/adr/adr.schema-base.md":
                return entry
        raise ValueError("Reviewed inventory missing docs/adr/adr.schema-base.md")

    def parse_title(self, source_text: str) -> str | None:
        """Parse source H1 title when available."""
        # H1 is parseable even when status is not present as Markdown status.
        match: re.Match[str] | None = re.search(r"^#\s+(?P<title>.+?)\s*$", source_text, flags=re.MULTILINE)
        if match is None:
            return None
        return match.group("title")

    def parse_embedded_metadata(self, source_text: str) -> JsonObject | None:
        """Parse the first fenced JSON block as source-side provenance."""
        # Embedded JSON is source evidence, not an authoritative ADR content record.
        match: re.Match[str] | None = re.search(r"```json\s*(?P<payload>.*?)\s*```", source_text, flags=re.DOTALL)
        if match is None:
            return None
        # Payload is preserved as ambiguous source metadata evidence.
        payload: object = json.loads(match.group("payload"))
        if not isinstance(payload, dict):
            return None
        return payload

    def build_conflict_lossiness_report(
        self,
        source_hash_before: str,
        reviewed_entry: JsonObject,
        embedded_metadata: JsonObject | None,
    ) -> JsonObject:
        """Build explicit missing-status and lossiness report."""
        # Embedded status is preserved but not promoted to observed Markdown status.
        embedded_status: object = None if embedded_metadata is None else embedded_metadata.get("status")
        return {
            "slice_name": "adr-json-authority-messy-canary-slice-2",
            "source_path": "docs/adr/adr.schema-base.md",
            "source_hash": source_hash_before,
            "outcome": "conversion_candidate_blocked_pending_review",
            "candidate_only": True,
            "authority_change": False,
            "missing_status": True,
            "observed_markdown_status": None,
            "embedded_metadata_status_preserved_as_sidecar": embedded_status,
            "normalized_status_candidate": None,
            "status_inference": "blocked; no status invented to satisfy schema",
            "schema_validation_without_invented_status": {
                "can_validate_against_current_adr_content_schema": False,
                "blocked_by": ["missing_observed_status", "schema_implementation_contract_ambiguity"],
            },
            "reviewed_inventory_values": reviewed_entry["reviewed"],
            "lossiness_findings": [
                "source uses schema-record metadata/content envelope rather than normal ADR schema payload",
                "Markdown Status section is absent and must remain missing in canary evidence",
                "embedded JSON status is preserved as provenance but not promoted into ADR lifecycle authority",
                "schema/implementation-contract ambiguity requires manual review before conversion",
            ],
            "requires_review": True,
            "blocked_from_authority_promotion": True,
        }

    def build_sidecar_provenance(
        self,
        source_hash: str,
        title: str | None,
        embedded_metadata: JsonObject | None,
        reviewed_entry: JsonObject,
    ) -> JsonObject:
        """Build sidecar/provenance evidence for unsupported and ambiguous source material."""
        return {
            "slice_name": "adr-json-authority-messy-canary-slice-2",
            "source_path": "docs/adr/adr.schema-base.md",
            "source_hash": source_hash,
            "source_title": title,
            "observed_markdown_status": None,
            "embedded_metadata": embedded_metadata,
            "reviewed_inventory_reference": {
                "source_hash": reviewed_entry["source_hash"],
                "reviewed_category": reviewed_entry["reviewed"]["category_candidate"],
                "reviewed_disposition": reviewed_entry["reviewed"]["disposition_candidate"],
                "reviewed_authority_effect": reviewed_entry["reviewed"]["authority_effect"],
                "automatic_conversion_eligibility_candidate": reviewed_entry["reviewed"]["automatic_conversion_eligibility_candidate"],
                "candidate_only": reviewed_entry["candidate_only"],
                "authority_change": reviewed_entry["authority_change"],
            },
            "ambiguity": {
                "schema_implementation_contract": True,
                "missing_status_preserved": True,
                "manual_review_required": True,
            },
            "candidate_only": True,
            "authority_change": False,
        }

    def build_candidate_object(
        self,
        source_hash: str,
        title: str | None,
        reviewed_entry: JsonObject,
        conflict_lossiness_report: JsonObject,
        sidecar_provenance: JsonObject,
    ) -> JsonObject:
        """Build candidate messy canary object evidence."""
        return {
            "slice_name": "adr-json-authority-messy-canary-slice-2",
            "object_type": "AdrJsonAuthorityMessyCanaryCandidate",
            "object_version": "candidate-0",
            "source_path": "docs/adr/adr.schema-base.md",
            "source_hash": source_hash,
            "authority_mode": "candidate-evidence-only-not-repository-authority",
            "authority_change": False,
            "candidate_only": True,
            "source_mutation": False,
            "schema_change": False,
            "database_authority": False,
            "conversion_scope": {
                "source_count": 1,
                "sources": ["docs/adr/adr.schema-base.md"],
            },
            "content_candidate": {
                "title": title,
                "status": None,
                "status_preservation": "missing in Markdown source; not invented",
                "complete_adr_schema_payload": False,
                "schema_validation_blocked": True,
            },
            "reviewed_inventory": reviewed_entry["reviewed"],
            "conflict_lossiness": {
                "path": "dev/adr-json-authority-messy-canary-slice-2/conflict-lossiness-report.json",
                "outcome": conflict_lossiness_report["outcome"],
                "missing_status": True,
                "requires_review": True,
            },
            "sidecar_provenance": {
                "path": "dev/adr-json-authority-messy-canary-slice-2/sidecar-provenance.json",
                "embedded_metadata_preserved": sidecar_provenance["embedded_metadata"] is not None,
                "schema_implementation_contract_ambiguity": True,
            },
            "projection": {
                "generated": False,
                "reason": "Projection omitted because canary must not invent a status or imply schema-valid ADR content.",
            },
            "validation": {
                "source_hash_before": source_hash,
                "source_hash_after": None,
                "source_mutated": None,
                "docs_schemas_mutation": False,
                "mutable_database_files": False,
                "exactly_one_source": True,
            },
        }

    def build_conversion_evidence(self, candidate_object: JsonObject, conflict_lossiness_report: JsonObject) -> JsonObject:
        """Build conversion evidence summary."""
        return {
            "slice_name": "adr-json-authority-messy-canary-slice-2",
            "source_path": candidate_object["source_path"],
            "source_hash": candidate_object["source_hash"],
            "outcome": conflict_lossiness_report["outcome"],
            "candidate_only": True,
            "authority_change": False,
            "conversion_attempted": True,
            "conversion_completed_as_authoritative_record": False,
            "status_invented": False,
            "normalized_status_inserted": False,
            "source_non_mutation_proof": {
                "source_hash_before": candidate_object["source_hash"],
                "source_hash_after": None,
                "source_mutated": None,
            },
            "review_required_before_promotion": True,
            "blocked_reasons": [
                "missing_observed_status",
                "manual_review_required",
                "schema_implementation_contract_ambiguity",
            ],
        }

    def build_manifest(
        self,
        candidate_object: JsonObject,
        conversion_evidence: JsonObject,
        conflict_lossiness_report: JsonObject,
        sidecar_provenance: JsonObject,
        source_hash: str,
    ) -> JsonObject:
        """Build messy canary manifest."""
        return {
            "slice_name": "adr-json-authority-messy-canary-slice-2",
            "mode": "candidate messy canary evidence only",
            "authority_change": False,
            "source_mutation_allowed": False,
            "schema_change_allowed": False,
            "conversion_scope": "exactly-one-source",
            "database_authority": False,
            "generated_at": self.generated_at,
            "source": {
                "path": "docs/adr/adr.schema-base.md",
                "sha256": source_hash,
            },
            "source_refs": {
                "brief": "docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md",
                "hermes_decision": "docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md",
                "reviewed_inventory": "dev/adr-json-authority-inventory-review-overrides-slice-1/reviewed-inventory.json",
                "slice_1_acceptance": "docs/reviews/hermes-acceptance.20260711.143600_adr-json-authority-inventory-review-overrides-slice-1.md",
            },
            "artifacts": {
                "manifest": "dev/adr-json-authority-messy-canary-slice-2/manifest.json",
                "candidate_object": "dev/adr-json-authority-messy-canary-slice-2/adr.schema-base.candidate-object.json",
                "conversion_evidence": "dev/adr-json-authority-messy-canary-slice-2/conversion-evidence.json",
                "conflict_lossiness_report": "dev/adr-json-authority-messy-canary-slice-2/conflict-lossiness-report.json",
                "sidecar_provenance": "dev/adr-json-authority-messy-canary-slice-2/sidecar-provenance.json",
            },
            "artifact_hashes": {
                "candidate_object": DocumentRecord.payload_hash(candidate_object),
                "conversion_evidence": DocumentRecord.payload_hash(conversion_evidence),
                "conflict_lossiness_report": DocumentRecord.payload_hash(conflict_lossiness_report),
                "sidecar_provenance": DocumentRecord.payload_hash(sidecar_provenance),
            },
            "outcome": conflict_lossiness_report["outcome"],
            "candidate_only": True,
            "validation_command_summary": {
                "json_validity": "pending closeout validation",
                "source_schema_non_mutation": "pending closeout validation",
                "no_database_files": "pending closeout validation",
                "exactly_one_source": "docs/adr/adr.schema-base.md only",
            },
        }

    def write_artifacts(
        self,
        manifest: JsonObject,
        candidate_object: JsonObject,
        conversion_evidence: JsonObject,
        conflict_lossiness_report: JsonObject,
        sidecar_provenance: JsonObject,
    ) -> None:
        """Write deterministic messy canary evidence artifacts."""
        self.paths.manifest.write_text(DocumentRecord.canonical_payload_text(manifest), encoding="utf-8")
        self.paths.candidate_object.write_text(DocumentRecord.canonical_payload_text(candidate_object), encoding="utf-8")
        self.paths.conversion_evidence.write_text(DocumentRecord.canonical_payload_text(conversion_evidence), encoding="utf-8")
        self.paths.conflict_lossiness_report.write_text(
            DocumentRecord.canonical_payload_text(conflict_lossiness_report), encoding="utf-8"
        )
        self.paths.sidecar_provenance.write_text(DocumentRecord.canonical_payload_text(sidecar_provenance), encoding="utf-8")


def run_adr_json_authority_messy_canary(repo_root: Path) -> AdrMessyCanaryResult:
    """Run the one-source ADR JSON authority messy canary."""
    return AdrMessyCanaryRunner(paths=AdrMessyCanaryPaths(repo_root=repo_root)).run()
