```json
{
  "title": "HERMES acceptance: ADR schema-base source-disposition planning slice 12",
  "artifact_type": "completion-decision",
  "status": "accepted-proposal-only-after-koios-review",
  "datetime": "20260711.184119Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-base-source-disposition-planning-slice-12",
  "reviewed_artifact": "docs/plans/source-disposition-brief.20260711.183536_adr-schema-base.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.183536_adr-schema-base-source-disposition-planning-slice-12.md",
  "koios_review": "intercom:subagent-chat-019f51a8",
  "authority_change": false,
  "source_mutation": false,
  "schema_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260711.184119: ADR schema-base source-disposition planning slice 12

## Decision

HERMES accepts ATHENA's `adr-schema-base-source-disposition-planning-slice-12` brief as proposal-only source-disposition planning after KOIOS provenance/knowledge-domain review.

Accepted artifact:

```text
docs/plans/source-disposition-brief.20260711.183536_adr-schema-base.md
```

## Accepted recommendation

HERMES accepts the brief's recommendation as proposal input:

- keep `docs/adr/adr.schema-base.md` unchanged as draft architecture/source provenance;
- do not treat it as current ADR authority;
- preserve embedded JSON `"status": "draft"` as observed source metadata, not inferred top-level ADR lifecycle status;
- pursue a later ATHENA architecture-extraction planning/extraction slice rather than in-place revision or immediate successor ADR as the first repair.

Proposed disposition wording accepted for future reference:

```text
source/provenance for schema-family record-envelope architecture; not current ADR authority until lifecycle/status and surface placement are resolved
```

## Acceptance basis

ATHENA scoped exactly one target source:

```text
docs/adr/adr.schema-base.md
```

KOIOS reviewed the brief and found it provenance-adequate for HERMES proposal-only acceptance with no blockers.

HERMES incorporates KOIOS comments:

- The brief correctly preserves `docs/adr/adr.schema-base.md` as source/provenance rather than current ADR authority.
- The embedded JSON `status: draft` is handled safely as source metadata.
- The brief accurately reflects the source shape: no top-level `## Status`, embedded JSON metadata in `## Context`, and substantial schema-family architecture/specification/implementation-planning material.
- The brief accurately represents current control-surface layering: `adr.schema.json` as current ADR content-shape schema, `schema.record-base.json` as draft record-envelope direction, Markdown as source/control for unmigrated records, and generated projections as evidence/review surfaces unless later cutover.
- The preferred architecture-extraction path is safer than in-place revision or immediate successor ADR.

## Clarification watchpoints

HERMES records these watchpoints for future slices:

1. Current ADR template/schema contract authority is `docs/adr/adr.adr-template-schema-contract.md`, accepted by `docs/reviews/hermes-acceptance.20260711.182653_adr-template-schema-contract-successor-draft-slice-11.md` and source-dispositioned by `docs/reviews/hermes-decision.20260711.183303_adr-template-contract-source-disposition.md`.
2. If a future ATHENA output creates an ADR filename, the current no-timestamp ADR filename policy applies. The accepted brief does not propose an ADR filename.
3. References to current accepted boundaries are control-surface state only; this acceptance does not create schema authority, record-envelope authority, migration authority, or JSON cutover authority.
4. Future provenance-hardening may cite Slice 4 per-source evidence and KOIOS Slice 5 review, but those additions are optional for this proposal-only acceptance.

## Boundaries preserved

This acceptance does not authorize:

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

## Accepted next recommended slice

Recommended next ADR-track slice:

```text
adr-schema-base-architecture-extraction-planning-slice-13
```

Purpose: decide and plan a clearer ATHENA-owned architecture extraction surface for still-current schema-family record-envelope concepts from `docs/adr/adr.schema-base.md`, while preserving the source unchanged as provenance.

Any architecture extraction, source status repair, schema change, migration, generated projection, or cutover requires a separate HERMES/USER-approved slice.

## Closeout validation

HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result: no `docs/adr`, `docs/schemas`, or Slice 4 dry-run evidence mutation from this planning acceptance; diff hygiene passes.
