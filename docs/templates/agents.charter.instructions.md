# Agent charter instructions

Use this file for formatting and structure rules that apply when editing or
creating `docs/agent-charter.md` and related agent-routing notes.

## When to use this template

Use these instructions when:
- changing agent charter formatting
- updating routing language or role descriptions
- creating new agent-routing notes or workspaces
- normalizing charter structure across the bootstrap repo

## Required note format

- Keep the charter human-readable and concise.
- Use short role sections with explicit responsibilities.
- Keep routing rules centralized here or in `docs/agent-charter.md`.
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

### Hermes (`pi`)
...
```

## Link rules

- Link to workspace, architecture, and routing notes with Markdown links.
- Prefer file-name-based links over vague references.

## Editing rule

If a request is about agent routing, role split, or charter formatting, update
this file first or alongside the charter change so the convention stays durable.

Only Hermes may edit `docs/agent-charter.md`, and only when Zeus explicitly
requests the change.
