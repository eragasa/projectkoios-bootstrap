# ADR 20260702.125257Z: ADR-to-Workflow Binding

## Status

draft
date: 20260702.125257Z

## Context

Origin: user request
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap ADR binding surface
Repository: projectkoios-bootstrap
Architecture-Domain: software

The workflow ontology defines the control language. This note binds ADRs to that language so individual `adr.adr-*.md` files can participate in lifecycle transitions without inventing a separate process taxonomy.

The binding layer should stay close to implementation specifics: it is where an ADR declares its current state, which gates matter to it, and which gating ADR is responsible for allowing the transition.

## Decision

Bind ADRs to the workflow ontology as first-class workflow objects.

An ADR instance may declare workflow binding fields such as:

- `Current State`
- `Allowed Operators`
- `Entrance Gate`
- `Transition Gate`
- `Exit Gate`
- `Gating ADR`
- `Blocked By`
- `Enabled By`

Rules for the binding surface:

- `adr.adr-*.md` is the place where ADRs attach to workflow semantics
- gate fields are optional
- if a gate field is present, it must point at the specific gating ADR by filename link
- gate semantics are control semantics, not commentary
- the ADR itself is the object moving through states
- operators act on the ADR object to produce a new state
- routing is not used as the canonical binding abstraction

The binding note does not redefine the workflow ontology. It applies the ontology to ADR instances.

## Consequences

- ADRs become inspectable workflow objects
- gate references become explicit and traceable
- lifecycle control can be reasoned about without a separate routing model
- future tooling can validate ADR transitions against declared gates
- ADR template fields can be kept aligned with workflow semantics

## architecture-spec

The ADR binding layer defines:

- how an ADR declares its workflow state
- how an ADR points to its controlling gate or gating ADR
- how operators are named in the ADR surface
- how transition-related fields map onto the workflow ontology
- the rule that gate references, when present, must resolve to explicit ADR links

Stated negatively:

- no routing field as the primary control surface
- no gate reference without a target ADR
- no state transitions hidden in prose only
- no duplicate workflow ontology inside instance-level ADRs

## acceptance-criteria

- a reviewer can look at an ADR and tell what workflow state it is in
- a reviewer can see which gate, if any, controls the transition
- the gate reference points to a specific ADR
- the ADR binding fields do not redefine the workflow ontology
- the binding layer is suitable for use in `adr.adr-*.md` files

## implementation-brief

If accepted, update the ADR template guidance and any ADR-instance guidance so `adr.adr-*.md` files can declare workflow state and gate references consistently.

## resolved_open_questions

- Should every ADR instance require `Current State`, or only workflow-bound ADRs?
- Should entrance, transition, and exit gates all be optional per ADR instance?
- Should these fields be rendered in Markdown only or mirrored into JSON immediately?

## non_goals

- redefining the workflow ontology
- building the executor implementation
- turning routing back into the primary abstraction
- requiring every ADR to expose all gate fields

## validation_expectations

- a sample ADR instance can point to a gating ADR without ambiguity
- the instance-level binding fields read like workflow state, not prose routing
- the binding surface remains consistent with `adr.workflow.draft.md`

## routing

- Owner: Athena
- Next phase: proposed
- Notes: ADR-instance binding surface; workflow fields for `adr.adr-*.md`.

## links

- back_to: [ADR 20260702.125257Z: Workflow Ontology for ADR Lifecycle](adr.workflow.draft.md)
- related: [ADR 20260702.121432Z: Adversarial Two-Plane Gate](adr.adversarial-two-plane-gate.draft.md)
- related: [ADR 20260702.030000: Implementation Brief Verification Method](adr.implementation-brief-verification-method.draft.md)
- supersedes: None
- superseded_by: None
