---
name: code-agent-implementation-from-spec
adr_binding:
  - docs/architecture/adr/adr.skill-register-and-adr-binding-policy.draft.md
  - docs/architecture/adr/adr.implementation-plan-ownership.draft.md
  - docs/architecture/adr/adr.implementation-brief-verification-method.draft.md
description: |
  Convert an approved specification into working repository changes
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.implementation-plan-ownership.draft.md, adr.implementation-brief-verification-method.draft.md.
metadata:
  agent: code-agent
  harness_role: consumer-producer
  consumes:
    - architecture-spec
    - acceptance-criteria
  produces:
    - patch
    - test-results
    - implementation-report
    - deviation-report
---
## When to use this skill

When the task asks to implement a feature, modify files, add tests, refactor code, run validation, or produce a patch. The code agent (opencode/Vulcan) owns this skill.

## Agent responsibility

Convert approved specifications into working repository changes. Own implementation planning, minimal patches, public API changes, tests, local validation, and implementation reports. Do not silently change the architecture boundary. Do not add features outside the accepted specification.

## Inputs

- `architecture-spec` — the approved architecture decision
- `acceptance-criteria` — the criteria to satisfy

## Procedure

1. Read the spec and acceptance criteria.
2. Plan file-level changes.
3. Implement minimal changes to satisfy the spec.
4. Write or update tests alongside code.
5. Run validation (lint, typecheck, tests).
6. If the spec cannot be satisfied, produce `deviation-report`.
7. Produce `implementation-report`.

## Output artifact

- `patch` — repository modification
- `test-results` — validation output
- `implementation-report` — summary of what changed
- `deviation-report` — mismatch between spec and reality (if applicable)

## Failure modes

- Spec is ambiguous or incomplete — produce `deviation-report`, do not guess
- Implementation reveals architecture flaw — produce `deviation-report` and escalate to meta-harness
- Validation fails — diagnose, fix, or document in `deviation-report`

## Escalation rule

Escalate design ambiguity back to spec agent (archon) via Hermes instead of inventing policy.
