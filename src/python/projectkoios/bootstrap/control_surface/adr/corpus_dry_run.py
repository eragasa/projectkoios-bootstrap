from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re

from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.documents import DocumentRecord
from projectkoios.bootstrap.schema.models import JsonObject


SLICE_NAME = "adr-json-authority-corpus-dry-run-inventory-slice-4"
TARGET_PATH = "dev/adr-json-authority-corpus-dry-run-inventory-slice-4"
SELECTED_SOURCES: tuple[str, ...] = (
    "docs/adr/adr.json-schemas.draft.md",
    "docs/adr/adr.petrinet.20260705.132740Z.md",
    "docs/adr/adr.adr-template-contract.md",
    "docs/adr/adr.schema-base.md",
    "docs/adr/adr.adr-lifecycle.draft.md",
    "docs/adr/README.md",
)


@dataclass(frozen=True, slots=True)
class AdrCorpusDryRunPaths:
    """Filesystem paths for the Slice 4 bounded corpus dry run."""

    repo_root: Path

    @property
    def reviewed_inventory(self) -> Path:
        """Return Slice 1 reviewed inventory evidence path."""
        return self.repo_root / "dev" / "adr-json-authority-inventory-review-overrides-slice-1" / "reviewed-inventory.json"

    @property
    def target_dir(self) -> Path:
        """Return Slice 4 evidence directory."""
        return self.repo_root / TARGET_PATH

    @property
    def manifest(self) -> Path:
        """Return manifest path."""
        return self.target_dir / "manifest.json"

    @property
    def selected_sources(self) -> Path:
        """Return selected sources path."""
        return self.target_dir / "selected-sources.json"

    @property
    def per_source_results(self) -> Path:
        """Return per-source results path."""
        return self.target_dir / "per-source-results.json"

    @property
    def conflict_lossiness_report(self) -> Path:
        """Return conflict/lossiness report path."""
        return self.target_dir / "conflict-lossiness-report.json"

    @property
    def projection_parseback_report(self) -> Path:
        """Return projection parse-back report path."""
        return self.target_dir / "projection-parseback-report.json"

    @property
    def skipped_or_blocked_sources(self) -> Path:
        """Return skipped/blocked sources path."""
        return self.target_dir / "skipped-or-blocked-sources.json"

    @property
    def candidate_objects_dir(self) -> Path:
        """Return candidate objects directory."""
        return self.target_dir / "candidate-objects"

    @property
    def generated_projections_dir(self) -> Path:
        """Return generated projections directory."""
        return self.target_dir / "generated-projections"

    @property
    def sidecars_dir(self) -> Path:
        """Return sidecars directory."""
        return self.target_dir / "sidecars"


@dataclass(frozen=True, slots=True)
class AdrCorpusDryRunResult:
    """Generated Slice 4 corpus dry-run evidence result."""

    manifest: JsonObject
    selected_sources: JsonObject
    per_source_results: JsonObject
    conflict_lossiness_report: JsonObject
    projection_parseback_report: JsonObject
    skipped_or_blocked_sources: JsonObject


