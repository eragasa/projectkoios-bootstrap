```json
{
  "title": "Candidate schema sketch: ADR bidirectional JSON-Markdown object",
  "artifact_type": "candidate-schema-sketch",
  "status": "koios-provenance-input-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "ADR bidirectional JSON-Markdown object shape",
  "requires_promotion_by": ["ATHENA", "USER/HERMES"]
}
```

# Candidate schema sketch: ADR bidirectional JSON↔Markdown object

## Authority boundary

This is KOIOS candidate/provenance input only. It is not a published schema, not an architecture decision, not implementation authority, and not repository-wide ADR storage authority.

Do not copy this into `docs/schemas/`, implement it, or use it for bulk migration unless ATHENA/USER promotes it through the normal architecture/spec workflow.

## Source basis

Grounded in:

- `docs/plans/architecture-intake.20260711.131140_adr-bidirectional-json-markdown-objects.md`
- `docs/architecture/architecture.json-adr-storage-topology.md`
- `docs/schemas/adr.schema.json`
- `docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md`
- `docs/implementation/json-document-database-separation.20260711.051951.md`
- `docs/implementation/json-schemas-adr-conformance.20260711.065704.md`
- `dev/adr-json-database-one-adr-pilot/manifest.json` and `mapping.json`
- `dev/adr-json-schemas-conformance/manifest.json`, `mapping.json`, and `conversion-evidence.json`
- KOIOS intake: `workspaces/koios/working/provenance-intake.20260711_adr-rationalization-json-md-object-track.md`

Observed pressure: current ADR Markdown, schema-valid JSON checkpoints, generated Markdown projections, and sidecar evidence already exist, but object/envelope boundaries are not formalized.

## Candidate object model

### Top-level shape

```json
{
  "object_type": "adr_bidirectional_object",
  "object_version": "candidate-0",
  "authority_mode": "candidate_non_authoritative",
  "content": {},
  "markdown_projection": {},
  "conversion_evidence": {},
  "source_refs": [],
  "sidecar": {},
  "validation": {},
  "conflict_policy": {}
}
```

### Field intent

| Field | Candidate meaning | Source basis |
|---|---|---|
| `object_type` | Identifies this as an ADR bidirectional object envelope, not a plain ADR payload. | ATHENA intake asks what the ADR object is. |
| `object_version` | Version for envelope evolution, separate from ADR schema version. | Prior conformance preserved schema vs sidecar separately. |
| `authority_mode` | Explicit authority label: candidate/non-authoritative, active-conformance-record, projection-evidence, etc. | Prior manifests distinguish pilot/evidence/active conformance. |
| `content` | Schema-valid ADR payload compatible with `docs/schemas/adr.schema.json`. | Current ADR schema and conformance slices. |
| `markdown_projection` | Deterministic projection metadata and generated Markdown hash/marker. | One-ADR pilot and conformance projection evidence. |
| `conversion_evidence` | Lossiness, omitted fields, normalized fields, parse warnings, source-to-content mapping. | `mapping.json` and `conversion-evidence.json`. |
| `source_refs` | Original Markdown path/hash/status/date and related source artifacts. | KOIOS provenance requirements and pilot manifests. |
| `sidecar` | Provenance fields not accepted by ADR content schema, e.g. old `routing.*`, `links.related`. | JSON schemas conformance preserved unsupported fields outside record. |
| `validation` | Schema validation, round-trip equality, source-mutation check, DB-file check. | VULCAN reports and KOIOS audits. |
| `conflict_policy` | Rules for JSON vs Markdown divergence and allowed ingest/projection behavior. | Architecture storage topology open questions. |

## Candidate JSON Schema-like sketch

