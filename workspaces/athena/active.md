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

1. Route or specify follow-up for schema-record base conformance gap: implementation conforms-with-gaps due to shallow metadata/generic mapping immutability.
2. Advance an Athena-owned portfolio after the review: maintain multiple spec/ADR tracks that do not touch implementation files.
3. Promote or reconcile the canonical workspace-state / next-action protocol draft so all role workspaces have a shared control-surface standard.
4. Consolidate ADR lifecycle and naming drafts into the next accepted lifecycle slice, preserving provenance and avoiding architecture-index edits unless Hermes/Zeus directs them.
5. Prepare the next implementation-ready brief from an accepted or near-ready plan after checking document authority, with candidates including template representation namespace split or workflow Petri-net executor.

## Waiting on

- VULCAN/user direction on whether to remediate the schema-record shallow immutability gap or document it as the accepted first-slice limitation.
- Hermes/user direction before editing `docs/architecture/architecture.workspaces.00.md` or `docs/architecture/architecture.00.md`.
- Authority check before turning any draft ADR or plan into implementation authority.
- Schema-base conformance review output exists at `docs/reviews/architecture-conformance.20260704.212913_schema-record-base-slice.md` with outcome `conforms-with-gaps`.

## Working material

- Active working items: `docs/adr/adr.schema-base.md`, `docs/plans/schema-base-adr-records-workplan.md`, `docs/plans/implementation-brief.20260704.172632_schema-record-base.md`, `docs/schemas/README.md`, `docs/schemas/schema.record-base.json`, `docs/schemas/adr-draft.schema.json`, `docs/implementation/implementation-report.20260704.174859_schema-record-base.md`.
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
