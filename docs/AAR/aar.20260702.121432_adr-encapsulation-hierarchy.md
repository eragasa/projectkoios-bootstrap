# AAR 20260702.121432: ADR encapsulation and hierarchy

## Scope

Clarified how ADR encapsulation and repository hierarchy should relate in the bootstrap architecture notes.

## What happened

Updated `docs/architecture/architecture.00.md` and `docs/architecture/architecture.lifecycle.00.md` to state that ADRs are encapsulated, independently readable decision records, while hierarchy, readiness, and promotion ordering are represented by `architecture.00`.

Also added the same rule to `docs/architecture/adr/adr.idea-spike-adr-implementation-workflow.draft.md`.

## Process issues

- The distinction between incubator ideas, spikes, and ADR drafts needed tighter language.
- The hierarchy question was clarified only after checking the existing architecture index and lifecycle notes.

## Proposed follow-up improvements

- Keep `architecture.00` as the single place for hierarchy and readiness links.
- Add a small template note for ADR encapsulation rules if this pattern recurs.
- Continue using draft ADRs as the working surface until promotion review is explicit.

## Candidate ADR or implementation topics

- Encapsulated ADR rules for the bootstrap architecture surface.
- A structured hierarchy/readiness index for ADRs in `architecture.00`.

## Current status

Complete.
