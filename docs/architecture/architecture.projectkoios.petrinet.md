# Architecture: projectkoios.petrinet first-class subsystem

```json
{
  "title": "projectkoios.petrinet first-class subsystem",
  "artifact_type": "architecture-note",
  "status": "working-draft",
  "datetime": "20260706.031842Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "proposed first-class Petri-net subsystem/package boundary for Project Koios",
  "canonical_location": "docs/architecture/architecture.projectkoios.petrinet.md",
  "source_proposal": "workspaces/koios/working/user-proposal.20260706T031715Z_projectkoios-petrinet-first-class-subsystem.md",
  "controlling_context": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "authority_boundary": "working architecture proposal only; not accepted ADR authority, implementation authority, extraction authority, or product-domain authority"
}
```

## Purpose

This note preserves and organizes the user's proposal for `projectkoios.petrinet` as a first-class Petri-net subsystem and possible extractable package/distribution.

The proposal is broader than the accepted bootstrap-held Petri-net vocabulary ADR at `docs/adr/adr.petrinet.20260705.132740Z.md`. That ADR controls the current bootstrap implementation vocabulary/runtime separation slice only. This note proposes a larger package boundary, subsystem layering, projection/adapter/event-log policies, packaging direction, and relationships to graph/workflow/application packages.

This note is a working-draft architecture surface. It does not create implementation or extraction authority until decomposed into an accepted ADR, specification, or implementation brief.

## Index

### Architecture Decomposition

| # | Surface | Role / Scope |
|---|---|---|
| 1 | `projectkoios.petrinet.modeling` | Declarative Petri-net language and static net definition. |
| 2 | `projectkoios.petrinet.runtime` | Runtime markings, tokens, bindings, firing requests, events, and executor semantics. |
| 3 | `projectkoios.petrinet.projections` | Internal read-model transformations from canonical models, markings, and event logs. |
| 4 | `projectkoios.petrinet.adapters` | External format/tool/storage bridges. |
| 5 | `projectkoios.petrinet.testing` | Test builders, fixtures, reference models, and golden serialization fixtures. |

### Controlling ADR

| # | ADR | Applicability |
|---|---|---|
| 1 | `docs/adr/adr.petrinet.20260705.132740Z.md` | Accepted authority for the narrower bootstrap-held Petri-net vocabulary/runtime separation slice. It does not accept this first-class subsystem proposal. |

### Source Material

| # | Source | Applicability |
|---|---|---|
| 1 | `workspaces/koios/working/user-proposal.20260706T031715Z_projectkoios-petrinet-first-class-subsystem.md` | KOIOS-preserved exact user proposal text. This note derives from that source and corrects the pasted heading typo to `Relationship to projectkoios.graph`. |

### Future ADR Candidates

| # | Candidate ADR | Trigger |
|---|---|---|
| 1 | `adr.petrinet-first-class-subsystem.<timestamp>.md` | User direction to accept or bind the package/subsystem boundary. |
| 2 | Adapter/file-format policy ADR | Need to bind JSON/YAML/Mermaid first and defer SQLite/NetworkX/Graphviz/PNML/db event stores. |
| 3 | Event-log policy ADR | Need to bind runtime event logs as committed append-only facts and projection sources. |
| 4 | Projection policy ADR/spec | Need to bind graph/Gantt/dashboard read models as derived views, not sources of workflow truth. |
| 5 | Architecture-note/subsystem schema ADR or implementation brief | Need to validate subsystem architecture content as first-class machine-readable records. |

## Package Boundary

Proposed import package:

```text
projectkoios.petrinet
```

Possible distribution name:

```text
projectkoios-petrinet
```

The package is proposed as the first-class Petri-net subsystem for Project Koios. It should not be buried under `projectkoios.graph`, `projectkoios.runtime`, or `projectkoios.ingestor` because Petri nets are central to agent workflows, ingestion pipelines, review loops, messaging protocols, human approval gates, provenance-preserving knowledge construction, workflow visualization, and dashboard projections.

Central rule:

