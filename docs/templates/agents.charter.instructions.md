# Agent charter instructions

Use this file for formatting and structure rules that apply when editing or
creating `docs/agent-charter.md` and related agent message-delivery notes.
Controlled by: [adr.templates](../architecture/adr/adr.templates.draft.md).
Template index: [templates.00](templates.00.md).

## When to use this template

Use these instructions when:
- changing agent charter formatting
- updating sandbox message delivery language or role descriptions
- creating new agent message-delivery notes or workspaces
- normalizing charter structure across the bootstrap repo

## Required note format

- Keep the charter human-readable and concise.
- Use short role sections with explicit responsibilities.
- Keep sandbox message delivery rules centralized here or in
  `docs/agent-charter.md`.
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

- Link to workspace, architecture, and sandbox message delivery notes with
  Markdown links.
- Prefer file-name-based links over vague references.

## Editing rule

If a request is about agent sandbox message delivery, role split, or charter
formatting, update this file first or alongside the charter change so the
convention stays durable.

Only Hermes may edit `docs/agent-charter.md`, and only when Zeus explicitly
requests the change.
