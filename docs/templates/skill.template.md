# Skill template

Use this template to create new skills. Every committed skill must declare its ADR binding in both machine-readable and human-readable form.

## Template

```yaml
---
name: <skill-name>
adr_binding:
  - docs/architecture/adr/<adr-filename-1>.draft.md
  - docs/architecture/adr/<adr-filename-2>.draft.md
description: |
  <Short description of when to use this skill>
  Bound to ADRs: adr.<adr-1>.draft.md, adr.<adr-2>.draft.md.
metadata:
  agent: <agent-type>
  harness_role: <consumer | producer | consumer-producer | arbiter>
  consumes:
    - <artifact-type>
  produces:
    - <artifact-type>
---
```

## Rules

1. `adr_binding` must list every ADR this skill implements, supports, or is governed by.
2. The `description` must also name the bound ADRs in human-readable form (e.g., `Bound to ADRs: ...`).
3. Register the skill in `docs/skills/skill-register.md` with owning harness, purpose, binding mode, status, and binding note.
4. Binding mode is `primary`, `supporting`, or `exempt`. Exempt skills must include a justification in the register.
5. Use relative paths from the repo root for `adr_binding` entries.

## When to create a skill

- The task pattern is complex or repetitious enough to benefit from structured guidance.
- The task crosses multiple sessions.
- The task is specific enough for clear instructions but general enough to reuse.
- The skill will bind to at least one ADR. Skills with no ADR binding must be marked exempt.

## When not to create a skill

- One-off utility that will not be reused.
- Simple rule that fits in workspace guidance.
- Task that is entirely context-dependent with no repeatable pattern.
