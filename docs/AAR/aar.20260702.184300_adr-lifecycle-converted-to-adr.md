# AAR 20260702.184300: ADR Lifecycle Converted to ADR

## Scope

ATHENA session in `projectkoios-bootstrap` converting the ADR lifecycle policy into an ADR using the canonical ADR template.

## What happened

- Created `docs/architecture/adr/adr.adr-lifecycle.draft.md`
- Updated `docs/policies/adr-lifecycle.md` so it now points to the ADR as source of truth
- Preserved the lifecycle policy doc as a consumption aid
- Kept the file-status vs operational-phase distinction explicit in the new ADR

## Process issues

- The lifecycle content had been split between archived ADR history and an active policy note
- The user wanted the lifecycle logic expressed as an ADR rather than only as policy prose

## Proposed follow-up improvements

- Decide whether the new lifecycle ADR should be promoted to accepted or stay draft until review
- Consider whether any workflow docs should link directly to the new ADR instead of the policy note

## Candidate ADR or implementation topics

- ADR lifecycle control surface promotion
- Policy doc as consumption aid vs active authority

## Current status

New lifecycle ADR drafted; policy doc now references it.
