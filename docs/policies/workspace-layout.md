```json
{
  "title": "Workspace layout policy",
  "artifact_type": "workspace-control-surface",
  "status": "accepted-adr-aligned",
  "repository": "projectkoios-bootstrap",
  "scope": "workspaces/",
  "acting_as": "ATHENA",
  "document_domain": "workspace layout and resume-control convention",
  "workspace_roles": ["hermes", "athena", "vulcan", "koios"],
  "material_directories": ["decisions/", "working/", "scratch/", "sessions/"],
  "updated": "20260705.105021Z"
}
```

# Workspace layout policy

## Purpose

Provide persistent, per-agent working context across sessions without mixing
role memory. The controlling decision is
`docs/adr/adr.workspaces.20260705.105021Z.md`.
The durable workflow state is the repository document set and each document's
status. Workspace files are local control surfaces for resuming an agent run;
they are not the authoritative project state and do not replace ADRs,
architecture documents, implementation reports, validation results, knowledge
notes, provenance indexes, or completion decisions.

The bootstrap CLI materializes each workspace and its local control folders.

## Canonical directory tree

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
Each role workspace MUST maintain `state.md` as its local resume/control surface.

`state.md` is the effective cold-start state for that workspace. Its purpose is to preserve the minimum durable context needed for a new session to resume correctly without chat history.

`state.md` MUST include:
- stable top JSON metadata section
- represented role
- current scope
- current branch / repo focus
- current document domain
- validated durable facts relevant to resumption, each with a provenance pointer when available
- active control surfaces
- blockers and unresolved questions
- known cross-domain inconsistencies
- next coherent transition / next state owner

When `state.md` records a claim, it SHOULD identify whether the claim is a validated fact, a working assumption, or an unresolved question, and SHOULD link to the source artifact when one exists.

`state.md` MUST NOT be treated as project architecture authority, implementation authority, acceptance authority, validation evidence, or completion evidence. When `state.md` conflicts with ADRs, implementation reports, reviews, schemas, policies, or other authoritative repository artifacts, the authoritative artifact wins and `state.md` MUST be corrected.

`state.md` MUST NOT duplicate full review, implementation, or chat history when durable artifacts already preserve that provenance. It MUST summarize current actionable state and link to ADRs, reviews, implementation reports, AARs, knowledge notes, or provenance indexes for detail.

When correcting stale state, agents SHOULD update only the state summary and preserve the authoritative source artifact unchanged unless separately authorized.

### `active.md`
Current priority filter and next-action surface.
- stable top JSON metadata section
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
- Do not duplicate full review, implementation, or chat history inside `state.md` when durable artifacts preserve that provenance

## Non-goals

- Not a replacement for `maps/`
- Not a replacement for `docs/agents/agent-charter.md`
- Not a place for product architecture
- Not a transport system
- Not a place for machine-local secrets

## Validation expectation

Lightweight startup/stop checks SHOULD verify:
- the workspace directories exist
- each agent has an `AGENTS.md`
- each agent has a `state.md`
- each agent has an `active.md`
- each agent has `decisions/`, `working/`, `scratch/`, and `sessions/`
- no workspace uses `working/incoming/` or `working/outgoing/`
- the agent can identify its current document domain and next state transition

Use `projectkoios bootstrap workspaces init` to materialize or refresh the
layout.
