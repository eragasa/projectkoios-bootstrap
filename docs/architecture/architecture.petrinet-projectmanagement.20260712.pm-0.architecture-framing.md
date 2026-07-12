```json
{
  "title": "Filesystem-backed Petri-net Project Management",
  "artifact_type": "architecture-note",
  "status": "working-draft",
  "datetime": "20260712",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "bootstrap-incubated project-management architecture and phase decomposition",
  "canonical_location": "docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md",
  "source_alignment": "docs/plans/petrinet-projectmanagement.20260712.pm-0.project-alignment.md",
  "source_handoff": "HERMES/USER handoff via intercom 20260712",
  "not_an_adr": true,
  "not_implementation_authorization": true
}
```

# Architecture: Filesystem-backed Petri-net Project Management

## Status

Working-draft architecture and phase decomposition.

This document is ATHENA-owned architecture framing. It is not an ADR, schema, implementation brief, implementation authorization, or product-domain cutover decision.

## Purpose

Define the long-term architecture for a filesystem-backed Project Koios project-management system that uses Petri-net workflow state and transition payloads as source/control direction while exposing Gantt and Operator Console views as projections.

The architecture decomposes the system into technology-maturity phases and component dependencies suitable for later Gantt projection and implementation planning.

## Source alignment

Primary alignment input:

- `docs/plans/petrinet-projectmanagement.20260712.pm-0.project-alignment.md`

Current USER direction captured there and in the HERMES handoff:

- build a working filesystem-backed project-management workflow through the Project Koios working process, outside the ADR process;
- ATHENA owns long-term architecture and phase planning;
- Petri-net state and transition payloads are intended source/control direction;
- Gantt is a projection;
- avoid heavy provenance at first; use thin operational traceability;
- pilot work should track itself and later be extractable as a template;
- preserve strict layering and dependency flow: `petrinet -> workflow -> pm`;
- reuse existing workflow/Petri-net code and clean it up as needed while preserving behavior;
- use Petri-net adapters for validation;
- external engines such as SNAKES may be encapsulated as execution/reference-image providers;
- Operator Console fixture is the initial projection-only primary visibility surface;
- interactive user input through Operator Console requires separate design and approval.

## Architecture boundary

This architecture applies first to `projectkoios-bootstrap` as an incubation and self-tracking environment.

It must avoid decisions that prevent later use across:

1. bootstrap harness project management;
2. product/vault project management;
3. cross-repo coordination.

It does not by itself create mothership/product authority, replace existing document-domain authority, or supersede ADRs, implementation reports, reviews, AARs, workspace state files, or current Petri-net workflow fixtures.

## Core model

### Source/control surfaces

The intended source/control direction is:

1. Petri-net definitions describe workflow topology.
2. Marking/state files record current token state.
3. Transition payload files record the work product, gate evidence, and approval required for state movement.
4. Thin operational trace records what was attempted or accepted without becoming a heavyweight provenance system.

The exact file format is implementation-sliced later. Early slices should favor explicit, readable JSON files under an incubation namespace over databases, daemons, or hidden runtime state.

### Projections

Projection surfaces are derived from source/control surfaces and must be labeled as projections:

- Gantt planning and status views;
- Operator Console fixture/read-model views;
- Petri-net diagrams and external-engine reference images;
- reports, dashboards, or critical-path summaries.

A projection must not be treated as state authority unless a later architecture and approval explicitly changes that.

### Task and work-product relationship

Project-management tasks are workflow-facing planning units. A task may correspond to a place, subnet, transition payload, or projected work package depending on the maturity phase.

A work product may have its own lifecycle separate from the task that carries it. Early design must avoid forcing documents, code, tests, reviews, and generated projections into one universal state model.

### Recursion and decomposition

The project-management layer must support recursive decomposition:

```text
project
  -> task
    -> subtask
      -> subtask ...
```

Decomposition is needed for visibility, critical-path reasoning, moving work to subprojects, and extracting templates. The mechanism may evolve from explicit parent/child references to composed Petri-net subnets.

## Layering and dependency flow

Dependency flow is strict:

```text
petrinet -> workflow -> pm -> projections/ui
```

No lower layer may import from or rely on a higher layer.

### `petrinet` layer

Owns:

- Petri-net places, transitions, arcs, markings, tokens, bindings, and firing semantics;
- adapter protocols for external engines;
- validation against Petri-net semantics;
- optional reference-image/reference-execution providers such as SNAKES.

Must not know about:

- project-management tasks or Gantt bars;
- Operator Console;
- ADRs or document-domain policy;
- workflow approval rules;
- cross-repo project identity.

### `workflow` layer

Owns:

- named workflow instances over Petri-net primitives;
- gate semantics and transition payload interpretation;
- work-product references;
- approval requirements and decision status;
- read models such as status and queue surfaces;
- safe mutation protocols when approved.

May depend on `petrinet`.

Must not depend on `pm`, Gantt, Operator Console, or UI concerns.

### `pm` layer

Owns:

- project-management concepts: project, task, subtask, dependency, milestone, critical path, template seed;
- mapping project-management concepts to workflow instances/read models;
- cross-repo/project visibility and extraction boundaries;
- Gantt-ready read models and operational planning views.

May depend on `workflow` read models and protocols.

Must not mutate Petri-net internals directly or bypass workflow transition/gate semantics.

### Projection/UI layer

Owns:

- Operator Console fixture/read-model presentation;
- Gantt projection rendering;
- Petri-net diagram presentation;
- human-readable status and planning surfaces.

For initial phases, this layer is read-only and projection-only. Interactive user input or mutation through the Operator Console requires a separate architecture/design and approval.

## Technology maturity phases

The phases are waterfall-like maturity stages. They are not scrum sprints. A later implementation plan may split each phase into smaller patches, but phase ordering protects architecture dependencies.

| Phase | Maturity | Goal | Source/control maturity | Projection maturity | Exit criteria |
|---|---|---|---|---|---|
| PM-0 | Alignment and architecture baseline | Establish architecture, layering, and phase plan | No new runtime authority | Gantt exists as dependency plan only | Architecture and phase dependency map accepted for implementation planning |
| PM-1 | Layered read-only foundation | Cleanly separate/reuse existing Petri-net and workflow code while preserving behavior | Existing fixtures are loaded through layer-respecting boundaries | Existing status/queue surfaces continue to work | Validation proves no behavior regression and no upward dependencies |
| PM-2 | Filesystem source/control pilot | Introduce a minimal self-tracking project-management pilot over explicit files | Petri-net definition, marking/state, transition payload, and thin trace are explicit files | Deterministic PM read model exists | Pilot tracks itself read-only and can be inspected from CLI |
| PM-3 | Adapter-backed validation | Validate pilot Petri-net/workflow state through adapter seams | Source/control files can be validated against native and external/reference semantics | Reference images or reports may be generated as projections | Adapter validation is deterministic, optional-backend-safe, and isolated in `petrinet` |
| PM-4 | Operator Console projection | Make the pilot visible in the Operator Console as projection-only primary visibility | No UI mutation authority | Console shows workflow/Petri-net/PM/Gantt-ready status from fixtures/read models | User can inspect current state without confusing projection for authority |
| PM-5 | Gantt projection and dependency analysis | Produce Gantt-ready planning view from PM/workflow read models | Source remains Petri-net/workflow/PM files | Gantt shows components, dependencies, planned/current/actual state, and critical path where available | Gantt output is reproducible and labeled as projection |
| PM-6 | Controlled transition execution | Add approved filesystem mutation for transitions | Transition firing writes explicit state/payload/trace files with dry-run and optimistic checks | Projections refresh from written source/control files | Mutation reports exact files written and blocks unsafe concurrent writes |
| PM-7 | Recursive project/template extraction | Generalize self-tracking pilot into reusable project template | Source/control package is portable and parameterized | Projection package can be generated for new projects | Template can instantiate a new project without bootstrap-specific hidden dependencies |
| PM-8 | Cross-repo/product expansion | Apply the template to product/vault and cross-repo coordination | Source/control boundaries across repos are explicit | Cross-repo visibility is projected without central hidden authority | Product/vault adoption is separately approved in the appropriate document domain |

## Component dependency map for Gantt projection

The following component IDs are intended to be machine-readable enough for a later Gantt/read-model fixture while remaining architecture prose here.

