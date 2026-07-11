```json
{
  "title": "Petri-net Workflow Runtime",
  "artifact_type": "architecture-note",
  "status": "working-draft",
  "datetime": "20260705.180521",
  "updated_on": "20260705",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "bootstrap-held workflow runtime architecture decomposition",
  "canonical_location": "docs/architecture/architecture.petrinet.00.md",
  "moved_from": "dev/petrinet-runtime-authority/architecture-proposal.20260705.180521_petrinet-workflow-runtime.md",
  "controlling_context": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "source_input": "user proposal in Athena session 20260705",
  "next_phase": "maintain as single Petri-net architecture elaboration surface until a section is decomposed into bounded ADR/spec slices"
}
```

# Architecture: Petri-net Workflow Runtime

## Status

working-draft

## Purpose

Lay out the broader Petri-net workflow runtime direction, then decompose it into bounded ADR/spec/implementation slices.

This is not yet an accepted ADR. It is a working architecture proposal and decomposition surface.

## Authority boundary

This architecture note is scoped to `projectkoios-bootstrap` and the bootstrap-held `src/python/projectkoios/workflow` implementation surface.

It does not decide mothership/product-domain workflow semantics unless separately accepted in that domain.

Accepted context:

- `docs/adr/adr.petrinet.20260705.132740Z.md` already controls the first-slice separation of Petri-net definition, marking, binding, request, state, executor, and events.

## Working-document policy

This document is the single working elaboration surface for Petri-net architecture until a section is explicitly decomposed into a bounded ADR, architecture spec, implementation brief, or validation plan.

Rules:

- New Petri-net architecture ideas SHOULD be added here first.
- Do not create parallel Petri-net proposal files unless this document explicitly links to the decomposed child surface.
- When a section becomes decision-ready, extract only that bounded decision into an ADR proposal and leave a link/back-reference here.
- When a section becomes implementation-ready, extract only that bounded implementation scope into a Vulcan brief and leave a link/back-reference here.
- Historical documents remain provenance; this document is the current workspace-level synthesis surface, not accepted authority by itself.

## Source inventory

Current Petri-net development documents collected for synthesis:

### Accepted/current control

- `docs/adr/adr.petrinet.20260705.132740Z.md` — accepted first-slice Petri-net separation ADR.
- `docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md` — older workflow executor draft; current first-slice vocabulary points to accepted Petri-net ADR.
- `docs/plans/projectkoios-workflow-petri-net-executor.md` — older implementation plan; current first-slice vocabulary points to accepted Petri-net ADR.
- `docs/petri-net-model.md` — read-only colored Petri-net handoff evaluator model.

### Accepted ADR source package

- `dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.record.json`
- `dev/petrinet-definition-marking-runtime/adr.20260705.132740_petrinet-definition-marking-runtime.schema-backed.md`
- `dev/petrinet-definition-marking-runtime/user-proposal.20260705.132740_petrinet-definition-marking-runtime.md`
- `dev/petrinet-definition-marking-runtime/decision-source-addendum.20260705.md`

### Implementation evidence and reviews

- `docs/implementation/workflow-petri-net-executor-first-slice.20260705.102506.md`
- `docs/implementation/workflow-adapter-dependency-encapsulation.20260705.105604.md`
- `docs/implementation/petrinet-separation-adr-remediation.20260705.142149.md`
- `docs/implementation/petrinet-followups.20260705.173808.md`
- `docs/implementation/workflow-adapter-contract-hardening.20260706.045501.md`
- `docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md`
- `docs/reviews/architecture-conformance.20260705.174118_petrinet-followups.md`
- `docs/reviews/architecture-conformance.20260706.023601_workflow-adapter-topology-roundtrip.md`

### Implementation briefs and process capture

- `docs/plans/implementation-brief.20260706_workflow-adapter-topology-roundtrip.md` — ATHENA-owned brief preserving the topology-only adapter round-trip acceptance criteria that were initially conveyed by intercom.
- `docs/process-capture/pc.workflow.document-trace.md` — KOIOS process capture for workflow/document trace context.
- `docs/process-capture/pc.workflow.document-trace.20260706.025408Z.md` — KOIOS process capture snapshot for the same trace context.

