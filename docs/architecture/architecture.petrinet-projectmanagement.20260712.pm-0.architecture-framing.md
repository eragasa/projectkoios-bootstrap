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

The phases are waterfall-like maturity stages. They are not scrum sprints. A later implementation plan may split each phase into smaller patches, but phase ordering protects architecture dependencies.

| Phase | Maturity | Goal | Source/control maturity | Projection maturity | Exit criteria |
|---|---|---|---|---|---|
| PM-0 | Alignment and architecture baseline | Establish architecture, layering, and phase plan | No new runtime authority | Gantt exists as dependency plan only | Architecture and phase dependency map accepted for implementation planning |
| PM-1 | Layered read-only foundation | Cleanly separate/reuse existing Petri-net and workflow code while preserving behavior | Existing fixtures are loaded through layer-respecting boundaries | Existing status/queue surfaces continue to work | Validation proves no behavior regression and no upward dependencies |
| PM-2 | Filesystem source/control pilot | Introduce a minimal self-tracking project-management pilot over explicit files | Petri-net definition, marking/state, transition payload, and thin trace are explicit files | Deterministic `koios pm status` read model and Operator Console projection fixture exist | Pilot tracks itself read-only and can be inspected from CLI and projection fixture |
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
| PM-TASK | Project/task/decomposition model | `project_management` | WF-INSTANCE, WF-PAYLOAD | PM-2 | First pilot should track the PM bootstrap effort itself. |
| PM-DEPEND | Dependency/critical-path model | `project_management` | PM-TASK | PM-5 | Supports Gantt projection and recursive decomposition. |
| PM-TEMPLATE | Template extraction model | `project_management` | PM-TASK, PM-DEPEND, WF-STATE | PM-7 | Must remove bootstrap-specific assumptions. |
| PROJ-CLI | CLI/read-model inspection | projection | WF-INSTANCE, PM-TASK | PM-2 | Read-only before PM-6. |
| PROJ-CONSOLE | Operator Console projection fixture | projection/ui | PROJ-CLI, PM-TASK | PM-4 | Projection-only until separate interaction design. |
| PROJ-GANTT | Gantt projection | projection/ui | PM-DEPEND, PM-TASK | PM-5 | Gantt is never source/control in this architecture. |
| XREPO | Cross-repo visibility | `project_management`/projection | PM-TEMPLATE | PM-8 | Requires separate repo/domain acceptance. |

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

## Implementation outlook and phase risks

VULCAN implementation-outlook comments are incorporated as constraints for later briefs. They do not replace the architecture, but they define likely implementation hazards that ATHENA briefs should explicitly avoid.

Phase risk controls:

- PM-0 architecture and indexes must remain navigation/planning surfaces, not runtime state or implementation authorization.
- PM-1 must avoid broad behavioral refactor; package-boundary establishment is allowed only with behavior preservation before cleanup.
- PM-2 must avoid premature schema or file-format lock-in; first pilot model should be tiny, filesystem-backed, and read-only.
- PM-3 external adapters should be integrated while they are working and useful, but must remain optional, lazy, adapter-owned, and fail-soft when unavailable or blocking.
- PM-4 Operator Console projection must be visibly labeled as projection/non-source/non-control.
- PM-5 must avoid full Gantt duration, calendar, resource, and critical-path semantics until the dependency model is proven.
- PM-6 mutation is the highest-risk phase and must address stale reads, race conditions, partial writes, event/state divergence, dry-run behavior, exact file-write reporting, and failure recovery before it is authorized.
- PM-7 template extraction must include portability checks that prevent bootstrap path assumptions from leaking into reusable templates.
- PM-8 product/vault/cross-repo expansion requires separate domain acceptance.

Likely implementation topology:

- Petri-net code should live under `src/python/projectkoios/petrinet/`.
- Workflow code should live under `src/python/projectkoios/workflow/`.
- Project-management code should live under `src/python/projectkoios/project_management/`.
- `src/python/projectkoios/workflow/petrinet.py`, `runtime.py`, `validation.py`, and `adapters.py` currently represent the conceptual `petrinet` layer; PM-1 should establish the target package boundary without changing behavior.
- `src/python/projectkoios/workflow/workflownet.py` and `fixtures.py` are candidates for workflow/read-model boundaries.
- The `project_management` layer should start additive under `src/python/projectkoios/project_management/` and should import workflow read models/protocols only.
- The first CLI surface should use the user-facing namespace `koios pm *`; the initial command should be narrow and read-only, such as `koios pm status`, or limited to deterministic file/read-model generation. Extending `workflow` commands requires explicit rationale.

Layer enforcement should become executable once a PM package exists:

- `projectkoios.petrinet` must not import workflow, project-management, projection, or UI modules.
- `projectkoios.workflow` must not import project-management, projection, or UI modules.
- `projectkoios.project_management` must not import projection or UI modules.
- Optional external backends must be imported lazily inside adapters.
- Shared communication should use public protocols and DataObject-style records rather than higher-layer concrete classes.

Testing strategy by phase:

- PM-1: behavior preservation for existing workflow CLI/status/queue/reconcile surfaces and Petri-net tests, plus import-boundary checks.
- PM-2: fixture validator for unique IDs, reference resolution, no unexpected cycles in decomposition/dependency records, current-state references to definitions, source/projection markers, and parseable thin trace records.
- PM-3: native validation plus adapter parity tests where the adapter is available; unavailable or broken external backends skip/fail-soft without blocking core validation.
- PM-4/PM-5: projection determinism and visible non-source/non-control labels.
- PM-6: dry-run, revision/hash mismatch, exact files-written report, event/state consistency, and failure recovery.
- PM-7/PM-8: portability and no hidden bootstrap-path assumptions.

