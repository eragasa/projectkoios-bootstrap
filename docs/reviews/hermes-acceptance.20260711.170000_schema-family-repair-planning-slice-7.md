```json
{
  "title": "HERMES acceptance: schema-family repair planning slice 7",
  "artifact_type": "completion-decision",
  "status": "accepted-proposal-only",
  "datetime": "20260711.170000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-family-repair-planning-slice-7",
  "reviewed_artifact": "docs/plans/repair-plan.20260711.165300_schema-family-adr-contract-slice-7.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.165218_schema-family-repair-planning-slice-7.md",
  "authority_change": false,
  "source_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260711.170000: schema-family repair planning slice 7

## Decision

HERMES accepts `schema-family-repair-planning-slice-7` as proposal-only repair planning.

## Accepted artifact

```text
docs/plans/repair-plan.20260711.165300_schema-family-adr-contract-slice-7.md
```

## Acceptance rationale

The plan satisfies the Slice 7 decision boundary by comparing the approved schema-family surfaces and preserving planning-only scope.

The accepted plan identifies the key cross-domain inconsistency: the repository currently has a flat ADR content schema, emerging schema-backed record-envelope schemas, staged JSON-authority migration goals, and an accepted-like template/schema/source-of-truth contract that overstates current authority for Markdown-derived JSON and stale fields such as `routing`.

The plan correctly recommends a schema-family / ADR-contract reconciliation proposal before schema mutation, source mutation, projection generation, migration, or cutover.

## Accepted findings

HERMES accepts these Slice 7 planning findings as proposal input:

- `docs/schemas/adr.schema.json` is current ADR content-shape schema, not a complete record-envelope schema.
- `docs/schemas/schema.record-base.json` and `docs/schemas/adr-draft.schema.json` express the emerging metadata/content record-envelope direction.
- `docs/schemas/adr-active.schema.json` is a compatibility/reconciliation candidate, not co-authoritative with the newer base-envelope family by implication.
- Markdown remains source/control for unmigrated records; generated projections remain evidence unless a later authority cutover is explicitly accepted.
- `routing` is not current ADR content-schema data and should not be added, removed, or promoted without a separate decision.
- `dcn` remains unresolved namespace/control metadata and should not be silently added to or removed from schema authority.
- `workflow_binding` is schema-supported optional content, not current operational workflow authority.
- Status placement across content schema and record-envelope metadata requires explicit reconciliation before implementation or migration expansion.

## Accepted recommended next slice

Primary recommended next slice:

```text
adr-schema-family-contract-reconciliation-slice-8
```

Recommended output:

```text
docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md
```

This next slice should be proposal-only unless HERMES/USER separately approves ADR creation or source/schema edits. It should decide the contract boundary between ADR content schema, record envelope, source Markdown, generated projections, sidecar/provenance, and migration authority.

## Boundaries preserved

This acceptance does not authorize editing `docs/adr/`, editing `docs/schemas/`, changing source status or casing, supersession, acceptance, activation, rejection, promotion, demotion, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

Creating a new ADR draft, editing a schema, editing `docs/adr/adr.adr-template-contract.md`, changing lifecycle relations, or running migration requires a future HERMES/USER-approved slice.

## Closeout validation

Observed planning-only validation:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Both produced no output / passed at acceptance time.