### Related draft/workflow surfaces

- `docs/adr/adr.workflow.draft.md`
- `docs/adr/adr.adr-workflow.draft.md`
- `docs/adr/adr.workflow-ui.draft.md`
- `docs/architecture/architecture.workflow-ui.md`
- `docs/architecture/architecture.draft-comment-and-promotion-workflow.md`
- `docs/process-capture/workflow.process-capture.md`
- `docs/process-capture/20260704T091052Z_subagent-intercom-workflow-design-input.md`

### Historical provenance

- `docs/archive/architecture/adr/adr.20260630.042202_colored-petri-net-meta-harness.md`
- `docs/archive/architecture/adr/adr.20260630.171204_interactive-interview-petri-net-piv.md`
- `docs/archive/architecture/adr/adr.20260630.171442_first-class-interview-petri-net-phase.md`
- `docs/archive/handoffs/archon/20260630.042202_colored-petri-net-meta-harness.md`
- `docs/archive/handoffs/archon/20260630.044545_colored-petri-net-meta-harness-draft.md`

## Implementation

### Phase I

#### Implementation and Conformance Reports

- `docs/implementation/petrinet-separation-adr-remediation.20260705.142149.md`
- `docs/implementation/petrinet-followups.20260705.173808.md`
- `docs/implementation/workflow-adapter-contract-hardening.20260706.045501.md`
- `docs/reviews/architecture-conformance.20260706.023601_workflow-adapter-topology-roundtrip.md`
- `docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md`
- `docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md`
- `docs/reviews/architecture-conformance.20260711.115100_live-petri-net-skeleton-slice-0.md`

#### Workflow adapter topology round-trip slice

ATHENA brief: `docs/plans/implementation-brief.20260706_workflow-adapter-topology-roundtrip.md`.

The workflow adapter topology round-trip slice records the concrete adapter acceptance criteria requested by the user after the initial adapter-boundary work. It is bounded to bidirectional topology equivalence:

```text
canonical PetriNet / WorkflowNet
  -> backend representation
  -> canonical topology payload
```

Topology equivalence covers place IDs/labels, transition IDs/labels, arc endpoints, arc kind/direction, and weights. The comparison must be deterministic and must not depend on backend object identity or backend-specific ordering.

The current implementation uses SNAKES as the first backend and keeps it as a dev/test dependency only. Normal adapter export remains library-neutral and optional backend imports remain lazy and adapter-owned.

Non-goals for this slice: token/marking state, guards/callables, execution history, event provenance, persistence/restart, event bus, handoff migration, PM4Py conversion, and product workflow semantics.

#### Live Petri-net skeleton slice 0

ATHENA brief: `docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md`.

Implementation evidence:

- `docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md`
- `docs/reviews/architecture-conformance.20260711.115100_live-petri-net-skeleton-slice-0.md`

`live-petri-net-skeleton-slice-0` adds the first directly inspectable CLI status surface:

```bash
uv run projectkoios workflow status
```

As built, the command loads the static bootstrap fixture `dev/workflow-nets/bootstrap-harness.workflow-net.json`, maps it into existing `projectkoios.workflow` Petri-net runtime classes, validates/computes enabled transitions through `PetriNetExecutor.enabled_bindings(...)`, and prints workflow id, fixture path, places, token locations, enabled transitions, and whether user decision is required.

This slice is intentionally read-only. It does not add transition firing, persistence, event-log storage, Operator Console integration, workflow-object integration, graph UI, `docs/schemas/` authority, generalized loader/schema authority, role/permission expansion, live adapters, or product/mothership workflow authority.

The static fixture is a bootstrap inspectability fixture, not canonical workflow authority. It proves the user's requested pivot from document/process surfaces toward visibly inspectable Petri-net workflow state.

## Decomposition map

