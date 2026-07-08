# User proposal source: projectkoios.petrinet first-class subsystem

## Metadata

- Type: user-proposal-source
- Status: captured
- Captured-By: KOIOS
- Captured-At: 20260706T031715Z
- Repository: projectkoios-bootstrap
- Scope: proposed `projectkoios.petrinet` first-class subsystem architecture
- Intended-Consumer: ATHENA
- Authority: source/provenance only; not accepted architecture authority

## Non-authority statement

This file preserves the user's pasted proposal text as source material for ATHENA architecture work. It does not create architecture authority, implementation authority, extraction authority, workflow policy, or acceptance status.

## Exact user proposal text

```md
# Architecture: `projectkoios.petrinet`

## Status

Proposed

## Purpose

`projectkoios.petrinet` is the first-class Petri-net subsystem for Project Koios.

It provides two related capabilities:

1. a Petri-net modeling language for describing workflows and coordination protocols;
2. a Petri-net runtime for executing those models through markings, bindings, firing requests, and events.

Petri nets are used across Project Koios for:

* agent workflows,
* ingestion pipelines,
* review loops,
* messaging protocols,
* human approval gates,
* provenance-preserving knowledge construction,
* workflow visualization and dashboard projections.

Because Petri nets are central to the architecture, they should not be buried under `projectkoios.graph`, `projectkoios.runtime`, or `projectkoios.ingestor`.

The package boundary should be:

```text
projectkoios.petrinet
```

with possible distribution name:

```text
projectkoios-petrinet
```

## Architectural decision

`projectkoios.petrinet` will be a first-class subsystem with internal separation between:

```text
projectkoios.petrinet.modeling
projectkoios.petrinet.runtime
projectkoios.petrinet.projections
projectkoios.petrinet.adapters
projectkoios.petrinet.testing
```

The central rule is:

```text
modeling defines the language
runtime interprets the language
projections derive read models
adapters connect to external formats and tools
```

## Package-level responsibilities

### `projectkoios.petrinet.modeling`

The modeling layer owns the declarative Petri-net language.

It is responsible for:

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

$$
N = (P, T, A)
$$

where:

* $P$ is the set of places,
* $T$ is the set of transitions,
* $A$ is the set of arcs.

The modeling layer must not own runtime state.

It must not depend on:

```text
markings
runtime token instances
bindings
firing requests
executors
event logs
timestamps
agent memory
dashboard state
```

Rule:

```text
A Petri-net model can exist, validate, serialize, and diagram without being executed.
```

### `projectkoios.petrinet.runtime`

The runtime layer owns execution semantics.

It is responsible for:

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

$$
(N, M)
$$

where:

$$
M : P \to \mathrm{Multiset}(\mathrm{Token})
$$

A firing is:

$$
(N, M) \xrightarrow{t,b} (N, M')
$$

where:

* $t$ is the selected transition,
* $b$ is the selected binding,
* $M'$ is the resulting marking.

The runtime may depend on the modeling layer.

The modeling layer must not depend on the runtime layer.

Rule:

```text
models do not know execution exists
execution interprets models
```

### `projectkoios.petrinet.projections`

The projections layer derives internal read models from canonical Petri-net objects.

It is responsible for transformations such as:

```text
Petri-net model → graph view
Petri-net model → diagram view
Petri-net state → marking board view
transition event log → Gantt intervals
transition event log → audit timeline
```

Projections are internal transformations.

They do not define Petri-net semantics.

They do not mutate runtime state.

Rule:

```text
projection = internal read-model transformation
```

### `projectkoios.petrinet.adapters`

Adapters are boundary code.

They connect Petri-net models, runtime states, events, and projections to external formats, tools, storage systems, and libraries.

Adapter responsibilities include:

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

Adapters must not define Petri-net semantics.

Adapters must not own workflow state.

Adapters must not be imported by the executor.

Rule:

```text
adapter = external format/tool/storage bridge
```

### `projectkoios.petrinet.testing`

The testing layer provides test builders, fixtures, and reference models.

It may depend on all internal layers.

It is responsible for:

```text
minimal valid model builders
invalid model builders
sample markings
sample firing requests
sample event logs
golden serialization fixtures
```

Testing utilities should not become production APIs unless promoted deliberately.

## Recommended package layout

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

Start smaller:

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

## Dependency rules

Internal dependencies should flow inward and downward:

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
modeling → runtime
modeling → adapters
runtime → adapters
executor → YAML / JSON / SQLite / NetworkX / Graphviz
concrete workflows → imported by petrinet core
agents → imported by petrinet core
ingestor → imported by petrinet core
dashboard → imported by petrinet core
```

Allowed dependencies:

```text
runtime → modeling
projections → modeling
projections → runtime
adapters → modeling
adapters → runtime
adapters → projections
applications → projectkoios.petrinet
```

## Relatio[118;1:3unship to `projectkoios.graph`

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

## Relationship to concrete workflows

Concrete Project Koios workflows should live outside the Petri-net package.

Examples:

```text
projectkoios.workflows.three_agent
projectkoios.workflows.ingestion
projectkoios.workflows.messaging
projectkoios.workflows.review
```

Those workflows may be expressed as Petri-net models, but they should not be part of the Petri-net core package.

This keeps `projectkoios.petrinet` reusable.

Rule:

```text
projectkoios.petrinet defines the language and runtime.
projectkoios.workflows defines concrete Koios workflows.
```

## Relationship to agents, ingestion, review, and dashboard

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

## Adapter policy

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

Defer:

```text
SQLite
NetworkX
Graphviz
PNML
database-backed event stores
```

until there is a concrete need.

Optional dependencies should be used for adapters requiring external libraries.

## File format policy

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

## Event-log policy

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

## Projection policy

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

## Build order

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

## Packaging

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

## Decision summary

`projectkoios.petrinet` will be a first-class package and possible subrepo.

It will contain:

```text
projectkoios.petrinet.modeling
  declarative Petri-net language

projectkoios.petrinet.runtime
  executable Petri-net semantics

projectkoios.petrinet.projections
  internal read-model transformations

projectkoios.petrinet.adapters
  external format/tool/storage bridges

projectkoios.petrinet.testing
  builders, fixtures, and reference models
```

The modeling layer defines the language.

The runtime layer interprets the language.

Projections derive views.

Adapters connect to external formats and tools.

The executor is the only component that may commit marking changes.

Adapters are boundary code and must not define Petri-net semantics, own workflow state, or be imported by the executor.
```