@dataclass(frozen=True, slots=True)
class AdrCorpusDryRunRunner:
    """Generate candidate-only corpus-style dry-run evidence for six selected ADR entries."""

    paths: AdrCorpusDryRunPaths
    generated_at: str = "20260711.152000Z"

    def run(self) -> AdrCorpusDryRunResult:
        """Generate deterministic Slice 4 evidence artifacts."""
        self.prepare_directories()
        # Reviewed entries provide Slice 1 disposition and blocker evidence.
        reviewed_entries: dict[str, JsonObject] = self.reviewed_entries()
        # Per-source rows accumulate candidate, blocked, and skipped outcomes.
        rows: list[JsonObject] = []
        # Candidate objects are written only for candidate-safe rows.
        candidate_objects: dict[str, JsonObject] = {}
        # Projection parse-back rows are written only for generated projections.
        parseback_rows: list[JsonObject] = []
        # Sidecars preserve source-sensitive fields for every selected row.
        sidecars: dict[str, JsonObject] = {}
        # Selected source path is processed in approved fixed order.
        source_path: str
        for source_path in SELECTED_SOURCES:
            # Per-source result contains row evidence and optional artifacts.
            row: JsonObject
            # Optional candidate object is absent for skipped/excluded rows.
            candidate_object: JsonObject | None
            # Optional parse-back row is absent when projection is omitted/skipped.
            parseback_row: JsonObject | None
            # Sidecar is always present to keep provenance visible.
            sidecar: JsonObject
            row, candidate_object, parseback_row, sidecar = self.process_source(source_path, reviewed_entries[source_path])
            rows.append(row)
            sidecars[source_path] = sidecar
            if candidate_object is not None:
                candidate_objects[source_path] = candidate_object
            if parseback_row is not None:
                parseback_rows.append(parseback_row)
        # Selected-source evidence freezes subset membership and reviewed inputs.
        selected_sources: JsonObject = self.build_selected_sources(reviewed_entries)
        # Per-source result evidence carries the six dry-run rows.
        per_source_results: JsonObject = self.build_per_source_results(rows)
        # Conflict/lossiness report keeps per-source blockers visible.
        conflict_lossiness_report: JsonObject = self.build_conflict_lossiness_report(rows)
        # Projection parse-back report summarizes generated projection checks.
        projection_parseback_report: JsonObject = self.build_projection_parseback_report(parseback_rows)
        # Skipped/blocked report makes non-projectable rows easy to review.
        skipped_or_blocked_sources: JsonObject = self.build_skipped_or_blocked_sources(rows)
        # Manifest aggregates counts and artifact hashes.
        manifest: JsonObject = self.build_manifest(
            selected_sources=selected_sources,
            per_source_results=per_source_results,
            conflict_lossiness_report=conflict_lossiness_report,
            projection_parseback_report=projection_parseback_report,
            skipped_or_blocked_sources=skipped_or_blocked_sources,
        )
        self.write_artifacts(
            manifest=manifest,
            selected_sources=selected_sources,
            per_source_results=per_source_results,
            conflict_lossiness_report=conflict_lossiness_report,
            projection_parseback_report=projection_parseback_report,
            skipped_or_blocked_sources=skipped_or_blocked_sources,
            candidate_objects=candidate_objects,
            sidecars=sidecars,
        )
        return AdrCorpusDryRunResult(
            manifest=manifest,
            selected_sources=selected_sources,
            per_source_results=per_source_results,
            conflict_lossiness_report=conflict_lossiness_report,
            projection_parseback_report=projection_parseback_report,
            skipped_or_blocked_sources=skipped_or_blocked_sources,
        )

    def prepare_directories(self) -> None:
        """Create the Slice 4 evidence directory tree."""
        self.paths.candidate_objects_dir.mkdir(parents=True, exist_ok=True)
        self.paths.generated_projections_dir.mkdir(parents=True, exist_ok=True)
        self.paths.sidecars_dir.mkdir(parents=True, exist_ok=True)

    def reviewed_entries(self) -> dict[str, JsonObject]:
        """Return reviewed inventory entries keyed by selected source path."""
        # Reviewed inventory is read-only provenance input.
        reviewed_inventory: JsonObject = json.loads(self.paths.reviewed_inventory.read_text(encoding="utf-8"))
        # Entry map lets the runner prove exact selected membership.
        entry_by_path: dict[str, JsonObject] = {}
        # Inventory entry loop is annotated for policy-compliant parsing.
        entry: JsonObject
        for entry in reviewed_inventory["entries"]:
            if entry["source_path"] in SELECTED_SOURCES:
                entry_by_path[entry["source_path"]] = entry
        # Missing reviewed entries would make provenance comparison unsafe.
        missing: list[str] = [source_path for source_path in SELECTED_SOURCES if source_path not in entry_by_path]
        if missing:
            raise ValueError(f"Reviewed inventory missing selected sources: {missing}")
        return entry_by_path

    def process_source(
        self,
        source_path: str,
        reviewed_entry: JsonObject,
    ) -> tuple[JsonObject, JsonObject | None, JsonObject | None, JsonObject]:
        """Process one selected source into row, optional candidate/projection, and sidecar evidence."""
        # Source file before processing is the non-mutation baseline.
        source_file: Path = self.paths.repo_root / source_path
        # Source text is read once before evidence generation.
        source_before: str = source_file.read_text(encoding="utf-8")
        # Current hash is compared with Slice 1 reviewed hash.
        source_hash_before: str = PilotManifestBuilder.hash_text(source_before)
        # Parsed sections preserve top-level source content for candidate rows.
        sections: dict[str, str] = self.sections(source_before)
        # Title is best-effort for README/control rows too.
        title: str = self.parse_title(source_before)
        # Observed status may be absent for schema-base and README.
        observed_status: str | None = self.observed_status(sections)
        # Normalized status is review-only and never written back to source.
        normalized_status_candidate: str | None = None if observed_status is None else observed_status.lower()
        # Entry type distinguishes ADR candidate, source-only, and control rows.
        entry_type: str = self.entry_type(source_path, reviewed_entry)
        # Outcome records final dry-run disposition.
        outcome: str = self.outcome_for(source_path, reviewed_entry, observed_status)
        # Candidate object is generated only when safe as evidence.
        candidate_object: JsonObject | None = self.build_candidate_object(
            source_path=source_path,
            source_hash=source_hash_before,
            title=title,
            observed_status=observed_status,
            normalized_status_candidate=normalized_status_candidate,
            sections=sections,
            reviewed_entry=reviewed_entry,
            entry_type=entry_type,
            outcome=outcome,
        )
        # Projection is generated only for projectable candidate evidence rows.
        projection_path: str | None
        # Parse-back result is present only when projection is generated.
        parseback_row: JsonObject | None
        projection_path, parseback_row = self.maybe_generate_projection(source_path, candidate_object, outcome)
        # Source after processing proves no mutation occurred.
        source_after: str = source_file.read_text(encoding="utf-8")
        # Source hash after processing must match before hash.
        source_hash_after: str = PilotManifestBuilder.hash_text(source_after)
        if source_before != source_after:
            raise AssertionError(f"Slice 4 source mutated: {source_path}")
        # Sidecar preserves unsupported/source-sensitive material for every selected source.
        sidecar: JsonObject = self.build_sidecar(
            source_path=source_path,
            source_hash_before=source_hash_before,
            source_hash_after=source_hash_after,
            title=title,
            observed_status=observed_status,
            normalized_status_candidate=normalized_status_candidate,
            sections=sections,
            reviewed_entry=reviewed_entry,
            entry_type=entry_type,
            outcome=outcome,
            projection_path=projection_path,
        )
        # Row is the aggregate-facing source result.
        row: JsonObject = self.build_row(
            source_path=source_path,
            source_hash_before=source_hash_before,
            source_hash_after=source_hash_after,
            reviewed_entry=reviewed_entry,
            entry_type=entry_type,
            outcome=outcome,
            observed_status=observed_status,
            normalized_status_candidate=normalized_status_candidate,
            candidate_object=candidate_object,
            projection_path=projection_path,
            parseback_row=parseback_row,
            sections=sections,
        )
        return row, candidate_object, parseback_row, sidecar

    def sections(self, markdown: str) -> dict[str, str]:
        """Split Markdown into top-level `##` section bodies."""
        # Source lines are scanned without parsing nested content as records.
        lines: list[str] = markdown.splitlines()
        # Sections use normalized top-level heading keys.
        sections: dict[str, list[str]] = {}
        # Current section receives text until next top-level heading.
        current_key: str | None = None
        # Section loop line is annotated for policy-compliant parsing.
        line: str
        for line in lines[1:]:
            # Only `##` headings define top-level dry-run sections.
            match: re.Match[str] | None = re.match(r"^## (?P<heading>.+)$", line)
            if match is not None:
                current_key = self.section_key(match.group("heading"))
                sections[current_key] = []
                continue
            if current_key is not None:
                sections[current_key].append(line)
        return {key: "\n".join(value).strip() for key, value in sections.items()}

    def section_key(self, heading: str) -> str:
        """Normalize heading spelling for dry-run field lookup."""
        return heading.strip().lower().replace(" ", "_").replace("-", "_")

    def parse_title(self, markdown: str) -> str:
        """Return the first Markdown H1 title without inventing ADR identity."""
        # First heading match captures ADR and README titles uniformly.
        match: re.Match[str] | None = re.search(r"^#\s+(?P<title>.+?)\s*$", markdown, flags=re.MULTILINE)
        if match is None:
            return ""
        return match.group("title")

    def observed_status(self, sections: dict[str, str]) -> str | None:
        """Return observed source status/casing when a Status section is present."""
        # Status body is absent for missing-status/control rows.
        body: str | None = sections.get("status")
        if body is None:
            return None
        # First non-empty line is the observed source status text.
        lines: list[str] = [line.strip() for line in body.splitlines() if line.strip()]
        if not lines:
            return None
        return lines[0]

    def bullets(self, body: str) -> list[str]:
        """Return Markdown bullets while preserving wrapped continuation lines."""
        # Bullet values preserve source continuation text from Slice 3 regression.
        values: list[str] = []
        # Current bullet accumulates wrapped Markdown source lines.
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

    def entry_type(self, source_path: str, reviewed_entry: JsonObject) -> str:
        """Return dry-run entry type for a selected source."""
        if source_path == "docs/adr/README.md":
            return "index_control_surface"
        if reviewed_entry["reviewed"]["disposition_candidate"] == "source_only_provenance_candidate":
            return "source_provenance_draft"
        return "adr_source_candidate"

    def outcome_for(self, source_path: str, reviewed_entry: JsonObject, observed_status: str | None) -> str:
        """Return final per-source dry-run outcome."""
        if source_path == "docs/adr/README.md":
            return "index_control_surface_skipped"
        if reviewed_entry["reviewed"]["disposition_candidate"] == "source_only_provenance_candidate":
            return "source_only_provenance_draft_skipped_or_blocked"
        if observed_status is None:
            return "blocked_missing_status_pending_review"
        if source_path == "docs/adr/adr.adr-template-contract.md":
            return "projectable_candidate_blocked_pending_template_contract_and_status_review"
        if source_path == "docs/adr/adr.petrinet.20260705.132740Z.md":
            return "accepted_source_candidate_not_json_authority"
        return "candidate_projectable_pending_review"

    def build_candidate_object(
        self,
        source_path: str,
        source_hash: str,
        title: str,
        observed_status: str | None,
        normalized_status_candidate: str | None,
        sections: dict[str, str],
        reviewed_entry: JsonObject,
        entry_type: str,
        outcome: str,
    ) -> JsonObject | None:
        """Build a candidate evidence object or return None for skipped rows."""
        if entry_type in {"index_control_surface", "source_provenance_draft"}:
            return None
        # Content candidate intentionally remains evidence-only and incomplete.
        content_candidate: JsonObject = {
            "title": title,
            "observed_status_text": observed_status,
            "normalized_status_candidate": normalized_status_candidate,
            "status_missing": observed_status is None,
            "decision": sections.get("decision"),
            "consequences": sections.get("consequences"),
            "acceptance_criteria": self.bullets(sections.get("acceptance_criteria", "")),
        }
        return {
            "slice_name": SLICE_NAME,
            "object_type": "AdrJsonAuthorityCorpusDryRunCandidate",
            "source_path": source_path,
            "source_hash": source_hash,
            "authority_mode": "candidate-evidence-only-not-repository-authority",
            "authority_change": False,
            "candidate_only": True,
            "source_mutation": False,
            "schema_change": False,
            "database_authority": False,
            "conversion_completed_as_authoritative_record": False,
            "corpus_dry_run": True,
            "bounded_subset_only": True,
            "bulk_migration": False,
            "cutover_authorized": False,
            "entry_type": entry_type,
            "outcome": outcome,
            "reviewed_inventory": reviewed_entry["reviewed"],
            "content_candidate": content_candidate,
            "blocked_from_authority_promotion": True,
        }

    def maybe_generate_projection(
        self,
        source_path: str,
        candidate_object: JsonObject | None,
        outcome: str,
    ) -> tuple[str | None, JsonObject | None]:
        """Generate projection and parse-back evidence for projectable candidate rows only."""
        if candidate_object is None:
            return None, None
        if outcome == "blocked_missing_status_pending_review":
            return None, None
        # Projection file name is deterministic and remains under Slice 4 dev evidence.
        projection_name: str = self.artifact_stem(source_path) + ".generated-projection.md"
        # Projection path is relative to repository root for evidence references.
        projection_path: str = f"{TARGET_PATH}/generated-projections/{projection_name}"
        # Projection body embeds only the candidate object for generated parse-back.
        projection_text: str = self.render_projection(candidate_object)
        (self.paths.repo_root / projection_path).write_text(projection_text, encoding="utf-8")
        # Projection parse-back reads only generated projection JSON.
        parsed_candidate: JsonObject = self.parse_projection(projection_text)
        return projection_path, {
            "slice_name": SLICE_NAME,
            "source_path": source_path,
            "projection_path": projection_path,
            "projection_hash": PilotManifestBuilder.hash_text(projection_text),
            "parseback_source": "generated_projection_only",
            "hand_authored_source_parsed_as_replacement": False,
            "semantic_equal_for_candidate_fields": parsed_candidate == candidate_object,
            "projection_introduced_authority": False,
            "projection_resolves_review_blockers": False,
            "observed_status_text": candidate_object["content_candidate"]["observed_status_text"],
            "normalized_status_candidate": candidate_object["content_candidate"]["normalized_status_candidate"],
        }

    def render_projection(self, candidate_object: JsonObject) -> str:
        """Render a generated non-authoritative projection evidence file."""
        # Candidate JSON is canonical to make parse-back deterministic.
        candidate_json: str = DocumentRecord.canonical_payload_text(candidate_object).rstrip()
        return "\n".join(
            [
                "<!-- GENERATED SLICE 4 DRY-RUN PROJECTION EVIDENCE: non-authoritative; not ADR source. -->",
                f"# Slice 4 Projection Evidence: {candidate_object['source_path']}",
                "",
                "## Projection metadata",
                "",
                f"- Slice name: {SLICE_NAME}",
                "- Authority mode: candidate evidence only; not repository authority",
                "- Corpus dry run: true",
                "- Bounded subset only: true",
                "- Cutover authorized: false",
                "",
                "```json adr-corpus-dry-run-candidate",
                candidate_json,
                "```",
                "",
            ]
        )

    def parse_projection(self, projection_text: str) -> JsonObject:
        """Parse only the generated projection's embedded candidate JSON."""
        # Start marker identifies the generated candidate JSON fence.
        start_marker: str = "```json adr-corpus-dry-run-candidate"
        # Start index locates the generated evidence block.
        start_index: int = projection_text.find(start_marker)
        if start_index < 0:
            raise ValueError("Generated projection missing candidate JSON fence")
        # JSON starts after the fence marker.
        json_start: int = start_index + len(start_marker)
        # End index locates the closing fence.
        end_index: int = projection_text.find("```", json_start)
        if end_index < 0:
            raise ValueError("Generated projection candidate JSON fence is unclosed")
        # Payload is parsed as generated evidence only.
        payload: object = json.loads(projection_text[json_start:end_index].strip())
        if not isinstance(payload, dict):
            raise ValueError("Generated projection payload must be an object")
        return payload

    def build_sidecar(
        self,
        source_path: str,
        source_hash_before: str,
        source_hash_after: str,
        title: str,
        observed_status: str | None,
        normalized_status_candidate: str | None,
        sections: dict[str, str],
        reviewed_entry: JsonObject,
        entry_type: str,
        outcome: str,
        projection_path: str | None,
    ) -> JsonObject:
        """Build sidecar/provenance evidence for one selected source."""
        return {
            "slice_name": SLICE_NAME,
            "source_path": source_path,
            "source_hash_before": source_hash_before,
            "source_hash_after": source_hash_after,
            "source_hash_matches_reviewed_inventory": source_hash_before == reviewed_entry["source_hash"],
            "source_title": title,
            "observed_source_status_text": observed_status,
            "normalized_status_candidate": normalized_status_candidate,
            "normalized_status_review_only": normalized_status_candidate is not None,
            "status_invented": False,
            "entry_type": entry_type,
            "outcome": outcome,
            "reviewed_inventory_reference": reviewed_entry["reviewed"],
            "projection_path": projection_path,
            "candidate_content_section_keys": self.candidate_content_section_keys(),
            "omitted_or_sidecar_preserved_source_sections": self.omitted_source_sections(sections),
            "source_to_candidate_complete": False,
            "projection_parseback_scope": "candidate_fields_only_not_source_completeness",
            "unsupported_or_sidecar_preserved_fields": self.sidecar_fields(source_path, sections, reviewed_entry),
            "authority_change": False,
            "candidate_only": True,
        }

    def sidecar_fields(self, source_path: str, sections: dict[str, str], reviewed_entry: JsonObject) -> list[str]:
        """Return sidecar-preserved field descriptions for one source."""
        # Field descriptions keep source-to-candidate lossiness visible.
        fields: list[str] = [
            "reviewed category/disposition/authority-effect",
            "owner/manual/domain review flags",
            "routing or lifecycle material outside content candidate",
        ]
        if source_path == "docs/adr/adr.adr-template-contract.md":
            fields.append("Slice 3 wrapped-list acceptance criteria preserved in content candidate")
        if reviewed_entry["reviewed"]["disposition_candidate"] == "source_only_provenance_candidate":
            fields.append("source/provenance draft not promoted to current lifecycle authority")
        if source_path == "docs/adr/README.md":
            fields.append("index/control Markdown skipped as non-ADR record")
        if "routing" in sections:
            fields.append("routing section preserved as sidecar/provenance")
        return fields

    def build_row(
        self,
        source_path: str,
        source_hash_before: str,
        source_hash_after: str,
        reviewed_entry: JsonObject,
        entry_type: str,
        outcome: str,
        observed_status: str | None,
        normalized_status_candidate: str | None,
        candidate_object: JsonObject | None,
        projection_path: str | None,
        parseback_row: JsonObject | None,
        sections: dict[str, str],
    ) -> JsonObject:
        """Build one per-source dry-run result row."""
        # Reviewed flags drive blockers and aggregate counts.
        reviewed: JsonObject = reviewed_entry["reviewed"]
        # Candidate object path is present only for generated candidate evidence.
        candidate_path: str | None = None if candidate_object is None else f"{TARGET_PATH}/candidate-objects/{self.artifact_stem(source_path)}.json"
        return {
            "slice_name": SLICE_NAME,
            "source_path": source_path,
            "source_hash_before": source_hash_before,
            "source_hash_after": source_hash_after,
            "source_hash_matches_reviewed_inventory": source_hash_before == reviewed_entry["source_hash"],
            "reviewed_inventory": reviewed,
            "entry_type": entry_type,
            "attempted_candidate_conversion": candidate_object is not None,
            "skipped_or_excluded_reason": self.skip_reason(entry_type, outcome),
            "candidate_object_path": candidate_path,
            "projection_status": "generated" if projection_path is not None else self.projection_skip_status(outcome),
            "projection_path": projection_path,
            "parseback_status": None if parseback_row is None else "semantic_equal_for_candidate_fields",
            "observed_status_text": observed_status,
            "normalized_status_candidate": normalized_status_candidate,
            "status_missing": observed_status is None,
            "status_casing_or_text_would_normalize": observed_status is not None and observed_status != normalized_status_candidate,
            "accepted_source_status_not_json_authority": source_path == "docs/adr/adr.petrinet.20260705.132740Z.md",
            "manual_review_required": reviewed["owner_domain_review_flags"]["manual_review_required"],
            "blockers": reviewed["exclusion_blocking_reasons"],
            "omitted_or_sidecar_preserved_source_sections": self.omitted_source_sections(sections),
            "source_to_candidate_complete": False,
            "projection_parseback_scope": "candidate_fields_only_not_source_completeness",
            "lossiness_conflict_findings": self.lossiness_findings(source_path, outcome, observed_status, normalized_status_candidate),
            "sidecar_path": f"{TARGET_PATH}/sidecars/{self.artifact_stem(source_path)}.sidecar.json",
            "final_outcome": outcome,
            "authority_mode": "candidate/evidence only",
            "authority_change": False,
            "candidate_only": True,
            "source_mutation": False,
            "schema_change": False,
            "database_authority": False,
            "conversion_completed_as_authoritative_record": False,
            "corpus_dry_run": True,
            "bounded_subset_only": True,
            "bulk_migration": False,
            "cutover_authorized": False,
        }

    def skip_reason(self, entry_type: str, outcome: str) -> str | None:
        """Return skip/exclusion reason for blocked or skipped rows."""
        if entry_type == "index_control_surface":
            return "index/control surface is not an ADR candidate record"
        if entry_type == "source_provenance_draft":
            return "source/provenance draft is skipped from authority promotion"
        if outcome == "blocked_missing_status_pending_review":
            return "missing observed Markdown status blocks authority promotion"
        return None

    def projection_skip_status(self, outcome: str) -> str:
        """Return projection status for rows without generated projections."""
        if outcome == "blocked_missing_status_pending_review":
            return "blocked_missing_status"
        if outcome == "source_only_provenance_draft_skipped_or_blocked":
            return "skipped_source_only_provenance"
        if outcome == "index_control_surface_skipped":
            return "skipped_index_control_surface"
        return "omitted"

    def lossiness_findings(
        self,
        source_path: str,
        outcome: str,
        observed_status: str | None,
        normalized_status_candidate: str | None,
    ) -> list[str]:
        """Return per-source conflict/lossiness findings."""
        # Findings preserve source-to-candidate blockers per selected source.
        findings: list[str] = []
        if observed_status is None:
            findings.append("observed Markdown status missing; no status invented")
        if observed_status is not None and observed_status != normalized_status_candidate:
            findings.append("observed status casing/text preserved separately from normalized candidate")
        if source_path == "docs/adr/adr.petrinet.20260705.132740Z.md":
            findings.append("accepted/current source status remains source observation, not JSON authority")
        if source_path == "docs/adr/adr.adr-template-contract.md":
            findings.append("Slice 3 wrapped-list continuation preserved in multi-file dry run")
            findings.append("template/schema-contract manual-review blocker remains active")
        if outcome == "source_only_provenance_draft_skipped_or_blocked":
            findings.append("source/provenance draft not promoted or superseded")
        if outcome == "index_control_surface_skipped":
            findings.append("index/control surface skipped, not converted as ADR record")
        findings.append("source-to-candidate omitted sections are enumerated separately; projection equality covers candidate fields only")
        return findings

    def candidate_content_section_keys(self) -> list[str]:
        """Return source section keys represented directly in reduced candidates."""
        return ["status", "decision", "consequences", "acceptance_criteria"]

    def omitted_source_sections(self, sections: dict[str, str]) -> list[str]:
        """Return source section keys omitted from reduced candidate content and preserved in sidecars."""
        # Included section keys are represented directly in the reduced candidate.
        included: set[str] = set(self.candidate_content_section_keys())
        # Omitted keys are sorted for deterministic source-to-candidate lossiness evidence.
        omitted: list[str] = sorted(section_key for section_key in sections if section_key not in included)
        return omitted

    def count_omitted_sections(self, rows: list[JsonObject]) -> JsonObject:
        """Count omitted/sidecar-preserved source sections across per-source rows."""
        # Counts keep aggregate lossiness visible instead of hiding it behind parse-back equality.
        counts: dict[str, int] = {}
        # Row loop is annotated for policy-compliant parsing.
        row: JsonObject
        for row in rows:
            # Section name is one omitted source section from this row.
            section_name: str
            for section_name in row["omitted_or_sidecar_preserved_source_sections"]:
                counts[section_name] = counts.get(section_name, 0) + 1
        return counts

    def build_selected_sources(self, reviewed_entries: dict[str, JsonObject]) -> JsonObject:
        """Build selected-source evidence for exact subset proof."""
        return {
            "slice_name": SLICE_NAME,
            "selected_entry_count": len(SELECTED_SOURCES),
            "selected_sources": list(SELECTED_SOURCES),
            "exact_subset_only": True,
            "no_extra_sources": True,
            "reviewed_inventory_values": [reviewed_entries[source_path] for source_path in SELECTED_SOURCES],
            "authority_change": False,
            "candidate_only": True,
            "corpus_dry_run": True,
            "bounded_subset_only": True,
        }

    def build_per_source_results(self, rows: list[JsonObject]) -> JsonObject:
        """Build per-source result evidence."""
        return {
            "slice_name": SLICE_NAME,
            "selected_entry_count": len(rows),
            "results": rows,
            "aggregate_counts": self.aggregate_counts(rows),
            "authority_change": False,
            "candidate_only": True,
            "corpus_dry_run": True,
            "bounded_subset_only": True,
        }

    def aggregate_counts(self, rows: list[JsonObject]) -> JsonObject:
        """Return aggregate counts derived from per-source rows."""
        return {
            "selected_entry_count": len(rows),
            "by_reviewed_category": self.count_by(rows, ["reviewed_inventory", "category_candidate"]),
            "by_reviewed_disposition": self.count_by(rows, ["reviewed_inventory", "disposition_candidate"]),
            "by_authority_effect": self.count_by(rows, ["reviewed_inventory", "authority_effect"]),
            "by_automatic_conversion_eligibility_candidate": self.count_bool(rows, ["reviewed_inventory", "automatic_conversion_eligibility_candidate"]),
            "by_entry_type": self.count_key(rows, "entry_type"),
            "by_final_outcome": self.count_key(rows, "final_outcome"),
            "generated_candidate_objects": sum(1 for row in rows if row["candidate_object_path"] is not None),
            "skipped_or_excluded_entries": sum(1 for row in rows if row["skipped_or_excluded_reason"] is not None),
            "generated_projections": sum(1 for row in rows if row["projection_status"] == "generated"),
            "omitted_blocked_skipped_projections": sum(1 for row in rows if row["projection_status"] != "generated"),
            "parseback_comparisons_run": sum(1 for row in rows if row["parseback_status"] is not None),
            "missing_status_findings": sum(1 for row in rows if row["status_missing"]),
            "status_casing_normalization_sensitive_findings": sum(
                1 for row in rows if row["status_casing_or_text_would_normalize"]
            ),
            "source_only_provenance_blockers": sum(1 for row in rows if row["entry_type"] == "source_provenance_draft"),
            "index_control_surface_exclusions": sum(1 for row in rows if row["entry_type"] == "index_control_surface"),
            "manual_review_blockers": sum(1 for row in rows if row["manual_review_required"]),
            "sidecar_provenance_required": len(rows),
            "omitted_sidecar_preserved_source_sections_total": sum(
                len(row["omitted_or_sidecar_preserved_source_sections"]) for row in rows
            ),
            "by_omitted_sidecar_preserved_source_section": self.count_omitted_sections(rows),
        }

    def count_key(self, rows: list[JsonObject], key: str) -> JsonObject:
        """Count rows by a direct key."""
        # Counts are string-keyed for deterministic JSON evidence.
        counts: dict[str, int] = {}
        # Row loop is annotated for policy-compliant parsing.
        row: JsonObject
        for row in rows:
            counts[str(row[key])] = counts.get(str(row[key]), 0) + 1
        return counts

    def count_by(self, rows: list[JsonObject], path: list[str]) -> JsonObject:
        """Count rows by a nested string path."""
        # Counts are string-keyed for deterministic JSON evidence.
        counts: dict[str, int] = {}
        # Row loop is annotated for policy-compliant parsing.
        row: JsonObject
        for row in rows:
            # Current nested value starts at the row object.
            value: object = row
            # Path part walks to the target nested value.
            part: str
            for part in path:
                value = value[part]  # type: ignore[index]
            counts[str(value)] = counts.get(str(value), 0) + 1
        return counts

    def count_bool(self, rows: list[JsonObject], path: list[str]) -> JsonObject:
        """Count rows by a nested boolean path."""
        # Boolean counts are represented by explicit true/false keys.
        counts: dict[str, int] = {"true": 0, "false": 0}
        # Row loop is annotated for policy-compliant parsing.
        row: JsonObject
        for row in rows:
            # Current nested value starts at the row object.
            value: object = row
            # Path part walks to the target nested value.
            part: str
            for part in path:
                value = value[part]  # type: ignore[index]
            counts["true" if value else "false"] += 1
        return counts

    def build_conflict_lossiness_report(self, rows: list[JsonObject]) -> JsonObject:
        """Build aggregate conflict/lossiness evidence."""
        return {
            "slice_name": SLICE_NAME,
            "summary": self.aggregate_counts(rows),
            "per_source_findings": [
                {
                    "source_path": row["source_path"],
                    "final_outcome": row["final_outcome"],
                    "lossiness_conflict_findings": row["lossiness_conflict_findings"],
                    "omitted_or_sidecar_preserved_source_sections": row["omitted_or_sidecar_preserved_source_sections"],
                    "source_to_candidate_complete": row["source_to_candidate_complete"],
                    "blockers": row["blockers"],
                }
                for row in rows
            ],
            "slice_2_missing_status_preserved": True,
            "slice_3_wrapped_list_regression_preserved": True,
            "projection_equality_does_not_resolve_blockers": True,
            "projection_equality_does_not_imply_source_to_candidate_completeness": True,
            "accepted_source_status_not_json_authority": True,
            "authority_change": False,
            "candidate_only": True,
        }

    def build_projection_parseback_report(self, parseback_rows: list[JsonObject]) -> JsonObject:
        """Build projection parse-back report evidence."""
        return {
            "slice_name": SLICE_NAME,
            "parseback_count": len(parseback_rows),
            "parseback_results": parseback_rows,
            "all_parsebacks_generated_projection_only": all(
                row["parseback_source"] == "generated_projection_only" for row in parseback_rows
            ),
            "all_semantic_equal_for_candidate_fields": all(
                row["semantic_equal_for_candidate_fields"] for row in parseback_rows
            ),
            "authority_change": False,
            "candidate_only": True,
        }

    def build_skipped_or_blocked_sources(self, rows: list[JsonObject]) -> JsonObject:
        """Build skipped/blocked source evidence."""
        # Skipped rows include explicit skip reasons or manual blockers.
        skipped_rows: list[JsonObject] = [
            row for row in rows if row["skipped_or_excluded_reason"] is not None or row["manual_review_required"]
        ]
        return {
            "slice_name": SLICE_NAME,
            "skipped_or_blocked_count": len(skipped_rows),
            "sources": skipped_rows,
            "authority_change": False,
            "candidate_only": True,
        }

    def build_manifest(
        self,
        selected_sources: JsonObject,
        per_source_results: JsonObject,
        conflict_lossiness_report: JsonObject,
        projection_parseback_report: JsonObject,
        skipped_or_blocked_sources: JsonObject,
    ) -> JsonObject:
        """Build Slice 4 manifest evidence."""
        return {
            "slice_name": SLICE_NAME,
            "mode": "candidate-only bounded subset corpus dry run",
            "authority_mode": "candidate/evidence only",
            "authority_change": False,
            "candidate_only": True,
            "source_mutation": False,
            "schema_change": False,
            "database_authority": False,
            "conversion_completed_as_authoritative_record": False,
            "corpus_dry_run": True,
            "bounded_subset_only": True,
            "bulk_migration": False,
            "cutover_authorized": False,
            "generated_at": self.generated_at,
            "selected_entry_count": len(SELECTED_SOURCES),
            "selected_sources": list(SELECTED_SOURCES),
            "aggregate_counts": per_source_results["aggregate_counts"],
            "source_refs": {
                "brief": "docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md",
                "hermes_decision": "docs/reviews/hermes-decision.20260711.152000_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
                "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md",
                "reviewed_inventory": "dev/adr-json-authority-inventory-review-overrides-slice-1/reviewed-inventory.json",
                "slice_2_acceptance": "docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md",
                "slice_3_acceptance": "docs/reviews/hermes-acceptance.20260711.151000_adr-json-authority-projectable-messy-canary-slice-3.md",
            },
            "artifacts": {
                "manifest": f"{TARGET_PATH}/manifest.json",
                "selected_sources": f"{TARGET_PATH}/selected-sources.json",
                "per_source_results": f"{TARGET_PATH}/per-source-results.json",
                "conflict_lossiness_report": f"{TARGET_PATH}/conflict-lossiness-report.json",
                "projection_parseback_report": f"{TARGET_PATH}/projection-parseback-report.json",
                "skipped_or_blocked_sources": f"{TARGET_PATH}/skipped-or-blocked-sources.json",
                "candidate_objects_dir": f"{TARGET_PATH}/candidate-objects/",
                "generated_projections_dir": f"{TARGET_PATH}/generated-projections/",
                "sidecars_dir": f"{TARGET_PATH}/sidecars/",
            },
            "artifact_hashes": {
                "selected_sources": DocumentRecord.payload_hash(selected_sources),
                "per_source_results": DocumentRecord.payload_hash(per_source_results),
                "conflict_lossiness_report": DocumentRecord.payload_hash(conflict_lossiness_report),
                "projection_parseback_report": DocumentRecord.payload_hash(projection_parseback_report),
                "skipped_or_blocked_sources": DocumentRecord.payload_hash(skipped_or_blocked_sources),
            },
            "validation_command_summary": {
                "exactly_six_sources": "pending closeout validation",
                "source_schema_non_mutation": "pending closeout validation",
                "json_validity": "pending closeout validation",
                "no_database_files": "pending closeout validation",
                "aggregate_counts_match_per_source": "pending closeout validation",
            },
        }

    def write_artifacts(
        self,
        manifest: JsonObject,
        selected_sources: JsonObject,
        per_source_results: JsonObject,
        conflict_lossiness_report: JsonObject,
        projection_parseback_report: JsonObject,
        skipped_or_blocked_sources: JsonObject,
        candidate_objects: dict[str, JsonObject],
        sidecars: dict[str, JsonObject],
    ) -> None:
        """Write deterministic Slice 4 evidence artifacts."""
        self.paths.manifest.write_text(DocumentRecord.canonical_payload_text(manifest), encoding="utf-8")
        self.paths.selected_sources.write_text(DocumentRecord.canonical_payload_text(selected_sources), encoding="utf-8")
        self.paths.per_source_results.write_text(DocumentRecord.canonical_payload_text(per_source_results), encoding="utf-8")
        self.paths.conflict_lossiness_report.write_text(
            DocumentRecord.canonical_payload_text(conflict_lossiness_report), encoding="utf-8"
        )
        self.paths.projection_parseback_report.write_text(
            DocumentRecord.canonical_payload_text(projection_parseback_report), encoding="utf-8"
        )
        self.paths.skipped_or_blocked_sources.write_text(
            DocumentRecord.canonical_payload_text(skipped_or_blocked_sources), encoding="utf-8"
        )
        # Candidate object files are written only for generated candidates.
        source_path: str
        candidate_object: JsonObject
        for source_path, candidate_object in candidate_objects.items():
            # Candidate path keeps each source artifact under the Slice 4 evidence directory.
            candidate_path: Path = self.paths.candidate_objects_dir / f"{self.artifact_stem(source_path)}.json"
            candidate_path.write_text(DocumentRecord.canonical_payload_text(candidate_object), encoding="utf-8")
        # Sidecar files are written for every selected source.
        sidecar: JsonObject
        for source_path, sidecar in sidecars.items():
            # Sidecar path keeps per-source provenance under the Slice 4 evidence directory.
            sidecar_path: Path = self.paths.sidecars_dir / f"{self.artifact_stem(source_path)}.sidecar.json"
            sidecar_path.write_text(DocumentRecord.canonical_payload_text(sidecar), encoding="utf-8")

    def artifact_stem(self, source_path: str) -> str:
        """Return a deterministic filesystem-safe artifact stem for a source path."""
        return source_path.replace("/", "__").replace(".", "_")


def run_adr_json_authority_corpus_dry_run(repo_root: Path) -> AdrCorpusDryRunResult:
    """Run the Slice 4 ADR JSON authority corpus dry-run inventory."""
    return AdrCorpusDryRunRunner(paths=AdrCorpusDryRunPaths(repo_root=repo_root)).run()
