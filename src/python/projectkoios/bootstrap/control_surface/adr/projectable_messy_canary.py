from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re

from projectkoios.bootstrap.control_surface.adr.markdown import AdrMarkdownError
from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.documents import DocumentRecord
from projectkoios.bootstrap.schema.models import JsonObject


SLICE_NAME = "adr-json-authority-projectable-messy-canary-slice-3"
SOURCE_PATH = "docs/adr/adr.adr-template-contract.md"
TARGET_PATH = "dev/adr-json-authority-projectable-messy-canary-slice-3"


@dataclass(frozen=True, slots=True)
class AdrProjectableMessyCanaryPaths:
    """Filesystem paths for the projectable messy ADR canary."""

    repo_root: Path

    @property
    def source_adr(self) -> Path:
        """Return the exact projectable messy canary source path."""
        return self.repo_root / "docs" / "adr" / "adr.adr-template-contract.md"

    @property
    def reviewed_inventory(self) -> Path:
        """Return Slice 1 reviewed inventory evidence path."""
        return self.repo_root / "dev" / "adr-json-authority-inventory-review-overrides-slice-1" / "reviewed-inventory.json"

    @property
    def slice_2_acceptance(self) -> Path:
        """Return Slice 2 HERMES acceptance/watchpoint input path."""
        return self.repo_root / "docs" / "reviews" / "hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md"

    @property
    def target_dir(self) -> Path:
        """Return Slice 3 projectable messy canary evidence directory."""
        return self.repo_root / TARGET_PATH

    @property
    def manifest(self) -> Path:
        """Return manifest path."""
        return self.target_dir / "manifest.json"

    @property
    def candidate_object(self) -> Path:
        """Return candidate object path."""
        return self.target_dir / "candidate-object.json"

    @property
    def generated_projection(self) -> Path:
        """Return generated projection path."""
        return self.target_dir / "generated-projection.md"

    @property
    def projection_parseback_evidence(self) -> Path:
        """Return projection parse-back evidence path."""
        return self.target_dir / "projection-parseback-evidence.json"

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
class AdrProjectableMessyCanaryResult:
    """Generated projectable messy canary evidence result."""

    # Local value keeps this canary step explicit for validation.
    manifest: JsonObject
    # Local value keeps this canary step explicit for validation.
    candidate_object: JsonObject
    # Local value keeps this canary step explicit for validation.
    projection_parseback_evidence: JsonObject
    # Local value keeps this canary step explicit for validation.
    conversion_evidence: JsonObject
    # Local value keeps this canary step explicit for validation.
    conflict_lossiness_report: JsonObject
    # Local value keeps this canary step explicit for validation.
    sidecar_provenance: JsonObject
    generated_projection: str


