---
name: meta-harness-disagreement-resolution
adr_binding:
  - docs/architecture/adr/adr.skill-register-and-adr-binding-policy.draft.md
  - docs/architecture/adr/adr.control-surfaces-and-ownership-boundaries.draft.md
  - docs/architecture/adr/adr.comment-scope-and-control-boundary-review-rule.draft.md
description: |
  Resolve conflicts between artifacts using the authority hierarchy
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md, adr.comment-scope-and-control-boundary-review-rule.draft.md.
metadata:
  agent: meta-harness
  harness_role: arbiter
  consumes:
    - deviation-report
    - architecture-spec
    - acceptance-criteria
    - implementation-report
    - test-results
  produces:
    - revision-request
---
## When to use this skill

When two artifacts contain conflicting claims and one agent has flagged the conflict via a `deviation-report`, or when the meta-harness detects inconsistency during completion gating.

## Agent responsibility

The meta-harness (pi) resolves disagreements using the authority hierarchy. Do not invent compromise between incompatible claims.

## Inputs

- Conflicting artifacts — at least two of `architecture-spec`, `deviation-report`, `implementation-report`, `test-results`, `acceptance-criteria`

## Procedure

1. Identify the conflicting claims and their source artifacts.
2. Determine the authority level of each artifact per the hierarchy (user > repo state > tests > spec > criteria > report > note > inference).
3. Identify the controlling claim.
4. Identify the artifact that must be revised.
5. Identify the agent responsible for revision.
6. Produce `revision-request`.

## Output artifact

- `revision-request` — conflict description, evidence, controlling authority, required correction, next responsible agent

## Failure modes

- Both artifacts have equal authority but genuinely conflict — escalate to user
- Conflict reveals a flaw in the authority hierarchy design — escalate to user

## Escalation rule

Escalate to user only when the authority hierarchy cannot resolve the conflict.
