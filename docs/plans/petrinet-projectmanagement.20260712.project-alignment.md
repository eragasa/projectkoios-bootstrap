```json
{
  "title": "Project alignment: Filesystem-backed Petri-net project management with Gantt projections",
  "artifact_type": "project-alignment-note",
  "status": "draft-alignment",
  "datetime": "20260712",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "filesystem-backed project management across bootstrap harness, product/vault, and cross-repo coordination",
  "source": "USER interview with HERMES",
  "not_a_spec": true,
  "not_architecture_authority": true,
  "next_recommended_owner": "HERMES",
  "koios_review": "subagent-chat-019f51a8 intercom reply 20260712: provenance-adequate as draft alignment/intake; no blockers",
  "user_process_update": "USER wants project management bootstrapped through the operational process, outside the ADR process"
}
```

# Project alignment: Filesystem-backed Petri-net project management with Gantt projections

## Status

This is a HERMES project-alignment note from an initial USER interview.

It is not a specification, ADR, implementation brief, architecture decision, or implementation authorization.

It preserves early alignment so KOIOS can review provenance/terminology and ATHENA can later receive a bounded architecture-framing request if HERMES/USER chooses.

## User intent, preserved

USER initially stated:

> i think we need a filesystem only project management system, i think it should be based upon gannt and will be eventually a petrinet workflow

USER later clarified:

- Scope should cover all three: bootstrap harness project management, product/vault project management, and cross-repo coordination.
- The reason for filesystem-first operation is: databases should not get in the way of having an operational system.
- Gantt should not be the source of truth.
- Petri-net state and associated transition payloads should be source/control authority.
- Gantt is a projection.
- Each task in the Gantt is simply a place on the Petri net.
- The system exists so Project Koios has a way of tracking documents and work products.
- The smallest first tracked object is likely a task.
- The system should align with DAG-style workflows, while using Petri nets for enhancements beyond typical DAG implementations.
- The system should cover the whole implementation while supporting recursive decomposition: task to subtask to subsubtask and beyond.
- Recursive decomposition is needed to identify critical paths, move work to subprojects, and avoid losing visibility.
- Transition payload details are to be determined, but must include the required work product and approval from the process or agent that controls the gate.
- Gantt views should support planned future places, current markings/state, and combined planned plus actual state.
- Whether tasks are durable records or derived from places/transition payloads is deferred.
- A task may encapsulate a document or work product that has a different state space than the task itself.
- The design should stay YAGNI but not brittle.
- Almost everything produced in code development can be treated as a work product.
- Approvals can be human or agent/process approvals, but some gates should explicitly require human approval.
- The project-management system should be bootstrapped using the Project Koios working process itself.
- The bootstrap path should produce a working workflow system outside the ADR process rather than depending on ADR production as the primary path.
- The pilot should leverage existing workflow/Petri-net code rather than starting from scratch.
- The pilot should be used to clean up existing workflow/Petri-net code as needed while preserving current working behavior.
- There should be a UI renderer of the workflow and of the Petri net at each step.
- Petri-net adapters should be used for validation.
- There should be strict separation of concerns among a Petri-net subpackage, workflow subpackage, and project-management layer.
- The dependency/protocol flow should be one-way: `petrinet -> workflow -> pm`.
- The pilot should track itself and later be extracted as a template for other projects.
- The Operator Console fixture should be the user's primary visibility surface for system state.
- The Operator Console fixture should initially be projection-only, not source/control.
- Later, the Operator Console may become a source of interactive user input through a separately approved interaction/mutation design.
- The project should be set up as a multi-phase project resembling waterfall, not scrum.
- Work should proceed through explicit phases and phase gates rather than scrum-style sprint slicing.
- External Petri-net engines such as SNAKES may be used as initial execution engines if their APIs are encapsulated.
- External engines may also produce reference images so Project Koios can validate its visualizer against a known-good implementation.

## Current aligned framing

Project Koios needs a filesystem-backed, project-wide Petri-net task and work-product tracking system.

The system should avoid making a database, daemon, or hidden runtime a prerequisite for operational project tracking.

Petri-net state and transition payloads are the intended source/control authority. Gantt is a projection for planning and visibility, not execution truth.

The system should support DAG-like planning and critical-path reasoning while preserving Petri-net capabilities for richer workflow state, gate approvals, concurrent state, and transition semantics.

The system must support recursive task decomposition so project-wide visibility is preserved when work moves between subprojects or breaks into subtasks.

The system should track documents, code, tests, reviews, reports, decisions, generated projections, and other work products while preserving distinctions between source/control artifacts and projections.

## Scope

Initial scope spans:

1. bootstrap harness project management;
2. product/vault project management;
3. cross-repo coordination.

This does not mean the first implementation must cover every surface at once. It means the concept should avoid decisions that prevent later shared visibility across those scopes.

## Source/control and projection alignment

Current alignment:

- Petri-net state is intended source/control authority.
- Transition payloads are intended source/control authority for state movement and gate evidence.
- Gantt is a projection/view.
- A Gantt task corresponds to a Petri-net place in the user's current mental model.
- Planned future places, current markings, and combined planned/actual views should all be representable.

Deferred:

