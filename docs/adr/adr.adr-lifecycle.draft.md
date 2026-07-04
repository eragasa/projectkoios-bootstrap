# ADR 20260702.182000: ADR Lifecycle Policy

## Status

draft

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

Project Koios needs one canonical ADR lifecycle so reviewers and agents stop inventing lifecycle rules. The active policy doc in `docs/policies/architecture.adr.lifecycle.md` is a consumption aid, but the lifecycle contract itself belongs in an ADR.

The lifecycle contract must stay harness-agnostic and token-light while still making the active state of an ADR obvious:

- draft means comment-open working record
- proposed means active review surface and moving to dev
- active means the implementation plan is complete and the ADR is in production
- historical means the ADR was superseded
- rejected means the ADR was archived and did not proceed

Workflow-bound ADRs may also carry an optional gate block defined by
`adr.workflow.draft.md` and `adr.adr-workflow.draft.md`. When present, gate
fields must point to explicit gating ADRs.

When JSON storage becomes authoritative later, the controlling ADR document will be JSON and the Markdown file will be a knowledge projection.

## Decision

Adopt a canonical ADR lifecycle for Project Koios bootstrap.

### File status values

ADR files keep these human-facing statuses:

- `Draft`
- `Proposed`
- `Active`
- `Historical`
- `Rejected`

### Operational lifecycle states

These are the canonical operational states for ADR work:

1. `draft`
2. `proposed`
3. `active`
4. `historical`
5. `rejected`

### State meanings

- `draft` — comment-open working record
- `proposed` — active review surface and moving to dev
- `active` — implementation plan complete and ADR in production
- `historical` — superseded record after replacement
- `rejected` — archived record that did not proceed

### Canonical state ownership

- `draft` — Hermes
- `proposed` — Athena
- `active` — Vulcan
- `historical` — Athena
- `rejected` — Athena

### Required ADR sections at `proposed`

When an ADR reaches `proposed`, it must include these machine-relevant sections:

- `architecture-spec`
- `acceptance-criteria`
- `implementation-brief`
- `resolved-open-questions`
- `non-goals`
- `validation-expectations`
- `routing`

### Canonical transitions

Draft-to-production path:

`draft -> proposed -> active`

Replacement path:

`active -> historical`

Terminal rejection path:

`draft -> rejected`

### Spike packaging rule

A draft ADR plus `ADR_implementation_plan` is a spike, and the spike lives in `reporoot/spike/<spike-id>/`.

### Rules

- Do not invent new lifecycle states.
- Do not invent new allowed-next transitions.
- Do not use `active` as a synonym for `proposed`.
- Do not treat draft comments as acceptance.
- Do not mark an ADR complete without implementation-plan completion.
- Do not change lifecycle semantics without a new or superseding Athena ADR.
- Do not treat routing as the primary control model for workflow-bound ADRs.

## Consequences

- reviewers and agents have one active lifecycle contract to follow
- file status and operational state stay separate and machine-readable
- the active production state is distinguishable from the active review surface
- spikes have a single packaging rule instead of ad hoc local conventions
- JSON can become the source of truth later without changing the lifecycle intent

## architecture_spec

The ADR lifecycle contract defines:

- the file status set
- the operational state set
- the state ownership mapping
- the required `proposed` sections
- the allowed state transitions
- the optional workflow-binding gate surface for workflow-bound ADRs
- the rule that lifecycle semantics only change through Athena ADR authority

Stated negatively:
- no ad hoc state names
- no silent transition additions
- no validation shortcuts
- no lifecycle semantics hidden in policy prose alone

## acceptance_criteria

- a reviewer can route an ADR to the correct state
- file status and operational state are clearly distinct
- the required `proposed` sections are inspectable
- the allowed transitions are explicit
- the lifecycle policy can be referenced from `docs/policies/architecture.adr.lifecycle.md`

## implementation_brief

If accepted, update `docs/policies/architecture.adr.lifecycle.md` and any workflow guidance so they point to this ADR as the source of truth.

### Verification method

Review a sample ADR and confirm the file status, operational state, required `proposed` sections, and allowed transition path are unambiguous.

## resolved_open_questions

- Should the operational state be mirrored in JSON schema as well as Markdown?
- Should draft ADRs be comment-open until `proposed`?
- Should a no-implementation ADR skip `active` entirely?
- Should `historical` be reserved only for superseded ADRs?
- Should workflow-bound ADRs require explicit gate links or only when a gate is declared?

## non_goals

- Redefining the canonical ADR JSON schema
- Removing historical lifecycle ADRs
- Changing the meaning of ADR file statuses outside this contract
- Adding new lifecycle states

## validation_expectations

- a reviewer can distinguish status from state
- the state ownership table is internally consistent
- the lifecycle path is understandable from the file alone
- workflow-bound ADRs can name their gating ADRs without conflicting with the core lifecycle states

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Active ADR lifecycle control surface.

## links

- back_to: architecture.00
- supersedes: docs/archive/architecture/adr/adr.20260630.175315_athena-owned-adr-lifecycle.md
- superseded_by: None
