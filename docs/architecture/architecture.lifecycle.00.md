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

This note indexes the workflow surface controlled by:

- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` — active lifecycle/status compatibility decision
- `docs/adr/adr.idea-spike-adr-implementation-workflow.draft.md` — draft broader workflow source
- `docs/adr/adr.adr-lifecycle.draft.md` — source/provenance draft
- `docs/adr/adr.adr-lifecycle-promotion-mechanics.md` — source/provenance draft

It is the index note for lifecycle-oriented architecture guidance inside
`projectkoios-bootstrap`. If this note conflicts with the active ADR, the
active ADR wins.

## Decision

Use the active ADR lifecycle/status compatibility decision:

`proposal -> draft -> accepted -> active -> superseded`

with terminal or follow-on paths:

- `accepted -> superseded`
- `active -> superseded`
- `draft -> superseded`
- `proposal -> superseded`

Where:

- ideas are rough, messy, and non-authoritative, and remain outside the ADR lifecycle unless separately promoted into `proposal`
- proposals are candidate packets that are not yet complete ADR review records
- draft ADRs are complete enough to review but are not accepted authority
- accepted ADRs are approved document authority, but may be accepted and not active for enforcement or routing
- active ADRs are accepted and current controlling authority for work, enforcement, routing, or document interpretation
- superseded ADRs remain traceable records after another accepted or active record replaces or narrows them
- implementation briefs translate accepted or active decisions into build work when implementation is authorized separately

## Related files

- `docs/architecture/architecture.00.md`
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
- `docs/adr/adr.idea-spike-adr-implementation-workflow.draft.md`
- `docs/adr/adr.adr-lifecycle.draft.md`
- `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`
- `docs/adr/adr.adversarial-two-plane-gate.draft.md`
- `docs/policies/architecture.adr.lifecycle.md`

## Notes

- This note is intentionally light until the process stabilizes further.
- If the lifecycle changes materially, update the controlling ADR first.
- `proposed`, `completed`, `rejected`, and `historical` are legacy lifecycle terms and are not canonical ADR statuses under the current lifecycle.
- Deprecated staging directories, required proposal/draft sections, gate fields, rejection/disposition records, and role ownership remain deferred unless separately accepted.
- ADRs are encapsulated decision records; hierarchy and readiness are represented by `architecture.00`, not by nested ADR body structure.
- Gates are workflow-facing control surfaces; ownership is a higher-level architectural concern.
