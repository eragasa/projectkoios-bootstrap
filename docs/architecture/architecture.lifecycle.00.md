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

- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` — accepted lifecycle/status compatibility decision
- `docs/adr/adr.idea-spike-adr-implementation-workflow.draft.md` — draft broader workflow source
- `docs/adr/adr.adr-lifecycle.draft.md` — source/provenance draft
- `docs/adr/adr.adr-lifecycle-promotion-mechanics.md` — source/provenance draft

It is the index note for lifecycle-oriented architecture guidance inside
`projectkoios-bootstrap`. If this note conflicts with the accepted ADR, the
accepted ADR wins.

## Decision

Use the accepted ADR lifecycle/status compatibility decision:

`draft -> proposed -> accepted`

with terminal or follow-on paths:

- `proposed -> rejected`
- `accepted -> completed`
- `accepted -> superseded`
- `completed -> superseded`
- `draft -> rejected`

Where:

- ideas are rough, messy, and non-authoritative, and remain outside the accepted lifecycle unless separately promoted
- spikes are draft ADR + implementation-plan bundles in `spike/<spike-id>/`
- draft ADRs are working records
- proposed ADRs are review surfaces and may live in `dev/<proposal-id>/`
- accepted ADRs are adopted authority records
- completed ADRs record applicable rollout or documentation reconciliation completion
- superseded and rejected ADRs remain traceable records
- implementation briefs translate accepted decisions into build work when implementation is authorized separately

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
- `active` and `historical` are legacy lifecycle terms and are not canonical ADR statuses under the accepted ADR.
- Deprecated staging directories, required proposed sections, gate fields, and role ownership remain deferred unless separately accepted.
- ADRs are encapsulated decision records; hierarchy and readiness are represented by `architecture.00`, not by nested ADR body structure.
- Gates are workflow-facing control surfaces; ownership is a higher-level architectural concern.
