# Implementation Plan: projectkoios-workflow Petri-Net Executor

## Source

- ADR: `docs/architecture/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md`
- Related context: `docs/petri-net-model.md`, `docs/archive/architecture/adr/adr.20260630.042202_colored-petri-net-meta-harness.md`

## Scope

Implement the workflow substrate described by the ADR:

- canonical Petri-net IR
- execution/runtime layer
- adapter boundary for SNAKES and PM4Py
- restart/inspection/event tracing support
- domain-package workflow validation and execution hooks

## Repository target

- Primary target: `src/python/projectkoios/workflow` in `projectkoios-bootstrap`
- This plan is the file-level implementation guide that Vulcan can execute after
  the ADR is accepted
- Existing workflow-adjacent code under `src/python/projectkoios/bootstrap/harness/`
  should be migrated or wrapped under the new package boundary and regression-
  tested against current behavior

## File-level tasks

### 1) Package skeleton

- create `src/python/projectkoios/workflow/`
- create modules for model, runtime, validation, adapters, and events
- add package exports for the canonical API
- add compatibility shims or migration entry points for existing handoff/
  evaluator code

### 2) Canonical model

- define `Place`, `Transition`, `Token`, `Arc`, `Marking`, `WorkflowNet`
- define `Guard`, `Binding`, `FiringRule`, `NetSchema`
- define `ExecutionState`, `Event`, `ExecutionTrace`, `EventLog`
- define the semantic wrapper types (`DataObject`, `ActivityObject`,
  `AgentObject`, `WorkspaceObject`, `ArtifactObject`, `PermissionObject`)

### 3) Validation layer

- validate workflow objects against the schema before execution
- verify place/transition/token consistency
- verify enabled-transition logic can be computed from a marking
- reject workflow objects that violate the boundary between substrate and domain

### 4) Runtime / orchestrator

- implement the orchestrator that advances a marking by firing enabled
  transitions
- emit structured events for validation, enablement, firing, and completion
- track execution state and history
- support restart/checkpoint hooks for future persistence

### 5) Adapter boundary

- implement `SnakesColoredNetAdapter`
- implement `Pm4pyProcessMiningAdapter`
- keep `SimPN` and `PNet` deferred
- prohibit direct imports of third-party Petri-net libraries outside adapters

### 6) Inspection / trace surface

- expose current net, marking, enabled transitions, and execution history
- provide serializable event/history output for debugging and tests

### 7) Tests

- schema validation tests
- enabled-transition tests
- firing/marking mutation tests
- event emission tests
- adapter boundary tests
- round-trip inspection tests
- regression tests that prove current handoff/evaluator behavior is preserved
  through migration

## Task breakdown order

1. package skeleton
2. canonical model
3. schema validation
4. runtime/orchestrator
5. adapters
6. inspection/trace helpers
7. tests
8. docs/examples

## Verification method

- unit tests for model and runtime semantics
- adapter boundary tests that fail on direct third-party imports
- a sample workflow that validates, executes, and emits trace output
- inspection of marking/history after repeated firings

## Risks / escalation

- If restart support requires more persistence shape than planned, escalate back
  to Athena before hard-coding storage assumptions.
- If adapter APIs drift toward direct third-party coupling, stop and refactor
  before adding more runtime behavior.
- If domain workflow definitions need extra semantic types, defer until Athena
  revises the substrate model.

## Deliverables

- working workflow substrate package under `src/python/projectkoios/workflow/`
- adapter modules for SNAKES and PM4Py
- tests proving execution semantics and boundary enforcement
- migration or compatibility layer for existing handoff/evaluator code
- sample workflow object and execution trace
- brief usage note for downstream domain packages

## Notes

- Preserve the read-only handoff evaluator as a specialized use case, not the
  whole workflow architecture.
- Keep the first slice small enough to validate the executor before expanding
  to deferred adapters.
- Favor migration plus shims over a clean-room rewrite when current behavior can
  be retained.
