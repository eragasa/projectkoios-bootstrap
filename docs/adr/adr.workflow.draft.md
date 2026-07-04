# ADR 20260702.125257Z: Workflow Ontology for ADR Lifecycle

## Status

draft
date: 20260702.125257Z

## Context

Origin: user request
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap workflow ontology surface
Repository: projectkoios-bootstrap
Architecture-Domain: software

Project Koios wants workflow language that is first-class, explicit, and Petri-net-shaped without forcing the repo to speak only in Petri-net jargon. The workflow model should be the primary control vocabulary; ADRs are artifacts that bind to it later.

The current source of confusion is that "routing" describes movement without describing state change. The repo needs a model where agents act on objects, gates permit or block transitions, and state change is the thing being observed.

## Decision

Adopt a workflow ontology with these primary concepts:

- `State` — the named condition or position of an object
- `Transition` — the connection between states that can move an object forward
- `Gate` — the control behavior of a transition node
- `Operator` — the agent or harness that acts on the object
- `WorkflowObject` — the artifact being advanced through states

Map the workflow ontology to Petri-net semantics as follows:

- `State` corresponds to a Petri-net place
- `Transition` corresponds to a Petri-net transition node
- `Gate` is the control function of the transition node
- `Operator` acts on the workflow object and requests or enables movement
- the transition node is the thing that connects states and enforces the gate

The ontology must support entrance, transition, and exit control points:

- `Entrance Gate` — permits entry into the workflow surface
- `Transition Gate` — permits movement from one state to another
- `Exit Gate` — signals termination or completion

Routing is not a first-class concept in this model. State transition semantics replace routing semantics.

This note is the mother surface for all `adr.workflow-*` documents and for the later ADR-binding note.

## Consequences

- workflow language becomes explicit instead of implied
- agents are understood as operators that cause state changes
- gates become control objects rather than comments
- ADR lifecycle can later be modeled natively as a workflow
- routing language can be retired in favor of state-transition language

## architecture-spec

The workflow ontology defines:

- the meaning of `State`, `Transition`, `Gate`, `Operator`, and `WorkflowObject`
- the Petri-net correspondence for each term
- the difference between transition structure and gate behavior
- the entrance / transition / exit control roles
- the rule that state transition, not routing, is the primary lifecycle motion

Stated negatively:

- no routing as the canonical lifecycle abstraction
- no agent-as-path concept
- no transition without a state-to-state relationship
- no gate semantics hidden inside prose alone

## acceptance-criteria

- a reviewer can explain the workflow model without using routing language
- a reviewer can map each workflow term to the corresponding Petri-net concept
- the model clearly separates state, transition, gate, and operator
- entrance, transition, and exit control points are understandable from the note alone
- the model is suitable as the parent reference for ADR-bound workflow documents

## implementation-brief

If accepted, update `adr.adr-workflow.draft.md`, the ADR template guidance, and related lifecycle notes so they use the workflow vocabulary defined here.

## resolved_open_questions

- Should transition roles be modeled as explicit node labels or derived gate roles?
- Should gate semantics be mirrored in JSON as well as Markdown?
- Should the workflow ontology include token terminology now or defer it to the executor ADR?

## non_goals

- defining the full workflow executor implementation
- prescribing a specific Petri-net library
- defining ADR instance fields
- reintroducing routing as the primary abstraction

## validation_expectations

- a sample lifecycle can be described using state, transition, gate, and operator language
- the note can serve as the parent reference for ADR workflow binding
- a reader can distinguish control behavior from the node connection itself

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Workflow ontology surface; Petri-net-shaped lifecycle vocabulary.

## links

- back_to: architecture.00
- child: [ADR 20260702.125257Z: ADR-to-Workflow Binding](adr.adr-workflow.draft.md)
- related: [ADR 20260702.121432Z: Adversarial Two-Plane Gate](adr.adversarial-two-plane-gate.draft.md)
- related: [ADR 20260702.030000: Implementation Brief Verification Method](adr.implementation-brief-verification-method.draft.md)
- supersedes: None
- superseded_by: None
