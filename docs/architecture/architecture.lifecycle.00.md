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

It is the index note for lifecycle-oriented architecture guidance inside
`projectkoios-bootstrap`.

## Decision

Use the following lifecycle:

`idea -> spike -> ADR -> implementation brief -> iterative implementation`

Where:

- ideas are rough, messy, and non-authoritative
- spikes are timeboxed learning artifacts
- ADRs are durable decisions
- implementation briefs translate decisions into build work
- iterative implementation is where code changes happen

## Related files

- `docs/architecture/architecture.00.md`
- `docs/architecture/adr/adr.idea-spike-adr-implementation-workflow.draft.md`
- `docs/policies/policy-baseline.md`
- `docs/policies/review-baseline.md`

## Notes

- This note is intentionally light until the process stabilizes further.
- If the lifecycle changes materially, update the controlling ADR first.
- Use `docs/incubator/` for raw ideas and `docs/spikes/` for timeboxed
  experiments once those surfaces exist.
