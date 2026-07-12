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
- strategy starts with Gantt planning first, then a simplified Petri-net skeleton matching Gantt components, then progressive gates/work products/validation/mutation;
- Petri-net state and transition payloads are intended source/control direction once those maturity phases exist;
- Gantt is a projection, including the initial planning Gantt;
- avoid heavy provenance at first; use thin operational traceability;
- pilot work should track itself and later be extractable as a template;
- preserve strict layering and dependency flow: `petrinet -> workflow -> project_management`;
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

## Planning and implementation ownership

Project-management work uses role separation:

- HERMES owns user alignment, routing, acceptance coordination, and deciding when a phase or brief is approved for implementation.
- ATHENA owns long-term architecture, phase architecture, phase gates, and at least a two-phase lookahead in architecture/phase planning.
- VULCAN owns implementation decomposition within an accepted phase, implementation dependency planning, file/task-level plans, tests, and validation evidence.

ATHENA should keep the architecture mature enough that the active implementation phase and the next two phases have clear intent, boundaries, dependencies, non-goals, and acceptance expectations. ATHENA may keep later phases coarser, but must preserve enough architecture shape to prevent local implementation choices from blocking PM-8/PM-9 direction.

VULCAN may take an accepted implementation phase and break it into smaller implementation tasks or patches. VULCAN should produce implementation plans phased with dependencies. VULCAN may maintain a coarse requirements/dependency outline through PM-8, then add detail as implementation progresses phase-by-phase.

This process framing does not authorize implementation by itself. A phase still requires HERMES/USER routing/acceptance of a bounded brief or equivalent implementation authorization.

## Core model

### Source/control surfaces

The intended mature source/control direction is:

1. Petri-net definitions describe workflow topology.
2. Marking/state files record current token state.
3. Transition payload files record the work product, gate evidence, and approval required for state movement.
4. Thin operational trace records what was attempted or accepted without becoming a heavyweight provenance system.

The maturity path does not start by designing all source/control structures. It starts with a non-authoritative Gantt planning projection, backs into a simplified Petri-net/workflow skeleton, then adds filesystem state, visibility, validation, gates/work products, and mutation in later phases.

