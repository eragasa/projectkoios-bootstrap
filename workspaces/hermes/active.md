```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.171000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES_USER",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. Package/commit accepted Slice 8 ADR schema-family contract reconciliation.
2. Decide whether to activate recommended `schema-family-doc-index-clarification-slice-9`.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Accepted Slice 8: ADR schema-family contract reconciliation

- HERMES decision: `docs/reviews/hermes-decision.20260711.170500_adr-schema-family-contract-reconciliation-slice-8.md`
- ATHENA proposal: `docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md`
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.171000_adr-schema-family-contract-reconciliation-slice-8.md`

## Accepted Slice 8 meaning

- `docs/schemas/adr.schema.json` is current ADR content-shape schema until explicitly wrapped, replaced, or retired.
- `docs/schemas/schema.record-base.json` is current draft direction for schema-backed record envelopes.
- Markdown remains source/control for unmigrated records; generated projections remain evidence unless later cutover is accepted.
- `routing` defaults to sidecar/provenance preservation unless later promoted by workflow/envelope decision.
- `dcn` remains unresolved namespace/control metadata.
- `workflow_binding` remains optional schema content, not operational workflow authority.
- `docs/schemas/adr-active.schema.json` remains a compatibility/reconciliation candidate.

## Accepted next recommendation

Primary recommended next bounded action:

```text
schema-family-doc-index-clarification-slice-9
```

Purpose: edit only planning/control documentation, not schemas or ADR source authority, to make the content-schema vs envelope-schema boundary visible to readers.

Alternative: approve a successor template/schema contract ADR creation slice.

## Waiting on

- Packaging/commit decision for accepted Slice 8 changes.
- HERMES/USER decision to activate Slice 9 or choose a different bounded repair action.

## Exit criteria

Hermes state is stable when accepted Slice 8 changes are packaged/committed and the next bounded action is chosen without implicitly authorizing source mutation, schema changes, lifecycle/status changes, supersession, migration, generated projection replacement, database/storage authority, or cutover.
