---
name: meta-harness-state-reconciliation
adr_binding:
  - docs/adr/adr.skill-register-and-adr-binding-policy.draft.md
  - docs/adr/adr.control-surfaces-and-ownership-boundaries.draft.md
description: |
  Reconcile a user request or repo observation against the document-domain state
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md.
metadata:
  agent: meta-harness
  harness_role: arbiter
  consumes:
    - user-request
    - repository-document-state
  produces:
    - state-reconciliation
---
## When to use this skill

Use when Hermes must decide how the repository document state should become
consistent across architecture, implementation, validation, and knowledge
domains.

## Agent responsibility

Hermes owns document-domain consistency, artifact validation, disagreement
resolution, escalation decisions, and completion gating. Do not perform
specialist work unless no specialist document domain needs to change.

## Inputs

- `user-request` — the original task or instruction
- `repository-document-state` — current docs, statuses, claims, and evidence

## Procedure

1. Read the user request and the relevant repository documents.
2. Identify the document domain with the inconsistency or missing state:
   - Design/scope uncertainty → Athena-owned architecture/spec state
   - File changes, implementation, tests → Vulcan-owned implementation/validation state
   - Durable documentation, knowledge capture → Koios-owned knowledge/provenance state
   - Cross-domain disagreement, completion check, or dirty-state cleanup → Hermes
3. If classification is ambiguous, prefer the smallest reversible document-state change.
4. Produce `state-reconciliation`.

## Output artifact

- `state-reconciliation` — document domains involved, inconsistency found, and next coherent repository state

## Failure modes

- Request is too ambiguous to classify — escalate to user for clarification
- Multiple document domains disagree — reconcile the inconsistency before expanding scope

## Escalation rule

Escalate to user only when user intent is ambiguous and materially affects which
document domain should change next.