| Section | Current state | Decomposes to | Trigger |
|---|---|---|---|
| Runtime authority and firing request semantics | working | ADR proposal | when actor/request mutation authority needs acceptance |
| Transition permissions | working | ADR or architecture spec | when role/permission model affects executor semantics |
| Produced token semantics | working | ADR/spec | when output tokens must be generated rather than moved/preserved |
| Provenance-bearing runtime events | working | ADR/spec | when audit payload exceeds debug event collection |
| Dry-run execution | working | ADR/spec | when planning/simulation must be non-authoritative |
| WorkflowNet domain wrapper | working | ADR/spec | when workflow-specific semantics exceed generic PetriNet |
| Workflow adapter topology round trip | completed/validated | implementation brief + implementation report + conformance review | completed SNAKES topology-only round trip; expand only with new authority for PM4Py, markings/tokens, guards, runtime history, or persistence semantics |
| UI/Gantt/projection surfaces | incubating | architecture spec | when a projection target is selected |
| Ingestion pipeline workflows | incubating | product/bootstrap boundary ADR | when a concrete pipeline fixture is selected |

## Context

Project Koios needs a workflow model that can represent structured work, agent actions, human review, provenance, rework, and executable state transitions.

A conventional workflow implementation would likely collapse the process into procedural code or a single global status field:

```text
draft → review → implementation → approved
```

That is too weak for multi-agent execution, ingestion, provenance, and auditability. The system needs a state model where:

- workflow structure is explicit;
- current state is inspectable;
- transitions are validated before mutation;
- work items are represented as tokens;
- provenance can be attached to transition events;
- agents do not directly mutate canonical state.

The proposed model is a Petri-net-style runtime.

The static workflow net is:

```text
N = (P, T, A)
```

where:

- `P` is the set of places;
- `T` is the set of transitions;
- `A` is the set of arcs.

The runtime state is a marking:

```text
M : P -> Multiset(Token)
```

The full runtime state is:

```text
(N, M)
```

A transition firing is:

```text
(N, M) --[t,b]--> (N, M')
```

where:

- `t ∈ T` is the selected transition;
- `b` is the transition binding;
- `M'` is the new marking.

## Proposal

Implement the workflow runtime as a Petri-net execution system with three conceptual layers:

```text
Static net definition
Runtime state
Execution runtime
```

## Static net definition

The static layer defines the allowed workflow structure.

Conceptual objects:

```text
PetriNet
Place
Transition
InputArc
OutputArc
TransitionGuard
```

First-slice implementation names are controlled by `docs/adr/adr.petrinet.20260705.132740Z.md` and use prefixed names such as `PetriNetPlace`, `PetriNetTransition`, `PetriNetArc`, and `PetriNetArcKind`.

A `PetriNet` owns the static graph:

```text
PetriNet
├── places
├── transitions
└── arcs
```

For the accepted first slice, arcs remain `PetriNetArc + PetriNetArcKind` under YAGNI rather than separate `InputArc` and `OutputArc` classes.

A `Place` is a stable location in the graph. It has identity and metadata. It does not own tokens.

A `Transition` is a possible state change. It defines what may fire and may have a guard.

An input arc connects a place to a transition and defines what is consumed.

An output arc connects a transition to a place and defines what is produced.

A `TransitionGuard` is a predicate evaluated by the executor before committing a transition.

## Runtime state

The runtime layer represents a particular state of a Petri net.

Conceptual objects:

```text
Token
Marking
TransitionBinding
FiringRequest
PetriNetState
```

First-slice implementation names are prefixed:

```text
PetriNetToken
PetriNetMarking
PetriNetTransitionBinding
PetriNetFiringRequest
PetriNetState
```

A `Token` represents a work item, artifact, message, fact, code patch, review finding, approval, or other unit of runtime state.

A `Marking` maps place IDs to token multisets:

```python
Mapping[PlaceId, TokenMultiset]
```

A `TransitionBinding` is the concrete selection of tokens that satisfy a transition's input requirements.

A `FiringRequest` is an explicit request to fire a transition.

A `PetriNetState` pairs the static net with the current marking:

```python
@dataclass(frozen=True)
class PetriNetState:
    net: PetriNet
    marking: PetriNetMarking
```

## Execution runtime

The execution layer validates and commits state changes.

Conceptual objects:

```text
BindingResolver
PetriNetExecutor
TransitionFiredEvent
MarkingChangedEvent
```

First-slice implementation names include:

```text
PetriNetExecutor
PetriNetTransitionFiredEvent
PetriNetMarkingChangedEvent
PetriNetEventCollection
```

