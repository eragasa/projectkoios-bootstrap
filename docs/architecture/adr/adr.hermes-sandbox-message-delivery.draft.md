# ADR 20260702.020244Z: Hermes Sandbox Message Delivery

## Status

draft

## Context

Origin: user request
From: HERMES
Acting-As: ATHENA
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap

The bootstrap repo already has explicit `inbox/` and `outbox/` surfaces, and
workspace guidance says each harness reads inbox first and writes outgoing
material to outbox. Active prose also now prefers "sandbox message delivery"
over abstract "routing" language.

What remains underspecified is the operator boundary: who actually delivers a
message into the recipient harness sandbox, and who is only the author of the
message content.

That ambiguity matters because it can collapse delivery, authorship, and
architecture ownership into one blurred step.

## Decision

Hermes is the sole cross-role message deliverer for this repository.

Hermes owns the act of placing a message into the recipient harness sandbox
and is responsible for preserving sender identity, recipient identity,
provenance, and the original artifact owner.

Other harnesses may author outbound material, but they do not self-deliver
across harness boundaries.

Use "sandbox message delivery" in prose. Preserve existing machine-facing
compatibility identifiers such as `routing-decision` and
`routing-recommendation` where needed, but do not describe Hermes as a passive
mailbox or abstract router.

## Consequences

- one accountable operator handles cross-role delivery
- delivery paths stay explicit and auditable
- message authorship stays separate from delivery authority
- Hermes becomes a coordination bottleneck if the delivery surface grows too
  broad
- future automation, if any, should assist Hermes rather than replace the
  delivery boundary

## architecture-spec

- `inbox/` and `outbox/` are the delivery boundary surfaces
- Hermes is the only cross-role deliverer
- the producing role owns message content and artifact identity
- delivery records must preserve provenance and the intended recipient
- prose should say "sandbox message delivery", not just "routing"

## acceptance-criteria

- active guidance names Hermes as the deliverer
- no other role is instructed to deliver directly into another role's sandbox
- message content remains attributable to its producing role
- legacy `routing-*` identifiers remain available for compatibility
- delivery instructions stay distinct from architecture, implementation, and
  knowledge-capture ownership

## implementation-brief

No code implementation is requested.

If this ADR advances, update the workspace guides and message-delivery notes so
all active prose matches the Hermes-delivered mailbox model.

### Verification method

Manual review of updated bootstrap guidance and a grep for conflicting mail or
routing wording in active docs.

## resolved-open-questions

- Should Hermes expose a mail-status command?
- Should delivery progress be summarized in workspace state?

## non-goals

- Renaming machine-facing `routing-*` identifiers
- Changing architecture, implementation, or knowledge ownership
- Building a new mailbox UI

## validation-expectations

- readers can distinguish delivery from authorship and architecture ownership
- the mail path is explicit from one workspace to another
- active prose uses the same delivery terminology everywhere

## routing

- Owner: Athena
- Next phase: draft
- Notes: Hermes executes delivery; Athena owns the decision surface.

## links

- back_to: architecture.00
- related: adr.control-surfaces-and-ownership-boundaries.draft.md
