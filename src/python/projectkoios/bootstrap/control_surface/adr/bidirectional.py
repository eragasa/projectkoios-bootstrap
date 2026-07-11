from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from projectkoios.bootstrap.control_surface.adr.manifest import PilotManifestBuilder
from projectkoios.bootstrap.control_surface.adr.markdown import AdrMarkdownRecordParser, AdrProjectionRenderer
from projectkoios.bootstrap.control_surface.adr.models import PilotAdrSourceConfig
from projectkoios.bootstrap.control_surface.adr.validation import AdrRecordValidator
from projectkoios.bootstrap.control_surface.documents import DocumentRecord
from projectkoios.bootstrap.schema.models import JsonObject


@dataclass(frozen=True, slots=True)
class AdrBidirectionalCanaryPaths:
    """Filesystem paths for the one-source ADR bidirectional object canary.

    Args:
        repo_root: Repository root.
        source_config: Exact canary source configuration.
    """

    repo_root: Path
    source_config: PilotAdrSourceConfig = PilotAdrSourceConfig(
        source_path="docs/adr/adr.json-schemas.draft.md",
        legacy_filename_status_suffix=".draft",
        record_id="adr.json-schemas",
        slug="json-schemas",
        delegated_operator="pi",
        source_date="20260702.213000Z",
    )

    @property
    def source_adr(self) -> Path:
        """Return source Markdown ADR path."""
        return self.repo_root / self.source_config.source_path

    @property
    def schema(self) -> Path:
        """Return current ADR schema path."""
        return self.repo_root / "docs" / "schemas" / "adr.schema.json"

    @property
    def target_dir(self) -> Path:
        """Return canary evidence directory."""
        return self.repo_root / "dev" / "adr-bidirectional-object-canary-slice-0"

    @property
    def bidirectional_object(self) -> Path:
        """Return candidate object envelope path."""
        return self.target_dir / "adr.json-schemas.bidirectional-object.json"

    @property
    def markdown_projection(self) -> Path:
        """Return generated Markdown projection path."""
        return self.target_dir / "adr.json-schemas.projected.md"

    @property
    def conversion_evidence(self) -> Path:
        """Return conversion evidence path."""
        return self.target_dir / "conversion-evidence.json"

    @property
    def manifest(self) -> Path:
        """Return canary manifest path."""
        return self.target_dir / "manifest.json"


@dataclass(frozen=True, slots=True)
class AdrBidirectionalCanaryResult:
    """Result of generating one candidate ADR bidirectional object."""

    envelope: JsonObject
    projection_record: JsonObject
    conversion_evidence: JsonObject
    manifest: JsonObject


