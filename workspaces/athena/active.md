```json
{
  "title": "Athena active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260704.212913",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "priority_count": 5,
  "working_directory": "working/",
  "active_working_items": [],
  "scratch_directory": "scratch/",
  "local_decision_record": "decisions/workspace.state.canonical.athena.20260704.041431.md",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md"
}
```

# Athena active work

## Current priority stack

1. Schema immutability remediation code/tests/report are already committed in `82740ea`; remaining clean follow-up candidate is only `docs/reviews/architecture-conformance.20260704.164710_schema-immutability-gap-closure.md`, pending explicit user execution direction.
2. HERMES made commit-packaging decision for workspace-state policy/bootstrap reconciliation as its own slice; VULCAN is waiting on explicit user execution approval before staging/committing only the HERMES include set.
3. Advance an Athena-owned portfolio only if it does not touch implementation/bootstrap surfaces currently owned by VULCAN.
4. Consolidate ADR lifecycle and naming drafts into the next accepted lifecycle slice, preserving provenance and avoiding architecture-index edits unless Hermes/Zeus directs them.
5. Prepare the next implementation-ready brief from an accepted or near-ready plan after checking document authority, with candidates including template representation namespace split or workflow Petri-net executor.

## Waiting on

- Explicit user execution direction on whether VULCAN should stage/commit only `docs/reviews/architecture-conformance.20260704.164710_schema-immutability-gap-closure.md` as the remaining schema immutability follow-up artifact.
- User execution approval for VULCAN to stage/commit the workspace-state policy/bootstrap reconciliation package.
- Hermes/user direction before editing `docs/architecture/architecture.workspaces.00.md` or `docs/architecture/architecture.00.md`.
- Authority check before turning any draft ADR or plan into implementation authority.
- Any needed action by another role/agent should be sent as an explicit intercom handoff/request, then recorded here as waiting-on.
- Schema-base conformance review output exists at `docs/reviews/architecture-conformance.20260704.212913_schema-record-base-slice.md` with outcome `conforms-with-gaps`.

## Working material

- Active working items: `docs/adr/adr.schema-base.md`, `docs/plans/schema-base-adr-records-workplan.md`, `docs/plans/implementation-brief.20260704.172632_schema-record-base.md`, `docs/schemas/README.md`, `docs/schemas/schema.record-base.json`, `docs/schemas/adr-draft.schema.json`, `docs/implementation/implementation-report.20260704.174859_schema-record-base.md`.
- Workspace-state accepted ADR: `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`; proposal retained as review provenance at `dev/canonical-workspace-state-next-action-protocol/adr.canonical-workspace-state-next-action-protocol.proposed.md`; historical draft `docs/adr/adr.canonical-workspace-state-next-action-protocol.draft.md` points to the accepted ADR.
- Conformance-review output: `docs/reviews/architecture-conformance.20260704.212913_schema-record-base-slice.md`; outcome `conforms-with-gaps`; gap is shallow immutability in metadata/generic mappings.
- Scratch: `scratch/` is available for temporary notes and non-durable exploration.
- Note: files may exist under `working/` as transitional artifacts; they are not active unless explicitly re-opened.
- `working/` has no `incoming/` or `outgoing/` subdirectories.

## Ignore for now

- Broad ADR lifecycle refactors.
- Full-repo archive cleanup.
- Machine-readable companion schema design outside the schema-base ADR scope.
- Further implementation work from this Athena workspace.
- Any attempt to implement or test the GraphRAG persisted-index slice from Athena.
- Editing Python implementation files while Vulcan has active/shared-tree work.

## Exit criteria

Athena state is stable when a new session can read `state.md`, `active.md`, and any active `working/` material, then identify the represented role, current scope, validated state, open questions, next transition, and ignored scope without chat history.