## First implementation direction after architecture acceptance

The first implementation brief should target PM-1/PM-2 only and should be a narrow read-only foundation/pilot.

Recommended bounded slice name:

- `petrinet-pm-self-tracking-foundation-slice-0`

Recommended scope:

- preserve current workflow/Petri-net behavior;
- add behavior-preservation and import-boundary checks before or alongside any cleanup;
- keep layer cleanup mechanical/read-only except for package-boundary establishment and avoid broad behavior redesign;
- create one tiny self-tracking filesystem pilot fixture for the project-management architecture effort itself;
- classify every first-slice file as source/control, projection, or test/evidence;
- define minimal PM-2 validator criteria before CLI/read-model expansion;
- include a minimal transition-payload example with work-product refs and approval/gate refs, without locking a broad schema;
- expose a deterministic read-only `koios pm status` surface or the read-model needed by that command;
- produce an immediate Operator Console projection fixture/read-model with clear non-source/non-control labels and update rules;
- integrate adapter validation while it works and remains encapsulated, but treat adapter breakage as non-blocking for the PM-1/PM-2 foundation;
- leave Gantt rendering and transition mutation out of the required slice unless separately scoped as optional non-blocking outputs.

Recommended non-goals for the first slice:

- no ADR process dependency;
- no database;
- no daemon;
- no broad provenance system;
- no schema authority under `docs/schemas/`;
- no mutation commands;
- no hard external-engine dependency requirement; external adapters must be encapsulated and non-blocking if broken;
- no Operator Console interactive rendering beyond a projection fixture/read-model with exact non-source labels;
- no Operator Console interactive input;
- no Gantt engine commitment;
- no duration/calendar/resource/critical-path semantics;
- no cross-repo writes;
- no product/vault authority;
- no broad migration, replacement, or behavior redesign beyond the package-boundary establishment explicitly required for `projectkoios.petrinet`, `projectkoios.workflow`, and `projectkoios.project_management`.

## PM-1/PM-2 architecture answers before implementation brief

USER/HERMES answered the package, CLI, Operator Console, validator-example, payload-YAGNI, and adapter direction before the implementation brief. ATHENA supplies the remaining architecture recommendations here so a later brief can be concrete.

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

Do not put first PM source/control files directly under `docs/plans/` or workspace-local state. Those may be referenced as work products, but they should not become the PM source/control namespace.

### Recommended minimal source/control file set

For PM-2, prefer a small split file set over one combined bundle so source/control classification is visible without locking a broad schema:

```text
dev/project-management/self/source/
  project.json                 # project-management identity, phase/component IDs, decomposition roots
  workflow.json                # workflow instance reference over Petri-net places/transitions
  marking.json                 # current Petri-net token/place state for the pilot
  transition-payloads.json     # minimal gate/work-product/approval payload examples
  trace.jsonl                  # thin operational trace; append-like evidence, not heavyweight provenance
```

This is an architecture recommendation, not schema authority. PM-2 may adjust filenames if VULCAN finds a smaller equivalent, but it must preserve distinct source/control concepts: project/task identity, workflow topology/reference, current marking/state, transition payloads, and thin trace.

### Recommended classification

Source/control in PM-2:

- Petri-net/workflow definition or workflow reference files.
- Marking/current-state files.
- Transition payload files containing required work product and approval/gate references.
- PM project/task/decomposition files.
- Thin operational trace files.

Projection/read-model in PM-2:

- `koios pm status` output/read model.
- Operator Console fixture/read model.
- Gantt-ready dependency/component projection, if produced.
- Petri-net diagrams, external-engine reference images, reports, and dashboards.

Test/evidence in PM-2:

- validator output;
- adapter parity output;
- implementation reports and review artifacts;
- generated comparison reports.

Projection files must visibly say they are projections, not source/control. Source/control files must not be generated from projections.

### Transition payload YAGNI baseline

Start with only the fields needed by the self-project-management use case. The conceptual minimum is:

- transition/gate identifier;
- required work-product reference(s);
- approval/gate evidence reference(s), if available;
- optional actor/process label when needed for inspectability.

Do not add a broad payload schema, lifecycle taxonomy, timestamp model, role model, or provenance model until a concrete gate needs it. Thin trace may carry operational timing if necessary, but timing should not become a global schema requirement in PM-2.

### CLI/read-model surface

The user-facing command namespace is:

```bash
koios pm *
```

The first PM-2 command should be read-only, preferably:

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

The first validator should be grounded in the self-project-management pilot. It should check at least:

- all referenced IDs are unique and resolvable;
- source/control files and projection files are labeled/classified;
- current marking/state references defined places/workflow elements;
- transition payloads reference existing gates/transitions and work products;
- project/task decomposition has no accidental cycle unless explicitly modeled as Petri-net behavior;
- projection fixtures identify their source/control inputs;
- thin trace parses and references known events or gates.

### Operator Console fixture/read-model

An Operator Console projection fixture/read-model is immediate PM-2 scope, but it remains projection-only. It must update as the source/control files change and must visibly state:

- generated/static snapshot status;
- source/control input refs;
- not source/control;
- not an interactive mutation surface.

Actual Operator Console UI rendering may remain a separate PM-4 concern if PM-2 only produces the fixture/read-model.

### Adapter/SNAKES scope

Use SNAKES or other external engines while they are useful and working, but preserve encapsulation:

- adapter code belongs in `projectkoios.petrinet`;
- optional backend imports are lazy;
- unavailable/broken adapters fail soft or skip adapter-specific tests;
- adapter images/reports are projections/evidence, not source/control;
- adapter breakage must not block the core PM-1/PM-2 foundation unless the brief explicitly scopes adapter parity as a gate.

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