The executor is the only component allowed to advance canonical workflow state.

The execution flow is:

```text
PetriNetState
+ PetriNetFiringRequest
→ resolve PetriNetTransitionBinding
→ validate actor permissions
→ validate TransitionGuard
→ consume input tokens
→ produce output tokens
→ return new PetriNetState
→ append PetriNetTransitionFiredEvent / PetriNetMarkingChangedEvent
```

## Naming decision candidate

Use conceptual terms in architecture prose:

```text
PetriNet
Place
Transition
InputArc
OutputArc
Token
Marking
TransitionBinding
FiringRequest
PetriNetState
TransitionGuard
BindingResolver
PetriNetExecutor
TransitionFiredEvent
MarkingChangedEvent
```

Use prefixed implementation names for the bootstrap-held first implementation slice:

```text
PetriNetPlace
PetriNetTransition
PetriNetToken
PetriNetArc
PetriNetArcKind
PetriNetMarking
PetriNetTransitionBinding
PetriNetFiringRequest
PetriNetState
PetriNetExecutor
PetriNetTransitionFiredEvent
PetriNetMarkingChangedEvent
PetriNetEventCollection
```

Avoid:

```text
FiringRule
ExecutionState
on_update
place.tokens
transition.fire_mutating_state()
```

`FiringRule` is rejected because the object is not a rule of Petri-net semantics. It is a request.

`ExecutionState` is rejected for the net-plus-marking pair because it is too broad. Use `PetriNetState`.

`Place` must not own tokens. Token distribution belongs only to `Marking`.

## Minimal implementation shape candidate

This shape is a decomposition input, not yet accepted implementation authority.

```python
@dataclass(frozen=True)
class PetriNet:
    places: Mapping[PlaceId, PetriNetPlace]
    transitions: Mapping[TransitionId, PetriNetTransition]
    arcs: tuple[PetriNetArc, ...]


@dataclass(frozen=True)
class PetriNetPlace:
    place_id: PlaceId
    label: str


@dataclass(frozen=True)
class PetriNetTransition:
    transition_id: TransitionId
    label: str
    allowed_roles: frozenset[str]
    guard: PetriNetTransitionGuard | None = None


@dataclass(frozen=True)
class PetriNetArc:
    place_id: PlaceId
    transition_id: TransitionId
    kind: PetriNetArcKind
    token_count: int = 1


@dataclass(frozen=True)
class PetriNetToken:
    token_id: TokenId
    color: str
    data: Mapping[str, object]


@dataclass(frozen=True)
class PetriNetMarking:
    tokens_by_place: Mapping[PlaceId, tuple[PetriNetToken, ...]]


@dataclass(frozen=True)
class PetriNetState:
    net: PetriNet
    marking: PetriNetMarking


@dataclass(frozen=True)
class PetriNetTransitionBinding:
    transition_id: TransitionId
    consumed: Mapping[PlaceId, tuple[PetriNetToken, ...]]


@dataclass(frozen=True)
class PetriNetFiringRequest:
    transition_id: TransitionId
    binding: PetriNetTransitionBinding | None = None
    actor: AgentIdentity | None = None
    produced_tokens: tuple[PetriNetToken, ...] = ()
```

## Decomposition candidates

### Slice A: Firing request authority and actor identity

Potential ADR: `PetriNet Firing Request Authority`

Decision candidates:

- Agents and humans submit `PetriNetFiringRequest`; they do not mutate canonical marking directly.
- `PetriNetExecutor` is the only runtime component that advances canonical `PetriNetState`.
- `PetriNetFiringRequest` may carry `actor` identity.
- Actor identity is checked before guard evaluation or state mutation.

Open questions:

- What is the minimal `AgentIdentity` shape?
- Is actor identity required for every request or optional in the first slice?
- Does actor identity live in the generic Petri-net layer or a workflow wrapper layer?

### Slice B: Transition permissions

Potential ADR/spec: `PetriNet Transition Permission Model`

Decision candidates:

- `PetriNetTransition` may declare allowed roles or permission requirements.
- `PetriNetExecutor` validates actor permission before firing.
- Permission failures produce typed errors/events and do not mutate state.

