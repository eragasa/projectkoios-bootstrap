```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.181500Z",
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

1. Package/commit Hermes normative-language guardrail tightening if USER approves.
2. Decide whether next work is ATHENA Slice 11 successor draft creation, ATHENA naming-policy/documentation reconciliation, or another bounded action.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Active guardrail update

Updated in working tree:

```text
workspaces/hermes/AGENTS.md
```

Guardrails tightened to RFC-style normative language:

- Hermes MUST treat feedback as review input, not execution authority.
- Hermes MUST NOT send implementation work to VULCAN for document-policy/spec/schema/filename/lifecycle/acceptance-criteria changes until ATHENA supplies the owning brief or criteria, unless USER waives.
- Hermes MUST NOT accept cross-domain artifacts until required reviews are present or USER waives.
- Hermes MUST check root `AGENTS.md`, Hermes `AGENTS.md`, `state.md`, and `active.md` before new workflow decisions.
- Hermes MAY assign next owner and bounded task, but SHOULD NOT produce other roles' artifacts unless USER delegates and provenance is recorded.
- Hermes MUST distinguish working-tree, committed, and pushed acceptance states.

## Waiting on

- USER decision to package/commit this normative-language update.
- USER decision for the next bounded work after packaging.

## Exit criteria

Hermes state is stable when the guardrail update is packaged or explicitly revised, and any next work is assigned to the correct document-domain owner before implementation begins.
