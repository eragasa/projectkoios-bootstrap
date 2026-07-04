```json
{
  "title": "Athena workspace state",
  "artifact_type": "workspace-state",
  "status": "active",
  "datetime": "20260704.151749",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "document_domain": "architecture, ADRs, specs, acceptance criteria, implementation briefs",
  "controlling_workspace_policy": "docs/policies/workspace-layout.md",
  "compatibility_pointer": "docs/workspaces.md",
  "control_files": ["state.md", "active.md"],
  "workspace_material_dirs": {
    "working": "working/",
    "scratch": "scratch/",
    "decisions": "decisions/",
    "sessions": "sessions/"
  },
  "local_decision_record": "decisions/workspace.state.canonical.athena.20260704.041431.md",
  "next_owner": "ATHENA",
  "blockers": []
}
```

# Athena workspace state

## Current scope

- Focus: canonical Athena workspace-state protocol
- Authority boundary: workspace files are resume/control surfaces, not authoritative project architecture or product decisions
- Controlling workspace layout policy: `docs/policies/workspace-layout.md`
- Compatibility pointer retained at `docs/workspaces.md`

## Validated state

- Working tree was clean at session start on 2026-07-04.
- Canonical workspace-state format is now a Markdown pair with top JSON metadata sections:
  - `state.md` = durable resume snapshot for Athena sessions
  - `active.md` = current priority filter and exit criteria
- No separate machine-readable companion is required unless future automation proves the need.
- Stable headings and short bullet fields are sufficient for grepable startup checks.
- Previous ADR-skill boundary sweep remains recorded as clean.
- No active working items are pending; files under `working/` are current working material only when explicitly marked active.
- `scratch/` exists for temporary notes and should not be treated as durable state.
- Process correction recorded: the next best step is always an incremental edit to the relevant control surface before expanding work.
- Reconciliation recorded on 20260704.151218: the untracked GraphRAG persisted-index plan files are VULCAN-owned implementation-domain artifacts and have been handed off to the idle Vulcan session via intercom.
- Portfolio correction recorded on 20260704.151749: Athena should keep multiple larger spec/ADR tracks moving while Vulcan owns implementation work, as long as Athena avoids implementation files and preserves document-domain authority.
- No Athena implementation/code work is active.

## Open questions

- Whether Hermes should promote the workspace-state pattern into shared repo policy for all role workspaces.
- Whether a future validator should parse the top JSON metadata sections directly or require a structured companion.
- Whether historical/transitional working files should be archived or removed from the active workspace surface.
- Whether Athena should create a conformance review artifact after Vulcan completes the GraphRAG persisted-index implementation report.
- Which larger Athena track should be advanced first: workspace-state protocol promotion, ADR lifecycle/naming consolidation, template representation brief, or workflow Petri-net executor readiness.

## Next transition

- Owner: ATHENA
- Highest-leverage next action: advance Athena's independent spec/ADR portfolio while Vulcan owns the GraphRAG persisted-index implementation.
- Secondary action: perform a bounded Athena conformance review after Vulcan produces the implementation report.
- Blockers: none for Athena; avoid implementation files while shared-tree implementation work is active.

## Startup checklist

1. Confirm represented role from workspace and user request.
2. Read `state.md` and `active.md`.
3. Confirm whether any `working/` files are active before treating them as current work.
4. Check focused repo status before editing.
5. Preserve Athena boundary: draft specs/ADRs/criteria only; do not implement code.
