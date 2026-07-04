---
name: meta-harness-completion-gate
adr_binding:
  - docs/adr/adr.skill-register-and-adr-binding-policy.draft.md
  - docs/adr/adr.control-surfaces-and-ownership-boundaries.draft.md
description: |
  Check that required output artifacts exist and satisfy acceptance criteria
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md.
metadata:
  agent: meta-harness
  harness_role: arbiter
  consumes:
    - acceptance-criteria
    - implementation-report
    - test-results
    - deviation-report
    - knowledge-note
  produces:
    - completion-decision
---
## When to use this skill

When an agent reports that its work is done and the meta-harness must decide whether the task is complete.

## Agent responsibility

Hermes owns completion gating. A task is complete only when required output artifacts exist and satisfy the relevant acceptance criteria.

## Inputs

- `acceptance-criteria` — the criteria to check against
- `implementation-report` — summary of implementation
- `test-results` — validation output
- `deviation-report` — any deviations from spec (if applicable)
- `knowledge-note` — durable notes (if knowledge capture was required)

## Procedure

1. Check that all required artifacts exist for the task type.
2. Cross-reference each artifact against acceptance criteria.
3. If criteria are met, issue `completion-decision: accept`.
4. If criteria are not met but the gap is correctable, issue `revision-request` to the responsible agent.
5. If criteria cannot be met within the current approach, issue `completion-decision: reject` and escalate.

## Output artifact

- `completion-decision` — final acceptance or rejection with rationale

## Failure modes

- Acceptance criteria are not measurable — decide based on best available evidence, note for future spec refinement

## Escalation rule

Escalate to user when acceptance criteria are fundamentally unmet and revision is not possible within the current spec.
