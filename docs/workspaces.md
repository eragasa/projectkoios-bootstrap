# Workspace layout proposal

## Status

draft

## Purpose

Provide persistent, per-agent state across sessions without mixing role memory.
The bootstrap CLI now materializes these workspaces and their local mail folders.

## Proposed directory tree

```text
workspaces/
├── hermes/
│   ├── AGENT.md
│   ├── state.md
│   ├── active.md
│   ├── inbox/
│   ├── outbox/
│   ├── decisions/
│   ├── handoffs/
│   │   ├── incoming/
│   │   └── outgoing/
│   └── sessions/
├── athena/
│   ├── AGENT.md
│   ├── state.md
│   ├── active.md
│   ├── inbox/
│   ├── outbox/
│   ├── decisions/
│   ├── handoffs/
│   │   ├── incoming/
│   │   └── outgoing/
│   └── sessions/
├── vulcan/
│   ├── AGENT.md
│   ├── state.md
│   ├── active.md
│   ├── inbox/
│   ├── outbox/
│   ├── decisions/
│   ├── handoffs/
│   │   ├── incoming/
│   │   └── outgoing/
│   └── sessions/
└── koios/
    ├── AGENT.md
    ├── state.md
    ├── active.md
    ├── inbox/
    ├── outbox/
    ├── decisions/
    ├── handoffs/
    │   ├── incoming/
    │   └── outgoing/
    └── sessions/
```

## File conventions

### `state.md`
Short-lived current context.
- current branch / repo focus
- current objective
- blockers
- last validated decision
- inbox summary
- outbox summary

### `active.md`
Current priorities.
- top 1-3 tasks
- what to ignore for now
- next recommended action
- pending inbox items
- pending outbox items

### `decisions/`
Durable agent-local decisions.
- one file per decision
- timestamped filename
- brief rationale

### `inbox/`
Incoming mail for the workspace.
- Hermes deposits mail here for the target agent
- keep original provenance headers when the item is a handoff note
- do not rewrite unless explicitly revising the mail item
- if live notification is needed, write the inbox file first, then use intercom to notify the target
- prefer one message per file

### `outbox/`
Outgoing mail produced by the workspace.
- one mail item per task boundary
- explicit owner, scope, and next step
- Hermes will deliver mail from outbox to the target workspace inbox
- prefer the same timestamped markdown filename pattern as inbox mail

### `handoffs/incoming/`
Artifacts received from another harness.
- keep original provenance headers
- do not rewrite unless explicitly revising the handoff

### `handoffs/outgoing/`
Artifacts produced for another harness.
- one handoff per task boundary
- explicit owner, scope, and next step

### `sessions/`
Session notes.
- append-only chronological records
- one file per session
- useful for resuming after interruption

## Role-specific content

### Hermes
- repo state summary
- dirty-tree notes
- sandbox message delivery decisions
- pending handoffs
- next recommended repo/task

### Athena
- bounded spec notes
- ADR draft links
- open questions
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
- Use timestamped markdown filenames for inbox/outbox messages: `YYYYMMDD.HHMMSS.<topic>.md`
- Prefer one topic per file
- Do not store secrets
- Do not duplicate canonical repo docs inside workspace files

## Non-goals

- Not a replacement for `maps/`
- Not a replacement for `docs/agent-charter.md`
- Not a place for product architecture
- Not a place for machine-local secrets

## Validation expectation

If adopted, add lightweight startup/stop checks that verify:
- the workspace directories exist
- each agent has an `AGENT.md`
- each agent has a `state.md`
- handoffs are placed in the correct incoming/outgoing folder

Use `projectkoios bootstrap workspaces init` to materialize or refresh the
layout.
