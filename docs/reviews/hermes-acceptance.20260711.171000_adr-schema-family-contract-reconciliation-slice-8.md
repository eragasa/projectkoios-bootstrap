```json
{
  "title": "HERMES acceptance: ADR schema-family contract reconciliation slice 8",
  "artifact_type": "completion-decision",
  "status": "accepted-proposal-only",
  "datetime": "20260711.171000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-family-contract-reconciliation-slice-8",
  "reviewed_artifact": "docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.170500_adr-schema-family-contract-reconciliation-slice-8.md",
  "authority_change": false,
  "source_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260711.171000: ADR schema-family contract reconciliation slice 8

## Decision

HERMES accepts `adr-schema-family-contract-reconciliation-slice-8` as proposal-only reconciliation.

## Accepted artifact

```text
docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md
```

## Acceptance rationale

The proposal satisfies the Slice 8 decision boundary. It defines a clear non-mutating contract boundary between ADR content schema, schema-backed record envelope, rendered/source Markdown, sidecar/provenance evidence, and migration/cutover authority.

The proposal preserves current authority constraints: Markdown remains source/control for unmigrated records; generated projections remain evidence unless a later cutover package is accepted; `routing` and `dcn` are not current content-schema fields; and `workflow_binding` remains optional schema content without operational workflow authority.

## Accepted proposal findings

HERMES accepts these findings as proposal input:

- `docs/schemas/adr.schema.json` is the current ADR content-shape schema until a later approved slice wraps, replaces, or retires it.
- `docs/schemas/schema.record-base.json` is the current draft direction for schema-backed record envelopes.
- Future ADR family schemas should constrain `content` and may narrow metadata constants without redefining unrelated base metadata.
- Future schema reconciliation should prefer canonical lifecycle status in `metadata.status`, with any content/rendered status either derived or strictly mirrored, but this is not implemented by this acceptance.
- `routing` should default to sidecar/provenance preservation unless a later workflow/envelope decision promotes a replacement.
- `dcn` should default to unresolved namespace/control metadata, with likely mapping pressure toward `metadata.record_id` / filename conventions.
- `docs/schemas/adr-active.schema.json` remains a compatibility/reconciliation candidate until explicitly wrapped, replaced, retired, or preserved for compatibility.

## Accepted recommended next action

Primary recommended next bounded action:

```text
schema-family-doc-index-clarification-slice-9
```

Purpose: edit only planning/control documentation, not schemas or ADR source authority, to make the content-schema vs envelope-schema boundary visible to readers.

Alternative next action: approve a successor template/schema contract ADR creation slice if USER wants to move directly toward source repair.

## Boundaries preserved

This acceptance does not authorize editing `docs/adr/`, editing `docs/schemas/`, creating a new ADR draft, changing source status or casing, supersession, acceptance, activation, rejection, promotion, demotion, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

Any future doc edit, source mutation, schema edit, lifecycle relation change, projection generation, migration, or cutover requires a separate HERMES/USER-approved slice.

## Closeout validation

Observed planning-only validation:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Both produced no output / passed at acceptance time.
