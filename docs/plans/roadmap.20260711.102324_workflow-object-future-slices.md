```json
{
  "title": "Workflow object future slice roadmap",
  "artifact_type": "architecture-roadmap",
  "status": "draft-for-user-hermes-review",
  "datetime": "20260711.102324Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_architecture": "docs/architecture/architecture.workflow-object.md",
  "current_first_slice": "docs/plans/implementation-brief.20260711.102123_workflow-object-static-operator-console-record.md"
}
```

# Roadmap 20260711.102324: Workflow object future slices

## Purpose

Draft likely future workflow-object slices after the first static Operator Console record.

This roadmap is planning guidance only. It does not authorize implementation and does not create schema, storage, CLI, UI, Petri-net runtime, or product authority.

## Controlling boundary

All future slices must preserve the accepted distinction from `docs/architecture/architecture.workflow-object.md`:

- artifacts/documents are durable referenced records with status, provenance, owner/domain, authority boundary, and hash/version/ref where required;
- Petri-net places are workflow states, not documents;
- tokens reference work items and artifact versions/records;
- gates evaluate typed evidence/status predicates;
- workflow objects are projection/index records, not source artifact authority or completion authority.

## Slice 0: Static Operator Console workflow-object record

Status: brief and candidate static JSON record shape drafted for VULCAN planning.

Brief and candidate shape:

- `docs/plans/implementation-brief.20260711.102123_workflow-object-static-operator-console-record.md`
- `docs/plans/schema-proposal.workflow-object.static-record.20260711.102743.md`

Goal:

- Create one static JSON workflow-object record for accepted Operator Console P0/P1/readability evidence.

Out of scope:

- accepted repository-wide schema, storage, CLI, UI, Petri-net runtime, live adapters, bulk generation.

## Slice 1: Static record validator

Goal:

- Add a narrow validator for the Slice 0 static record.

Candidate scope:

- verify referenced paths exist;
- verify hashes/refs are present for generated, fixture-backed, or immutable review evidence;
- verify required non-authority markers exist;
- verify gate evaluations include evidence refs and evaluator/owner role;
- verify no `docs/adr/` mutation is required.

Out of scope:

- repository-wide workflow-object schema;
- CLI command;
- database/storage adapter;
- runtime Petri-net integration;
- bulk record discovery/generation.

Pause triggers:

- needing formal JSON schema authority;
- needing repository-wide validation command naming;
- needing live file watchers or runtime repo scans.

## Slice 2: Second static workflow-object record for non-UI work

Goal:

- Prove the model against a non-Operator-Console work item to avoid overfitting to UI preview evidence.

Candidate proving cases:

- `adr.json-schemas` conformance slice;
- JSON document database separation slice;
- control-surface cleanup/schema conformance slice.

Candidate scope:

- one additional static workflow-object record;
- artifact refs, gate evaluations, validation evidence, review/acceptance refs, provenance links;
- compare which fields are common versus UI-specific.

Out of scope:

- bulk backfill;
- schema redesign;
- storage authority;
- changing ADR source documents.

Gate:

- USER/HERMES selects the proving case before ATHENA drafts a brief.

## Slice 3: Minimal workflow-object vocabulary consolidation

Goal:

- Consolidate common vocabulary observed across two static records.

Candidate scope:

- define stable architecture vocabulary for artifact refs, workflow tokens, transition gates, gate evaluations, validation evidence, preview evidence, lifecycle markers;
- identify required vs optional fields;
- identify artifact-type-specific extensions;
- record where UI preview evidence is special-case rather than universal.

Out of scope:

- JSON schema;
- database model;
- code generation;
- runtime execution semantics.

Gate:

- requires at least two reviewed static records.

## Slice 4: Schema authority decision, not automatic schema authority

Status: candidate static record shape exists at `docs/plans/schema-proposal.workflow-object.static-record.20260711.102743.md` for Slice 0 only.

Goal:

- Decide whether evidence from implemented static records warrants promoting the candidate shape toward a formal schema.

Candidate scope:

- review candidate shape against implemented records;
- field semantics, examples, and validation requirements;
- migration notes from static records if needed;
- explicit recommendation whether to keep candidate shape as prose guidance, draft JSON Schema, or accepted `docs/schemas/` authority.

Out of scope:

- accepting a repository-wide schema;
- changing existing static records automatically;
- storage/database decisions.

Gate:

- ATHENA/HERMES/USER must decide whether schema authority is warranted by repeated evidence.

## Slice 5: Read-only index of workflow-object records

Goal:

- Make multiple static workflow-object records discoverable without creating runtime workflow state.

Candidate scope:

- static manifest listing workflow-object record paths, ids, titles, status, and content hashes;
- validation that manifest entries exist and match hashes;
- no live scanning required unless explicitly approved.

Out of scope:

- database/storage adapter;
- live repository indexer;
- CLI/UI support;
- completion authority.

Gate:

- requires at least two accepted workflow-object records and USER/HERMES confirmation that discoverability is the next pain point.

## Slice 6: Adapter-library projection contract

Goal:

- Define how workflow-object records map onto adapter-library payloads without passing raw workflow-object JSON directly into backend adapters.

Candidate scope:

- define an adapter-neutral `WorkflowObjectAdapterPayload` or equivalent projection contract;
- map `workflow_places` to adapter-neutral place payloads;
- map transition/gate names to transition/topology metadata only where explicitly evidenced;
- keep `artifact_records` as token/evidence metadata, never Petri-net places;
- keep `gate_evaluations` as evidence unless a later slice defines executable guard projection;
- reference current adapter-neutral workflow payload patterns in `src/python/projectkoios/workflow/adapters.py`.

Out of scope:

- backend-specific SNAKES or other dependency changes;
- runtime token firing;
- Petri-net runtime semantics changes;
- raw workflow-object JSON as backend adapter input.

Gate:

- requires one accepted static workflow-object JSON record and review of whether adapter projection is the next pressure.

## Slice 7: Petri-net projection experiment

Goal:

- Explore whether workflow-object records can project into Petri-net places/tokens/gates without conflating artifacts with places.

Candidate scope:

- read-only projection from one workflow-object record into domain-level `WorkflowPlace`, `WorkflowToken`, and `TransitionGate` structures;
- no firing transitions;
- no mutation;
- no runtime orchestration.

Out of scope:

- changing Petri-net runtime semantics;
- making artifacts Petri-net nodes;
- live execution;
- graph editor/UI.

Gate:

- only after static records and vocabulary have stabilized enough to avoid architecture churn.

## Slice 8: Operator Console read-only display of workflow-object record

Goal:

- Let the incubated Operator Console display a static workflow-object record as read-only evidence.

Candidate scope:

- fixture import of one workflow-object record;
- read-only display of artifact refs, gate evaluations, validation evidence, preview evidence, and non-authority markers;
- clear static/non-live/stale-by-design labeling.

Out of scope:

- live workflow-object loading;
- mutation/activation controls;
- backend/API;
- product authority;
- broad UI redesign.

Gate:

- requires accepted static record and a separate Operator Console UI brief.

## Slice 9: Handoff packet integration

Goal:

- Use workflow-object record vocabulary to improve role handoffs without making the workflow object the authority.

Candidate scope:

- define a handoff packet excerpt: work item id, artifact refs/hashes, expected next gate, owner/domain, evidence refs, blockers;
- document how HERMES routes using refs and gates;
- avoid mandatory automation.

Out of scope:

- live intercom/session integration;
- orchestrator runtime changes;
- completion automation.

Gate:

- HERMES must own/review orchestration mechanics.

## Slice 10: Storage/database decision intake

Goal:

- Decide whether workflow objects need persistent storage beyond static fixture records and manifests.

Candidate scope:

- architecture intake comparing static files, JSON document store, SQLite-backed document store, or product-side storage;
- evidence from prior slices;
- authority and extraction-boundary analysis.

Out of scope:

- implementing storage;
- migrating records;
- product repository decision without mothership authority.

Gate:

- only after static records/manifests demonstrate concrete storage pressure.

## Recommended ordering

1. Complete Slice 0.
2. Add Slice 1 validator only if manual validation is already error-prone.
3. Add Slice 2 non-UI record to test generality.
4. Consolidate vocabulary in Slice 3.
5. Choose between Slice 4 schema authority decision, Slice 5 manifest, Slice 6 adapter projection contract, or Slice 8 UI display based on the next observed pain point.
6. Defer Petri-net projection, handoff integration, and storage decisions until static evidence proves the need.

## Current recommended next action

Proceed with VULCAN planning for Slice 0. Do not start later slices until Slice 0 is implemented, reviewed, and reconciled.
