# Agent charter instructions

Use this file for formatting and structure rules that apply when editing or
creating `docs/agents/agent-charter.md` and related document-domain ownership notes.
Controlled by: [adr.templates](../adr/adr.templates.md).
Template index: [templates.00](templates.00.md).

## When to use this template

Use these instructions when:
- changing agent charter formatting
- updating document-domain ownership language or role descriptions
- creating new agent state-reconciliation notes or workspaces
- normalizing charter structure across the bootstrap repo

## Required note format

- Keep the charter human-readable and concise.
- Use short role sections with explicit responsibilities.
- Keep document-domain ownership rules centralized here or in
  `docs/agents/agent-charter.md`.
- Use Markdown links for navigation when linking other notes.
- Keep authority language explicit: who may edit what, and when.

## Example structure

```md
# Project Koios Agent Charter

## Status

accepted

## Purpose

...

## Roles

### Hermes
...
```

## Link rules

- Link to workspace, architecture, and document-domain ownership notes with
  Markdown links.
- Prefer file-name-based links over vague references.

## Editing rule

If a request is about agent document-domain ownership, role split, or charter
formatting, update this file first or alongside the charter change so the
convention stays durable.

Agents may edit `docs/agents/agent-charter.md` when the user explicitly requests
a charter/control-surface change and the edit stays within the agent's document-domain authority.
Hermes remains responsible for cross-domain reconciliation.
