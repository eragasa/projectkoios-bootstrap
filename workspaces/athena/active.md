```json
{
  "title": "Athena active work",
  "artifact_type": "workspace-active-priorities",
  "status": "clean-ready",
  "datetime": "20260705.190757Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "priority_count": 3,
  "active_working_items": []
}
```

# Athena active work

## Current priority stack

1. Select the next bounded architecture/specification slice.
2. If resuming workflow/Petri-net work, inspect the current architecture and ADR surfaces first.
3. If work becomes implementation, tests, or validation patching, route to Vulcan or ask for explicit role switch.

## Waiting on

- User direction for the next architecture/spec focus.
- Decision on whether `projectkoios-spec` archive handling needs separate policy documentation.
- Decision on whether template JSON↔Markdown implementation work should be handed off to Vulcan.

## Current repo state

- `master...origin/master` is clean.
- Latest observed commit: `1e4340d Stabilize lifecycle templates and archive relocation`.
- No dirty-state stabilization work is currently active.

## Ready follow-up candidates

- Resume bounded Petri-net/workflow architecture elaboration.
- Review lifecycle/template/schema control surfaces for remaining ADR follow-up.
- Draft a handoff/brief for Vulcan if implementation work is desired.

## Ignore for now

- Product-domain decisions that belong in the `projectkoios` mothership repository.
- Implementation code changes from the Athena workspace.
- Full repo-wide reference rewriting unless explicitly requested.

## Exit criteria

Athena state remains stable when any new work is captured as a bounded artifact change, handoff, or explicit no-change finding, with repo status checked before closeout.
