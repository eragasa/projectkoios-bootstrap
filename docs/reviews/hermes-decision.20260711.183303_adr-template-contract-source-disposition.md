```json
{
  "title": "HERMES decision: ADR template contract source disposition",
  "artifact_type": "workflow-decision",
  "status": "accepted-source-disposition",
  "datetime": "20260711.183303Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-contract-source-disposition",
  "source_artifact": "docs/adr/adr.adr-template-contract.md",
  "current_authority": "docs/adr/adr.adr-template-schema-contract.md",
  "source_mutation": "disposition-note-only",
  "schema_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES decision 20260711.183303: ADR template contract source disposition

## Decision

HERMES accepts the source disposition for:

```text
docs/adr/adr.adr-template-contract.md
```

Disposition: preserve as legacy/source provenance, not current ADR template/schema contract authority.

Current authority is:

```text
docs/adr/adr.adr-template-schema-contract.md
```

## Rationale

The accepted successor ADR records the current template/schema contract and resolves the mixed/stale authority in the older source without requiring destructive handling of the old file.

The older source remains useful provenance because it records the prior accepted-like template/schema/source-of-truth contract, observed status/casing `Accepted`, and the historical claims that drove Slices 6-11.

## Source mutation authorized

This decision authorizes only adding a bounded source-disposition note to `docs/adr/adr.adr-template-contract.md` pointing to this decision and to the accepted successor authority.

The note preserves the observed `Accepted` status/casing and makes the older file's current role explicit.

## What this does not authorize

This decision does not authorize:

- renaming, moving, archiving, deleting, or splitting `docs/adr/adr.adr-template-contract.md`;
- changing its observed status/casing from `Accepted`;
- treating it as rejected or deleted;
- editing `docs/schemas/`;
- migrating ADR records;
- generating or replacing projections;
- creating authoritative JSON ADR records;
- database/storage authority changes;
- JSON authority cutover;
- Petri-net workflow runtime, Operator Console, or lifecycle automation authority changes.

## Validation

HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result: only `docs/adr/adr.adr-template-contract.md` changes under `docs/adr`; no `docs/schemas` or Slice 4 dry-run evidence mutation; diff hygiene passes.

## Next recommended action

After this source-disposition decision is committed, the ADR template/schema repair track is coherent. HERMES_USER may either explicitly activate the next queued item or define another ADR-track slice.
