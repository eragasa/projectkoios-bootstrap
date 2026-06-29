---
name: meta-harness-task-routing
description: Route a user request to the correct agent based on dominant transformation
metadata:
  agent: meta-harness
  harness_role: arbiter
  consumes:
    - user-request
  produces:
    - routing-decision
---

## When to use this skill

When the meta-harness (pi) receives a new user request and must decide which agent handles it.

## Agent responsibility

The meta-harness (pi) owns task routing, artifact validation, disagreement resolution, escalation decisions, and completion gating. Do not perform specialist work unless no specialist role is needed.

## Inputs

- `user-request` — the original task or instruction

## Procedure

1. Read the user request and classify the dominant required transformation.
2. Apply routing rules:
   - Design/scope uncertainty → spec agent (archon)
   - File changes, implementation, tests → code agent (opencode)
   - Durable documentation, knowledge capture → knowledge agent (goose)
   - Disagreement, completion check, coordination → meta-harness (pi)
3. If classification is ambiguous, prefer the smallest reversible step.
4. Produce `routing-decision`.

## Output artifact

- `routing-decision` — next agent and action selection

## Failure modes

- Request is too ambiguous to classify — escalate to user for clarification
- Request spans multiple agents — split into sequential steps

## Escalation rule

Escalate to user only when user intent is ambiguous and materially affects routing.
