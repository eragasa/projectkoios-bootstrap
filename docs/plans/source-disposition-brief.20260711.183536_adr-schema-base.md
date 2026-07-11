```json
{
  "title": "Source-disposition brief: ADR schema-base",
  "artifact_type": "source-disposition-planning-brief",
  "status": "proposal-only-pending-hermes-user-acceptance",
  "datetime": "20260711.183536Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-base-source-disposition-planning-slice-12",
  "target_source": "docs/adr/adr.schema-base.md",
  "hermes_decision": "docs/reviews/hermes-decision.20260711.183536_adr-schema-base-source-disposition-planning-slice-12.md",
  "source_mutation": false,
  "schema_mutation": false,
  "authority_change": false,
  "next_owner": "HERMES_USER"
}
```

# Source-disposition brief 20260711.183536: ADR schema-base

## Purpose

Determine a safe proposed path for `docs/adr/adr.schema-base.md` after Slice 5 classified it as authority-relevant but unsafe to treat as current ADR authority.

This brief is proposal-only. It does not edit `docs/adr/adr.schema-base.md`, edit `docs/schemas/`, change lifecycle state, accept, activate, supersede, reject, promote, demote, move, rename, delete, archive, split, generate projections/JSON records, migrate, or cut over authority.

## Source basis

Target source:

```text
docs/adr/adr.schema-base.md
```

Decision and review inputs:

```text
docs/reviews/hermes-decision.20260711.183536_adr-schema-base-source-disposition-planning-slice-12.md
docs/reviews/hermes-acceptance.20260711.155200_adr-semantic-rationalization-six-entry-slice-5.md
docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md
docs/schemas/README.md
docs/adr/adr.adr-lifecycle.20260705.011836Z.md
docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md
```

Relevant current accepted boundaries:

- `docs/adr/adr.adr-template-schema-contract.md` is current ADR template/schema contract authority after template-contract successor/source-disposition resolution.
- `docs/schemas/adr.schema.json` is current ADR content-shape schema until later approved replacement/wrap/retirement.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction, not current universal emitted-record authority.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Source summary

`docs/adr/adr.schema-base.md` is titled:

```text
# ADR: Schema Base Class for ADR Records
```

The file begins with `## Context` containing embedded JSON metadata. That embedded JSON includes:

```json
"status": "draft"
```

However, the file does not contain a top-level ADR `## Status` section. Slice 5 therefore correctly treated it as missing top-level ADR status and blocked ordinary current-authority interpretation.

Substantively, the source contains valuable schema-family architecture and implementation-oriented design ideas:

- shared `metadata` + `content` record envelope;
- schema-backed repository records;
- schema-family contracts;
- rendered document surfaces;
- Markdown renderer/ingester behavior;
- base metadata and provenance fields;
- JSON Schema `$id` conventions;
- future implementation brief content.

Those ideas overlap with later/current surfaces, especially `docs/schemas/README.md`, `docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md`, and the accepted successor template/schema contract direction.

## Problem statement

`docs/adr/adr.schema-base.md` is useful source material but unsafe as current ADR authority because:

1. It lacks top-level ADR lifecycle status.
2. Its embedded JSON status should be preserved as source metadata, not silently promoted into top-level lifecycle authority.
3. It reads more like schema-family architecture/specification and implementation planning than a clean bounded ADR decision.
4. Some renderer/ingester and projection/source-of-truth claims may be ahead of current accepted authority.
5. It predates later clarifications that `schema.record-base.json` is draft record-envelope direction, while `adr.schema.json` remains the current ADR content-shape schema.
6. It could confuse readers into thinking a universal `metadata` + `content` record envelope is already current emitted-record authority.

## Options evaluated

### Option A: Keep unchanged as draft architecture provenance

Assessment: safe immediate disposition.

Pros:

- No source mutation.
- Preserves the source exactly as provenance for schema-family and renderer/ingester thinking.
- Avoids silently inferring lifecycle status from embedded JSON.
- Avoids changing schema authority.

Cons:

- Readers may still mistake the file for current ADR authority.
- Missing top-level status remains unresolved.
- Later planning slices must remember that it is source/provenance, not current control.

Use as the default until a clearer successor/extraction path is approved.

### Option B: Revise in place

Assessment: not recommended as first action.

Pros:

- Could add a top-level `## Status` and reduce reader confusion.
- Could align prose with current schema-family layering.

Cons:

- In-place revision of an existing source could silently rewrite provenance.
- It would require explicit lifecycle/status handling.
- The file contains multiple concerns that should probably be separated rather than patched.
- It risks creating schema/envelope authority by edit rather than by accepted decision.

Use only after HERMES/USER explicitly approves source mutation and lifecycle handling.

### Option C: Replace with successor ADR

Assessment: possible, but not the highest-leverage first repair.

Pros:

- A successor ADR could state a clean current decision about schema-family record envelope authority.
- It could preserve the old file as source/provenance.

Cons:

- Current accepted boundaries already say the record envelope is draft direction, not current universal authority.
- A successor ADR would need careful coordination with `docs/schemas/README.md`, the template/schema contract, and any future schema-change slice.
- It may prematurely promote record-envelope direction before implementation/schema evidence is ready.

Use later if HERMES/USER wants to accept a record-envelope authority decision.

### Option D: Extract schema-family material into a clearer architecture document

Assessment: preferred primary path.

Pros:

