```json
{
  "title": "HERMES decision: ADR schema-base source-disposition planning slice 12",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-handoff",
  "datetime": "20260711.183536Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-base-source-disposition-planning-slice-12",
  "target_source": "docs/adr/adr.schema-base.md",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.155200_adr-semantic-rationalization-six-entry-slice-5.md",
  "prior_resolution": "docs/reviews/hermes-decision.20260711.183303_adr-template-contract-source-disposition.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.183536: ADR schema-base source-disposition planning slice 12

## Decision

HERMES keeps priority on the ADR track and approves `adr-schema-base-source-disposition-planning-slice-12` for ATHENA handoff.

## Rationale

Slice 5 identified two authority-relevant but semantically unsafe ADR entries requiring bounded repair/revision planning:

```text
docs/adr/adr.adr-template-contract.md
docs/adr/adr.schema-base.md
```

The first target has now been resolved by the accepted successor ADR and source-disposition decision:

```text
docs/adr/adr.adr-template-schema-contract.md
docs/reviews/hermes-decision.20260711.183303_adr-template-contract-source-disposition.md
```

The next coherent ADR-track action is the remaining Slice 5 target:

```text
docs/adr/adr.schema-base.md
```

## Handoff target

ATHENA should produce one proposal-only planning/source-disposition brief for `docs/adr/adr.schema-base.md`.

Suggested output path:

```text
docs/plans/source-disposition-brief.20260711.183536_adr-schema-base.md
```

## Required ATHENA output content

The brief should determine a safe proposed path for `docs/adr/adr.schema-base.md`, including whether to:

- keep it as draft architecture provenance;
- revise it in place;
- replace it with a successor ADR;
- extract schema-family material into a clearer architecture document;
- repair lifecycle/status placement;
- or leave it unchanged with an explicit source-disposition note.

The brief must preserve current accepted boundaries:

- `docs/adr/adr.adr-template-schema-contract.md` is current ADR template/schema contract authority.
- `docs/schemas/adr.schema.json` is current ADR content-shape schema until later approved replacement/wrap/retirement.
- `docs/schemas/schema.record-base.json` remains draft record-envelope direction, not current universal emitted-record authority.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence/review surfaces unless later cutover changes a file's disposition.

## Boundaries

This HERMES decision does not authorize HERMES to produce the ATHENA planning artifact directly.

This decision does not authorize editing `docs/adr/adr.schema-base.md`, editing `docs/schemas/`, changing lifecycle state, accepting, activating, superseding, rejecting, promoting, demoting, moving, renaming, deleting, archiving, splitting, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

## Required closeout for ATHENA output

ATHENA/HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```
