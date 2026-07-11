```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
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

# Hermes active work

## Current priority stack

1. ATHENA produces the approved Slice 7 schema-family repair planning artifact.
2. HERMES reviews/accepts the Slice 7 plan and selects the next concrete repair action.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Active Slice 7: schema-family repair planning

- HERMES decision: `docs/reviews/hermes-decision.20260711.165218_schema-family-repair-planning-slice-7.md`
- Prior Slice 6 acceptance: `docs/reviews/hermes-acceptance.20260711.160700_adr-template-schema-contract-repair-planning-slice-6.md`
- Preferred ATHENA output: `docs/plans/repair-plan.20260711.165300_schema-family-adr-contract-slice-7.md`

## Approved Slice 7 scope

Review/planning surfaces:

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

## Slice 7 purpose

Classify schema-family surfaces by role, identify contradictions/stale/ahead-of-authority claims, and recommend a staged repair sequence that separates proposal/errata, successor ADR(s), schema edits, source mutations, projections, and authority cutover.

## Required watchpoints

- ADR content schema vs record-envelope schema boundaries.
- Markdown current source/control vs future generated projection state.
- `routing` disposition.
- `dcn` disposition.
- Optional `workflow_binding` boundary.
- `accepted-staged-direction` JSON authority gates.
- Legacy schema markers vs canonical `docs/schemas/` namespace.

## Waiting on

- ATHENA planning/review output for Slice 7.

## Exit criteria

Hermes state is stable when the Slice 7 plan is accepted or revised, and the next concrete repair action is chosen without implicitly authorizing source mutation, schema changes, lifecycle/status changes, supersession, migration, generated projection replacement, database/storage authority, or cutover.
