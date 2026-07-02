# AAR 20260702.193846: Lifecycle Status and Promotion Model Refresh

## Scope

ATHENA session in `projectkoios-bootstrap` revising ADR lifecycle semantics to use draft / proposed / active / historical / rejected and to define spike packaging as draft ADR + implementation plan.

## What happened

- Rewrote `docs/architecture/adr/adr.adr-lifecycle.draft.md` to use the updated lifecycle status model
- Rewrote `docs/architecture/adr/adr.adr-lifecycle-promotion-mechanics.md` to define spike packaging, draft-to-proposed promotion, and proposed-to-active promotion
- Kept the docs harness-agnostic by removing `Delegated-Operator` from active ADRs earlier in the session

## Process issues

- The lifecycle model needed an explicit distinction between proposed and active
- The spike concept needed a formal packaging rule rather than ad hoc local conventions

## Proposed follow-up improvements

- Update the policy consumption doc if it should mirror the new active/proposed/active/historical model
- Decide whether the repository should standardize archive path behavior for historical ADRs later

## Candidate ADR or implementation topics

- JSON schema alignment for the revised lifecycle states
- Archive path rules for historical ADRs

## Current status

Lifecycle and promotion-mechanics ADRs updated to the new model.
