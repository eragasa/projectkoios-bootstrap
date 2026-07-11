```json
{
  "title": "Hermes workspace state",
  "artifact_type": "workspace-state",
  "status": "active",
  "datetime": "20260711.165218Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "ATHENA",
  "blockers": []
}
```

# Hermes workspace state

## Current focus

Advance USER-selected option 3: broader schema-family repair planning.

## Current validated state

- Slice 5 is complete, committed, and pushed as `f2df856 Accept ADR semantic rationalization slice 5`.
- Slice 6 is complete, accepted, packaged, and committed as `df4dedc2 Accept ADR template schema contract repair planning slice 6`.
- `adr-template-schema-contract-repair-planning-slice-6` was accepted as proposal-only repair planning in `docs/reviews/hermes-acceptance.20260711.160700_adr-template-schema-contract-repair-planning-slice-6.md`.
- Repo startup check on 20260711.1652Z found the working tree clean before Slice 7 activation.
- Petri-net workflow status showed `current-slice` at `user_decision`, enabled transition `approve_next_slice`, and `user decision required: yes`.
- USER selected option `3`: broader schema-family repair planning.
- HERMES recorded approval for `schema-family-repair-planning-slice-7` in `docs/reviews/hermes-decision.20260711.165218_schema-family-repair-planning-slice-7.md`.

## Active Slice 7 scope

Slice name:

```text
schema-family-repair-planning-slice-7
```

Approved planning/review surfaces:

```text
docs/adr/adr.adr-template-contract.md
docs/adr/adr.schema-base.md
docs/adr/adr.json-authoritative-adr-store.draft.md
docs/plans/schema-base-adr-records-workplan.md
docs/schemas/README.md
docs/schemas/adr.schema.json
docs/schemas/schema.record-base.json
docs/schemas/adr-draft.schema.json
docs/schemas/adr-active.schema.json
```

Preferred ATHENA output:

```text
docs/plans/repair-plan.20260711.165300_schema-family-adr-contract-slice-7.md
```

## Active boundaries

Slice 7 is planning/review only. It does not authorize editing `docs/adr/`, editing `docs/schemas/`, changing source status or casing, supersession, acceptance, activation, rejection, promotion, demotion, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

## Current blockers

- None for routing the planning slice.
- ATHENA planning output is required before HERMES can accept or choose the next concrete repair action.

## Next owner

ATHENA for schema-family repair planning/review under the approved Slice 7 scope.
