```json
{
  "title": "HERMES acceptance: ADR schema-base architecture extraction planning slice 13",
  "artifact_type": "completion-decision",
  "status": "accepted-proposal-only-after-koios-review",
  "datetime": "20260711.185430Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-base-architecture-extraction-planning-slice-13",
  "reviewed_artifact": "docs/plans/architecture-extraction-brief.20260711.184325_adr-schema-base.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.184325_adr-schema-base-architecture-extraction-planning-slice-13.md",
  "koios_review": "intercom:subagent-chat-019f51a8",
  "authority_change": false,
  "source_mutation": false,
  "schema_mutation": false,
  "architecture_artifact_created": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260711.185430: ADR schema-base architecture extraction planning slice 13

## Decision

HERMES accepts ATHENA's `adr-schema-base-architecture-extraction-planning-slice-13` brief as proposal-only architecture-extraction planning after KOIOS provenance/knowledge-domain review.

Accepted artifact:

```text
docs/plans/architecture-extraction-brief.20260711.184325_adr-schema-base.md
```

## Accepted recommendation

HERMES accepts the brief's recommendation as proposal input:

- later extract still-current schema-family record-envelope architecture to a single architecture artifact, preferably:

  ```text
  docs/architecture/architecture.schema-record-envelope.md
  ```

- keep `docs/adr/adr.schema-base.md` unchanged as source/provenance;
- preserve embedded JSON `"status": "draft"` as observed source metadata, not top-level ADR lifecycle status;
- preserve `docs/schemas/schema.record-base.json` as draft record-envelope direction;
- keep renderer/ingester implementation, schema edits, source status repair, generated projections, migration, and cutover deferred to later approved slices.

The architecture path above is a recommended future path only. Creating it requires separate HERMES/USER approval.

## Acceptance basis

KOIOS found the brief provenance-adequate for HERMES proposal-only acceptance with no blockers.

HERMES incorporates KOIOS findings:

- The brief correctly starts from accepted Slice 12 disposition: `docs/adr/adr.schema-base.md` is source/provenance for schema-family record-envelope architecture, not current ADR authority until lifecycle/status and surface placement are resolved.
- It safely preserves embedded JSON `status: draft` as source metadata and does not infer a top-level ADR lifecycle status.
- It accurately represents current boundaries: `docs/schemas/adr.schema.json` is current ADR content-shape schema; `docs/schemas/schema.record-base.json` is draft record-envelope direction; Markdown under `docs/adr/` remains source/control for unmigrated records; generated projections remain evidence/review surfaces unless later cutover changes a file disposition.
- It classifies useful/current concepts conservatively as draft architecture/future implementation inputs, not current universal authority.
- It classifies stale/ahead-of-authority concepts safely and defers implementation/schema/migration work.
- `docs/architecture/architecture.schema-record-envelope.md` is an appropriate future provenance-preserving architecture surface because the material is architecture/specification rather than a clean ADR decision.

## Watchpoints carried forward

1. `docs/architecture/architecture.schema-record-envelope.md` is only a recommended future path; creation requires separate approval.
2. This acceptance does not make `docs/schemas/schema.record-base.json` accepted record-envelope authority; it remains draft direction.
3. This acceptance does not make `metadata` + `content` current universal emitted-record authority.
4. A future extraction should extract/reconcile only still-current concepts and avoid copying `docs/adr/adr.schema-base.md` wholesale.
5. Renderer/ingester implementation, schema edits, source status repair, generated projections, migration, and cutover remain deferred to later approved slices.

Optional future provenance hardening may cite KOIOS Slice 5 review and Slice 4 per-source evidence for `adr.schema-base.md`; those references are not blocking for this proposal-only acceptance.

## Boundaries preserved

This acceptance does not authorize:

- editing `docs/adr/adr.schema-base.md`;
- editing `docs/schemas/`;
- creating `docs/architecture/architecture.schema-record-envelope.md` yet;
- changing lifecycle state;
- accepting, activating, superseding, rejecting, promoting, or demoting any source;
- moving, renaming, deleting, archiving, or splitting files;
- JSON conversion or projection generation;
- generated projection replacement;
- authoritative JSON ADR records;
- database/storage authority;
- migration;
- JSON authority cutover;
- treating `docs/adr/adr.schema-base.md` as current ADR authority;
- treating `schema.record-base.json` as accepted current universal envelope authority.

## Accepted next recommended slice

Recommended next ADR-track slice:

```text
adr-schema-record-envelope-architecture-slice-14
```

Purpose: create one ATHENA-owned architecture artifact at an approved path, preferably `docs/architecture/architecture.schema-record-envelope.md`, extracting/reconciling only still-current schema-family record-envelope concepts while preserving all source/schema boundaries.

## Closeout validation

HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result: no `docs/adr`, `docs/schemas`, or Slice 4 dry-run evidence mutation from this planning acceptance; diff hygiene passes.
