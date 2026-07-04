```json
{
  "title": "Athena active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260704.172155",
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

1. Hand off the schema-record base slice from the new implementation-ready draft brief: `docs/plans/implementation-brief.20260704.172632_schema-record-base.md`.
2. Advance an Athena-owned portfolio while Vulcan works: maintain multiple spec/ADR tracks that do not touch implementation files.
3. Promote or reconcile the canonical workspace-state / next-action protocol draft so all role workspaces have a shared control-surface standard.
4. Consolidate ADR lifecycle and naming drafts into the next accepted lifecycle slice, preserving provenance and avoiding architecture-index edits unless Hermes/Zeus directs them.
5. Prepare the next implementation-ready brief from an accepted or near-ready plan after checking document authority, with candidates including template representation namespace split or workflow Petri-net executor.

## Waiting on

- Vulcan implementation report under `docs/implementation/` before Athena conformance review of the GraphRAG persisted-index slice.
- Hermes/user direction before editing `docs/architecture/architecture.workspaces.00.md` or `docs/architecture/architecture.00.md`.
- Authority check before turning any draft ADR or plan into implementation authority.
- Schema-base design blockers: none for the current pre-Vulcan slice; implementation brief is drafted and ready for VULCAN after worktree/commit separation is agreed.

## Working material

- Active working items: `docs/adr/adr.schema-base.md`, `docs/plans/schema-base-adr-records-workplan.md`, `docs/plans/implementation-brief.20260704.172632_schema-record-base.md`, `docs/schemas/README.md`, `docs/schemas/schema.record-base.json`, `docs/schemas/adr-draft.schema.json`.
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
