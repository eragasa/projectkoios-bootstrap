# ADR 20260702.121432Z: Spike Entry Conditions and Packaging

## Status

draft
date: 20260702.121432Z

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

The repository needs a clear rule for what a spike is. VULCAN's decision is that a spike is not a separate artifact class; it is a draft ADR packaged with an implementation attachment.

Without this rule, spikes drift into a parallel taxonomy and the repo splits decision work from build work. That creates duplicated authority, unclear promotion, and noisy lifecycle state.

This ADR defines the minimum conditions for a spike package and the rule for moving a topic from incubator material into spike form.

## Decision

A spike is valid only when it is anchored to a draft ADR and includes an implementation attachment.

### Required shape

- **Draft ADR**: the authoritative decision surface
- **Implementation attachment**: notes, plan, tests, or patch work that exercises the draft decision
- **Spike**: the working package containing both while the decision is still being explored

### Minimum conditions

A topic may be treated as a spike only if it has:

- one bounded question
- one draft ADR
- one implementation attachment
- one clear exit condition
- one owner for the ADR

### Operational review

- A spike should remain bounded and reviewable.
- If a spike and its attached work have not moved for three days, bring it to human review for archive, continuation, or conversion.
- The spike may evolve, but it does not become a new artifact class.

### Rules

- A spike must not exist without a draft ADR.
- The ADR remains the authoritative architecture artifact.
- The implementation attachment is subordinate to the ADR.
- Spike findings may refine the ADR or the attachment, but they do not create a new artifact family.
- Promotion means the ADR is stabilized and the attachment is either attached, rewritten, or split out as needed.
- `docs/spikes/` is staging for draft ADR work, not a competing decision surface.

## Consequences

- spikes become easier to review because decision and build work stay coupled
- ADRs remain the canonical architectural record
- implementation work stays visible without inventing a separate taxonomy
- promotion becomes a packaging/normalization step rather than a category change
- workflow docs and templates must reflect the ADR + attachment model

## architecture-spec

This ADR defines the entry gate for spike packages.

The gate requires:
- one question
- one draft ADR
- one implementation attachment
- one clear exit condition
- one owner

Stated negatively:
- no spike without an ADR anchor
- no spike without attached build work
- no open-ended exploration
- no parallel spike ontology

## acceptance-criteria

- a reviewer can tell whether a spike is anchored to a draft ADR
- a reviewer can identify the implementation attachment
- a spike without a draft ADR is rejected
- a spike without an implementation attachment is rejected
- the repo no longer treats spikes as a separate artifact class

## implementation-brief

If accepted, update spike templates and workflow guidance so:
- spike creation requires a draft ADR
- spike notes reference the implementation attachment
- promotion normalizes the draft ADR and attachment into the main ADR lifecycle

## validation_method

Review a sample topic and confirm it either:
- remains idea/incubator material, or
- becomes a draft ADR with an implementation attachment

## routing

- Owner: Athena
- Next phase: proposed
