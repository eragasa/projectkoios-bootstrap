---
name: condense
description: |
  Shortens long docs, policies, handoffs, and ADR drafts without losing meaning. Use when a document is too verbose, repetitive, or hard to scan.
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md.
---
# Condense

Use this skill when a document needs to be made shorter and clearer while preserving:
- authority and scope
- decisions and requirements
- safety and provenance
- file paths, commands, and names

## Workflow

1. Identify the document’s purpose and audience.
2. Remove repeated statements and overlapping sections.
3. Merge adjacent bullets that say the same thing.
4. Convert long prose into rules, bullets, and links.
5. Keep only examples that add new information.
6. If something belongs elsewhere, move it instead of repeating it.

## Rules

- Keep the strongest version of each rule once.
- Prefer actionable language over narrative.
- Preserve headings that help navigation.
- Do not drop citations, paths, or exact commands.
- For policy docs, keep the “what to do” and trim most rationale.
- For ADRs, keep context, decision, consequences, and provenance; trim backstory.
- For handoffs and notes, keep owners, next steps, blockers, and references.

## Output

When asked to condense a document, return:
- a shorter rewrite ready to paste
- a brief list of what was removed or merged
- any items that should move to another file

## Good default target

Aim for about 50–70% of the original length unless the user asks for more or less compression.