```text
modeling defines the language
runtime interprets the language
projections derive read models
adapters connect to external formats and tools
```

## Layer Responsibilities

### `projectkoios.petrinet.modeling`

The modeling layer owns the declarative Petri-net language and static net definition.

Responsible for:

```text
static Petri-net structure
places
transitions
arcs
guard declarations
token color/type declarations
model validation
model serialization metadata
diagram/projection metadata
```

The modeling layer represents the static net:

```text
N = (P, T, A)
```

where `P` is places, `T` is transitions, and `A` is arcs.

Rules:

- A Petri-net model can exist, validate, serialize, and diagram without being executed.
- The modeling layer must not own runtime state.
- The modeling layer must not depend on markings, runtime token instances, bindings, firing requests, executors, event logs, timestamps, agent memory, or dashboard state.

### `projectkoios.petrinet.runtime`

The runtime layer owns execution semantics.

Responsible for:

```text
runtime tokens
markings
state snapshots
transition bindings
firing requests
guard evaluation
actor/role checks
transition firing
marking updates
runtime events
```

The runtime interprets a model plus a marking:

```text
(N, M)
M : P -> Multiset(Token)
(N, M) --[t,b]--> (N, M')
```

where `t` is the selected transition, `b` is the selected binding, and `M'` is the resulting marking.

Rules:

- The runtime may depend on modeling.
- The modeling layer must not depend on runtime.
- Models do not know execution exists; execution interprets models.

### `projectkoios.petrinet.projections`

The projections layer derives internal read models from canonical Petri-net objects.

Responsible for transformations such as:

```text
Petri-net model -> graph view
Petri-net model -> diagram view
Petri-net state -> marking board view
transition event log -> Gantt intervals
transition event log -> audit timeline
```

Rules:

- Projections are internal read-model transformations.
- Projections do not define Petri-net semantics.
- Projections do not mutate runtime state.

### `projectkoios.petrinet.adapters`

Adapters are external boundary code connecting Petri-net models, runtime states, events, and projections to external formats, tools, storage systems, and libraries.

Adapter responsibilities may include:

```text
YAML import/export
JSON import/export
PNML import/export
Mermaid export
Graphviz export
NetworkX conversion
SQLite persistence
JSONL event logs
filesystem model stores
```

Rules:

- Adapters must not define Petri-net semantics.
- Adapters must not own workflow state.
- Adapters must not be imported by the executor.

### `projectkoios.petrinet.testing`

The testing layer provides test builders, fixtures, and reference models.

It may depend on all internal layers.

Responsible for:

```text
minimal valid model builders
invalid model builders
sample markings
sample firing requests
sample event logs
golden serialization fixtures
```

Testing utilities should not become production APIs unless promoted deliberately.

## Package Layout

Target layout:

```text
projectkoios-petrinet/
├── pyproject.toml
├── README.md
├── src/
│   └── projectkoios/
│       └── petrinet/
│           ├── __init__.py
│           ├── modeling/
│           ├── runtime/
│           ├── projections/
│           ├── adapters/
│           └── testing/
└── tests/
    ├── modeling/
    ├── runtime/
    ├── projections/
    └── adapters/
```

Smaller starting layout:

```text
projectkoios-petrinet/
├── src/
│   └── projectkoios/
│       └── petrinet/
│           ├── __init__.py
│           ├── modeling/
│           └── runtime/
└── tests/
    ├── modeling/
    └── runtime/
```

Add `projections` and `adapters` only when the modeling/runtime boundary is stable.

## Dependency Rules

Internal dependencies should flow inward/downward:

```text
modeling
  depends on shared/core utilities only

runtime
  depends on modeling

projections
  depends on modeling and runtime as needed

adapters
  depends on modeling, runtime, projections, and external libraries

testing
  may depend on all internal layers
```

Forbidden dependencies:

```text
modeling -> runtime
modeling -> adapters
runtime -> adapters
executor -> YAML / JSON / SQLite / NetworkX / Graphviz
concrete workflows -> imported by petrinet core
agents -> imported by petrinet core
ingestor -> imported by petrinet core
dashboard -> imported by petrinet core
```

