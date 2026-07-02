# AAR: Routing cleanup and UI namespace sweep

## Scope
Project Koios bootstrap documentation cleanup focused on Hermes/routing wording, workspace state, and adjacent UI namespace ADRs.

## What happened
- Removed or rewrote routing-heavy language across active control-plane docs and workspace files.
- Deleted obsolete Hermes sandbox message delivery architecture files.
- Added/updated workspace state files (`state.md`, `active.md`) and then collapsed the active list to `status: none`.
- Added new ADRs for `ui-core`, `workflow-ui`, and `json-schemas`, plus a template/implementation ingestion-scope ADR and companion notes.
- Committed and pushed the documentation changes.

## Process issues
- The Hermes/routing cleanup needed to be done line-by-line; trying to treat whole files as a single routing concern created unnecessary churn.
- The intercom system was discovered mid-session and briefly confused role boundaries around who should draft what.
- `state.md` existed before workspace guidance explicitly referenced it, so canonical-state discovery remained ambiguous until discussed.
- The previous note system created extra scope pressure; the user clarified that this should now be treated as Vulcan responsibility rather than note capture.

## Proposed follow-up improvements
- Explicitly wire `state.md` into workspace guidance if the workspace-state protocol is to be used operationally.
- Keep future cleanup tasks scoped to one file at a time when removing control-plane jargon.
- Route implementation-only work directly to Vulcan without reintroducing an intermediate note workflow.

## Candidate ADR or implementation topics
- Workspace guidance update for canonical `state.md` usage.
- Vulcan implementation handoff for the template-representation plan.
- Further refinement of the `ui-core` / `workflow-ui` / `json-schemas` family.

## Current status
Cleanup committed and pushed. No active routing-cleanup work remains in this scope.