The exact file format is implementation-sliced later. Early source/control slices should favor explicit, readable JSON files under an incubation namespace over databases, daemons, or hidden runtime state.

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
projectkoios/petrinet -> projectkoios/workflow -> projectkoios/project_management -> projections/ui
```

`pm` may appear as a CLI abbreviation, but the Python package name is `projectkoios/project_management`.

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

Must not depend on `project_management`, Gantt, Operator Console, or UI concerns.

### `project_management` layer

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

The phases are waterfall-like maturity stages. They are not scrum sprints. ATHENA owns this phase architecture and should keep at least two phases of lookahead clear. VULCAN may split an accepted phase into smaller implementation tasks and dependency-ordered patches, but phase ordering protects architecture dependencies.

The intended strategy is Gantt-informed but engine-first for implementation: use Gantt as a planning/design projection, then make the first implementation step a minimal working engine that can load a simplified Petri-net/workflow skeleton and produce deterministic inspectable output. Each backend maturity step should have a corresponding Console UI projection/read model that reflects the capability available at that phase. Later phases progressively add self-tracking filesystem state, visibility surfaces, validation/adapters, gates/work products, mutation, operational Gantt, templates, and schema/database readiness.

| Phase | Maturity | Goal | Source/control maturity | Projection maturity | Exit criteria |
|---|---|---|---|---|---|
| PM-0 | Architecture and planning Gantt | Establish architecture, layering, phase/component dependencies, and initial non-authoritative Gantt planning projection | No new runtime authority | Early Gantt-style planning projection is generated from the architecture component map | Architecture, phase dependency map, and planning Gantt accepted as planning input |
| PM-1 | Minimal working engine and skeleton | Implement a minimal executable/inspectable engine that loads a simplified Petri-net/workflow skeleton matching Gantt components while preserving existing behavior | YAGNI engine core and skeleton exist; engine can load and inspect the skeleton and may perform in-memory step/enablement checks; no heavy gates, payloads, persistence mutation, database, or full validation regime | Console projection/read model shows what the engine can load/inspect/step; planning Gantt may be revised from engine/skeleton findings | Engine loads the skeleton, emits deterministic inspectable output, Console projection reflects engine capability, skeleton matches planning components, and current workflow behavior/package boundaries are preserved |
| PM-2 | Self-tracking read-only pilot | Use the simplified net to track this PM project itself with filesystem state | Minimal project/task identity, net reference, and marking/current state exist as readable filesystem files | Console projection/read model shows the read-only pilot state | Self-project-management pilot tracks itself without transition mutation or full gate/work-product payloads, and Console projection reflects that state |
| PM-3 | Projection visibility hardening | Harden CLI and Console projection patterns for current pilot state | Source remains PM-2 filesystem state | `koios pm status` and Operator Console projection fixture/read-model show current state and non-source labels | User can inspect current state without confusing projections for authority; projection update rules are explicit |
| PM-4 | Petri-net validation and adapters | Validate net/state with internal logic and optional external engines such as SNAKES | Skeleton/state can be validated through internal and adapter-owned checks | Console projection shows validation status; adapter reports/images are evidence/projections | Validation is deterministic for core logic and fail-soft for optional external engines, and Console projection reflects validation capability |
| PM-5 | Gates, work products, approvals, and thin trace | Add transition payloads, required work products, approvals, and thin operational trace | Gate/work-product/approval payloads and thin trace become explicit source/control files | Console projection can show gate/work-product/approval/trace status | Gate evidence is inspectable without broad provenance ceremony or mutation commands, and Console projection reflects gate/work-product capability |
| PM-6 | Controlled transition execution | Add approved filesystem mutation for transitions | Transition firing writes explicit state/payload/trace files with dry-run and optimistic checks | Console projection shows dry-run/result/exact-file-write reports and refreshed state | Mutation reports exact files written, blocks unsafe concurrent writes, and Console projection reflects mutation outcomes without becoming authority |
| PM-7 | Operational Gantt from live/current state | Generate Gantt from actual PM/workflow source-control state | Source remains Petri-net/workflow/project-management files | Console projection includes operational Gantt showing components, dependencies, planned/current/actual state, and critical path where available | Operational Gantt output is reproducible, source-linked, labeled as projection, and visible in Console projection |
| PM-8 | Template and cross-project expansion | Extract reusable template, then expand to product/vault/cross-repo coordination | Source/control package is portable and cross-domain boundaries are explicit | Console projection can show template/cross-project visibility without central hidden authority | Template passes portability checks, Console projection reflects extraction/cross-project boundaries, and product/vault adoption is separately approved |
| PM-9 | Terminal schema-backed JSON/database readiness | Make the mature PM control surface schema-implemented and ready for JSON control through a possible database implementation | JSON control records have schema-backed contracts and can be mapped to a database implementation without changing semantics | Console projection can evaluate schema/database-readiness status; database-backed views/control surfaces may be evaluated as implementation options | System is ready for separately approved schema-backed JSON/database control; Console projection reflects readiness only; no database cutover occurs without separate acceptance |

## Backend/frontend phase decomposition

Each maturity phase may be decomposed into backend and frontend/projection subphases when useful:

```text
PM-nB  backend/source-control capability
PM-nF  Console UI projection/read model for that capability
```

This decomposition is optional naming guidance for briefs, not a requirement to split every patch. The architectural requirement is that each backend capability has a matching Console projection appropriate to what that backend can actually do.

Console projections remain read-model/projection surfaces. They must not become source/control authority, direct mutation surfaces, or workflow truth unless a later phase explicitly grants interactive input/mutation authority through separate design and acceptance.

The first implementation direction therefore includes both:

1. a minimal working engine backend; and
2. a Console projection/read model that reflects that engine's load/inspect/optional non-persistent-step capability.

## Gantt-informed working-engine-first approach

Use Gantt in two different maturity roles:

1. Early planning Gantt projection in PM-0/PM-1.
2. Operational/live Gantt projection in PM-7.

The early planning Gantt comes first as design input. It is allowed before PM source/control files exist and should be derived from this architecture's phase table and component dependency map. Its purpose is to reveal sequencing, likely critical path, missing dependencies, and required work products before VULCAN implementation planning.

The first implementation step, however, must be a working engine implementation, not only static Gantt/skeleton artifacts. PM-1 backs from the planning projection into a simplified Petri-net/workflow skeleton and a minimal executable/inspectable engine that can load that skeleton and produce deterministic output. The engine should be YAGNI: enough to load, inspect, report enabled/basic state, and optionally perform non-persistent in-memory step checks over places/transitions matching the planning components, but no full gate model, work-product payload model, persistence mutation, database dependency, or broad validation regime up front.

The early planning Gantt is not source/control authority. It must not become the state machine, workflow truth, implementation authorization, or replacement for Petri-net/workflow/project-management files. Any dependency or work-product gaps found through the planning Gantt must be incorporated back into the architecture, simplified skeleton, or later source/control design before they become implementation requirements.

PM-7 is different: PM-7 is the later operational Gantt projection generated from PM/workflow source/control read models after project-management source/control surfaces exist and are visible. PM-7 may show planned/current/actual state and critical path from live or current filesystem state, but it remains a projection.

## Component dependency map for Gantt projection

The following component IDs are intended to be machine-readable enough for early planning Gantt projection and later operational Gantt/read-model fixtures while remaining architecture prose here.

| Component ID | Component | Layer | Depends on | Earliest phase | Notes |
|---|---|---|---|---|---|
| PN-CORE | Petri-net core model/runtime boundary | `petrinet` | none | PM-1 | Target package boundary for Petri-net primitives; behavior preservation required. |
| PN-ENGINE | Minimal working Petri-net engine | `petrinet`/`workflow` | PROJ-GANTT-PLAN, PN-CORE | PM-1 | Executable/inspectable engine that loads the skeleton and emits deterministic output; may do in-memory enablement/step checks without persistence mutation. |
| PN-SKELETON | Simplified Petri-net skeleton | `petrinet`/`workflow` | PROJ-GANTT-PLAN, PN-CORE, PN-ENGINE | PM-1 | Minimal places/transitions/workflow identity matching the planning Gantt components; no heavy gates/payloads. |
| PN-ADAPTER | External engine adapter protocol | `petrinet` | PN-CORE, PN-SKELETON | PM-4 | SNAKES or similar engines are adapter-owned and optional. |
| PN-VALIDATE | Petri-net semantic validation/reference checks | `petrinet` | PN-CORE, PN-SKELETON, PN-ADAPTER | PM-4 | Includes topology/state validation and optional reference-image generation. |
| WF-INSTANCE | Workflow instance/read-model boundary | `workflow` | PN-SKELETON | PM-1 | Named workflow instances over Petri-net primitives. |
| WF-STATE | Filesystem marking/current state | `workflow` | WF-INSTANCE | PM-2 | Source/control state files, not database-backed in early phases. |
| WF-PAYLOAD | Transition payload, work-product, approval, and thin-trace model | `workflow` | WF-INSTANCE, WF-STATE | PM-5 | Added after skeleton/self-tracking flow is visible. |
| WF-MUTATE | Safe transition execution | `workflow` | WF-STATE, WF-PAYLOAD, PN-VALIDATE | PM-6 | Dry-run, exact written-file reporting, and optimistic checks required. |
| PM-TASK | Project/task/decomposition model | `project_management` | WF-INSTANCE, WF-STATE | PM-2 | First pilot should track the PM bootstrap effort itself. |
| PM-DEPEND | Dependency/critical-path model | `project_management` | PM-TASK | PM-7 | Supports operational Gantt projection and recursive decomposition. |
| PM-TEMPLATE | Template extraction model | `project_management` | PM-TASK, PM-DEPEND, WF-STATE | PM-8 | Must remove bootstrap-specific assumptions. |
| PROJ-CLI | CLI/read-model inspection | projection | WF-INSTANCE, PM-TASK | PM-3 | Read-only before PM-6. |
| PROJ-CONSOLE | Operator Console projection fixture/read model | projection/ui | phase backend read model | PM-1 | Every phase should expose a Console projection matching current backend capability; projection-only until separate interaction design. |
| PROJ-GANTT-PLAN | Early Gantt planning projection | projection/ui | PM-0 phase table, component dependency map | PM-0 | Planning/design projection only; used to reveal sequencing, critical path, missing dependencies, and required work products before skeleton/source-control design is complete. |
| PROJ-GANTT-OPS | Operational Gantt projection | projection/ui | PM-DEPEND, PM-TASK, WF-STATE | PM-7 | Generated from PM/workflow source-control read models; never source/control in this architecture. |
| XREPO | Cross-repo visibility | `project_management`/projection | PM-TEMPLATE | PM-8 | Requires separate repo/domain acceptance. |
| PM-SCHEMA | Schema-backed JSON control records | `project_management`/storage boundary | WF-MUTATE, PM-TEMPLATE, XREPO | PM-9 | Terminal readiness for schema-implemented JSON control; not early schema authority and not database cutover. |
| PM-DB-READY | Database implementation readiness | storage boundary | PM-SCHEMA | PM-9 | Proves JSON control records can map to a database implementation without changing source/control semantics; actual database control requires separate acceptance. |

## Phase dependency graph

```text
PM-0 Architecture + planning Gantt
  -> PM-1 Minimal working engine + simplified skeleton + Console projection
    -> PM-2 Self-tracking read-only filesystem pilot + Console projection update
      -> PM-3 CLI and Console projection hardening
        -> PM-4 Petri-net validation and optional adapters
          -> PM-5 Gates, work products, approvals, and thin trace
            -> PM-6 Controlled transition execution
              -> PM-7 Operational Gantt from live/current source-control state
                -> PM-8 Template and cross-project expansion
                  -> PM-9 Terminal schema-backed JSON/database readiness
