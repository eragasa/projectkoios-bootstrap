```json
{
  "title": "HERMES decision: ADR schema-base architecture extraction planning slice 13",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-handoff",
  "datetime": "20260711.184325Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-base-architecture-extraction-planning-slice-13",
  "target_source": "docs/adr/adr.schema-base.md",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.184119_adr-schema-base-source-disposition-planning-slice-12.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.184325: ADR schema-base architecture extraction planning slice 13

## Decision

HERMES keeps priority on the ADR track and approves `adr-schema-base-architecture-extraction-planning-slice-13` for ATHENA handoff.

## Rationale

Slice 12 accepted ATHENA's source-disposition brief for `docs/adr/adr.schema-base.md` as proposal-only planning after KOIOS review. The accepted recommendation is to keep `docs/adr/adr.schema-base.md` unchanged as draft architecture/source provenance and pursue a later architecture-extraction planning/extraction slice rather than in-place revision or immediate successor ADR.

The next coherent ADR-track action is a proposal-only architecture extraction planning slice.

## Handoff target

ATHENA should produce one proposal-only architecture-extraction brief for still-current schema-family record-envelope concepts in:

```text
docs/adr/adr.schema-base.md
```

Suggested output path:

```text
docs/plans/architecture-extraction-brief.20260711.184325_adr-schema-base.md
```

## Required ATHENA output content

The brief should define:

- which concepts in `docs/adr/adr.schema-base.md` remain useful/current source material;
- which concepts are stale, ahead of authority, or superseded by later control surfaces;
- the recommended future durable surface for extracted architecture material, likely a later `docs/architecture/` artifact or another explicitly approved plan;
- whether the future extracted artifact should be architecture documentation, an ADR, a schema README update, or a schema-change proposal;
- acceptance criteria for any later extraction artifact;
- explicit boundaries preserving source/provenance and schema authority.

The brief should treat `docs/adr/adr.schema-base.md` as:

```text
source/provenance for schema-family record-envelope architecture; not current ADR authority until lifecycle/status and surface placement are resolved
```

## Current boundaries to preserve

- `docs/adr/adr.adr-template-schema-contract.md` is current ADR template/schema contract authority.
- `docs/adr/adr.schema-base.md` remains unchanged source/provenance.
- Embedded JSON `"status": "draft"` in `docs/adr/adr.schema-base.md` is observed source metadata, not inferred top-level ADR lifecycle status.
- `docs/schemas/adr.schema.json` is current ADR content-shape schema until later approved replacement/wrap/retirement.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction, not current universal emitted-record authority.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Boundaries

This HERMES decision does not authorize HERMES to produce the ATHENA planning artifact directly.

This decision does not authorize editing `docs/adr/adr.schema-base.md`, editing `docs/schemas/`, creating the final architecture extraction artifact, changing lifecycle state, accepting, activating, superseding, rejecting, promoting, demoting, moving, renaming, deleting, archiving, splitting, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

## Required closeout for ATHENA output

ATHENA/HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```