Allowed dependencies:

```text
runtime -> modeling
projections -> modeling
projections -> runtime
adapters -> modeling
adapters -> runtime
adapters -> projections
applications -> projectkoios.petrinet
```

## Relationship to `projectkoios.graph`

`projectkoios.graph` remains the generic graph substrate.

`projectkoios.petrinet` may project Petri-net models into graph representations, but Petri nets should not be implemented as subclasses of generic graphs.

Correct relationship:

```text
projectkoios.petrinet
  owns Petri-net semantics

projectkoios.graph
  owns generic graph mechanics

projectkoios.petrinet.projections
  may convert Petri-net models/states/events into graph views
```

Rule:

```text
Petri nets are graph-shaped execution models.
They may be projected into graphs.
They are not merely generic graphs.
```

## Relationship to Concrete Workflows

Concrete Project Koios workflows should live outside the Petri-net package.

Examples:

```text
projectkoios.workflows.three_agent
projectkoios.workflows.ingestion
projectkoios.workflows.messaging
projectkoios.workflows.review
```

Those workflows may be expressed as Petri-net models, but they should not be part of the Petri-net core package.

Rule:

```text
projectkoios.petrinet defines the language and runtime.
projectkoios.workflows defines concrete Koios workflows.
```

## Relationship to Agents, Ingestion, Review, and Dashboard

Application packages depend on `projectkoios.petrinet`.

`projectkoios.petrinet` must not depend on application packages.

Recommended dependency direction:

```text
projectkoios.petrinet
  used by projectkoios.workflows
  used by projectkoios.agents
  used by projectkoios.ingestor
  used by projectkoios.review
  used by projectkoios.dashboard
```

Application package responsibilities:

```text
projectkoios.agents
  agent identities, roles, policies, and behavior over enabled transitions

projectkoios.ingestor
  source ingestion actions and source-derived token schemas

projectkoios.review
  validators, review reports, approval/rework policies

projectkoios.dashboard
  Gantt charts, marking boards, graph views, audit views

projectkoios.workflows
  concrete Petri-net models for Koios processes
```

## Adapter Policy

Adapters should be added incrementally.

First adapters:

```text
JSON
YAML
Mermaid
```

Reason:

```text
JSON supports machine-readable interchange and test fixtures.
YAML supports human-editable workflow definitions.
Mermaid supports quick diagrams in Markdown, Obsidian, and GitHub.
```

Defer until concrete need:

```text
SQLite
NetworkX
Graphviz
PNML
database-backed event stores
```

Optional dependencies should be used for adapters requiring external libraries.

## File Format Policy

A Petri-net model file should describe the modeling layer only.

It may contain:

```text
model identity
places
transitions
arcs
guard declarations
allowed roles
token color/type declarations
metadata
```

It should not contain:

```text
current marking
event log
agent memory
executor state
dashboard layout
runtime lock state
```

Runtime state and events should be serialized separately.

## Event-log Policy

Runtime events are committed facts.

They should be append-only and sufficient for audit and projections.

They should support:

```text
transition identity
actor identity
actor role
consumed token identities
produced token identities
timestamp
previous marking identity
new marking identity
correlation identity
```

The event log is the source for projections such as:

```text
audit timeline
Gantt chart
agent activity timeline
artifact lifecycle timeline
```

## Projection Policy

Gantt charts, graph views, and marking boards are read models.

They must be generated from canonical models, markings, and event logs.

They must not become sources of workflow truth.

Rule:

```text
Petri-net model = allowed structure
marking = current state
event log = execution history
projection = derived view
```

## Invariants

The architecture should preserve these invariants:

```text
A static model does not contain a marking.
A place definition does not own tokens.
A marking does not define allowed transitions.
Only the runtime executor may commit marking changes.
A firing request is a command, not an event.
A transition event is a committed fact, not a request.
Adapters do not define Petri-net semantics.
Projections do not mutate runtime state.
Concrete Koios workflows depend on projectkoios.petrinet.
projectkoios.petrinet does not depend on concrete workflows.
```

