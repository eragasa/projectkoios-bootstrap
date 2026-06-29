---
name: spec-agent-acceptance-criteria
description: Derive inspectable acceptance criteria from an architecture specification
metadata:
  agent: spec-agent
  harness_role: producer
  consumes:
    - architecture-spec
  produces:
    - acceptance-criteria
---

## When to use this skill

After producing an `architecture-spec`, when explicit completion criteria are needed before implementation begins.

## Agent responsibility

The spec agent (archon/Athena) ensures that acceptance criteria are observable, testable, and unambiguous. Each criterion must be a pass/fail condition that the code agent can validate independently.

## Inputs

- `architecture-spec` — the bounded architecture decision

## Procedure

1. For each in-scope item, define the observable state that constitutes completion.
2. For each non-goal, define a negative test if applicable.
3. For each public API item, define the expected behavior contract.
4. Order criteria by dependency.
5. Produce `acceptance-criteria` artifact.

## Output artifact

- `acceptance-criteria` — ordered list of inspectable pass/fail conditions

## Failure modes

- Criteria cannot be made testable — mark as unresolved question in the spec
- Spec lacks sufficient detail to derive criteria — escalate to meta-harness to route back for refinement

## Escalation rule

If the spec does not contain enough detail to derive criteria, escalate to meta-harness (pi) for routing back to the spec agent.
