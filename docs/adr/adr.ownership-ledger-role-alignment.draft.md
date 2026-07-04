# ADR 20260702.121432Z: Ownership Ledger and Role Alignment

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

The adversarial two-plane gate needs an authoritative way to record who owns PetriNet places and transitions. That ownership must be transferable, and the closest role alignment should determine who owns a place or transition at a given time.

The exact runtime implementation is not yet known. The definition belongs in an ADR now, while the concrete storage/runtime mechanism can be implemented later. The lack of a runtime definition is intentional because it should gate development until implementation phase forces a concrete choice.

## Decision

Define an ownership ledger as the authoritative record of current owners for PetriNet places and transitions.

Rules:
- the ledger records places, transitions, and their current owners
- ownership is transferable between agents
- the closest role alignment determines the current owner when ownership is reassigned
- the terminal owner can always request an ADR once the implementation is complete
- the runtime implementation may be chosen later

## Consequences

- ownership becomes explicit instead of implicit
- specialized agents can take over ownership as the system evolves
- the architecture can define control boundaries before the runtime exists
- implementation work is gated until the runtime choice is made
- the eventual runtime can be chosen to preserve the ledger semantics with the least complexity
- the terminal owner can request an ADR without breaking the ledger model

## architecture-spec

The ledger is a conceptual and architectural record, not yet a committed runtime.

It must support:
- place ownership
- transition ownership
- ownership transfer
- role-alignment-based reassignment

The ledger is the authority that the adversarial two-plane gate consults when deciding who can control a place or transition.

## acceptance-criteria

- a reviewer can explain what the ledger owns
- ownership can move between agents without rewriting the architecture
- the runtime implementation can be deferred without losing the decision
- specialized agents can be added by adjusting role alignment, not by changing the gate definition

## implementation-brief

If accepted, define the runtime representation of the ledger and the transfer mechanism, then connect it to the adversarial two-plane gate.

verification_method: confirm that a place or transition can change owner without changing the gate semantics or losing the current owner record.

## resolved_open_questions

- What runtime should store the ledger?
- Should the ledger live in a file, a database, or both?
- How should role alignment be scored when more than one agent matches?

## non_goals

- choosing the runtime implementation now
- collapsing ownership into the agent identity itself
- removing the adversarial two-plane gate

## validation_expectations

- ownership can be described independently of the runtime
- the ledger can be linked from the gate ADR
- a specialist agent can take ownership without reworking the gate semantics

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Ownership authority surface for PetriNet places and transitions.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
