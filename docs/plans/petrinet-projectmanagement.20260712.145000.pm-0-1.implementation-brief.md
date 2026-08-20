```json
{
  "title": "Implementation brief: Petri-net PM working engine slice 0",
  "artifact_type": "implementation-brief",
  "status": "draft-for-user-review",
  "datetime": "20260712.145000Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-pm-working-engine-slice-0",
  "phase_label": "pm-0-1",
  "phase_label_reason": "The slice consumes PM-0 architecture/planning-Gantt input and implements PM-1 working-engine plus Console projection capability.",
  "source_architecture": "docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md",
  "source_alignment": "docs/plans/petrinet-projectmanagement.20260712.pm-0.project-alignment.md",
  "project_index": "docs/plans/petrinet-projectmanagement.00.md",
  "architecture_index": "docs/architecture/architecture.project-management.00.md",
  "not_an_adr": true,
  "implementation_authorization": false,
  "next_owner": "HERMES_USER"
}
```

# Implementation brief: `petrinet-pm-working-engine-slice-0`

## Status

Draft for USER/HERMES review.

This brief does not authorize implementation. VULCAN must not begin coding until USER/HERMES accepts or revises this brief and explicitly routes implementation planning.

## Source authority

This brief is derived from:

- `docs/plans/petrinet-projectmanagement.00.md`
- `docs/plans/petrinet-projectmanagement.20260712.pm-0.project-alignment.md`
- `docs/architecture/architecture.project-management.00.md`
- `docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md`
- `docs/reviews/petrinet-projectmanagement.20260712.143207.pm-0.hermes-acceptance.md`

## Scope

Implement PM-0/PM-1 only:

1. PM-0 planning projection input:
   - non-authoritative planning Gantt derived from architecture phase/component map.
2. PM-1 backend:
   - minimal working Petri-net/workflow engine backend and simplified skeleton.
3. PM-1 frontend/projection:
   - Console projection/read-model that reflects what the minimal engine can do.

This is not “build the PM system.” It is the first working engine proof with phase-appropriate Console visibility.

## Required implementation result

VULCAN should produce a minimal executable/inspectable engine that can:

- load a simplified Petri-net/workflow skeleton fixture;
- inspect places, transitions, arcs, initial/current marking, and component mappings;
- report deterministic engine state/output;
- report enabled/basic transition state if supported by existing runtime semantics;
- optionally perform a non-persistent in-memory step/enablement proof;
- write no persistent state changes;
- generate or expose a Console projection/read-model for that engine capability.

## Package boundaries

Target package boundaries:

```text
src/python/projectkoios/petrinet/
src/python/projectkoios/workflow/
src/python/projectkoios/project_management/
```

Allowed import direction:

```text
projectkoios.petrinet -> projectkoios.workflow -> projectkoios.project_management
```

Interpretation:

- `projectkoios.workflow` may import `projectkoios.petrinet`.
- `projectkoios.project_management` may import `projectkoios.workflow`.
- `projectkoios.petrinet` must not import upward.
- `projectkoios.workflow` must not import `projectkoios.project_management`.
- projection/UI code must not be imported by `petrinet`, `workflow`, or `project_management` runtime packages.

If moving existing Petri-net modules from `projectkoios.workflow` is non-trivial, VULCAN may use compatibility re-exports or wrappers to preserve current import paths for this slice. Any compatibility path must be documented in the implementation plan and covered by tests.

## Minimal engine API/output expectations

VULCAN should define concrete names in its implementation plan, but the PM-1 engine capability must include equivalent behavior to this conceptual API:

```text
load_skeleton(path) -> EngineSkeleton
inspect_engine(skeleton) -> EngineInspection
render_inspection(inspection) -> deterministic text or JSON-ready data
```

Optional if low-risk and non-persistent:

```text
enabled_transitions(skeleton, marking) -> list[transition_id]
step_in_memory(skeleton, marking, transition_id) -> new_marking_preview
```

The deterministic output must include at least:

- engine id or fixture id;
- skeleton source path;
- phase label: `PM-1`;
- places/components loaded;
- transitions loaded;
- arcs loaded;
- current/initial marking used for inspection;
- component mapping summary;
- enabled/basic transition summary if implemented;
- explicit `persistent_mutation: false`;
- exact input refs used to compute output.

The engine may reuse existing `projectkoios.workflow` Petri-net classes where behavior is already present. If reuse requires a package-boundary wrapper, prefer wrapper/re-export over behavior redesign.

## Planning Gantt projection

Required path:

```text
dev/project-management/self/projections/pm-0.planning-gantt.md
```

Preferred format:

- Markdown table plus Mermaid Gantt or flowchart if useful;
- no new Gantt engine dependency;
- deterministic text output.

Required labels/header content:

```text
artifact_type: planning-gantt-projection
projection: true
planning_only: true
source_control: false
not_runtime_state: true
not_implementation_authorization: true
input_refs:
  - docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md
```

Required content:

- PM-0 through PM-9 phase rows or nodes;
- component IDs relevant to PM-0/PM-1, including at least `PROJ-GANTT-PLAN`, `PN-CORE`, `PN-ENGINE`, `PN-SKELETON`, `WF-INSTANCE`, and `PROJ-CONSOLE`;
- dependency ordering;
- any deferred components with rationale;
- clear statement that Gantt component IDs are planning components, not runtime places by default.

## Simplified skeleton fixture

Required path:

```text
dev/project-management/self/source/pm-1.engine-skeleton.workflow-net.json
```

The file is PM-1 source/control skeleton for the engine proof. It is not the mature PM source/control model, not a schema authority artifact, and not a mutable runtime database.

Required top-level shape, exact field names may be refined by VULCAN but must preserve these concepts:

```json
{
  "artifact_type": "pm-engine-skeleton",
  "phase": "PM-1",
  "source_control": true,
  "persistent_mutation_allowed": false,
  "input_refs": [
    "docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md",
    "dev/project-management/self/projections/pm-0.planning-gantt.md"
  ],
  "workflow_id": "petrinet-projectmanagement.pm-1.working-engine",
  "places": [],
  "transitions": [],
  "arcs": [],
  "initial_marking": {},
  "component_mappings": []
}
```

Skeleton mapping rules:

- every required PM-0/PM-1 planning component ID must have either:
  - a skeleton counterpart; or
  - an explicit deferred rationale;
- no extra skeleton ID may appear without a source planning component or rationale;
- planning components need not map only to places; mapping may be to place, transition, subnet, workflow instance, project task, or deferred rationale;
- skeleton must not inherit Gantt duration, calendar, resource, or critical-path semantics.

## Console projection/read-model

Required projection/read-model path:

```text
dev/project-management/self/projections/pm-1.console-engine-projection.json
```

If VULCAN also updates the TypeScript Operator Console package, the JSON projection should remain the source fixture/read-model and any TypeScript fixture should copy or import its values deterministically. If direct TypeScript integration is too large for this slice, VULCAN must still produce the Console-consumable JSON projection/read-model.

Required fields/concepts:

```json
{
  "artifact_type": "operator-console-projection",
  "phase": "PM-1",
  "projection": true,
  "source_control": false,
  "not_source_control": true,
  "interactive_mutation_allowed": false,
  "persistent_mutation_allowed": false,
  "engine_capability": {
    "loads_skeleton": true,
    "inspects_state": true,
    "reports_enabled_transitions": "implemented-or-not-implemented",
    "in_memory_step_preview": "implemented-or-not-implemented"
  },
  "input_refs": [],
  "engine_summary": {},
  "visible_labels": [
    "projection",
    "not source/control",
    "not interactive",
    "not persistent mutation"
  ]
}
```

The projection must reflect only what the PM-1 engine can actually do. It must not imply PM-2 self-tracking state, PM-5 gates/work products, PM-6 mutation, PM-7 operational Gantt, or PM-9 database readiness.

## CLI / command-surface recommendation

Long-term user-facing namespace remains:

```bash
koios pm *
```

Current repository CLI exposes the installed script:

```bash
projectkoios
```

PM-1 recommendation:

- Do not block the engine proof on a top-level `koios` script alias.
- Add a narrow `pm` command group behind the current CLI if low-risk, for example:

```bash
uv run projectkoios pm engine-status
```

- The command may print the deterministic engine inspection/read-model.
- If VULCAN chooses to add a `koios` script alias in this slice, it must be a small compatibility addition and tests must prove equivalent behavior for the PM command.
- Do not reuse or overload the existing `projectkoios koios` GraphRAG command group for PM.
- If CLI work threatens the engine proof, produce deterministic engine/read-model files and defer command alias polish to PM-3 projection hardening.

## Behavior-preservation requirements

VULCAN's implementation plan must include behavior-preservation gates for existing workflow/Petri-net behavior.

Required checks:

```bash
uv run projectkoios workflow status
uv run projectkoios workflow queue
uv run projectkoios workflow activate pi-skill-determinism-slice-0 --dry-run
uv run projectkoios workflow reconcile-status --dry-run
```

Required tests:

