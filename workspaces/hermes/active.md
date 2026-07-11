```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.172000Z",
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

1. Package/commit accepted Slice 9 schema-family doc/index clarification.
2. Decide whether to activate recommended `adr-template-schema-contract-successor-planning-slice-10`.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Accepted Slice 9: schema-family doc/index clarification

- HERMES decision: `docs/reviews/hermes-decision.20260711.171500_schema-family-doc-index-clarification-slice-9.md`
- Edited control/index doc: `docs/schemas/README.md`
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.172000_schema-family-doc-index-clarification-slice-9.md`

## Accepted Slice 9 meaning

- `adr.schema.json` is current ADR content-shape schema until explicitly wrapped, replaced, or retired.
- `schema.record-base.json` is the draft record-envelope direction.
- `adr-draft.schema.json` demonstrates ADR-family composition with the base envelope.
- `adr-active.schema.json` is a compatibility/reconciliation candidate.
- Markdown under `docs/adr/` remains source/control for unmigrated records.
- Generated projections remain evidence or review/navigation surfaces unless later cutover changes a specific file's disposition.
- `routing` and `dcn` are not current ADR content-schema fields.
- `workflow_binding` is optional schema content, not operational workflow authority.

## Accepted next recommendation

Primary recommended next bounded action:

```text
adr-template-schema-contract-successor-planning-slice-10
```

Purpose: draft a proposal-only successor plan or explicit ADR-creation brief for `docs/adr/adr.adr-template-contract.md`, preserving old-source provenance and requiring separate approval before ADR creation, supersession, source mutation, or schema edits.

## Waiting on

- Packaging/commit decision for accepted Slice 9 changes.
- HERMES/USER decision to activate Slice 10 or choose a different bounded repair action.

## Exit criteria

Hermes state is stable when accepted Slice 9 changes are packaged/committed and the next bounded action is chosen without implicitly authorizing source mutation, schema changes, lifecycle/status changes, supersession, migration, generated projection replacement, database/storage authority, or cutover.
