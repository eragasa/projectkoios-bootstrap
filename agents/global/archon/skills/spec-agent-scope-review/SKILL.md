---
name: spec-agent-scope-review
adr_binding:
  - docs/adr/adr.skill-register-and-adr-binding-policy.draft.md
  - docs/adr/adr.idea-spike-adr-implementation-workflow.draft.md
description: |
  Convert user intent into a bounded architecture specification
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.idea-spike-adr-implementation-workflow.draft.md.
metadata:
  agent: spec-agent
  harness_role: producer
  consumes:
    - user-request
  produces:
    - architecture-spec
    - acceptance-criteria
---
## When to use this skill

When the task asks about package boundaries, repository structure, public API design, feature existence, or responsibility splitting. The spec agent (archon/Athena) owns this skill.

## Agent responsibility

Convert user intent into bounded technical specifications. Own requirement normalization, package and repository scope, architecture boundaries, public API intent, non-goals, and unresolved questions. Draft preliminary acceptance-criteria notes only when needed, then hand off final criteria derivation to `spec-agent-acceptance-criteria`. Do not implement code or update durable knowledge notes.

## Inputs

- `user-request` — original task or instruction

## Procedure

1. Read the `user-request` and identify the scope boundary.
2. Read relevant maps and existing architecture.
3. Determine what is in scope and explicitly out of scope.
4. Define the public API intent, if applicable.
5. Identify non-goals.
6. List unresolved questions.
7. Write downstream instructions for implementation or knowledge capture.
8. Produce `architecture-spec` and any preliminary criteria notes needed for handoff.

## Output artifact

- `architecture-spec` — bounded architecture decision with scope, non-goals, API intent, unresolved questions
- `acceptance-criteria` — preliminary criteria notes for handoff; final inspectable pass/fail conditions are owned by `spec-agent-acceptance-criteria`

## Failure modes

- Request is too vague to bound — escalate to Hermes
- Architecture choice has multiple valid options with different consequences — escalate to Hermes/meta-harness

## Escalation rule

Escalate to meta-harness when user intent is ambiguous or when two valid architecture options have materially different project consequences.
