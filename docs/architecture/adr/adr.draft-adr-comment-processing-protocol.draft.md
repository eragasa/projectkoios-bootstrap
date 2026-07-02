# ADR 20260702.032435Z: Draft ADR Comment Processing Protocol

## Status

draft

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The repository needs a defined process for how the draft ADR owner processes
comments once the comments land on the draft ADR or its controlling ADR.
Without that process, comments can accumulate without a clear owner action,
closing rule, or promotion signal.

This protocol is for the draft ADR owner, not for general repository comment
policy.

## Decision

Use the following comment-processing loop for the draft ADR owner:

1. **Collect** — read new comments on the draft ADR and any controlling ADR it
   joins.
2. **Classify** — label each comment as one of:
   - substantive
   - needs revision
   - blocked by another role
   - out of scope
   - resolved
3. **Respond** — reply briefly with one of:
   - accepted
   - revised
   - deferred
   - rejected
   - needs more input
4. **Revise** — update the ADR text when a comment changes the decision,
   boundary, or wording materially.
5. **Resolve** — mark the comment thread resolved only when the change is made,
   the concern is answered, or the comment is explicitly deferred.
6. **Escalate** — if the comment requires another role, move the issue to that
   role's surface and leave a traceable backlink.

Apply these rules:

- draft ADR owners must not silently ignore substantive comments
- comments that alter the decision surface should be incorporated into the ADR
  text before promotion
- comments that are purely editorial can be resolved without changing the
  decision
- comments blocked by role authority should be acknowledged and routed rather
  than argued inside the draft
- if multiple comments repeat the same concern, consolidate the response into a
  single revision note

## Consequences

- draft ADR owners have a clear loop for processing review input
- comments do not linger without an owner action
- substantive feedback becomes part of the draft before promotion
- role-boundary issues stay visible instead of getting buried in thread noise

## architecture-spec

The owner comment loop is:

`collect -> classify -> respond -> revise -> resolve -> escalate`

The owner should keep a short review log in the draft ADR comments or linked
review note that records:

- comment author
- comment type
- owner response
- whether the ADR text changed
- whether the thread was resolved or escalated

## acceptance-criteria

- a draft ADR owner can process a comment without improvising the next step
- substantive comments trigger either revision or explicit rejection with a
  reason
- blocked comments are routed instead of being left hanging
- repeated concerns can be consolidated into one response
- the review trail remains visible to Athena and later reviewers

## implementation-brief

If accepted, update the controlling ADR set and workspace guidance so draft ADR
owners follow the collect/classify/respond/revise/resolve/escalate loop.

## resolved_open_questions

- Should the review log live in the draft ADR itself or in a linked review note?
- Should resolved comments be summarized in a bottom section of the ADR?
- Should the owner classify comments before replying, or can classification be
  implicit in the reply?

## non_goals

- Defining the content of each review comment
- Replacing the draft/proposed/accepted lifecycle
- Creating a new status system for comments
- Automating thread resolution

## validation-expectations

- a reviewer can tell what the draft owner does next after any given comment
- substantive comments either change the ADR or receive an explicit reply
- blocked comments are visibly routed to the correct role
- comment processing is consistent across related drafts

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Owner workflow for processing comments on draft ADRs.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- KOIOS: Keep the log lightweight; otherwise the comment workflow becomes a second ADR archive.
- VULCAN: The escalation step should preserve enough context that implementation concerns do not get lost when handed off.
