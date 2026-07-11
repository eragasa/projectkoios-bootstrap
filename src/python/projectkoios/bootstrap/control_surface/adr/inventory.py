from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.documents import DocumentRecord
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrInventoryPaths:
    """Filesystem paths for the review-only ADR authority inventory."""

    repo_root: Path

    @property
    def source_dir(self) -> Path:
        """Return ADR Markdown source directory."""
        return self.repo_root / "docs" / "adr"

    @property
    def schema_dir(self) -> Path:
        """Return repository schema directory checked for non-mutation."""
        return self.repo_root / "docs" / "schemas"

    @property
    def target_dir(self) -> Path:
        """Return review-only inventory evidence directory."""
        return self.repo_root / "dev" / "adr-json-authority-inventory-classification-slice-0"

    @property
    def manifest(self) -> Path:
        """Return manifest path."""
        return self.target_dir / "manifest.json"

    @property
    def source_inventory(self) -> Path:
        """Return per-source inventory path."""
        return self.target_dir / "source-inventory.json"

    @property
    def classification_summary(self) -> Path:
        """Return classification summary path."""
        return self.target_dir / "classification-summary.json"


@dataclass(frozen=True, slots=True)
class AdrInventoryResult:
    """Generated review-only ADR inventory result."""

    manifest: JsonObject
    source_inventory: JsonObject
    classification_summary: JsonObject


