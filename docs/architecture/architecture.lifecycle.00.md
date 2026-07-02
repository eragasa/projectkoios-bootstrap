---
status: draft
date: 20260702.000551Z
back_to: architecture.00
---

# Lifecycle Control Surface

## Purpose

This note is the bootstrap architecture index for lifecycle and control-surface
workflow. It exists to keep exploratory ideas, spikes, durable decisions, and
implementation work in separate layers.

## Scope

This note governs the workflow surface controlled by:

- `docs/architecture/adr/adr.idea-spike-adr-implementation-workflow.draft.md`
- `docs/architecture/adr/adr.adr-lifecycle.draft.md`
- `docs/architecture/adr/adr.adr-lifecycle-promotion-mechanics.md`

It is the index note for lifecycle-oriented architecture guidance inside
`projectkoios-bootstrap`.

## Decision

Use the following lifecycle:

`idea -> spike -> draft ADR -> proposed ADR -> active ADR -> implementation brief -> iterative implementation`

Where:

- ideas are rough, messy, and non-authoritative
- spikes are draft ADR + implementation-plan bundles in `reporoot/spike/<spike-id>/`
- draft ADRs are comment-open working records
- proposed ADRs are the active review surface and move to dev in `reporoot/dev/<proposal-id>/`
- active ADRs are production records
- implementation briefs translate decisions into build work
- iterative implementation is where code changes happen

## Related files

- `docs/architecture/architecture.00.md`
- `docs/architecture/adr/adr.idea-spike-adr-implementation-workflow.draft.md`
- `docs/architecture/adr/adr.adr-lifecycle.draft.md`
- `docs/architecture/adr/adr.adr-lifecycle-promotion-mechanics.md`
- `docs/architecture/adr/adr.adversarial-two-plane-gate.draft.md`
- `docs/policies/architecture.adr.lifecycle.md`

## Notes

- This note is intentionally light until the process stabilizes further.
- If the lifecycle changes materially, update the controlling ADR first.
- `docs/incubator/` and `docs/spikes/` are deprecated staging directories and should be migrated out and deleted.
- Draft ADR comments stay open until promotion to proposed; proposed then becomes the active review surface.
- ADRs are encapsulated decision records; hierarchy and readiness are represented by `architecture.00`, not by nested ADR body structure.
- Gates are workflow-facing control surfaces; ownership is a higher-level architectural concern.