Open questions:

- Is `allowed_roles: frozenset[str]` sufficient?
- Should permissions be generic Petri-net data or workflow-domain wrapper data?
- How do Athena/Vulcan/Koios/Hermes identities map to runtime roles?

### Slice C: Produced token semantics

Potential ADR/spec: `PetriNet Produced Token Semantics`

Decision candidates:

- A firing may produce explicit tokens supplied by a request, a transition producer, or both.
- Output arcs determine placement; production rules determine token content.
- The first implementation must avoid silent token fabrication.

Open questions:

- Should produced tokens be included in `PetriNetFiringRequest`?
- Should transitions own token producer functions?
- Should output arcs have production metadata?
- How are consumed-token colors transformed into produced-token colors?

### Slice D: Provenance-bearing runtime events

Potential ADR/spec: `PetriNet Runtime Event Provenance`

Decision candidates:

- `PetriNetTransitionFiredEvent` should record transition ID, actor, binding, consumed token IDs, produced token IDs, and timestamp.
- `PetriNetMarkingChangedEvent` should record changed places and before/after token IDs.
- Events are append-only runtime evidence for debugging and audit.

Open questions:

- Are events part of generic `PetriNet` or workflow-specific `WorkflowNet` runtime?
- Should event timestamps be runtime-generated, injected clocks, or logical counters?
- What is the minimal provenance payload?

### Slice E: Dry-run execution

Potential ADR/spec: `PetriNet Dry-run Execution`

Decision candidates:

- Executor should support validating and simulating a firing without committing state.
- Dry-run should produce predicted new marking and events marked as non-authoritative.

Open questions:

- Is dry-run part of `PetriNetExecutor` or a separate planner?
- How are dry-run events distinguished from committed events?

### Slice F: WorkflowNet domain wrapper

Potential ADR/spec: `WorkflowNet Domain Wrapper Semantics`

Decision candidates:

- `PetriNet` remains a reusable substrate.
- `WorkflowNet` carries Project Koios workflow-specific semantics such as roles, artifact types, agent policies, and workflow inspection conventions.

Open questions:

- Should `WorkflowNet` subclass `PetriNet`, contain it, or adapt it?
- Which semantics must stay out of generic `PetriNet`?

### Slice G: UI / Gantt / projection surfaces

Potential architecture spec, not immediate ADR.

Decision candidates:

- Petri-net state and event log can be projected into UI/Gantt/read models.
- Projection surfaces must not mutate canonical state.

Open questions:

- Which projection is needed first?
- Does Gantt require duration estimates and resource semantics?

### Slice H: Ingestion pipeline workflows

Potential future ADR/spec.

Decision candidates:

- Ingestion jobs can be represented as tokens moving through a workflow net.
- Source acquisition, parsing, review, and provenance checks become transitions.

Open questions:

- Is this bootstrap-only or product-domain?
- Which ingestion pipeline is the first real workflow fixture?

## Immediate recommendation

The next bounded ADR should be Slice A:

```text
PetriNet Firing Request Authority
```

Rationale:

- It is the smallest decision that changes runtime semantics beyond the accepted first slice.
- It clarifies that agents/humans submit requests and the executor owns mutation.
- It creates a clean place to discuss actor identity without prematurely deciding the full permission model.

## Consequences

This architecture makes workflow state explicit and inspectable.

It supports, as future follow-on capabilities:

- dry-run execution;
- provenance;
- audit logs;
- human-in-the-loop checkpoints;
- multi-agent execution;
- review loops;
- rework routing;
- UI visualization;
- Gantt projections;
- ingestion pipelines;
- colored Petri-net compatibility.

The tradeoff is that even simple actions require explicit transition modeling. This is acceptable when the purpose is controlled, inspectable execution rather than ad hoc scripting.

## Decision summary candidate

Project Koios workflow execution should be modeled as a Petri-net runtime. Static workflow structure belongs to `PetriNet`. Runtime token distribution belongs to `PetriNetMarking`. State mutation belongs only to `PetriNetExecutor`. Agents and humans submit `PetriNetFiringRequest` objects; they do not directly mutate canonical workflow state.
