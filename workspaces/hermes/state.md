```json
{
  "title": "Hermes workspace state",
  "artifact_type": "workspace-state",
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

# Hermes workspace state

## Current focus

Package Hermes control-surface guardrails after tightening `workspaces/hermes/AGENTS.md` to RFC-style normative language, then choose the next bounded action.

## Current validated state

- Stable ADR filename convention/control-surface corrections and corrected retrospective Slice 12 acceptance were committed and pushed as `d9aa360c Stabilize ADR filename convention and parser compatibility`.
- Initial Hermes control-surface guardrails were committed and pushed as `92556ac9 Harden Hermes control-surface guardrails`.
- USER asked to check whether control surfaces correspond with RFC normative language.
- HERMES reviewed root `AGENTS.md`, Hermes `AGENTS.md`, `state.md`, and `active.md` without changing files.
- Finding: root `AGENTS.md` uses uppercase normative keywords, while Hermes `AGENTS.md` used several non-RFC imperative/lowercase modal forms for guardrails.
- USER said `go`.
- HERMES updated `workspaces/hermes/AGENTS.md` in the working tree so the guardrails use uppercase normative language (`MUST`, `MUST NOT`, `SHOULD NOT`, `MAY`) where intended as durable policy.

## Current coherent state

Current uncommitted work is a Hermes workspace policy/control-surface normative-language tightening only:

```text
workspaces/hermes/AGENTS.md
workspaces/hermes/state.md
workspaces/hermes/active.md
```

## Active boundaries

This guardrail language update does not authorize creating the successor ADR draft, editing existing `docs/adr/` files, editing `docs/schemas/`, changing source status or casing, supersession, lifecycle changes, migration, generated projection replacement, database/storage authority, or cutover.

## Current blockers

- HERMES_USER decision is required for packaging/commit.

## Next owner

HERMES_USER for packaging and next bounded decision.