Non-authoritative illustrative shape:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "candidate://projectkoios/bootstrap/adr-bidirectional-object.schema.json",
  "title": "Candidate ADR Bidirectional Object",
  "type": "object",
  "required": [
    "object_type",
    "object_version",
    "authority_mode",
    "content",
    "source_refs",
    "conversion_evidence",
    "validation",
    "conflict_policy"
  ],
  "properties": {
    "object_type": { "const": "adr_bidirectional_object" },
    "object_version": { "type": "string" },
    "authority_mode": {
      "type": "string",
      "enum": [
        "candidate_non_authoritative",
        "pilot_evidence",
        "active_conformance_record",
        "projection_evidence",
        "authority_deferred"
      ]
    },
    "content": {
      "type": "object",
      "description": "ADR payload that should validate against docs/schemas/adr.schema.json; do not add conversion-only fields here without schema authority."
    },
    "source_refs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "kind", "content_hash"],
        "properties": {
          "path": { "type": "string" },
          "kind": { "type": "string" },
          "content_hash": { "type": "string" },
          "status_observed": { "type": ["string", "null"] },
          "date_observed": { "type": ["string", "null"] },
          "role": { "type": "string", "enum": ["source", "projection", "schema", "sidecar", "architecture", "implementation_report", "provenance_note"] }
        }
      }
    },
    "markdown_projection": {
      "type": "object",
      "properties": {
        "mode": { "type": "string", "enum": ["generated_only", "editable_with_ingest", "mixed_explicit_markers", "not_generated"] },
        "path": { "type": ["string", "null"] },
        "content_hash": { "type": ["string", "null"] },
        "generation_method": { "type": ["string", "null"] },
        "projection_marker_required": { "type": "boolean" },
        "round_trip_supported": { "type": "string", "enum": ["generated_projection_only", "hand_authored_markdown", "none"] }
      }
    },
    "conversion_evidence": {
      "type": "object",
      "properties": {
        "source_mutated": { "type": "boolean" },
        "omitted_from_content": { "type": "array", "items": { "type": "string" } },
        "normalized_fields": { "type": "array", "items": { "type": "string" } },
        "inferred_fields": { "type": "array", "items": { "type": "string" } },
        "lossiness": { "type": "string", "enum": ["none", "sidecar_preserved", "lossy_requires_review"] },
        "notes": { "type": "array", "items": { "type": "string" } }
      }
    },
    "sidecar": {
      "type": "object",
      "description": "Fields preserved for provenance but not accepted into the ADR content schema, such as legacy routing or related-link material."
    },
    "validation": {
      "type": "object",
      "properties": {
        "content_schema_valid": { "type": "boolean" },
        "schema_ref": { "type": "string" },
        "projection_round_trip_equal": { "type": ["boolean", "null"] },
        "source_markdown_unchanged": { "type": ["boolean", "null"] },
        "mutable_database_committed": { "type": ["boolean", "null"] },
        "commands": { "type": "array", "items": { "type": "string" } }
      }
    },
    "conflict_policy": {
      "type": "object",
      "required": ["json_vs_markdown", "unsupported_fields", "bulk_migration_allowed"],
      "properties": {
        "json_vs_markdown": {
          "type": "string",
          "enum": ["report_conflict", "json_wins", "markdown_wins", "projection_only_no_ingest"]
        },
        "unsupported_fields": {
          "type": "string",
          "enum": ["preserve_in_sidecar", "reject_conversion", "require_schema_change"]
        },
        "bulk_migration_allowed": { "const": false }
      }
    }
  }
}
```

## Candidate minimum instance outline

For a future canary based on `docs/adr/adr.json-schemas.draft.md`:

```json
{
  "object_type": "adr_bidirectional_object",
  "object_version": "candidate-0",
  "authority_mode": "candidate_non_authoritative",
  "content": {
    "id": "adr.json-schemas",
    "slug": "json-schemas",
    "status": "draft"
  },
  "source_refs": [
    {
      "path": "docs/adr/adr.json-schemas.draft.md",
      "kind": "markdown_source",
      "role": "source",
      "content_hash": "<source-hash>",
      "status_observed": "draft",
      "date_observed": "<source-date-if-present>"
    },
    {
      "path": "docs/schemas/adr.schema.json",
      "kind": "json_schema",
      "role": "schema",
      "content_hash": "<schema-hash>"
    }
  ],
  "markdown_projection": {
    "mode": "generated_only",
    "path": "dev/<canary>/adr.json-schemas.projected.md",
    "content_hash": "<projection-hash>",
    "generation_method": "projectkoios.bootstrap.control_surface.adr",
    "projection_marker_required": true,
    "round_trip_supported": "generated_projection_only"
  },
  "conversion_evidence": {
    "source_mutated": false,
    "omitted_from_content": ["routing", "links.related"],
    "normalized_fields": ["links.supersedes", "links.superseded_by"],
    "inferred_fields": [],
    "lossiness": "sidecar_preserved",
    "notes": ["Unsupported source fields preserved outside ADR schema payload."]
  },
  "sidecar": {
    "routing": {},
    "links_related": []
  },
  "validation": {
    "content_schema_valid": true,
    "schema_ref": "docs/schemas/adr.schema.json",
    "projection_round_trip_equal": true,
    "source_markdown_unchanged": true,
    "mutable_database_committed": false,
    "commands": []
  },
  "conflict_policy": {
    "json_vs_markdown": "projection_only_no_ingest",
    "unsupported_fields": "preserve_in_sidecar",
    "bulk_migration_allowed": false
  }
}
```

## KOIOS watchpoints for promotion

Before ATHENA/USER promotes any version of this shape:

1. Decide whether the envelope is architecture-owned separate from `docs/schemas/adr.schema.json`, or whether schema revisions are needed.
2. Define whether `content` is strictly schema-valid ADR payload or may include extensions.
3. Decide whether sidecar fields are durable object fields or migration evidence only.
4. Require clear conflict policy for human Markdown edits versus JSON records.
5. Keep broad hand-authored Markdown ingest out of scope until generated projection round-trip behavior is proven.
6. Forbid bulk ADR migration until inventory/classification and canary validation exist.
7. Preserve source paths, hashes, observed status/casing, omitted fields, and conversion notes for every converted ADR.
8. Keep generic document storage free of ADR-specific columns; ADR object behavior belongs above the generic store.
