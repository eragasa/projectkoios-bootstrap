```json
{
  "title": "Athena active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260704.041431",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [],
  "scratch_directory": "scratch/",
  "local_decision_record": "decisions/workspace.state.canonical.athena.20260704.041431.md",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md"
}
```

# Athena active work

## Current priority stack

1. End-session state is recorded; do not expand implementation work from Athena.
2. Next session should start by reconciling the dirty tree and identifying which files belong to Vulcan implementation vs Athena control-surface correction.
3. Preserve Athena boundary: route implementation/code cleanup to Vulcan or ask for explicit role switch before editing code.

## Waiting on

- User/Hermes decision on whether to revert, route, or accept the implementation changes made during the protocol miss.
- Review of uncommitted/untracked files before any further edits.
- Hermes/user direction before editing `docs/architecture/architecture.workspaces.00.md` or `docs/architecture/architecture.00.md`.

## Working material

- Active working items: session ending; no Athena working item is active.
- Scratch: `scratch/` is available for temporary notes and non-durable exploration.
- Note: files may exist under `working/` as transitional artifacts; they are not active unless explicitly re-opened.
- `working/` has no `incoming/` or `outgoing/` subdirectories.

## Ignore for now

- Broad ADR lifecycle refactors.
- Full-repo archive cleanup.
- Machine-readable companion schema design unless automation requires it.
- Further implementation work from this Athena workspace.
- Any attempt to continue code cleanup before the control surface records the intended state transition and correct owner.

## Exit criteria

Athena state is stable when a new session can read `state.md`, `active.md`, and any active `working/` material, then identify the represented role, current scope, validated state, open questions, next transition, and ignored scope without chat history.