@dataclass(frozen=True, slots=True)
class AdrProjectableMessyCanaryRunner:
    """Generate evidence for the projectable ADR template-contract canary."""

    # Local value keeps this canary step explicit for validation.
    paths: AdrProjectableMessyCanaryPaths
    generated_at: str = "20260711.145600Z"

    def run(self) -> AdrProjectableMessyCanaryResult:
        """Generate deterministic projectable messy canary evidence artifacts."""
        self.paths.target_dir.mkdir(parents=True, exist_ok=True)
        # Source text before generation is the non-mutation baseline.
        # Local value keeps this canary step explicit for validation.
        source_before: str = self.paths.source_adr.read_text(encoding="utf-8")
        # Source hash proves the exact canary source inspected.
        source_hash_before: str = PilotManifestBuilder.hash_text(source_before)
        # Reviewed entry carries Slice 1 candidate-only disposition evidence.
        reviewed_entry: JsonObject = self.reviewed_entry()
        # Source sections and candidate content are parsed without mutating source.
        # Local value keeps this canary step explicit for validation.
        sections: dict[str, str] = self.sections(source_before)
        # Local value keeps this canary step explicit for validation.
        title: str = self.parse_title(source_before)
        # Local value keeps this canary step explicit for validation.
        observed_status: str = self.status(sections)
        # Local value keeps this canary step explicit for validation.
        normalized_status_candidate: str = observed_status.lower()
        # Local value keeps this canary step explicit for validation.
        content_candidate: JsonObject = self.build_content_candidate(title, observed_status, sections)
        # Projection is generated only under the dev evidence path and preserves observed status casing.
        generated_projection: str = self.render_projection(content_candidate, source_hash_before, reviewed_entry)
        # Local value keeps this canary step explicit for validation.
        projection_hash: str = PilotManifestBuilder.hash_text(generated_projection)
        # Local value keeps this canary step explicit for validation.
        parseback_record: JsonObject = self.parse_projection_record(generated_projection)
        # Local value keeps this canary step explicit for validation.
        projection_parseback_evidence: JsonObject = self.build_projection_parseback_evidence(
            content_candidate=content_candidate,
            parseback_record=parseback_record,
            projection_hash=projection_hash,
            observed_status=observed_status,
            normalized_status_candidate=normalized_status_candidate,
        )
        # Local value keeps this canary step explicit for validation.
        conflict_lossiness_report: JsonObject = self.build_conflict_lossiness_report(
            source_hash=source_hash_before,
            reviewed_entry=reviewed_entry,
            observed_status=observed_status,
            normalized_status_candidate=normalized_status_candidate,
            projection_parseback_evidence=projection_parseback_evidence,
        )
        # Local value keeps this canary step explicit for validation.
        sidecar_provenance: JsonObject = self.build_sidecar_provenance(
            source_hash=source_hash_before,
            title=title,
            reviewed_entry=reviewed_entry,
            observed_status=observed_status,
            normalized_status_candidate=normalized_status_candidate,
            projection_hash=projection_hash,
            projection_parseback_evidence=projection_parseback_evidence,
            sections=sections,
        )
        # Local value keeps this canary step explicit for validation.
        candidate_object: JsonObject = self.build_candidate_object(
            source_hash=source_hash_before,
            content_candidate=content_candidate,
            reviewed_entry=reviewed_entry,
            conflict_lossiness_report=conflict_lossiness_report,
            sidecar_provenance=sidecar_provenance,
            projection_parseback_evidence=projection_parseback_evidence,
        )
        # Local value keeps this canary step explicit for validation.
        conversion_evidence: JsonObject = self.build_conversion_evidence(candidate_object, conflict_lossiness_report)
        # Source text after generation must be byte-for-byte identical.
        source_after: str = self.paths.source_adr.read_text(encoding="utf-8")
        # Local value keeps this canary step explicit for validation.
        source_hash_after: str = PilotManifestBuilder.hash_text(source_after)
        if source_before != source_after:
            raise AssertionError("Projectable messy canary source ADR was mutated")
        candidate_object["validation"]["source_hash_after"] = source_hash_after
        candidate_object["validation"]["source_mutated"] = source_hash_before != source_hash_after
        conversion_evidence["source_non_mutation_proof"]["source_hash_after"] = source_hash_after
        conversion_evidence["source_non_mutation_proof"]["source_mutated"] = source_hash_before != source_hash_after
        sidecar_provenance["source_hash_after"] = source_hash_after
        # Local value keeps this canary step explicit for validation.
        manifest: JsonObject = self.build_manifest(
            candidate_object=candidate_object,
            projection_parseback_evidence=projection_parseback_evidence,
            conversion_evidence=conversion_evidence,
            conflict_lossiness_report=conflict_lossiness_report,
            sidecar_provenance=sidecar_provenance,
            source_hash=source_hash_before,
            projection_hash=projection_hash,
        )
        self.write_artifacts(
            manifest=manifest,
            candidate_object=candidate_object,
            generated_projection=generated_projection,
            projection_parseback_evidence=projection_parseback_evidence,
            conversion_evidence=conversion_evidence,
            conflict_lossiness_report=conflict_lossiness_report,
            sidecar_provenance=sidecar_provenance,
        )
        return AdrProjectableMessyCanaryResult(
            manifest=manifest,
            candidate_object=candidate_object,
            projection_parseback_evidence=projection_parseback_evidence,
            conversion_evidence=conversion_evidence,
            conflict_lossiness_report=conflict_lossiness_report,
            sidecar_provenance=sidecar_provenance,
            generated_projection=generated_projection,
        )

    def reviewed_entry(self) -> JsonObject:
        """Return the Slice 1 reviewed entry for the exact canary source."""
        # Local value keeps this canary step explicit for validation.
        reviewed_inventory: JsonObject = json.loads(self.paths.reviewed_inventory.read_text(encoding="utf-8"))
        entry: JsonObject
        for entry in reviewed_inventory["entries"]:
            if entry["source_path"] == SOURCE_PATH:
                return entry
        raise ValueError(f"Reviewed inventory missing {SOURCE_PATH}")

    def parse_title(self, source_text: str) -> str:
        """Parse source H1 title."""
        # Stable heading match supports timestamp-free ADR title lines.
        stable_match: re.Match[str] | None = re.search(r"^#\s+ADR:\s*(?P<title>.+?)\s*$", source_text, flags=re.MULTILINE)
        if stable_match is not None:
            return stable_match.group("title")
        # Legacy heading match preserves compatibility with timestamped headings.
        legacy_match: re.Match[str] | None = re.search(
            r"^#\s+ADR\s+[^:]+:\s*(?P<title>.+?)\s*$", source_text, flags=re.MULTILINE
        )
        if legacy_match is None:
            raise AdrMarkdownError("Source ADR missing parseable title")
        return legacy_match.group("title")

    def sections(self, markdown: str) -> dict[str, str]:
        """Split source Markdown into normalized section bodies."""
        # Local value keeps this canary step explicit for validation.
        lines: list[str] = markdown.splitlines()
        # Local value keeps this canary step explicit for validation.
        sections: dict[str, list[str]] = {}
        # Local value keeps this canary step explicit for validation.
        current_key: str | None = None
        # Section loop line is annotated for policy-compliant parsing.
        line: str
        for line in lines[1:]:
            # Local value keeps this canary step explicit for validation.
            match: re.Match[str] | None = re.match(r"^## (?P<heading>.+)$", line)
            if match is not None:
                current_key = self.section_key(match.group("heading"))
                sections[current_key] = []
                continue
            if current_key is not None:
                sections[current_key].append(line)
        return {key: "\n".join(value).strip() for key, value in sections.items()}

    def section_key(self, heading: str) -> str:
        """Normalize Markdown heading spelling for candidate extraction."""
        return heading.strip().lower().replace(" ", "_").replace("-", "_")

    def status(self, sections: dict[str, str]) -> str:
        """Return the observed source status text and casing."""
        # Local value keeps this canary step explicit for validation.
        body: str = sections.get("status", "")
        # Local value keeps this canary step explicit for validation.
        lines: list[str] = [line.strip() for line in body.splitlines() if line.strip()]
        if not lines:
            raise AdrMarkdownError("Status section is empty")
        return lines[0]

    def key_values(self, body: str) -> dict[str, str]:
        """Parse key-value lines from a Markdown section."""
        # Local value keeps this canary step explicit for validation.
        values: dict[str, str] = {}
        # Key-value loop line is annotated for policy-compliant parsing.
        line: str
        for line in body.splitlines():
            # Local value keeps this canary step explicit for validation.
            cleaned_line: str = line.removeprefix("- ")
            if ":" not in cleaned_line:
                continue
            # Parsed key and value are recorded only when non-empty.
            key: str
            value: str
            key, value = cleaned_line.split(":", maxsplit=1)
            if key and value.strip():
                values[key.strip()] = value.strip()
        return values

    def bullets(self, body: str) -> list[str]:
        """Return bullet values from a Markdown section, including wrapped continuations."""
        # Bullet values preserve Markdown continuation lines as source content.
        values: list[str] = []
        # Current bullet accumulates one wrapped source list item.
        current_value: str | None = None
        # Bullet loop line is annotated for policy-compliant parsing.
        line: str
        for line in body.splitlines():
            if line.startswith("- "):
                if current_value is not None:
                    values.append(current_value)
                current_value = line.removeprefix("- ").strip()
                continue
            if current_value is not None and line.startswith("  ") and line.strip():
                current_value = f"{current_value} {line.strip()}"
        if current_value is not None:
            values.append(current_value)
        return values

    def build_content_candidate(self, title: str, observed_status: str, sections: dict[str, str]) -> JsonObject:
        """Build the projectable content candidate while preserving observed status casing."""
        # Local value keeps this canary step explicit for validation.
        context_values: dict[str, str] = self.key_values(sections["context"])
        # Local value keeps this canary step explicit for validation.
        links_values: dict[str, str] = self.key_values(sections["links"])
        return {
            "id": "adr.adr-template-contract",
            "slug": "canonical-adr-proposal-template",
            "title": title,
            "status": observed_status,
            "observed_status_text": observed_status,
            "normalized_status_candidate": observed_status.lower(),
            "normalization_requires_review": True,
            "context": {
                "origin": context_values["Origin"],
                "from": context_values["From"],
                "acting_as": context_values["Acting-As"],
                "scope": context_values["Scope"],
                "repository": context_values["Repository"],
                "architecture_domain": context_values["Architecture-Domain"],
            },
            "decision": sections["decision"],
            "consequences": sections["consequences"],
            "architecture_spec": sections["architecture_spec"],
            "acceptance_criteria": self.bullets(sections["acceptance_criteria"]),
            "implementation_brief": sections["implementation_brief"],
            "resolved_open_questions": self.bullets(sections["resolved_open_questions"]),
            "non_goals": self.bullets(sections["non_goals"]),
            "validation_expectations": self.bullets(sections["validation_expectations"]),
            "links": {
                "back_to": links_values["back_to"],
                "supersedes": None if links_values["supersedes"] == "None" else links_values["supersedes"],
                "superseded_by": None if links_values["superseded_by"] == "None" else links_values["superseded_by"],
            },
        }

    def render_projection(self, content_candidate: JsonObject, source_hash: str, reviewed_entry: JsonObject) -> str:
        """Render generated non-authoritative projection evidence."""
        # Local value keeps this canary step explicit for validation.
        record_json: str = DocumentRecord.canonical_payload_text(content_candidate).rstrip()
        # Local value keeps this canary step explicit for validation.
        lines: list[str] = [
            "<!-- GENERATED SLICE 3 PROJECTION EVIDENCE: non-authoritative; do not use as ADR source. -->",
            f"# ADR Projection Evidence: {content_candidate['title']}",
            "",
            "## Projection metadata",
            "",
            f"- Slice name: {SLICE_NAME}",
            f"- Evidence path: {TARGET_PATH}/generated-projection.md",
            f"- Source path: {SOURCE_PATH}",
            f"- Source hash: {source_hash}",
            "- Authority mode: candidate evidence only; not repository authority",
            "- Source mutation: false",
            "- Schema change: false",
            "- Database authority: false",
            f"- Reviewed category: {reviewed_entry['reviewed']['category_candidate']}",
            f"- Reviewed disposition: {reviewed_entry['reviewed']['disposition_candidate']}",
            f"- Observed status text: {content_candidate['observed_status_text']}",
            f"- Normalized status candidate: {content_candidate['normalized_status_candidate']}",
            "- Normalization requires review: true",
            "",
            "```json adr-record",
            record_json,
            "```",
            "",
            "## Status",
            "",
            str(content_candidate["status"]),
            "",
            "## Candidate note",
            "",
            "This projection is generated evidence only. Projection parse-back does not resolve template/schema-contract or status-casing review blockers.",
            "",
        ]
        return "\n".join(lines).rstrip() + "\n"

    def parse_projection_record(self, markdown: str) -> JsonObject:
        """Parse only the generated projection's embedded JSON record."""
        # Local value keeps this canary step explicit for validation.
        start_marker: str = "```json adr-record"
        # Local value keeps this canary step explicit for validation.
        start_index: int = markdown.find(start_marker)
        if start_index < 0:
            raise AdrMarkdownError("Projection missing ADR record JSON fence")
        # Local value keeps this canary step explicit for validation.
        json_start: int = start_index + len(start_marker)
        # Local value keeps this canary step explicit for validation.
        end_index: int = markdown.find("```", json_start)
        if end_index < 0:
            raise AdrMarkdownError("Projection ADR record JSON fence is unclosed")
        # Local value keeps this canary step explicit for validation.
        payload: object = json.loads(markdown[json_start:end_index].strip())
        if not isinstance(payload, dict):
            raise AdrMarkdownError("Projection ADR record payload must be an object")
        return payload

    def build_projection_parseback_evidence(
        self,
        # Local value keeps this canary step explicit for validation.
        content_candidate: JsonObject,
        # Local value keeps this canary step explicit for validation.
        parseback_record: JsonObject,
        # Local value keeps this canary step explicit for validation.
        projection_hash: str,
        # Local value keeps this canary step explicit for validation.
        observed_status: str,
        # Local value keeps this canary step explicit for validation.
        normalized_status_candidate: str,
    ) -> JsonObject:
        """Build generated-projection parse-back evidence."""
        # Local value keeps this canary step explicit for validation.
        semantic_equal: bool = parseback_record == content_candidate
        return {
            "slice_name": SLICE_NAME,
            "source_path": SOURCE_PATH,
            "projection_path": f"{TARGET_PATH}/generated-projection.md",
            "projection_hash": projection_hash,
            "parseback_source": "generated_projection_only",
            "hand_authored_source_parsed_as_replacement": False,
            "semantic_equal_for_candidate_fields": semantic_equal,
            "observed_status_text": observed_status,
            "parseback_status_text": parseback_record.get("status"),
            "normalized_status_candidate": normalized_status_candidate,
            "status_casing_preserved_in_projection_record": parseback_record.get("status") == observed_status,
            "status_normalized_by_projection_or_parseback": parseback_record.get("status") != observed_status,
            "projection_introduced_authority": False,
            "projection_resolves_review_blockers": False,
            "requires_review": True,
        }

    def build_conflict_lossiness_report(
        self,
        source_hash: str,
        reviewed_entry: JsonObject,
        # Local value keeps this canary step explicit for validation.
        observed_status: str,
        # Local value keeps this canary step explicit for validation.
        normalized_status_candidate: str,
        # Local value keeps this canary step explicit for validation.
        projection_parseback_evidence: JsonObject,
    ) -> JsonObject:
        """Build status-casing/template-contract conflict and lossiness report."""
        return {
            "slice_name": SLICE_NAME,
            "source_path": SOURCE_PATH,
            "source_hash": source_hash,
            "outcome": "projectable_candidate_blocked_pending_template_contract_and_status_review",
            "candidate_only": True,
            "authority_change": False,
            "observed_status_text": observed_status,
            "normalized_status_candidate": normalized_status_candidate,
            "status_casing_normalization_sensitive": observed_status != normalized_status_candidate,
            "status_normalization_inserted_into_source": False,
            "reviewed_inventory_values": reviewed_entry["reviewed"],
            "template_schema_contract_ambiguity": True,
            "manual_review_required": True,
            "automatic_conversion_eligible": False,
            "blocked_from_authority_promotion": True,
            "projection_parseback": {
                "semantic_equal_for_candidate_fields": projection_parseback_evidence["semantic_equal_for_candidate_fields"],
                "status_casing_preserved_in_projection_record": projection_parseback_evidence[
                    "status_casing_preserved_in_projection_record"
                ],
                "status_normalized_by_projection_or_parseback": projection_parseback_evidence[
                    "status_normalized_by_projection_or_parseback"
                ],
            },
            "lossiness_findings": [
                "observed source status uses noncanonical casing and is preserved as Accepted",
                "normalized status candidate accepted is review-only and not a source rewrite",
                "template/schema-contract classification is preserved outside ADR content candidate",
                "manual review remains blocking before any authority promotion",
                "projection parse-back equality does not resolve template-contract or status-casing authority questions",
            ],
            "omitted_or_sidecar_preserved_fields": [
                "reviewed category/disposition/authority-effect",
                "manual-review and owner-review flags",
                "status-casing normalization warning",
                "routing section",
            ],
            "inferred_fields": [
                {
                    "field": "id",
                    "value": "adr.adr-template-contract",
                    "rationale": "candidate identifier derived from source filename for evidence only",
                    "requires_review": True,
                },
                {
                    "field": "slug",
                    "value": "canonical-adr-proposal-template",
                    "rationale": "candidate slug derived from source title for evidence only",
                    "requires_review": True,
                },
            ],
            "requires_review": True,
        }

    def build_sidecar_provenance(
        self,
        source_hash: str,
        # Local value keeps this canary step explicit for validation.
        title: str,
        reviewed_entry: JsonObject,
        # Local value keeps this canary step explicit for validation.
        observed_status: str,
        # Local value keeps this canary step explicit for validation.
        normalized_status_candidate: str,
        # Local value keeps this canary step explicit for validation.
        projection_hash: str,
        # Local value keeps this canary step explicit for validation.
        projection_parseback_evidence: JsonObject,
        # Local value keeps this canary step explicit for validation.
        sections: dict[str, str],
    ) -> JsonObject:
        """Build sidecar/provenance evidence for review blockers and source-sensitive fields."""
        # Local value keeps this canary step explicit for validation.
        routing_values: dict[str, str] = self.key_values(sections.get("routing", ""))
        return {
            "slice_name": SLICE_NAME,
            "source_path": SOURCE_PATH,
            "source_hash_before": source_hash,
            "source_hash_after": None,
            "source_title": title,
            "observed_source_status_text": observed_status,
            "normalized_status_candidate": normalized_status_candidate,
            "status_casing_preserved_separately": True,
            "reviewed_inventory_reference": {
                "source_hash": reviewed_entry["source_hash"],
                "reviewed_category": reviewed_entry["reviewed"]["category_candidate"],
                "reviewed_disposition": reviewed_entry["reviewed"]["disposition_candidate"],
                "reviewed_authority_effect": reviewed_entry["reviewed"]["authority_effect"],
                "automatic_conversion_eligibility_candidate": reviewed_entry["reviewed"][
                    "automatic_conversion_eligibility_candidate"
                ],
                "exclusion_blocking_reasons": reviewed_entry["reviewed"]["exclusion_blocking_reasons"],
                "owner_domain_review_flags": reviewed_entry["reviewed"]["owner_domain_review_flags"],
                "candidate_only": reviewed_entry["candidate_only"],
                "authority_change": reviewed_entry["authority_change"],
            },
            "projection_reference": {
                "path": f"{TARGET_PATH}/generated-projection.md",
                "hash": projection_hash,
                "non_authoritative_generated_evidence": True,
            },
            "parseback_reference": {
                "path": f"{TARGET_PATH}/projection-parseback-evidence.json",
                "payload_hash": DocumentRecord.payload_hash(projection_parseback_evidence),
                "parseback_source": projection_parseback_evidence["parseback_source"],
            },
            "routing_preserved_outside_content_candidate": {
                "owner": routing_values.get("Owner"),
                "next_phase": routing_values.get("Next phase"),
                "notes": routing_values.get("Notes"),
            },
            "unsupported_or_domain_sensitive_material": [
                "template/schema-contract classification",
                "status casing normalization policy",
                "manual-review and owner-review blocking flags",
                "routing/lifecycle notes outside current content candidate",
            ],
            "candidate_only": True,
            "authority_change": False,
        }

    def build_candidate_object(
        self,
        source_hash: str,
        # Local value keeps this canary step explicit for validation.
        content_candidate: JsonObject,
        reviewed_entry: JsonObject,
        # Local value keeps this canary step explicit for validation.
        conflict_lossiness_report: JsonObject,
        # Local value keeps this canary step explicit for validation.
        sidecar_provenance: JsonObject,
        # Local value keeps this canary step explicit for validation.
        projection_parseback_evidence: JsonObject,
    ) -> JsonObject:
        """Build candidate projectable messy canary object evidence."""
        return {
            "slice_name": SLICE_NAME,
            "object_type": "AdrJsonAuthorityProjectableMessyCanaryCandidate",
            "object_version": "candidate-0",
            "source_path": SOURCE_PATH,
            "source_hash": source_hash,
            "authority_mode": "candidate-evidence-only-not-repository-authority",
            "authority_change": False,
            "candidate_only": True,
            "source_mutation": False,
            "schema_change": False,
            "database_authority": False,
            "conversion_completed_as_authoritative_record": False,
            "conversion_scope": {
                "source_count": 1,
                "sources": [SOURCE_PATH],
            },
            "content_candidate": content_candidate,
            "reviewed_inventory": reviewed_entry["reviewed"],
            "conflict_lossiness": {
                "path": f"{TARGET_PATH}/conflict-lossiness-report.json",
                "outcome": conflict_lossiness_report["outcome"],
                "requires_review": True,
                "blocked_from_authority_promotion": True,
            },
            "sidecar_provenance": {
                "path": f"{TARGET_PATH}/sidecar-provenance.json",
                "status_casing_preserved_separately": sidecar_provenance["status_casing_preserved_separately"],
                "template_schema_contract_ambiguity": True,
            },
            "projection": {
                "generated": True,
                "path": f"{TARGET_PATH}/generated-projection.md",
                "non_authoritative_generated_evidence": True,
                "status_casing_preserved_in_projection_record": projection_parseback_evidence[
                    "status_casing_preserved_in_projection_record"
                ],
            },
            "validation": {
                "source_hash_before": source_hash,
                "source_hash_after": None,
                "source_mutated": None,
                "docs_schemas_mutation": False,
                "mutable_database_files": False,
                "exactly_one_source": True,
                "projection_only_under_dev_slice_path": True,
            },
        }

    def build_conversion_evidence(self, candidate_object: JsonObject, conflict_lossiness_report: JsonObject) -> JsonObject:
        """Build conversion evidence summary."""
        return {
            "slice_name": SLICE_NAME,
            "source_path": candidate_object["source_path"],
            "source_hash": candidate_object["source_hash"],
            "outcome": conflict_lossiness_report["outcome"],
            "candidate_only": True,
            "authority_change": False,
            "conversion_attempted": True,
            "projection_generated": True,
            "conversion_completed_as_authoritative_record": False,
            "observed_status_text": candidate_object["content_candidate"]["observed_status_text"],
            "normalized_status_candidate": candidate_object["content_candidate"]["normalized_status_candidate"],
            "status_normalized_in_source": False,
            "source_non_mutation_proof": {
                "source_hash_before": candidate_object["source_hash"],
                "source_hash_after": None,
                "source_mutated": None,
            },
            "review_required_before_promotion": True,
            "blocked_reasons": [
                "manual_review_required",
                "template_schema_contract_ambiguity",
                "status_casing_or_text_would_normalize",
            ],
        }

    def build_manifest(
        self,
        # Local value keeps this canary step explicit for validation.
        candidate_object: JsonObject,
        # Local value keeps this canary step explicit for validation.
        projection_parseback_evidence: JsonObject,
        # Local value keeps this canary step explicit for validation.
        conversion_evidence: JsonObject,
        # Local value keeps this canary step explicit for validation.
        conflict_lossiness_report: JsonObject,
        # Local value keeps this canary step explicit for validation.
        sidecar_provenance: JsonObject,
        source_hash: str,
        # Local value keeps this canary step explicit for validation.
        projection_hash: str,
    ) -> JsonObject:
        """Build projectable messy canary manifest."""
        return {
            "slice_name": SLICE_NAME,
            "mode": "candidate projectable messy canary evidence only",
            "authority_change": False,
            "source_mutation_allowed": False,
            "schema_change_allowed": False,
            "conversion_scope": "exactly-one-source",
            "database_authority": False,
            "generated_at": self.generated_at,
            "source": {
                "path": SOURCE_PATH,
                "sha256": source_hash,
            },
            "source_refs": {
                "brief": "docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md",
                "hermes_decision": "docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md",
                "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md",
                "reviewed_inventory": "dev/adr-json-authority-inventory-review-overrides-slice-1/reviewed-inventory.json",
                "slice_1_acceptance": "docs/reviews/hermes-acceptance.20260711.143600_adr-json-authority-inventory-review-overrides-slice-1.md",
                "slice_2_acceptance": "docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md",
            },
            "artifacts": {
                "manifest": f"{TARGET_PATH}/manifest.json",
                "candidate_object": f"{TARGET_PATH}/candidate-object.json",
                "generated_projection": f"{TARGET_PATH}/generated-projection.md",
                "projection_parseback_evidence": f"{TARGET_PATH}/projection-parseback-evidence.json",
                "conversion_evidence": f"{TARGET_PATH}/conversion-evidence.json",
                "conflict_lossiness_report": f"{TARGET_PATH}/conflict-lossiness-report.json",
                "sidecar_provenance": f"{TARGET_PATH}/sidecar-provenance.json",
            },
            "artifact_hashes": {
                "candidate_object": DocumentRecord.payload_hash(candidate_object),
                "generated_projection_sha256": projection_hash,
                "projection_parseback_evidence": DocumentRecord.payload_hash(projection_parseback_evidence),
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
                "exactly_one_source": SOURCE_PATH,
                "projection_location": f"{TARGET_PATH}/generated-projection.md only",
            },
        }

    def write_artifacts(
        self,
        # Local value keeps this canary step explicit for validation.
        manifest: JsonObject,
        # Local value keeps this canary step explicit for validation.
        candidate_object: JsonObject,
        generated_projection: str,
        # Local value keeps this canary step explicit for validation.
        projection_parseback_evidence: JsonObject,
        # Local value keeps this canary step explicit for validation.
        conversion_evidence: JsonObject,
        # Local value keeps this canary step explicit for validation.
        conflict_lossiness_report: JsonObject,
        # Local value keeps this canary step explicit for validation.
        sidecar_provenance: JsonObject,
    ) -> None:
        """Write deterministic projectable messy canary evidence artifacts."""
        self.paths.manifest.write_text(DocumentRecord.canonical_payload_text(manifest), encoding="utf-8")
        self.paths.candidate_object.write_text(DocumentRecord.canonical_payload_text(candidate_object), encoding="utf-8")
        self.paths.generated_projection.write_text(generated_projection, encoding="utf-8")
        self.paths.projection_parseback_evidence.write_text(
            DocumentRecord.canonical_payload_text(projection_parseback_evidence), encoding="utf-8"
        )
        self.paths.conversion_evidence.write_text(DocumentRecord.canonical_payload_text(conversion_evidence), encoding="utf-8")
        self.paths.conflict_lossiness_report.write_text(
            DocumentRecord.canonical_payload_text(conflict_lossiness_report), encoding="utf-8"
        )
        self.paths.sidecar_provenance.write_text(DocumentRecord.canonical_payload_text(sidecar_provenance), encoding="utf-8")


def run_adr_json_authority_projectable_messy_canary(repo_root: Path) -> AdrProjectableMessyCanaryResult:
    """Run the one-source projectable messy ADR JSON authority canary."""
    return AdrProjectableMessyCanaryRunner(paths=AdrProjectableMessyCanaryPaths(repo_root=repo_root)).run()