@dataclass(frozen=True, slots=True)
class AdrBidirectionalCanaryRunner:
    """Generate evidence for a candidate AdrBidirectionalObject envelope.

    The runner is intentionally file/projection evidence only. It does not
    mutate `docs/adr/`, publish schemas, ingest hand-authored Markdown, or use a
    database/storage backend.
    """

    paths: AdrBidirectionalCanaryPaths
    timestamp: str = "20260711.134200Z"

    def run(self) -> AdrBidirectionalCanaryResult:
        """Generate deterministic canary evidence artifacts.

        Returns:
            Candidate envelope, generated projection parse-back record,
            conversion evidence, and manifest.
        """
        self.paths.target_dir.mkdir(parents=True, exist_ok=True)
        # Source text before generation is the mutation-proof baseline.
        source_before: str = self.paths.source_adr.read_text(encoding="utf-8")
        # Schema text is hashed as the content-validation authority input.
        schema_text: str = self.paths.schema.read_text(encoding="utf-8")
        # Source hash identifies the exact canary Markdown input.
        source_hash: str = PilotManifestBuilder.hash_text(source_before)
        # Schema hash identifies the unchanged ADR schema used for validation.
        schema_hash: str = PilotManifestBuilder.hash_text(schema_text)

        # Parser maps only the approved canary source into ADR schema content.
        parser: AdrMarkdownRecordParser = AdrMarkdownRecordParser(source_config=self.paths.source_config)
        content: JsonObject
        mapping: JsonObject
        content, mapping = parser.parse_source_record(source_before)
        # Validator proves the envelope content conforms before projection.
        validator: AdrRecordValidator = AdrRecordValidator()
        validator.validate(content)

        # Canonical content JSON is embedded for deterministic parse-back.
        content_json: str = DocumentRecord.canonical_payload_text(content)
        # Projection manifest supplies generated-only authority metadata.
        projection_manifest: JsonObject = self.build_projection_manifest(content, source_hash, schema_hash, validator.schema_id())
        # Projection is evidence under dev/ and never overwrites source Markdown.
        projection: str = self.render_projection(content, projection_manifest, content_json)
        # Projection hash lets reviewers detect generated artifact drift.
        projection_hash: str = PilotManifestBuilder.hash_text(projection)
        # Projection record is parsed only from generated Markdown evidence.
        projection_record: JsonObject = parser.parse_projection_record(projection)
        validator.validate(projection_record)
        # Semantic equality is the canary's bounded bidirectional proof.
        semantic_equal: bool = content == projection_record
        if not semantic_equal:
            raise AssertionError("Generated projection parse-back did not equal candidate content")

        # Source text after generation must remain byte-for-byte unchanged.
        source_after: str = self.paths.source_adr.read_text(encoding="utf-8")
        # After hash is recorded alongside the before hash as mutation proof.
        source_hash_after: str = PilotManifestBuilder.hash_text(source_after)
        if source_before != source_after:
            raise AssertionError("Source ADR Markdown was mutated during canary generation")

        # Envelope groups content, classification, sidecar, validation, and policy.
        envelope: JsonObject = self.build_envelope(
            content=content,
            mapping=mapping,
            source_hash=source_hash,
            source_hash_after=source_hash_after,
            schema_hash=schema_hash,
            projection_hash=projection_hash,
            schema_id=validator.schema_id(),
            semantic_equal=semantic_equal,
        )
        # Conversion evidence gives a concise sidecar-oriented review surface.
        conversion_evidence: JsonObject = self.build_conversion_evidence(envelope)
        # Manifest indexes the one-directory canary evidence set.
        manifest: JsonObject = self.build_manifest(envelope, conversion_evidence)
        self.write_artifacts(envelope, projection, conversion_evidence, manifest)
        return AdrBidirectionalCanaryResult(
            envelope=envelope,
            projection_record=projection_record,
            conversion_evidence=conversion_evidence,
            manifest=manifest,
        )

    def build_projection_manifest(
        self,
        content: JsonObject,
        source_hash: str,
        schema_hash: str,
        schema_id: str,
    ) -> JsonObject:
        """Build renderer metadata for the generated projection."""
        # Content hash ties the projection metadata to the candidate content.
        content_hash: str = DocumentRecord.payload_hash(content)
        return {
            "canary": {
                "name": "adr-bidirectional-object-canary-slice-0",
                "status": "candidate-object-evidence",
            },
            "authority_mode": "candidate-evidence-only-not-repository-authority",
            "source_adr": {
                "path": self.paths.source_config.source_path,
                "content_hash": source_hash,
                "status": "draft",
                "date": self.paths.source_config.source_date,
            },
            "schema": {
                "path": "docs/schemas/adr.schema.json",
                "id": schema_id,
                "content_hash": schema_hash,
            },
            "json_checkpoint": {
                "path": "dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json#/content",
                "content_hash": content_hash,
            },
            "markdown_projection": {
                "path": "dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.projected.md",
                "status": "generated-projection-evidence-only",
            },
            "generation": {
                "method": "projectkoios.bootstrap.control_surface.adr.bidirectional.AdrBidirectionalCanaryRunner.run",
            },
            "conflict_rule": "Generated projection parse-back only; source Markdown remains unmutated and no hand-authored Markdown ingest is implemented.",
        }

    def render_projection(self, content: JsonObject, manifest: JsonObject, content_json: str) -> str:
        """Render projection evidence with an explicit generated-only marker."""
        # Base projection reuses the existing deterministic generated renderer.
        projection: str = AdrProjectionRenderer().render(content, manifest, content_json)
        # Marker distinguishes this artifact from hand-authored ADR Markdown.
        marker: str = "<!-- ADR BIDIRECTIONAL OBJECT CANARY: generated projection evidence only; source Markdown is not ingested or overwritten. -->\n"
        return marker + projection

    def build_envelope(
        self,
        content: JsonObject,
        mapping: JsonObject,
        source_hash: str,
        source_hash_after: str,
        schema_hash: str,
        projection_hash: str,
        schema_id: str,
        semantic_equal: bool,
    ) -> JsonObject:
        """Build the candidate AdrBidirectionalObject envelope."""
        # Preserved source-only values become sidecar evidence outside content.
        preserved: object = mapping["preserved_outside_schema"]
        if not isinstance(preserved, dict):
            raise TypeError("preserved_outside_schema must be an object")
        return {
            "object_type": "AdrBidirectionalObject",
            "object_version": "candidate-0",
            "authority_mode": "candidate-evidence-only-not-repository-authority",
            "content": content,
            "classification": {
                "category": "template_schema_contract",
                "secondary_aspect": "architecture_blueprint",
                "source_role": "canary_source",
                "source_authority_effect": "none",
                "disposition_note": "Envelope metadata only; does not change source status, filename, lifecycle authority, or schema authority.",
            },
            "markdown_projection": {
                "path": "dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.projected.md",
                "sha256": projection_hash,
                "mode": "generated_projection_evidence_only",
                "parse_back_scope": "generated_projection_only",
                "hand_authored_markdown_ingest": False,
            },
            "conversion_evidence": {
                "source_mutated": False,
                "source_hash_before": source_hash,
                "source_hash_after": source_hash_after,
                "schema_valid": True,
                "projection_parse_back_semantic_equal": semantic_equal,
                "omitted_from_content_preserved_in_sidecar": [
                    "routing",
                    "links.related",
                    "source.date",
                    "source.filename_status_suffix",
                ],
                "normalized_fields": mapping["normalized_fields"],
                "inferred_fields": mapping["inferred_fields"],
                "lossiness": "unsupported source fields preserved outside content in sidecar/evidence",
                "notes": [
                    "Candidate object evidence only; source Markdown remains the source Markdown.",
                    "Classification and disposition metadata are outside content.",
                    "No docs/schemas publication or mutation is performed.",
                ],
            },
            "source_refs": {
                "source_markdown": {
                    "path": self.paths.source_config.source_path,
                    "sha256": source_hash,
                    "observed_status": content["status"],
                    "observed_status_casing": str(content["status"]),
                    "observed_date": self.paths.source_config.source_date,
                    "legacy_filename_status_suffix": self.paths.source_config.legacy_filename_status_suffix,
                },
                "schema": {
                    "path": "docs/schemas/adr.schema.json",
                    "id": schema_id,
                    "sha256": schema_hash,
                },
                "projection": {
                    "path": "dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.projected.md",
                    "sha256": projection_hash,
                },
                "architecture": {
                    "path": "docs/architecture/architecture.adr-bidirectional-objects.md",
                },
                "brief": {
                    "path": "docs/plans/implementation-brief.20260711.134200_adr-bidirectional-object-canary-slice-0.md",
                },
            },
            "sidecar": {
                "scope": "canary-evidence-only-not-published-schema",
                "source_path": self.paths.source_config.source_path,
                "source_hash": source_hash,
                "observed_source_status_text": content["status"],
                "observed_source_date": self.paths.source_config.source_date,
                "routing": preserved["routing"],
                "routing_section": preserved["routing_section"],
                "links.related": preserved["links.related"],
            },
            "validation": {
                "content_schema_valid": True,
                "schema_path": "docs/schemas/adr.schema.json",
                "schema_hash": schema_hash,
                "projection_parse_back_semantic_equal": semantic_equal,
                "source_mutation_proof": {
                    "source_hash_before": source_hash,
                    "source_hash_after": source_hash_after,
                    "mutated": source_hash != source_hash_after,
                },
                "no_docs_adr_mutation_intended": True,
                "no_docs_schemas_mutation_intended": True,
                "no_mutable_database_files_created": True,
            },
            "conflict_policy": {
                "json_vs_markdown": "projection_only_no_ingest",
                "hand_authored_markdown_ingest": False,
                "bulk_migration": False,
                "source_overwrite": False,
                "unsupported_fields": "preserve_in_sidecar_evidence",
            },
        }

    def build_conversion_evidence(self, envelope: JsonObject) -> JsonObject:
        """Build concise evidence parallel to the candidate envelope."""
        return {
            "status": "candidate-object-evidence-only",
            "source": envelope["source_refs"]["source_markdown"],
            "schema": envelope["source_refs"]["schema"],
            "projection": envelope["source_refs"]["projection"],
            "classification_outside_content": "classification" not in envelope["content"],
            "sidecar_preserves": {
                "routing": envelope["sidecar"]["routing"],
                "links.related": envelope["sidecar"]["links.related"],
                "observed_source_status_text": envelope["sidecar"]["observed_source_status_text"],
                "observed_source_date": envelope["sidecar"]["observed_source_date"],
            },
            "validation": envelope["validation"],
            "conflict_policy": envelope["conflict_policy"],
            "authority_note": "Candidate object evidence only; does not change ADR source authority, schema authority, storage authority, or lifecycle status.",
        }

    def build_manifest(self, envelope: JsonObject, conversion_evidence: JsonObject) -> JsonObject:
        """Build evidence manifest for the canary directory."""
        return {
            "canary": {
                "name": "adr-bidirectional-object-canary-slice-0",
                "status": "candidate-object-evidence-only",
                "source_count": 1,
            },
            "authority_mode": envelope["authority_mode"],
            "source": envelope["source_refs"]["source_markdown"],
            "artifacts": {
                "bidirectional_object": "dev/adr-bidirectional-object-canary-slice-0/adr.json-schemas.bidirectional-object.json",
                "markdown_projection": envelope["markdown_projection"]["path"],
                "conversion_evidence": "dev/adr-bidirectional-object-canary-slice-0/conversion-evidence.json",
                "manifest": "dev/adr-bidirectional-object-canary-slice-0/manifest.json",
            },
            "hashes": {
                "source": envelope["source_refs"]["source_markdown"]["sha256"],
                "schema": envelope["source_refs"]["schema"]["sha256"],
                "projection": envelope["source_refs"]["projection"]["sha256"],
                "content": DocumentRecord.payload_hash(envelope["content"]),
                "conversion_evidence": DocumentRecord.payload_hash(conversion_evidence),
            },
            "boundaries": {
                "docs_adr_mutation": False,
                "docs_schemas_mutation": False,
                "database_or_storage_authority": False,
                "mutable_database_files": False,
                "bulk_migration": False,
                "hand_authored_markdown_ingest": False,
            },
        }

    def write_artifacts(
        self,
        envelope: JsonObject,
        projection: str,
        conversion_evidence: JsonObject,
        manifest: JsonObject,
    ) -> None:
        """Write deterministic canary evidence artifacts."""
        self.paths.bidirectional_object.write_text(DocumentRecord.canonical_payload_text(envelope), encoding="utf-8")
        self.paths.markdown_projection.write_text(projection, encoding="utf-8")
        self.paths.conversion_evidence.write_text(
            DocumentRecord.canonical_payload_text(conversion_evidence), encoding="utf-8"
        )
        self.paths.manifest.write_text(DocumentRecord.canonical_payload_text(manifest), encoding="utf-8")


def run_adr_bidirectional_object_canary(repo_root: Path) -> AdrBidirectionalCanaryResult:
    """Run the ADR bidirectional object canary slice."""
    return AdrBidirectionalCanaryRunner(paths=AdrBidirectionalCanaryPaths(repo_root=repo_root)).run()
