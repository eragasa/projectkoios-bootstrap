# Architecture template instructions

Use this file for formatting and structure rules that should apply when editing
or creating `architecture.*` notes.
For the template namespace itself, see `docs/templates/templates.00.md` and
`docs/architecture/adr/adr.templates.draft.md`.

## When to use this template

Use these instructions when:
- changing architecture note formatting
- creating new `architecture.*` notes
- normalizing note structure across a workspace
- updating links, frontmatter, or title conventions

## Required note format

- Start with YAML frontmatter.
- Include `status:` and `date:` in frontmatter.
- Use a human-readable title line after frontmatter.
- Prefer `architecture.*` filenames for bootstrap architecture notes.
- Use Markdown links for navigation.
- Keep titles free of timestamps; keep timestamps in frontmatter only.

## Frontmatter example

```md
---
status: draft
date: 20260701.131500Z
---
```

## Title example

```md
# Architecture index
```

## Link rules

- Use Markdown links when the target is meant to be grep-friendly.
- Use Obsidian wiki links only when Obsidian navigation is the priority.
- Keep links stable and filename-based.

## Editing rule

If a request is about formatting architecture notes or workspace notes, update
this file first or alongside the note change so the convention stays durable.

Only Hermes may edit `docs/architecture*.md`, and only when Zeus explicitly
requests the change.
