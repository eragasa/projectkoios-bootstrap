```json
{
  "title": "Hermes workspace state",
  "artifact_type": "workspace-state",
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

# Hermes workspace state

## Current focus

Package Hermes control-surface guardrails after the Slice 10/Slice 12 workflow failures, then choose the next bounded action.

## Current validated state

- Stable ADR filename convention/control-surface corrections and corrected retrospective Slice 12 acceptance were committed and pushed as `d9aa360c Stabilize ADR filename convention and parser compatibility`.
- USER approved hardening the control surfaces.
- HERMES updated `workspaces/hermes/AGENTS.md` in the working tree with explicit guardrails:
  - root `AGENTS.md`, Hermes `AGENTS.md`, `state.md`, and `active.md` must be checked before cross-domain workflow decisions;
  - implementation/provenance/architecture feedback is review input, not execution authority;
  - VULCAN implementation must not begin for architecture/spec/schema/document-policy/filename/lifecycle/acceptance-criteria changes until ATHENA supplies the owning brief or acceptance criteria, unless USER explicitly waives that order;
  - HERMES acceptance requires required reviews or explicit USER waivers;
  - HERMES must distinguish control-surface edits from domain artifact production;
  - HERMES must distinguish working-tree, committed, and pushed acceptance states;
  - HERMES decision artifacts should follow a decision checklist.

## Current coherent state

Current uncommitted work is a Hermes workspace policy/control-surface hardening update only:

```text
workspaces/hermes/AGENTS.md
workspaces/hermes/state.md
workspaces/hermes/active.md
```

## Active boundaries

This guardrail update does not authorize creating the successor ADR draft, editing existing `docs/adr/` files, editing `docs/schemas/`, changing source status or casing, supersession, lifecycle changes, migration, generated projection replacement, database/storage authority, or cutover.

## Current blockers

- HERMES_USER decision is required for packaging/commit.

## Next owner

HERMES_USER for packaging and next bounded decision.