- existing Petri-net runtime tests;
- existing workflow fixture/status/queue/activation/reconciliation tests;
- any tests currently covering optional adapters must remain optional/fail-soft if backend is unavailable.

If VULCAN changes package boundaries, add tests proving compatibility imports/re-exports for current `projectkoios.workflow` import paths.

## New acceptance tests for this slice

VULCAN should add focused tests for:

1. Engine loading:
   - engine loads `pm-1.engine-skeleton.workflow-net.json`;
   - invalid/missing skeleton path fails with explicit error;
   - output is deterministic.
2. Engine inspection:
   - reports expected places/transitions/arcs/marking/component mappings;
   - includes `persistent_mutation: false` or equivalent.
3. Optional non-persistent stepping:
   - if implemented, step preview changes only in-memory data;
   - no source/control file is written.
4. Planning Gantt projection:
   - projection has required labels;
   - no source/control authority fields are implied;
   - component IDs used by PM-1 are present or explicitly deferred.
5. Skeleton-to-Gantt matching:
   - every required PM-0/PM-1 component has counterpart or deferred rationale;
   - no extra skeleton IDs lack source/rationale.
6. Console projection/read-model:
   - projection exists at the required path;
   - projection is deterministic JSON;
   - projection references engine/skeleton/planning inputs;
   - projection labels `projection`, `not source/control`, and no mutation authority;
   - projection reflects only PM-1 engine capability.
7. Layer/import boundaries:
   - `projectkoios.petrinet` does not import `projectkoios.workflow`, `projectkoios.project_management`, or UI/projection packages;
   - `projectkoios.workflow` does not import `projectkoios.project_management` or UI/projection packages;
   - `projectkoios.project_management` does not import UI/projection packages.

## Explicit non-goals

This slice must not add:

- ADR process dependency;
- persistent transition mutation;
- writes to marking/state as part of engine step;
- gates/work-product payloads;
- `transition-payloads.json` placeholder unless explicitly justified;
- `trace.jsonl` placeholder unless explicitly justified;
- broad provenance system;
- schema authority under `docs/schemas/`;
- JSON database or database dependency;
- operational/live Gantt generated from PM source/control state;
- Console interactive input;
- Console mutation controls;
- product/vault/cross-repo authority;
- package migration that breaks current workflow commands/imports;
- full duration/calendar/resource/critical-path semantics;
- external engine dependency requirement.

## VULCAN planning handoff criteria after USER review

After USER/HERMES review and acceptance, VULCAN's implementation plan should provide:

- file-level implementation plan;
- whether implementation is split into smaller tasks/patches;
- exact engine class/function names;
- exact skeleton JSON shape;
- exact Console projection/read-model shape;
- whether CLI command is included in PM-1 or deferred;
- compatibility import/re-export policy;
- test list and validation commands;
- risk list for behavior preservation and package-boundary changes;
- explicit confirmation that no persistent mutation, gates/payloads, trace, database/schema authority, operational Gantt, or interactive Console input is included.

## Recommended validation commands for VULCAN

Minimum expected validation after implementation:

```bash
uv run pytest tests/projectkoios/workflow tests/projectkoios/bootstrap -q
uv run mypy src/python/projectkoios/petrinet src/python/projectkoios/workflow src/python/projectkoios/project_management tests/projectkoios
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/petrinet src/python/projectkoios/workflow src/python/projectkoios/project_management tests/projectkoios
uv run projectkoios workflow status
uv run projectkoios workflow queue
uv run projectkoios workflow activate pi-skill-determinism-slice-0 --dry-run
uv run projectkoios workflow reconcile-status --dry-run
git diff --check
```

If Operator Console TypeScript files are changed:

```bash
cd src/typescript/projectkoios/ui/operator-console
npm ci --ignore-scripts
npm run typecheck
npm test
npm run build
npm audit --audit-level=moderate
```

Generated `node_modules`, `dist`, coverage, database files, and local preview state must not be committed.

## USER review questions

Before VULCAN implementation planning, USER/HERMES should confirm or revise:

1. Is `dev/project-management/self/source/pm-1.engine-skeleton.workflow-net.json` acceptable as the PM-1 skeleton path?
2. Is `dev/project-management/self/projections/pm-0.planning-gantt.md` acceptable as the planning Gantt projection path?
3. Is `dev/project-management/self/projections/pm-1.console-engine-projection.json` acceptable as the first Console projection/read-model path?
4. Should PM-1 include a CLI command (`uv run projectkoios pm engine-status`) or defer CLI until PM-3 if the engine/read-model files are deterministic?
5. Should non-persistent in-memory stepping be required in PM-1, or is load/inspect/enabled-state output sufficient for the first working engine proof?
