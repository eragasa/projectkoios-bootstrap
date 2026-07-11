```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.181000Z",
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

1. Package/commit Hermes control-surface guardrails if USER approves.
2. Decide whether next work is ATHENA Slice 11 successor draft creation, ATHENA naming-policy/documentation reconciliation, or another bounded action.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Active guardrail update

Updated in working tree:

```text
workspaces/hermes/AGENTS.md
```

Guardrails added:

- Check root `AGENTS.md`, Hermes `AGENTS.md`, `state.md`, and `active.md` before cross-domain decisions.
- Treat feedback as review input, not execution authority.
- Require ATHENA brief/acceptance criteria before VULCAN implementation for document-policy/spec/schema/filename/lifecycle/acceptance-criteria changes unless USER waives.
- Require reviews or USER waivers before HERMES acceptance.
- Distinguish control-surface edits from domain artifact production.
- Distinguish working-tree, committed, and pushed acceptance states.
- Use a workflow decision checklist.

## Waiting on

- USER decision to package/commit this guardrail update.
- USER decision for the next bounded work after packaging.

## Exit criteria

Hermes state is stable when the guardrail update is packaged or explicitly revised, and any next work is assigned to the correct document-domain owner before implementation begins.