| Component ID | Component | Layer | Depends on | Earliest phase | Notes |
|---|---|---|---|---|---|
| PN-CORE | Petri-net core model/runtime boundary | `petrinet` | none | PM-1 | May initially remain in `projectkoios.workflow` if imports preserve the conceptual boundary; extraction can be later. |
| PN-ADAPTER | External engine adapter protocol | `petrinet` | PN-CORE | PM-1 | SNAKES or similar engines are adapter-owned and optional. |
| PN-VALIDATE | Petri-net semantic validation/reference checks | `petrinet` | PN-CORE, PN-ADAPTER | PM-3 | Includes topology/state validation and optional reference-image generation. |
| WF-INSTANCE | Workflow instance/read-model boundary | `workflow` | PN-CORE | PM-1 | Named workflow instances over Petri-net primitives. |
| WF-PAYLOAD | Transition payload model | `workflow` | WF-INSTANCE | PM-2 | Minimum payload covers work-product refs and approval/gate evidence. |
| WF-STATE | Filesystem marking/state and thin trace | `workflow` | WF-INSTANCE, WF-PAYLOAD | PM-2 | Source/control files, not database-backed in early phases. |
| WF-MUTATE | Safe transition execution | `workflow` | WF-STATE, PN-VALIDATE | PM-6 | Dry-run, exact written-file reporting, and optimistic checks required. |
| PM-TASK | Project/task/decomposition model | `pm` | WF-INSTANCE, WF-PAYLOAD | PM-2 | First pilot should track the PM bootstrap effort itself. |
| PM-DEPEND | Dependency/critical-path model | `pm` | PM-TASK | PM-5 | Supports Gantt projection and recursive decomposition. |
| PM-TEMPLATE | Template extraction model | `pm` | PM-TASK, PM-DEPEND, WF-STATE | PM-7 | Must remove bootstrap-specific assumptions. |
| PROJ-CLI | CLI/read-model inspection | projection | WF-INSTANCE, PM-TASK | PM-2 | Read-only before PM-6. |
| PROJ-CONSOLE | Operator Console projection fixture | projection/ui | PROJ-CLI, PM-TASK | PM-4 | Projection-only until separate interaction design. |
| PROJ-GANTT | Gantt projection | projection/ui | PM-DEPEND, PM-TASK | PM-5 | Gantt is never source/control in this architecture. |
| XREPO | Cross-repo visibility | `pm`/projection | PM-TEMPLATE | PM-8 | Requires separate repo/domain acceptance. |

## Phase dependency graph

```text
PM-0 Architecture baseline
  -> PM-1 Layered read-only foundation
    -> PM-2 Filesystem source/control pilot
      -> PM-3 Adapter-backed validation
      -> PM-4 Operator Console projection
        -> PM-5 Gantt projection and dependency analysis
          -> PM-6 Controlled transition execution
            -> PM-7 Recursive project/template extraction
              -> PM-8 Cross-repo/product expansion
```

PM-3 may start after PM-2 source/control files exist. PM-4 may start once a stable read model exists. PM-5 requires at least a minimal task/dependency model from PM-2 and visibility from PM-4 if the user-facing Gantt is in the Operator Console.

## First implementation direction after architecture acceptance

The first implementation brief should target PM-1/PM-2 only.

Recommended bounded slice name:

- `petrinet-pm-self-tracking-foundation-slice-0`

Recommended scope:

- preserve current workflow/Petri-net behavior;
- identify or introduce layer-respecting module boundaries without broad package extraction;
- create one self-tracking filesystem pilot fixture for the project-management architecture effort itself;
- include a minimal transition-payload example with work-product refs and approval/gate refs;
- expose a deterministic read-only CLI/read-model summary;
- prepare, but not necessarily implement, Operator Console and Gantt projection inputs;
- include adapter-ready validation seams, with external engine use optional if it is already cheap and encapsulated.

Recommended non-goals for the first slice:

- no ADR process dependency;
- no database;
- no daemon;
- no broad provenance system;
- no schema authority under `docs/schemas/`;
- no mutation commands;
- no Operator Console interactive input;
- no Gantt engine commitment;
- no cross-repo writes;
- no product/vault authority;
- no broad migration or replacement of existing workflow fixtures.

## Open questions before a VULCAN implementation brief

The following questions should be answered in the implementation brief, not through a new ADR:

1. Incubation namespace: should first PM source/control fixtures live under `dev/project-management/`, `dev/workflow-nets/`, or a two-directory split between source/control and projections?
2. Minimal source/control file set: should PM-2 create Petri-net definition + marking + transition payload + trace files, or start with a single combined pilot bundle and split later?
3. Minimum transition payload fields: are `work_product_refs`, `approval_refs`, `gate`, and `actor` enough for Slice 0, or is a timestamp/status required immediately?
4. CLI/read-model surface: should the first read-only surface extend `uv run projectkoios workflow ...`, add `uv run projectkoios pm ...`, or produce fixture files only?
5. Cleanup allowance: may VULCAN reorganize existing workflow code if tests preserve behavior, or should Slice 0 be additive except for tiny imports/refactors?
6. Operator Console dependency: should the first slice produce a console fixture input, or should console rendering wait for PM-4?

## Acceptance expectations for phase planning

A phase or component is ready for Gantt projection when it has:

- stable component ID;
- phase assignment;
- explicit dependencies;
- owner layer;
- source/control vs projection classification;
- readiness or exit criteria;
- known non-goals.

The table in this document is the initial architecture-owned component map. Implementation may refine it, but lower-layer dependency boundaries and source/control vs projection rules should not be inverted without ATHENA/HERMES/USER review.