- whether task records are durable source files or derived from Petri-net definitions, markings, and transition payloads;
- exact payload schema;
- exact mapping between DAG dependencies, Petri-net places/transitions, and Gantt bars;
- whether documents/work products have independent state machines, independent Petri nets, or state metadata attached to tasks/places/payloads.

## Required work product and gate approval

Transition payloads must eventually capture at least:

- the required work product for a transition/gate;
- the approval from the process, agent, or human that controls the gate.

Some gates must require explicit human approval.

Agent/process approvals are allowed where the gate policy permits them.

## Non-goals for this note

This note does not decide:

- an ADR;
- an ADR-driven architecture path;
- a schema;
- a storage namespace;
- a file format;
- a command interface;
- a Petri-net runtime;
- an Operator Console integration;
- a Gantt renderer;
- a migration or cutover from existing workflow fixtures;
- replacement of `state.md`, `active.md`, workflow queue fixtures, ADRs, plans, implementation reports, reviews, or AARs.

## Risks and cautions carried forward

From KOIOS and VULCAN implementation/provenance input, future work should preserve these cautions:

- Filesystem-only must distinguish source/control files from generated projections, reports, caches, and runtime snapshots.
- Gantt must remain a planning/visibility projection unless later accepted otherwise.
- Petri-net runtime semantics must not be collapsed into task bars.
- Existing workflow fixtures are static inspectability surfaces, not broad product/runtime authority.
- Project-management records must not silently supersede ADRs, HERMES decisions, plans, implementation reports, reviews, AARs, workspace `state.md`/`active.md`, or Petri-net fixtures.
- Source-of-truth files should be explicit before any CLI, schema, UI, or renderer work.
- Concurrency matters: filesystem operation needs single-writer discipline and/or optimistic checks before any mutation command exists.
- Read-only status/projection commands should be default; mutation commands require explicit authorization, dry-run behavior, and exact written-file reporting.
- Existing document/work-product state spaces may differ from task workflow state; avoid a brittle one-state-model assumption.

## Open questions

1. What namespace should incubate the first filesystem PM records or examples: `dev/`, `docs/plans/`, workspace-local files, or another project-management namespace?
2. Is the first durable source/control surface a Petri-net definition, a marking file, transition payload logs, task records, or a combination?
3. How should a Gantt task-as-place projection represent duration, dependencies, milestones, critical path, and actual state?
4. How should task decomposition map to Petri-net composition or subnets?
5. What minimum transition payload is required for a gate to be inspectable?
6. Which gate types require explicit human approval?
7. How should the system preserve visibility when a task moves to another subproject or repository?
8. Which existing workflow surfaces should coexist unchanged in the first slice?

## Process-bootstrap update

USER later clarified that project management should be bootstrapped using the Project Koios process itself to produce a working workflow system outside the ADR process.

HERMES interpretation: the next path should not be an ADR-first architecture route. It should be a bounded operational process/pilot route that preserves alignment, provenance, and review gates while avoiding ADR process overhead as the primary mechanism.

USER further clarified that the pilot should leverage existing code, use the project-management work to clean up that code where appropriate, render both the workflow and Petri net in a UI at each step, and use Petri-net adapters for validation.

This does not authorize uncontrolled implementation. It means the first concrete workflow should be framed as a working-process bootstrap/pilot with explicit artifacts, gates, review, validation adapters, UI-rendering expectations, and rollback boundaries.

## Recommended next action

KOIOS reviewed this alignment note and found it provenance-adequate as draft alignment/intake, with no blockers to HERMES using it as input for a later bounded workflow decision.

HERMES/USER can next decide whether to define a non-ADR, multi-phase project brief for the project-management system. The brief should use waterfall-like phases and phase gates rather than scrum-style slices, while still starting with the smallest operational phase that reuses existing workflow/Petri-net code, preserves `petrinet -> workflow -> pm` separation, includes adapter-backed validation, and uses the Operator Console fixture as the primary projection-only visibility surface.

KOIOS watchpoints for any later architecture or workflow request:

- Treat Petri-net state and transition payloads as captured USER intent, not accepted architecture authority.
- Test the task-as-place mapping explicitly, because conventional Petri-net modeling may map tasks differently.
- Define an incubation boundary before spanning bootstrap, product/vault, and cross-repo coordination.
- Sharpen the filesystem-only definition.
- Separate transition payloads from event logs, approvals, work-product references, and generated projections.
- Define identity/provenance rules before mutation commands exist.

Additional USER alignment for pilot framing:

- Separate the Petri-net subpackage from the workflow subpackage and the project-management layer.
- Keep dependency/protocol flow strict: `petrinet -> workflow -> pm`.
- Use the pilot to track itself, then extract the pilot as a template for other projects.
- Use the Operator Console fixture as the user's primary visibility surface for state.
- Treat the Operator Console fixture as projection-only at first.
- Defer interactive user input through the Operator Console to a later separately approved design.
- Frame the pilot as a multi-phase/waterfall-like project with explicit phase gates, not as a scrum backlog or sprint sequence.
- Encapsulate external Petri-net execution engines such as SNAKES behind adapters.
- Use external engine outputs/images as known-good references for validating Project Koios visualizers.
