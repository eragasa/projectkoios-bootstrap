# ADR 20260702.121432Z: Adversarial Two-Plane Gate

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

The workflow and verification surfaces are not the same gate. The workflow surface decides whether a topic is ready to move forward; the verification surface decides whether implementation has returned a validated result back to architecture.

DataObjects and ActionObjects are a high-level separation of concerns: mutable structs and actions on those structs that produce a new DataObject. In workflow terms, the relevant primitives are PetriNet places and deterministic transitions, and ownership of places must be transferable between entities.

Those two surfaces control each other's gate. That makes the boundary intentionally adversarial: each side must be able to block progress until the other side is precise enough to continue.

Ownership is recorded in a ledger that maps places and transitions to agents. The closest role alignment determines current ownership, which allows new specialized agents to take over as the system evolves.

## Decision

Adopt the adversarial two-plane gate as a first-class architecture object.

The gate has two places:
- the workflow place, which governs idea → spike → ADR readiness
- the verification place, which governs implementation brief completion and return-to-architecture validation

Ownership of each place and transition is tracked in a separate ledger.

The implementation brief is the completion point of the gate. Its `verification_method` records how implementation returns a validated result back to architecture.

The most obvious candidate for a transition is Hermes interacting with the user, but that is only one implementation of the ownership ledger. Transition ownership must remain transferrable across agents and should follow the closest role alignment.

## Consequences

- workflow and verification remain separate but coupled
- each plane can reject vague or incomplete work from the other plane
- implementation briefs become completion records instead of loose delivery notes
- the gate can be discussed, reviewed, and refined as its own encapsulated ADR

## architecture-spec

The adversarial two-plane gate is a knowledge object spanning two control surfaces:

1. Workflow place
   - decides whether a topic is ready to become a spike or ADR
   - checks boundedness, exit conditions, and downstream ownership

2. Verification place
   - decides whether implementation has satisfied the architecture intent
   - checks the brief's `verification_method`

The two places are adversarial only in the sense that each may block the other until the requirements are explicit.

## acceptance-criteria

- a reviewer can explain both planes without guessing
- the gate clearly distinguishes workflow readiness from implementation verification
- the implementation brief is recognized as the completion point of the gate
- the rule can be linked from both the workflow ADR and the verification ADR

## implementation-brief

If accepted, update the workflow ADR, the verification-method ADR, and the ownership-ledger ADR so they all reference the adversarial two-plane gate and use consistent completion language.

verification_method: review the workflow ADR and the verification ADR together, then confirm that the brief is the completion point and that neither plane can silently bypass the other.

## resolved_open_questions

- Should the gate terminology remain exactly "adversarial two-plane gate" or gain a plain-language alias?
- How should the ownership ledger represent places, transitions, and current owners?
- How should role-alignment rules be encoded so specialized agents can assume ownership cleanly?

## non_goals

- collapsing workflow and verification into one surface
- defining every possible implementation brief field
- replacing the existing ADR lifecycle

## validation_expectations

- the gate can be described as two explicit planes with separate duties
- the brief completion point is visible in the ADR surface
- workflow and implementation can each reject ambiguity from the other side

## routing

- Owner: Athena
- Next phase: proposed
- Notes: High-level control object spanning workflow and verification surfaces.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