@dataclass(frozen=True, slots=True)
class AdrInventoryRunner:
    """Inspect and classify ADR Markdown sources without changing authority."""

    paths: AdrInventoryPaths
    generated_at: str = "20260711.141000Z"

    def run(self) -> AdrInventoryResult:
        """Generate deterministic review-only inventory artifacts."""
        self.paths.target_dir.mkdir(parents=True, exist_ok=True)
        # Source entries are sorted by path for stable manifest output.
        entries: list[JsonObject] = [self.inspect_file(path) for path in self.source_paths()]
        # Inventory groups the per-file records with review-only markers.
        source_inventory: JsonObject = self.build_source_inventory(entries)
        # Summary gives reviewers aggregate counts without changing authority.
        classification_summary: JsonObject = self.build_classification_summary(entries)
        # Manifest indexes evidence files and approved authority boundaries.
        manifest: JsonObject = self.build_manifest(entries, source_inventory, classification_summary)
        self.write_artifacts(manifest, source_inventory, classification_summary)
        return AdrInventoryResult(
            manifest=manifest,
            source_inventory=source_inventory,
            classification_summary=classification_summary,
        )

    def source_paths(self) -> tuple[Path, ...]:
        """Return inspected ADR Markdown and control surface paths."""
        # All top-level Markdown files in docs/adr are in the Phase 0 inventory.
        paths: list[Path] = sorted(self.paths.source_dir.glob("*.md"))
        return tuple(paths)

    def inspect_file(self, path: Path) -> JsonObject:
        """Inspect one source Markdown file for review-only classification."""
        # Relative path is the stable source identifier in evidence.
        relative_path: str = path.relative_to(self.paths.repo_root).as_posix()
        # Source text is read once and never written back.
        source_text: str = path.read_text(encoding="utf-8")
        # Source hash proves the exact inspected content.
        source_hash: str = PilotManifestBuilder.hash_text(source_text)
        # Parsed title is best-effort evidence, not an authority change.
        title: str | None = self.parse_title(source_text)
        # Status evidence keeps observed text separate from normalized candidate.
        observed_status: str | None = self.parse_status(source_text)
        # File kind separates ADR-like sources from index/control surfaces.
        file_kind: str = self.file_kind(path, title)
        # Normalized status is only a review candidate.
        normalized_status: str | None = self.normalized_status_candidate(observed_status)
        # Warnings explain uncertainty and blockers for automatic conversion.
        warnings: list[str] = self.warnings(file_kind, title, observed_status, normalized_status)
        # Category is candidate evidence derived from path/title/content hints.
        category: str = self.category_candidate(relative_path, title, source_text, file_kind)
        # Disposition candidate follows category and parse confidence.
        disposition: str = self.disposition_candidate(file_kind, category, warnings)
        # Authority effect candidate is review-only and never final in this slice.
        authority_effect: str = self.authority_effect_candidate(disposition, category)
        # Review flags call out owner/domain and manual review needs.
        review_flags: JsonObject = self.owner_domain_review_flags(category, warnings)
        # Auto-conversion eligibility is conservative evidence only.
        eligible: bool = self.auto_conversion_eligible(file_kind, normalized_status, warnings, category)
        # Blocking reasons explain why a file should not auto-convert.
        blocking_reasons: list[str] = self.blocking_reasons(file_kind, normalized_status, warnings, category, eligible)
        return {
            "source_path": relative_path,
            "source_hash": source_hash,
            "file_kind": file_kind,
            "source_title": title,
            "observed_status_text": observed_status,
            "observed_status_casing": observed_status,
            "normalized_status_candidate": normalized_status,
            "status_normalization_required": observed_status != normalized_status if observed_status and normalized_status else False,
            "parse_confidence": self.parse_confidence(file_kind, title, observed_status, warnings),
            "warnings": warnings,
            "uncertainty_flags": self.uncertainty_flags(warnings, category),
            "category_candidate": category,
            "disposition_candidate": disposition,
            "authority_effect": authority_effect,
            "owner_domain_review_flags": review_flags,
            "automatic_conversion_eligibility_candidate": eligible,
            "exclusion_blocking_reasons": blocking_reasons,
            "review_only": True,
        }

    def parse_title(self, source_text: str) -> str | None:
        """Return the first Markdown H1 title when present."""
        # H1 title is the most stable source title cue.
        match: re.Match[str] | None = re.search(r"^#\s+(?P<title>.+?)\s*$", source_text, flags=re.MULTILINE)
        if match is None:
            return None
        return match.group("title")

    def parse_status(self, source_text: str) -> str | None:
        """Return observed status text from frontmatter or Status section."""
        # Frontmatter status appears in newer control/ADR surfaces.
        frontmatter_match: re.Match[str] | None = re.search(r"^status:\s*(?P<status>.+?)\s*$", source_text, flags=re.MULTILINE)
        if frontmatter_match is not None:
            return frontmatter_match.group("status")
        # Status section first non-empty line appears in ADR Markdown sources.
        section_match: re.Match[str] | None = re.search(
            r"^## Status\s*$\n(?P<body>.*?)(?:\n##\s+|\Z)",
            source_text,
            flags=re.MULTILINE | re.DOTALL,
        )
        if section_match is None:
            return None
        # Lines preserve exact text except surrounding whitespace.
        lines: list[str] = [line.strip() for line in section_match.group("body").splitlines() if line.strip()]
        if not lines:
            return None
        return lines[0]

    def file_kind(self, path: Path, title: str | None) -> str:
        """Classify source file kind."""
        # README and index-like files are control surfaces, not ADR records.
        if path.name.lower() in {"readme.md", "index.md"}:
            return "index_or_control_surface"
        if title is None:
            return "other_discovered_control_or_reference_surface"
        if title.lower().startswith("adr"):
            return "adr_source_candidate"
        return "other_discovered_control_or_reference_surface"

    def normalized_status_candidate(self, observed_status: str | None) -> str | None:
        """Return safe lower-case lifecycle candidate when inferable."""
        if observed_status is None:
            return None
        # Lowercase normalization is evidence only; source is not rewritten.
        normalized: str = observed_status.strip().lower()
        # Common Markdown emphasis is stripped only for candidate comparison.
        normalized = normalized.strip("`*_ ")
        return normalized or None

    def warnings(
        self,
        file_kind: str,
        title: str | None,
        observed_status: str | None,
        normalized_status: str | None,
    ) -> list[str]:
        """Return parse and conversion warnings for one file."""
        # Warning list accumulates review blockers for this source.
        warnings: list[str] = []
        if file_kind != "adr_source_candidate":
            warnings.append("not_adr_source_candidate")
        if title is None:
            warnings.append("missing_h1_title")
        if observed_status is None:
            warnings.append("missing_observed_status")
        if observed_status and normalized_status and observed_status != normalized_status:
            warnings.append("status_casing_or_text_would_normalize")
        if normalized_status and normalized_status not in self.known_status_candidates():
            warnings.append("non_canonical_or_extended_status_candidate")
        return warnings

    def known_status_candidates(self) -> set[str]:
        """Return known status candidates for warning purposes."""
        return {
            "proposal",
            "draft",
            "accepted",
            "active",
            "superseded",
            "accepted-staged-direction",
        }

    def category_candidate(self, relative_path: str, title: str | None, source_text: str, file_kind: str) -> str:
        """Return review-only hierarchy category candidate."""
        if file_kind == "index_or_control_surface":
            return "index_or_control_surface"
        # Classification uses conservative filename/title/content hints.
        haystack: str = f"{relative_path}\n{title or ''}\n{source_text[:2000]}".lower()
        if any(token in haystack for token in ["template", "schema", "contract", "json schema"]):
            return "template_schema_contract"
        if any(token in haystack for token in ["workflow", "implementation", "handoff", "verification"]):
            return "implementation_workflow_support"
        if any(token in haystack for token in ["policy", "process", "lifecycle", "protocol", "review rule"]):
            return "policy_process"
        if any(token in haystack for token in ["architecture", "namespace", "topology", "boundary"]):
            return "architecture_blueprint"
        if any(token in haystack for token in ["product", "future", "training", "agent production"]):
            return "product_future_system_draft"
        if "draft" in relative_path:
            return "source_provenance"
        return "unknown_requires_review"

    def disposition_candidate(self, file_kind: str, category: str, warnings: list[str]) -> str:
        """Return review-only disposition candidate."""
        if file_kind == "index_or_control_surface":
            return "index_or_control_surface"
        if category == "product_future_system_draft":
            return "domain_review_required"
        if warnings:
            return "manual_review_required"
        if category in {"source_provenance", "unknown_requires_review"}:
            return "source_only_provenance_candidate"
        return "json_authority_candidate"

    def authority_effect_candidate(self, disposition: str, category: str) -> str:
        """Return review-only authority effect candidate."""
        if disposition == "index_or_control_surface":
            return "none"
        if disposition == "domain_review_required" or category == "product_future_system_draft":
            return "domain_review_required"
        if disposition == "manual_review_required":
            return "candidate"
        if disposition == "source_only_provenance_candidate":
            return "excluded"
        return "proposed_authority"

    def owner_domain_review_flags(self, category: str, warnings: list[str]) -> JsonObject:
        """Return manual owner/domain review flags."""
        return {
            "owner_review_required": bool(warnings),
            "domain_review_required": category == "product_future_system_draft",
            "manual_review_required": bool(warnings) or category in {"unknown_requires_review", "product_future_system_draft"},
        }

    def auto_conversion_eligible(
        self,
        file_kind: str,
        normalized_status: str | None,
        warnings: list[str],
        category: str,
    ) -> bool:
        """Return conservative automatic conversion eligibility candidate."""
        if file_kind != "adr_source_candidate":
            return False
        if warnings:
            return False
        if normalized_status not in self.known_status_candidates():
            return False
        if category in {"product_future_system_draft", "unknown_requires_review"}:
            return False
        return True

    def blocking_reasons(
        self,
        file_kind: str,
        normalized_status: str | None,
        warnings: list[str],
        category: str,
        eligible: bool,
    ) -> list[str]:
        """Return exclusion or blocking reasons for automatic conversion."""
        if eligible:
            return []
        # Reasons combine structural, status, warning, and domain blockers.
        reasons: list[str] = []
        if file_kind != "adr_source_candidate":
            reasons.append("not_adr_source_candidate")
        if normalized_status is None:
            reasons.append("missing_status")
        elif normalized_status not in self.known_status_candidates():
            reasons.append("status_requires_review")
        reasons.extend(warnings)
        if category == "product_future_system_draft":
            reasons.append("domain_review_required")
        if category == "unknown_requires_review":
            reasons.append("category_requires_review")
        return sorted(set(reasons))

    def parse_confidence(self, file_kind: str, title: str | None, observed_status: str | None, warnings: list[str]) -> str:
        """Return parse confidence label."""
        if title is None and observed_status is None:
            return "failed"
        if file_kind != "adr_source_candidate":
            return "medium"
        if warnings:
            return "medium"
        return "high"

    def uncertainty_flags(self, warnings: list[str], category: str) -> list[str]:
        """Return uncertainty flags for reviewers."""
        # Unknown category is an uncertainty even if parsing succeeded.
        flags: list[str] = list(warnings)
        if category == "unknown_requires_review":
            flags.append("category_unknown")
        return sorted(set(flags))

    def build_source_inventory(self, entries: list[JsonObject]) -> JsonObject:
        """Build source-inventory evidence object."""
        return {
            "slice_name": "adr-json-authority-inventory-classification-slice-0",
            "mode": "review-only inventory/classification",
            "authority_change": False,
            "source_mutation_allowed": False,
            "schema_change_allowed": False,
            "database_authority": False,
            "inspected_count": len(entries),
            "entries": entries,
        }

    def build_classification_summary(self, entries: list[JsonObject]) -> JsonObject:
        """Build aggregate classification summary."""
        return {
            "slice_name": "adr-json-authority-inventory-classification-slice-0",
            "mode": "review-only summary",
            "counts": {
                "total": len(entries),
                "by_file_kind": self.count_by(entries, "file_kind"),
                "by_category_candidate": self.count_by(entries, "category_candidate"),
                "by_disposition_candidate": self.count_by(entries, "disposition_candidate"),
                "by_authority_effect": self.count_by(entries, "authority_effect"),
                "by_parse_confidence": self.count_by(entries, "parse_confidence"),
            },
            "automatic_conversion_eligibility_candidate_count": sum(
                1 for entry in entries if entry["automatic_conversion_eligibility_candidate"] is True
            ),
            "review_required_count": sum(
                1 for entry in entries if entry["owner_domain_review_flags"]["manual_review_required"] is True
            ),
            "review_only": True,
        }

    def count_by(self, entries: list[JsonObject], key: str) -> JsonObject:
        """Count entries by one string key."""
        # Counts are sorted before serialization for deterministic summaries.
        counts: dict[str, int] = {}
        entry: JsonObject
        for entry in entries:
            # Missing values are grouped explicitly for reviewer visibility.
            value: str = str(entry.get(key, "missing"))
            counts[value] = counts.get(value, 0) + 1
        return dict(sorted(counts.items()))

    def build_manifest(
        self,
        entries: list[JsonObject],
        source_inventory: JsonObject,
        classification_summary: JsonObject,
    ) -> JsonObject:
        """Build review-only inventory manifest."""
        return {
            "slice_name": "adr-json-authority-inventory-classification-slice-0",
            "mode": "review-only inventory/classification",
            "authority_change": False,
            "source_mutation_allowed": False,
            "schema_change_allowed": False,
            "database_authority": False,
            "generated_at": self.generated_at,
            "inspected_paths": ["docs/adr/*.md"],
            "inspected_count": len(entries),
            "source_refs": {
                "source_adr": "docs/adr/adr.json-authoritative-adr-store.draft.md",
                "source_acceptance": "docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md",
                "source_brief": "docs/plans/implementation-brief.20260711.140700_adr-json-authority-inventory-classification-slice-0.md",
                "source_decision": "docs/reviews/hermes-decision.20260711.141000_adr-json-authority-inventory-classification-slice-0.md",
            },
            "artifacts": {
                "manifest": "dev/adr-json-authority-inventory-classification-slice-0/manifest.json",
                "source_inventory": "dev/adr-json-authority-inventory-classification-slice-0/source-inventory.json",
                "classification_summary": "dev/adr-json-authority-inventory-classification-slice-0/classification-summary.json",
            },
            "artifact_hashes": {
                "source_inventory": DocumentRecord.payload_hash(source_inventory),
                "classification_summary": DocumentRecord.payload_hash(classification_summary),
            },
            "validation_command_summary": {
                "json_validity": "pending closeout validation",
                "source_schema_non_mutation": "pending closeout validation",
                "no_database_files": "pending closeout validation",
                "deterministic_generation": "canonical JSON with sorted source paths and stable generated_at",
            },
            "review_only": True,
        }

    def write_artifacts(
        self,
        manifest: JsonObject,
        source_inventory: JsonObject,
        classification_summary: JsonObject,
    ) -> None:
        """Write deterministic JSON evidence files."""
        self.paths.manifest.write_text(DocumentRecord.canonical_payload_text(manifest), encoding="utf-8")
        self.paths.source_inventory.write_text(DocumentRecord.canonical_payload_text(source_inventory), encoding="utf-8")
        self.paths.classification_summary.write_text(
            DocumentRecord.canonical_payload_text(classification_summary), encoding="utf-8"
        )


def run_adr_json_authority_inventory(repo_root: Path) -> AdrInventoryResult:
    """Run review-only ADR authority inventory/classification."""
    return AdrInventoryRunner(paths=AdrInventoryPaths(repo_root=repo_root)).run()