```

PM-1 backs into a YAGNI working Petri-net/workflow engine and skeleton from the PM-0 Gantt planning projection and exposes a Console projection/read model for that engine capability. PM-2 uses that engine/skeleton for self-project-management state and updates the Console projection to show that state. PM-3 hardens CLI and Console projection update rules before heavy validation or gate semantics. PM-4 validates the skeleton/state with internal and optional adapter-backed checks and projects validation status. PM-5 adds gates, work products, approvals, and thin trace only after the engine/skeleton/self-tracking flow is visible.

PM-0/PM-1 produce an early planning Gantt from architecture-owned phases/components. That early planning Gantt is a design projection used to improve the PM-1 working engine/skeleton and PM-2 source/control design; it is not the PM-7 operational Gantt.

PM-9 is the terminal maturity target for this architecture: schema-backed JSON control records are implemented or explicitly validation-ready under a PM-9 brief, and ready to support a database implementation/control surface. PM-9 does not retroactively make PM-0 through PM-3 schema/database-driven, and it does not authorize database cutover. PM-9 also does not automatically grant `docs/schemas/` authority, schema authority promotion, database control authority, or product/vault/cross-repo authority; those require separate acceptance.

## Implementation outlook and phase risks

VULCAN implementation-outlook comments are incorporated as constraints for later briefs. They do not replace the architecture, but they define likely implementation hazards that ATHENA briefs should explicitly avoid.

Phase risk controls:

- PM-0 architecture and indexes must remain navigation/planning surfaces, not runtime state or implementation authorization.
- PM-1 must produce a working engine implementation, but still avoid broad behavioral refactor; package-boundary establishment, minimal engine core, and simplified skeleton creation are allowed only with behavior preservation and without full gate/payload/persistence mutation semantics.
- PM-2 must avoid premature schema or file-format lock-in; first self-tracking pilot model should be tiny, filesystem-backed, and read-only.
- Each phase's Console projection must match current backend capability and be visibly labeled as projection/non-source/non-control.
- PM-3 CLI and Operator Console projection hardening must keep update rules explicit.
- PM-4 external adapters should be integrated while they are working and useful, but must remain optional, lazy, adapter-owned, and fail-soft when unavailable or blocking.
- PM-5 must avoid broad provenance ceremony while adding only the gates, work products, approvals, and thin trace required by the visible self-tracking flow.
- PM-0/PM-1 early Gantt planning projection must not be mistaken for source/control authority or live operational status.
- PM-0/PM-1 Gantt component IDs are planning components, not runtime places by default; later mapping may be to places, transitions, subnets, or project/task records and must remain explicit and revisable.
- PM-7 operational Gantt must avoid full duration, calendar, resource, and critical-path semantics until the dependency model is proven.
- PM-6 mutation is the highest-risk phase and must address stale reads, race conditions, partial writes, event/state divergence, dry-run behavior, exact file-write reporting, and failure recovery before it is authorized.
- PM-8 template extraction must include portability checks that prevent bootstrap path assumptions from leaking into reusable templates.
- PM-8 product/vault/cross-repo expansion requires separate domain acceptance.
- PM-9 schema-backed JSON/database readiness is terminal late maturity only; it must not introduce early database dependency, silent `docs/schemas/` authority, database control authority, or database cutover without separate acceptance.
- PM-9 database readiness means semantic mappability from filesystem JSON to a database implementation; it is not an operational database dependency by itself.

Likely implementation topology:

- Petri-net code should live under `src/python/projectkoios/petrinet/`.
- Workflow code should live under `src/python/projectkoios/workflow/`.
- Project-management code should live under `src/python/projectkoios/project_management/`.
- Import direction is upward by layer: `projectkoios.workflow` may import `projectkoios.petrinet`; `projectkoios.project_management` may import `projectkoios.workflow`; `projectkoios.petrinet` must not import upward.
- `src/python/projectkoios/workflow/petrinet.py`, `runtime.py`, `validation.py`, and `adapters.py` currently represent the conceptual `petrinet` layer; PM-1 should establish the target package boundary without changing behavior.
- `src/python/projectkoios/workflow/workflownet.py` and `fixtures.py` are candidates for workflow/read-model boundaries.
- The `project_management` layer should start additive under `src/python/projectkoios/project_management/` and should import workflow read models/protocols only.
- The first CLI surface should use the user-facing namespace `koios pm *`; the initial command should be narrow and read-only, such as `koios pm status`, or limited to deterministic file/read-model generation. Extending `workflow` commands requires explicit rationale.

Layer enforcement should become executable once a PM package exists:

- `projectkoios.petrinet` must not import workflow, project-management, projection, or UI modules.
- `projectkoios.workflow` may import `projectkoios.petrinet`, but must not import project-management, projection, or UI modules.
- `projectkoios.project_management` may import `projectkoios.workflow`, but must not import projection or UI modules.
- Optional external backends must be imported lazily inside adapters.
- Shared communication should use public protocols and DataObject-style records rather than higher-layer concrete classes.

Testing strategy by phase:

- PM-1: behavior preservation for existing workflow CLI/status/queue/reconcile surfaces and Petri-net tests, import-boundary checks, engine-load/inspect deterministic output checks, optional in-memory enablement/step checks, and skeleton-to-Gantt component matching.
- PM-2: self-tracking pilot checks for unique IDs, reference resolution, current-state references to skeleton elements, source/projection markers, and no accidental decomposition cycles.
- PM-1: Console projection/read model reflects engine load/inspect/optional non-persistent step capability without implying control authority.
- PM-2: Console projection/read model reflects self-tracking filesystem state.
- PM-3: projection determinism, update rules, and visible non-source/non-control labels for CLI and Operator Console fixtures.
- PM-4: native validation plus adapter parity tests where the adapter is available; unavailable or broken external backends skip/fail-soft without blocking core validation.
- PM-5: payload/work-product/approval/trace checks grounded in the self-tracking use case.
- PM-6: dry-run, revision/hash mismatch, exact files-written report, event/state consistency, and failure recovery.
- PM-7: operational Gantt projection determinism, source-linking, and visible non-source labels.
- PM-8: portability and no hidden bootstrap-path assumptions.
- PM-9: schema-backed JSON validation or validation-only schema readiness under explicit acceptance, JSON-to-database mapping checks, and proof that database implementation readiness does not change source/control semantics.

## First implementation direction after architecture acceptance

The first implementation brief should target PM-0/PM-1 and must produce a working engine implementation plus a Console projection/read model for that engine. The planning Gantt remains useful design input, but the first implementation result must be an executable/inspectable minimal engine that can load the simplified Petri-net/workflow skeleton, produce deterministic output, and expose a projection/read model that the Console can render or consume.

Recommended bounded slice name:

- `petrinet-pm-working-engine-slice-0`

Recommended scope:

- preserve current workflow/Petri-net behavior;
- create or update an early non-authoritative Gantt planning projection from the PM-0 phase/component map as design input;
- use the planning projection to expose sequencing, missing dependencies, and required work products;
- use Markdown/Mermaid/table output for the first planning Gantt; do not add a Gantt engine dependency;
- establish or prepare concrete package boundaries for `projectkoios.petrinet`, `projectkoios.workflow`, and `projectkoios.project_management` without behavior redesign;
- implement a minimal working engine core that can load a simplified Petri-net/workflow skeleton and emit deterministic inspectable output;
- include enough engine behavior to prove execution semantics are real, such as enabled-transition/state inspection and optionally a non-persistent in-memory step check, without writing state changes;
- produce a Console projection/read model that reflects exactly what the minimal engine can do: loaded skeleton, inspectable state, enabled/basic state report, optional non-persistent step result if scoped, projection/non-source labels, and input refs;
- if package-boundary work is non-trivial, split implementation into working-engine/skeleton output first and mechanical package-boundary/wrapper work second;
- create a simplified Petri-net/workflow skeleton matching the planning Gantt components;
- keep the engine/skeleton YAGNI: component places/transitions, workflow identity, load/inspect/deterministic output, and optional in-memory stepping only; no heavy gates/work-product payloads, no persistence mutation, no database, no broad validation regime, and no inherited duration/calendar/resource/critical-path semantics;
- add behavior-preservation, import-boundary, engine-load/inspect, deterministic-output, Console projection/read-model, and skeleton-to-Gantt matching checks;
- require every required planning component ID to have a skeleton counterpart or explicit deferred rationale, and no extra skeleton IDs without a source component/rationale;
- classify first-slice planning outputs, skeleton files, engine outputs, and Console projection files as planning projection, source/control skeleton, runtime/inspection output, Console projection, or test/evidence;
- leave self-tracking filesystem state, CLI/Console visibility beyond the minimal engine capability projection, adapter validation, gates/work products, operational/live Gantt, persistent mutation, interactive Console input, and database work to later phases unless separately scoped as optional non-blocking outputs.

The PM-0/PM-1 implementation brief must specify before coding. VULCAN may then decompose the accepted phase into smaller implementation tasks and dependency-ordered patches, but the decomposition must preserve the phase boundary and first-step requirement for a working engine plus Console projection/read model.

The brief must specify:

- exact minimal engine interface and output: what it loads, what it inspects, whether it performs non-persistent in-memory stepping, and what deterministic output proves it is working;
- exact Console projection/read-model file path and fields for the engine capability projection, including non-source/non-control labels and input refs;
- exact PM-1 skeleton file output path(s), either under `dev/project-management/self/source/` or an explicitly named PM-1 planning/skeleton namespace;
- exact planning Gantt output format, with Markdown/Mermaid/table preferred and no Gantt engine dependency;
- projection headers or fields including `projection`, `planning-only`, `not source/control`, and input architecture/component-map references;
- skeleton-to-Gantt matching test rules: every required component ID has a skeleton counterpart or deferred rationale, and no extra skeleton IDs exist without source component/rationale;
- engine behavior tests: load skeleton, inspect state, produce deterministic output, and if scoped, perform non-persistent in-memory step/enablement checks;
- Console projection tests: projection exists, is deterministic, references engine/skeleton inputs, and cannot be mistaken for source/control or mutation authority;
- behavior-preservation gates for existing workflow CLI/status/queue/reconcile smoke checks plus current workflow/Petri-net tests;
- compatibility import policy if Petri-net modules move, including re-exports or wrappers for current `projectkoios.workflow` import paths;
- command/alias decision for whether `koios` is added now or whether existing `projectkoios` CLI mechanics are used until a later alias slice.

Recommended non-goals for the first slice:

- no ADR process dependency;
- no database;
- no daemon;
- no broad provenance system;
- no schema authority under `docs/schemas/`;
- no persistent mutation commands; non-persistent in-memory stepping is allowed only as part of the minimal working engine proof;
- no external-engine adapter requirement in the first slice;
- no interactive Operator Console input, live backend adapter, or mutation UI; the required Console surface is projection/read-model only for the minimal engine capability;
- no Operator Console interactive input;
- no operational/live Gantt engine commitment;
- no duration/calendar/resource/critical-path semantics in the skeleton; planning projection hints remain non-authoritative;
- no cross-repo writes;
- no product/vault authority;
- no broad migration, replacement, or behavior redesign beyond the package-boundary establishment explicitly required for `projectkoios.petrinet`, `projectkoios.workflow`, and `projectkoios.project_management`.

## Architecture answers for later PM phases

USER/HERMES answered the package, CLI, Operator Console, validator-example, payload-YAGNI, and adapter direction before an implementation brief. ATHENA supplies the remaining architecture recommendations here so later briefs can be concrete while preserving the corrected planning-Gantt plus working-engine-first maturity order.

### Package separation

Use concrete package boundaries:

```text
src/python/projectkoios/petrinet/
src/python/projectkoios/workflow/
src/python/projectkoios/project_management/
```

Allowed dependency flow:

```text
projectkoios.petrinet -> projectkoios.workflow -> projectkoios.project_management
```

The CLI abbreviation may be `pm`, but the Python package should be `project_management`.

### Recommended PM-2 incubation namespace

Use a PM-owned incubation namespace for the self-tracking pilot:

```text
dev/project-management/self/
```

Recommended substructure:

```text
dev/project-management/self/
  source/        # source/control fixtures
  projections/   # generated or copied projection fixtures/read models
  evidence/      # validation output or implementation evidence, if needed