## Build Order

Recommended build order:

```text
01. Stabilize the modeling/runtime package boundary.
02. Implement or preserve the existing modeling API.
03. Implement or preserve the existing runtime API.
04. Add validation at the modeling boundary.
05. Add executor-owned state mutation rules at the runtime boundary.
06. Add minimal event logging.
07. Add JSON serialization.
08. Add YAML serialization.
09. Add Mermaid export.
10. Add graph/Gantt projections only after event logs are stable.
```

Do not start with dashboard rendering, database persistence, PNML, or broad graph-library integration.

## Packaging Guidance

Recommended distribution name:

```text
projectkoios-petrinet
```

Recommended import package:

```text
projectkoios.petrinet
```

Use `src/` layout:

```text
src/projectkoios/petrinet/
```

If `projectkoios` is a namespace package across multiple distributions, avoid placing runtime logic at:

```text
src/projectkoios/__init__.py
```

The package should expose stable public interfaces through:

```text
projectkoios.petrinet
projectkoios.petrinet.modeling
projectkoios.petrinet.runtime
```

but avoid exposing every internal module as public API.

## Workplan

### Past Slices

| # | Slice | Evidence |
|---|---|---|
| 1 | Bootstrap-held Petri-net vocabulary/runtime separation | `docs/adr/adr.petrinet.20260705.132740Z.md` |
| 2 | Workflow adapter dependency encapsulation | `docs/implementation/workflow-adapter-dependency-encapsulation.20260705.105604.md` |
| 3 | Workflow adapter topology round trip | `docs/implementation/workflow-adapter-contract-hardening.20260706.045501.md` and `docs/reviews/architecture-conformance.20260706.023601_workflow-adapter-topology-roundtrip.md` |

### Current Slice

| # | Slice | Exit Criteria |
|---|---|---|
| 1 | Preserve first-class subsystem proposal as architecture working draft | This document records the source proposal, authority boundary, package/layer/dependency policies, and follow-on decomposition points. |

### Future Slices

| # | Slice | Trigger |
|---|---|---|
| 1 | Binding ADR for first-class `projectkoios.petrinet` subsystem | User directs acceptance or asks to make this proposal binding. |
| 2 | Package-boundary implementation brief | Accepted ADR/spec authorizes extraction or creation of `projectkoios.petrinet`. |
| 3 | Modeling/runtime split implementation brief | Need to move current bootstrap-held workflow Petri-net code into the proposed package layers. |
| 4 | JSON/YAML/Mermaid adapter briefs | Modeling/runtime boundary is stable and file/adapter policy is accepted. |
| 5 | Event-log policy ADR/spec | Runtime event facts need persistence, audit, replay, or projection authority. |
| 6 | Projection policy/spec | Graph/Gantt/dashboard projections require stable event-log and marking semantics. |
| 7 | Architecture-note schema work | Need to validate subsystem architecture notes with package boundaries, layer responsibilities, dependency rules, adapter/event/projection policies, invariants, and build order. |

## Open Questions

- Should `projectkoios.petrinet` first exist inside `projectkoios-bootstrap`, in the mothership/product repository, or as a separate extracted repository/distribution?
- What exact acceptance path should promote this working note into a binding ADR?
- Which current `src/python/projectkoios/workflow` objects map to future `projectkoios.petrinet.modeling` and `projectkoios.petrinet.runtime`?
- What is the minimal JSON model schema that can be accepted before YAML/Mermaid adapters?
- When do event logs become durable committed records rather than in-process debugging events?
- Does Project Koios need a dedicated `architecture-note` or `subsystem-architecture` schema for this structure?

## Non-goals

This note does not authorize:

- immediate code extraction;
- package or repository creation;
- migration from `projectkoios.workflow` to `projectkoios.petrinet`;
- adding new runtime dependencies;
- implementing JSON/YAML/Mermaid/PNML/Graphviz/NetworkX/SQLite adapters;
- committing event-log persistence semantics;
- product-domain workflow decisions outside the bootstrap-held architecture surface.
