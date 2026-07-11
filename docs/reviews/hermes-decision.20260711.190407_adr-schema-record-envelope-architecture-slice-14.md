```json
{
  "title": "HERMES decision: ADR schema record-envelope architecture slice 14",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-handoff",
  "datetime": "20260711.190407Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-record-envelope-architecture-slice-14",
  "target_source": "docs/adr/adr.schema-base.md",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.185430_adr-schema-base-architecture-extraction-planning-slice-13.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.190407: ADR schema record-envelope architecture slice 14

## Decision

HERMES keeps priority on the ADR track and approves `adr-schema-record-envelope-architecture-slice-14` for ATHENA handoff.

## Rationale

Slice 13 accepted ATHENA's architecture-extraction planning brief as proposal-only planning after KOIOS review. The accepted recommendation is to create one ATHENA-owned architecture artifact, preferably:

```text
docs/architecture/architecture.schema-record-envelope.md
```

This slice executes that architecture extraction as an architecture-document creation slice while preserving source and schema boundaries.

## Handoff target

ATHENA should create one architecture artifact:

```text
docs/architecture/architecture.schema-record-envelope.md
```

## Required ATHENA output content

The architecture artifact should extract/reconcile only still-current schema-family record-envelope concepts from `docs/adr/adr.schema-base.md` and accepted planning surfaces.

The artifact should include:

1. Status and non-authority boundary.
2. Source/provenance basis, including `docs/adr/adr.schema-base.md`.
3. Current schema-family control surfaces.
4. Record-envelope purpose and non-purpose.
5. `metadata` + `content` model as draft direction.
6. Metadata field families and provenance/evidence separation.
7. Relationship to ADR content schema.
8. Relationship to Markdown source/control and generated projections.
9. Relationship to `docs/schemas/README.md` and machine-readable schema files.
10. Deferred renderer/ingester requirements.
11. Explicit non-actions and later gates.

The artifact should avoid copying `docs/adr/adr.schema-base.md` wholesale.

## Current boundaries to preserve

- `docs/adr/adr.adr-template-schema-contract.md` is current ADR template/schema contract authority.
- `docs/adr/adr.schema-base.md` remains unchanged source/provenance.
- Embedded JSON `"status": "draft"` in `docs/adr/adr.schema-base.md` is observed source metadata, not inferred top-level ADR lifecycle status.
- `docs/schemas/adr.schema.json` is current ADR content-shape schema until later approved replacement/wrap/retirement.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction, not current universal emitted-record authority.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Boundaries

This HERMES decision does not authorize HERMES to produce the ATHENA architecture artifact directly.

This decision authorizes ATHENA to create exactly one new architecture artifact at `docs/architecture/architecture.schema-record-envelope.md`.

This decision does not authorize editing `docs/adr/adr.schema-base.md`, editing `docs/schemas/`, changing lifecycle state, accepting record-envelope authority, making `metadata` + `content` current universal emitted-record authority, accepting, activating, superseding, rejecting, promoting, demoting, moving, renaming, deleting, archiving, splitting existing sources, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

## Required closeout for ATHENA output

ATHENA/HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git status --short -- docs/architecture/architecture.schema-record-envelope.md
git diff --check
```
