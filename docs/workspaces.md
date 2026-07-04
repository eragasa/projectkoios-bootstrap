# Workspace layout proposal

## Status

draft

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
│   ├── AGENT.md
│   ├── state.md
│   ├── active.md
│   ├── decisions/
│   ├── handoffs/
│   │   ├── incoming/
│   │   └── outgoing/
│   └── sessions/
├── athena/
│   ├── AGENT.md
│   ├── state.md
│   ├── active.md
│   ├── decisions/
│   ├── handoffs/
│   │   ├── incoming/
│   │   └── outgoing/
│   └── sessions/
├── vulcan/
│   ├── AGENT.md
│   ├── state.md
│   ├── active.md
│   ├── decisions/
│   ├── handoffs/
│   │   ├── incoming/
│   │   └── outgoing/
│   └── sessions/
└── koios/
    ├── AGENT.md
    ├── state.md
    ├── active.md
    ├── decisions/
    ├── handoffs/
    │   ├── incoming/
    │   └── outgoing/
    └── sessions/
```

## File conventions

### `state.md`
Short-lived current context for an agent run.
- current branch / repo focus
- current document domain
- current objective
- blockers
- last validated document-state change
- known cross-domain inconsistencies
- next state owner

### `active.md`
Current priorities.
- top 1-3 state transitions
- what to ignore for now
- next recommended document-state change
- pending domain inconsistencies
- items intentionally ignored for now

### `decisions/`
Agent-local decision notes.
- one file per decision
- timestamped filename
- brief rationale
- not authoritative until promoted into the appropriate repository document domain

### `handoffs/incoming/` and `handoffs/outgoing/`
Compatibility folders for transitional artifacts from older workflows.
- preserve provenance when they exist
- do not treat folder placement as authority
- prefer updating the owned repository document directly when the next state is clear

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
- Use timestamped session filenames: `YYYYMMDD.HHMMSS-topic.md`
- Use timestamped markdown filenames for transitional artifacts: `YYYYMMDD.HHMMSS.<topic>.md`
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
- each agent has an `AGENT.md`
- each agent has a `state.md`
- the agent can identify its current document domain and next state transition

Use `projectkoios bootstrap workspaces init` to materialize or refresh the
layout.
