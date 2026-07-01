# ADR 20260702.012900: ADR Draft Comment and Promotion Workflow

## Status

draft

## Context

Origin: user request
From: Hermes
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

Draft ADRs need a defined comment lifecycle so agents can keep reviewing and shaping them before they are promoted. The repository also needs a clear promotion boundary: once a draft becomes proposed, the proposed ADR becomes the active review surface and the draft should be archived as superseded history.

The workflow also needs to reflect how ADRs move from spike output into the main source tree. Proposed ADRs are the iteration surface for MVP-oriented refinement, while accepted ADRs represent the stabilized decision that can drive implementation and promotion into the main tree.

## Decision

Allow comments on ADR drafts until the draft is promoted to proposed.

When a draft ADR is promoted:

- the proposed ADR supersedes the draft ADR
- the draft ADR is archived as historic/superseded material
- comments continue on the proposed ADR, not the archived draft

Use the following promotion model:

- spike output becomes a draft ADR when it is ready for durable wording
- draft ADRs stay comment-open while they are being shaped
- proposed ADRs are the active iteration surface for review and MVP refinement
- accepted ADRs represent the stabilized decision and are eligible to drive implementation in the main source tree

## Consequences

- agents can comment directly on draft ADRs without ambiguity
- there is a single active review surface after promotion
- draft history remains available without competing with the proposed version
- accepted ADRs become the clear handoff point into implementation work

## architecture-spec

This ADR defines the lifecycle for commentable draft ADRs and their promotion into proposed and accepted states.

The lifecycle is:

`spike -> draft ADR (comment-open) -> proposed ADR (review/MVP iteration) -> accepted ADR (stabilized) -> implementation`

## acceptance-criteria

- Draft ADRs can receive agent comments before promotion
- Promotion to proposed creates a new active surface
- The draft ADR is archived or marked superseded after promotion
- Proposed ADRs become the main review/iteration surface
- Accepted ADRs are understood as the stabilized decision for implementation

## implementation-brief

If accepted, update the ADR template and any workflow guidance so draft ADRs are comment-open, proposed ADRs are the active review surface, and accepted ADRs are the implementation handoff point.

## resolved_open_questions

- Should all comments be append-only, or can they be edited while the ADR remains draft?
- Should proposed ADRs keep a visible backlink to the archived draft?
- Should accepted ADRs always originate from spike output, or can some be promoted directly from draft?

## non_goals

- Changing the canonical ADR JSON schema
- Removing historical draft ADRs
- Forcing every idea through a spike before it can become a draft ADR

## validation-expectations

- A reviewer can tell which ADR is the active surface for comments
- A promoted ADR clearly supersedes the draft version
- The lifecycle is understandable from the file and status alone

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Draft/proposed/accepted comment and promotion workflow for ADRs.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- KOIOS: Good direction; the exact draft-to-proposed promotion mechanics still need to be made concrete.
- KOIOS: Keep a visible backlink from proposed to archived draft so the review trail remains traceable.
