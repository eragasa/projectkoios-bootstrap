```json
{
  "title": "HERMES decision: ADR schema-family contract reconciliation slice 8",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-proposal",
  "datetime": "20260711.170500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-family-contract-reconciliation-slice-8",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.170000_schema-family-repair-planning-slice-7.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.170500: ADR schema-family contract reconciliation slice 8

## Decision

HERMES approves `adr-schema-family-contract-reconciliation-slice-8` for ATHENA proposal drafting.

## Rationale

Slice 7 accepted the need for a schema-family / ADR-contract reconciliation proposal before any schema mutation, source mutation, projection generation, migration, or authority cutover. The repository currently has a flat ADR content schema, emerging schema-backed record-envelope schemas, staged JSON-authority migration goals, and an accepted-like template/schema/source-of-truth contract that overstates current authority for JSON-derived Markdown and stale fields such as `routing`.

The next coherent state is a proposal-only reconciliation artifact that decides the contract boundary between ADR content schema, record envelope, source Markdown, generated projections, sidecar/provenance, and migration authority.

## Approved scope

ATHENA may draft one proposal artifact at:

```text
docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md
```

Approved source surfaces:

```text
docs/plans/repair-plan.20260711.165300_schema-family-adr-contract-slice-7.md
docs/reviews/hermes-acceptance.20260711.170000_schema-family-repair-planning-slice-7.md
docs/adr/adr.adr-template-contract.md
docs/adr/adr.schema-base.md
docs/adr/adr.json-authoritative-adr-store.draft.md
docs/adr/adr.adr-lifecycle.20260705.011836Z.md
docs/plans/schema-base-adr-records-workplan.md
docs/schemas/README.md
docs/schemas/adr.schema.json
docs/schemas/schema.record-base.json
docs/schemas/adr-draft.schema.json
docs/schemas/adr-active.schema.json
```

Do not expand into all ADRs, all schemas, implementation code, product/mothership architecture, or migration execution.

## Required proposal content

The proposal should decide, as proposal input only:

1. Layer contract: ADR content schema vs schema-backed record envelope.
2. Status placement: content status, metadata status, or explicit mirroring rule.
3. Markdown authority: current source/control vs future generated projections after cutover.
4. Sidecar/provenance boundary for unsupported source material.
5. `routing` disposition.
6. `dcn` disposition.
7. `workflow_binding` boundary.
8. Legacy schema marker handling for `adr-active.schema.json`.
9. Future staged repair sequence, with owner and approval requirements.

## Boundaries

This approval does not authorize editing `docs/adr/`, editing `docs/schemas/`, creating a new ADR draft under `docs/adr/`, changing source status or casing, supersession, acceptance, activation, rejection, promotion, demotion, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

The proposal must be non-mutating and must route any recommended source mutation, schema edit, lifecycle decision, projection generation, migration, or cutover as a separate HERMES/USER-approved slice.

## Required closeout

Closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```