```

The `source/`, `projections/`, and `evidence/` labels should also be visible in file contents or headers where practical, not only directory names.

Do not put first PM source/control files directly under `docs/plans/` or workspace-local state. Those may be referenced as work products, but they should not become the PM source/control namespace.

### Recommended minimal source/control file set

For PM-1, the minimal source/control file set is the simplified Petri-net/workflow skeleton matching the planning Gantt components. It should not include full transition payloads, work products, approvals, or thin trace yet.

For PM-2, prefer a small split file set over one combined bundle so source/control classification is visible without locking a broad schema:

```text
dev/project-management/self/source/
  project.json                 # project-management identity, phase/component IDs, decomposition roots
  workflow.json                # workflow instance or skeleton reference over Petri-net places/transitions
  marking.json                 # current Petri-net token/place state for the pilot
```

PM-5 later adds:

```text
dev/project-management/self/source/
  transition-payloads.json     # gate/work-product/approval payloads once the visible flow needs them
  trace.jsonl                  # thin operational trace; append-like evidence, not heavyweight provenance
```

Do not ask PM-1 or PM-2 to add placeholder empty `transition-payloads.json` or `trace.jsonl` files unless a brief explicitly needs deferred stubs; their normal maturity point is PM-5.

This is an architecture recommendation, not schema authority. PM-2 may adjust filenames if VULCAN finds a smaller equivalent, but it must preserve distinct source/control concepts: project/task identity, workflow skeleton/reference, and current marking/state. PM-5 then adds transition payloads and thin trace after the skeleton/self-tracking flow is visible.

### Recommended classification

Source/control in PM-1/PM-2:

- Simplified Petri-net/workflow skeleton files or references.
- Marking/current-state files.
- PM project/task/decomposition files.

Source/control added in PM-5:

- Transition payload files containing required work product and approval/gate references.
- Thin operational trace files.

Projection/read-model:

- Early Gantt planning projection derived from PM-0/PM-1 architecture components.
- Operator Console fixture/read model for engine capability, starting PM-1.
- Operator Console fixture/read model for self-tracking state, updated in PM-2.
- `koios pm status` output/read model and hardened projection update rules, starting PM-3.
- Later operational Gantt projection generated from PM source/control read models, deferred to PM-7.
- Petri-net diagrams, external-engine reference images, reports, and dashboards.

Test/evidence in PM-2:

- validator output;
- adapter parity output;
- implementation reports and review artifacts;
- generated comparison reports.

Projection files must visibly say they are projections, not source/control. Source/control files must not be generated from projections. If an early Gantt planning projection reveals missing sequencing or work-product requirements, those discoveries must be back-propagated into architecture or source/control design rather than treated as Gantt authority.

### Transition payload YAGNI baseline

Do not require transition payloads in PM-1/PM-2. Add them in PM-5 once the simplified skeleton and self-tracking flow are visible.

When PM-5 adds payloads, start with only the fields needed by the self-project-management use case. The conceptual minimum is:

- transition/gate identifier;
- required work-product reference(s);
- approval/gate evidence reference(s), if available;
- optional actor/process label when needed for inspectability.

Do not add a broad payload schema, lifecycle taxonomy, timestamp model, role model, or provenance model until a concrete gate needs it. Thin trace may carry operational timing if necessary, but timing should not become a global schema requirement in PM-5.

### CLI/read-model surface

The user-facing command namespace is:

```bash
koios pm *
```

The first PM-3 command should be read-only, preferably:

```bash
koios pm status
```

If the repository currently exposes `projectkoios` rather than `koios`, the implementation brief should explicitly state whether VULCAN is adding a `koios` command alias or implementing the underlying command behind existing CLI mechanics first. Do not overload `workflow` commands for PM unless the brief explains why.

### Concrete cleanup/refactor framing

The question is not whether VULCAN may clean up code in general. The concrete choice for PM-1 is:

- move or wrap the current Petri-net implementation into `projectkoios.petrinet` so the target package boundary exists;
- keep current workflow behavior and command output equivalent;
- avoid redesigning runtime semantics, payload semantics, queue semantics, or adapters in the same step;
- add compatibility imports or thin wrappers if needed to preserve existing callers during the transition;
- prove behavior preservation with existing tests and focused CLI/status/queue checks.

In short: allow package-boundary establishment and mechanical cleanup required for `projectkoios.petrinet`, `projectkoios.workflow`, and `projectkoios.project_management`; do not allow opportunistic behavior redesign under the name of cleanup.

### Validator criteria

Validation matures by phase and should be grounded in the concrete self-project-management pilot.

PM-1 skeleton checks:

- planning Gantt component IDs map to simplified Petri-net/workflow skeleton elements;
- skeleton IDs are unique and resolvable;
- package/import boundaries preserve `petrinet -> workflow -> project_management`.

PM-2 self-tracking checks:

- current marking/state references defined skeleton places/workflow elements;
- project/task decomposition has no accidental cycle unless explicitly modeled as Petri-net behavior;
- source/control files and projection files are labeled/classified.

PM-1 Console projection checks:

- engine capability projection identifies engine/skeleton inputs;
- projection is deterministic and labels itself as projection/non-source/non-control;
- projection reflects only load/inspect/optional non-persistent-step capability.

PM-2 Console projection checks:

- self-tracking state projection identifies source/control inputs;
- projection does not imply mutation or authority.

PM-3 projection-hardening checks:

- projection fixtures identify their source/control inputs;
- CLI and Operator Console read models visibly label projection/non-source status;
- projection update rules are explicit.

PM-5 gate/payload checks, once payloads exist:

- transition payloads reference existing gates/transitions and work products;
- thin trace parses and references known events or gates.

### Operator Console fixture/read-model

An Operator Console projection fixture/read-model begins in PM-1 with the minimal working engine and should be updated at each later phase to reflect only the backend capability available in that phase. It remains projection-only unless a later phase explicitly accepts interactive input or mutation authority.

Every phase projection must visibly state:

- generated/static snapshot or read-model status;
- source/control or engine input refs;
- phase/backend capability reflected;
- not source/control;
- not an interactive mutation surface unless separately accepted.

Actual Operator Console UI rendering may be decomposed from backend implementation as a frontend subphase, but the first implementation direction still requires a Console-consumable projection/read model for the working engine.

### Adapter/SNAKES scope

Use SNAKES or other external engines while they are useful and working, but preserve encapsulation:

- adapter code belongs in `projectkoios.petrinet`;
- optional backend imports are lazy;
- unavailable/broken adapters fail soft or skip adapter-specific tests;
- adapter images/reports are projections/evidence, not source/control;
- adapter breakage must not block the core PM-0 through PM-3 planning, skeleton, self-tracking, or visibility foundation unless the brief explicitly scopes adapter parity as a gate.

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
