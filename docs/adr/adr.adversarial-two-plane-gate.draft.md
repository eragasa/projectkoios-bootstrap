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
Architecture-Domain: software

This ADR defines the gate between architecture work and implementation work. The gate should be concrete, not abstract: it needs named objects, named actions, and explicit entry and exit requirements.

This ADR focuses on object-and-action chaining. Ownership is referenced here only as a control concern; the ownership ledger itself lives in its own ADR.

## Definitions

- DataObject: an inanimate state-bearing object.
- ActionObject: a grouped action that consumes and/or produces DataObjects.
- Entry Gate: the point where a topic is checked for readiness to become a spike or ADR.
- Exit Gate: the point where implementation is checked for validated return to architecture.
- Transition: a deterministic ActionObject that moves a DataObject through a gate.
- Entry requirement: the DataObjects and conditions that must exist before a node can enter.
- Exit requirement: the DataObjects and conditions that must exist before a node can leave.

## Decision

Adopt the adversarial two-plane gate as a first-class architecture object.

The gate has two gates:
- the Entry Gate, which governs idea → spike → ADR readiness
- the Exit Gate, which governs implementation brief completion and return-to-architecture validation

The implementation brief is the completion point of the gate. Its `verification_method` records how implementation returns a validated result back to architecture.

The most obvious candidate for a transition is Hermes interacting with the user, but that is only one implementation of the object-to-action chain. Transition ownership must remain transferable across agents and should follow the closest role alignment.

## Consequences

- entry readiness and exit verification stay separate but coupled
- each gate can reject vague or incomplete work from the other gate
- implementation briefs become completion records instead of loose delivery notes
- the gate can be discussed, reviewed, and refined as its own encapsulated ADR
- the transition cannot complete unless both sides approve

## architecture-spec

The adversarial two-plane gate is a knowledge object spanning two control surfaces:

1. Entry Gate
   - decides whether a topic is ready to become a spike or ADR
   - checks boundedness, exit conditions, and downstream ownership

2. Exit Gate
   - decides whether implementation has satisfied the architecture intent
   - checks the brief's `verification_method`

The two gates are adversarial only in the sense that each may block the other until the requirements are explicit. The gate requires approval from both sides before a transition completes.

## acceptance-criteria

- a reviewer can explain both gates without guessing
- the gate clearly distinguishes readiness from verification
- the implementation brief is recognized as the completion point of the gate
- the rule can be linked from both the workflow ADR and the verification ADR

## implementation-brief

The implementation block lives in `docs/implementation/implementation.adversarial-two-plane-gate.md`.

- related: [Implementation Note: Adversarial Two-Plane Gate](../../implementation/implementation.adversarial-two-plane-gate.md)

## resolved_open_questions

- Should the gate terminology remain exactly "adversarial two-plane gate" or gain a plain-language alias?
- How should the ownership ledger represent places, transitions, and current owners?
- How should role-alignment rules be encoded so specialized agents can assume ownership cleanly?

## non_goals

- collapsing readiness and verification into one surface
- defining every possible implementation brief field
- replacing the existing ADR lifecycle

## validation_expectations

- the gate can be described as two explicit gates with separate duties
- the brief completion point is visible in the ADR surface
- workflow and implementation can each reject ambiguity from the other side

## routing

- Owner: Athena
- Next phase: proposed
- Notes: High-level control object spanning readiness and verification surfaces.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
