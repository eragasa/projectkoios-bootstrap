```json
{
  "title": "HERMES acceptance: ADR template/schema contract successor draft slice 11",
  "artifact_type": "completion-decision",
  "status": "accepted-successor-adr-with-source-disposition-deferred",
  "datetime": "20260711.182653Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-successor-draft-slice-11",
  "accepted_artifact": "docs/adr/adr.adr-template-schema-contract.md",
  "prior_draft_artifact": "docs/adr/adr.adr-template-schema-contract.draft.md",
  "authority_change": true,
  "source_mutation": false,
  "schema_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260711.182653: ADR template/schema contract successor draft slice 11

## Decision

HERMES accepts the ATHENA-authored Slice 11 successor ADR as current ADR template/schema contract authority:

```text
docs/adr/adr.adr-template-schema-contract.md
```

The accepted artifact was renamed from the draft path:

```text
docs/adr/adr.adr-template-schema-contract.draft.md
```

The ADR status was changed from `draft` to `accepted` as part of this lifecycle decision.

## Decision basis

This acceptance follows the active ADR slice chain:

- Slice 6 identified `docs/adr/adr.adr-template-contract.md` as a mixed/stale template-schema contract needing repair planning.
- Slice 7 accepted schema-family repair planning and preserved content-schema/envelope/source/provenance boundaries.
- Slice 8 accepted the ADR schema-family contract reconciliation proposal.
- Slice 9 clarified `docs/schemas/README.md` without mutating schema JSON or ADR sources.
- Slice 10 accepted the successor planning brief and recommended Slice 11.
- Slice 11 produced the ATHENA-authored successor ADR draft, with VULCAN and KOIOS no-blocker reviews.

## Required reviews received

ATHENA authored/reconstructed the successor ADR fresh from current accepted control surfaces after HERMES routing. Invalid HERMES reflog and Archon/Codex drafts were treated as non-authoritative and were not used as source text.

VULCAN implementation-reality review:

- verdict: implementation-feasible / no blocking implementation objection;
- blockers: none;
- watchpoints retained for parser/ingester compatibility if immediate machine ingest is requested, future source-disposition handling, and preserving `metadata.record_id` / `dcn` distinction.

KOIOS provenance review:

- verdict: provenance-adequate for HERMES/USER review / no blocking provenance issues;
- blockers: none;
- watchpoints retained for explicit relation decision for `docs/adr/adr.adr-template-contract.md`, draft-internal statements becoming authority only if accepted, and invalid local drafts remaining non-authoritative.

## Accepted authority

HERMES accepts these Slice 11 ADR conclusions as current authority:

- `docs/schemas/adr.schema.json` is the current ADR content-shape schema until a later approved schema slice wraps, replaces, or retires it.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction, not current universal emitted-record authority.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence or review/navigation surfaces unless a later accepted migration/cutover package changes a specific file's disposition.
- `routing` is not current ADR content-schema data and defaults to sidecar/provenance preservation unless later promoted by workflow/envelope decision.
- `dcn` is not current ADR content-schema data and remains unresolved namespace/control metadata.
- `workflow_binding` is optional schema-supported content, not operational Petri-net workflow, lifecycle, or Operator Console authority.
- The old source status/casing `Accepted` is preserved as provenance and is not normalized by this acceptance.

## Source-disposition boundary

This acceptance does **not** supersede, edit, rename, move, archive, normalize, split, delete, migrate, demote, reject, or otherwise dispose of:

```text
docs/adr/adr.adr-template-contract.md
```

That old source remains source/provenance until HERMES/USER explicitly decides its relation to the accepted successor ADR in a separate source-disposition action.

## What this authorizes

This acceptance authorizes exactly:

- accepting the successor ADR;
- renaming `docs/adr/adr.adr-template-schema-contract.draft.md` to `docs/adr/adr.adr-template-schema-contract.md`;
- changing the successor ADR metadata/status language from draft/proposed to accepted/current;
- clearing the active Slice 11 queue item as accepted/committed work after validation.

## What this does not authorize

This acceptance does not authorize:

- editing `docs/adr/adr.adr-template-contract.md`;
- editing `docs/schemas/`;
- changing old-source status or casing;
- superseding, moving, renaming, deleting, archiving, splitting, rejecting, promoting, or demoting the old source;
- migrating ADR records;
- generating or replacing projections;
- creating authoritative JSON ADR records;
- database/storage authority changes;
- JSON authority cutover;
- Petri-net workflow runtime, Operator Console, or lifecycle automation authority changes.

## Closeout validation

HERMES ran:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Observed closeout before commit: only the accepted successor ADR rename/update appears under `docs/adr/`; no `docs/schemas` or Slice 4 dry-run evidence mutation; diff hygiene passes.

## Next required decision

The next ADR-track decision is source disposition for:

```text
docs/adr/adr.adr-template-contract.md
```

HERMES_USER must decide whether it should coexist as accepted historical/source provenance, be explicitly superseded by the accepted successor, receive errata, or follow another documented source-disposition path.