- Matches the source's actual shape: it is mostly schema-family architecture/specification.
- Avoids mutating the source ADR-like file.
- Can explicitly mark `schema.record-base.json` as draft direction and avoid overclaiming current authority.
- Can reconcile the useful schema-family concepts with `docs/schemas/README.md` and the template/schema contract.
- Keeps future schema changes and implementation slices separately gated.

Cons:

- Requires a later ATHENA architecture/extraction slice.
- Does not immediately resolve the old file's missing top-level status, except by documenting source disposition elsewhere.

Recommended.

### Option E: Repair lifecycle/status placement only

Assessment: useful but incomplete.

Pros:

- Could clarify whether the embedded JSON `draft` should become top-level `## Status`.
- Reduces parser/migration ambiguity.

Cons:

- Status repair alone would not address mixed architecture/implementation/schema claims.
- It may imply current ADR-track treatment when architecture extraction is safer.

Use only as a narrow follow-up if HERMES/USER wants source repair but not architecture extraction.

### Option F: Leave unchanged with explicit source-disposition note

Assessment: acceptable fallback.

Pros:

- No source mutation.
- Makes the unsafe authority state visible if recorded in a review/plan/index note.

Cons:

- Leaves useful schema-family architecture scattered.
- Adds another note rather than creating a clearer durable architecture surface.

Use if HERMES/USER wants no architecture extraction yet.

## Recommended path

Primary recommendation: **keep `docs/adr/adr.schema-base.md` unchanged as draft architecture/source provenance and create a future ATHENA architecture-extraction brief or architecture note for schema-family record-envelope direction.**

The future architecture/extraction slice should:

1. Treat `docs/adr/adr.schema-base.md` as source/provenance, not current ADR authority.
2. Preserve the embedded JSON `status: draft` as observed source metadata.
3. Avoid inferring or normalizing top-level ADR lifecycle status.
4. Extract only still-current schema-family concepts into a clearer architecture surface, likely under `docs/architecture/` or `docs/plans/` first.
5. State that `docs/schemas/adr.schema.json` remains current ADR content-shape schema.
6. State that `docs/schemas/schema.record-base.json` remains draft record-envelope direction until a separate schema-change/acceptance slice promotes it.
7. Avoid creating universal emitted-record authority.
8. Avoid schema edits, source edits, generated projections, migration, or JSON authority cutover.

Suggested next slice name:

```text
adr-schema-base-architecture-extraction-planning-slice-13
```

Suggested output path if HERMES/USER wants a plan first:

```text
docs/plans/architecture-extraction-brief.<datetime>_adr-schema-base.md
```

Suggested output path if HERMES/USER directly approves architecture extraction:

```text
docs/architecture/architecture.schema-record-envelope.md
```

The architecture document path is only a candidate. HERMES/USER should approve the exact target before creation.

## Source-disposition statement proposed for future use

If HERMES/USER accepts this brief, future references may describe `docs/adr/adr.schema-base.md` as:

```text
source/provenance for schema-family record-envelope architecture; not current ADR authority until lifecycle/status and surface placement are resolved
```

More detailed proposed disposition:

- retain in place unchanged for now;
- do not infer top-level ADR status from embedded JSON;
- do not migrate automatically to authoritative JSON;
- do not use as current schema/envelope authority;
- use as cited source input for a future architecture/schema-family extraction slice.

## Required owner decisions before execution beyond planning

Before any source mutation or authority change, HERMES/USER must decide:

- whether `docs/adr/adr.schema-base.md` remains source/provenance only;
- whether it should ever receive a top-level `## Status` repair;
- whether useful content should move into an architecture document, successor ADR, schema README update, or schema-change proposal;
- whether `schema.record-base.json` should remain draft direction or become accepted schema-record envelope authority;
- whether any future schema-family authority belongs in ADR, architecture, `docs/schemas/README.md`, or machine-readable schema files;
- whether and how the old source should be linked after extraction;
- whether generated projections or JSON conversion are ever appropriate for this source.

## Acceptance criteria for a future architecture-extraction slice

A future extraction/planning slice should be accepted only if it:

1. Mutates at most the explicitly approved new architecture/plan artifact.
2. Does not edit `docs/adr/adr.schema-base.md`.
3. Does not edit `docs/schemas/`.
4. Preserves embedded `status: draft` as observed source metadata and does not infer top-level lifecycle status.
5. Clearly states that `docs/adr/adr.schema-base.md` is source/provenance, not current ADR authority.
6. Separates current `adr.schema.json` content-shape authority from draft record-envelope direction.
7. Avoids claiming `metadata` + `content` is current universal emitted-record authority.
8. Identifies any claims that are stale, ahead of authority, or already superseded by later surfaces.
9. Keeps renderer/ingester implementation as deferred unless separately approved.
10. Does not generate projections, JSON records, migration evidence, or cutover authority.

## Explicit exclusions for this planning brief

This brief does not authorize:

- editing `docs/adr/adr.schema-base.md`;
- editing any existing `docs/adr/` source;
- editing `docs/schemas/`;
- changing lifecycle state;
- accepting, activating, superseding, rejecting, promoting, or demoting any source;
- moving, renaming, deleting, archiving, or splitting files;
- JSON conversion or projection generation;
- generated projection replacement;
- authoritative JSON ADR records;
- database/storage authority;
- migration;
- JSON authority cutover;
- treating `docs/adr/adr.schema-base.md` as current ADR authority.

## Closeout validation expectations

ATHENA/HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result for this planning slice: no `docs/schemas/` or dry-run evidence mutation; no mutation to `docs/adr/adr.schema-base.md`; any unrelated pre-existing `docs/adr/` changes should be identified separately from this planning brief.
