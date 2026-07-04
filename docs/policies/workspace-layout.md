```json
{
  "title": "Workspace layout proposal",
  "artifact_type": "workspace-control-surface",
  "status": "draft",
  "repository": "projectkoios-bootstrap",
  "scope": "workspaces/",
  "acting_as": "ATHENA",
  "document_domain": "workspace layout and resume-control convention",
  "workspace_roles": ["hermes", "athena", "vulcan", "koios"],
  "material_directories": ["decisions/", "working/", "scratch/", "sessions/"],
  "updated": "20260704"
}
```

# Workspace layout proposal

## Purpose

Provide persistent, per-agent working context across sessions without mixing
role memory. The durable workflow state is the repository document set and each
document's status. Workspace files are local control surfaces for resuming an
agent run; they are not the authoritative project state.

The bootstrap CLI materializes each workspace and its local state folders.

## Proposed directory tree

```text
workspaces/
├── hermes/
│   ├── AGENTS.md
│   ├── state.md
│   ├── active.md
│   ├── decisions/
│   ├── working/
│   ├── scratch/
│   └── sessions/
├── athena/
│   ├── AGENTS.md
│   ├── state.md
│   ├── active.md
│   ├── decisions/
│   ├── working/
│   ├── scratch/
│   └── sessions/
├── vulcan/
│   ├── AGENTS.md
│   ├── state.md
│   ├── active.md
│   ├── decisions/
│   ├── working/
│   ├── scratch/
│   └── sessions/
└── koios/
    ├── AGENTS.md
    ├── state.md
    ├── active.md
    ├── decisions/
    ├── working/
    ├── scratch/
    └── sessions/
```

## File conventions

### `state.md`
Short-lived current context for an agent run.
- top JSON metadata section
- current branch / repo focus
- current document domain
- current objective
- blockers
- last validated document-state change
- known cross-domain inconsistencies
- next state owner

### `active.md`
Current priorities.
- top JSON metadata section
- top 1-3 state transitions
- what to ignore for now
- next recommended document-state change
- pending domain inconsistencies
- items intentionally ignored for now

### `decisions/`
Agent-local decision notes.
- one file per decision
- filename SHOULD use a dotted scope form when useful, such as `workspace.state.canonical.athena.<datetime>.md`
- top JSON metadata section
- brief rationale
- not authoritative until promoted into the appropriate repository document domain

### `working/`
Current or transitional working material for the role workspace.
- preserve provenance when files exist
- do not create `incoming/` or `outgoing/` subdirectories
- do not treat folder placement as authority
- do not treat files as active merely because they are present
- active working items SHOULD be named in `active.md`
- prefer updating the owned repository document directly when the next state is clear

### `scratch/`
Temporary, non-durable notes and exploration.
- MAY contain rough notes, command output, or draft fragments
- MUST NOT be treated as authoritative state
- SHOULD be cleared or promoted before session close when material becomes useful
- MUST NOT contain secrets

### `sessions/`
Session notes.
- append-only chronological records
- one file per session
- useful for resuming after interruption

## Role-specific document domains

### Hermes
- cross-domain state reconciliation
- dirty-tree notes
- completion decisions
- document-status consistency checks
- next coherent repo state

### Athena
- bounded spec notes
- ADR draft links
- open architecture questions
- acceptance criteria

### Vulcan
- implementation plan
- file-level edits
- validation results
- deviation notes

### Koios
- validated summaries
- provenance indexes
- note candidates
- research follow-ups

## Naming rules

- Use lowercase agent names: `hermes`, `athena`, `vulcan`, `koios`
- Use `AGENTS.md` for workspace-local agent instructions
- Use timestamped session filenames: `YYYYMMDD.HHMMSS-topic.md`
- Use dotted, scoped markdown filenames for reusable local decisions when useful: `<domain>.<topic>.<role>.<datetime>.md`
- Prefer one topic per file
- Do not store secrets
- Do not duplicate canonical repo docs inside workspace files

## Non-goals

- Not a replacement for `maps/`
- Not a replacement for `docs/agents/agent-charter.md`
- Not a place for product architecture
- Not a transport system
- Not a place for machine-local secrets

## Validation expectation

If adopted, add lightweight startup/stop checks that verify:
- the workspace directories exist
- each agent has an `AGENTS.md`
- each agent has a `state.md`
- each agent has an `active.md`
- each agent has `decisions/`, `working/`, `scratch/`, and `sessions/`
- no workspace uses `working/incoming/` or `working/outgoing/`
- the agent can identify its current document domain and next state transition

Use `projectkoios bootstrap workspaces init` to materialize or refresh the
layout.
