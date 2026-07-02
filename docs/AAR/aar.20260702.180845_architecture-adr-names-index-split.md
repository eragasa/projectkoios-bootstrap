# AAR 20260702.180845: Architecture ADR Names Index Split

## Scope

ATHENA session in `projectkoios-bootstrap` adjusting the architecture index to point at an `architecture.*` note with a controlling ADR on the right.

## What happened

- Replaced the direct naming ADR rows in `architecture.00` with a single `architecture.adr.names` note row
- Created `docs/architecture/architecture.adr.names.md`
- Kept `docs/architecture/adr/adr.adr-names.draft.md` as the controlling ADR reference
- Updated the ADR names text to describe child ADR links using filesystem paths

## Process issues

- The index needed to distinguish navigation notes from controlling ADRs more clearly
- The user clarified that the left side should be an `architecture.*` note and the right side should be a controlling `adr.*` file link

## Proposed follow-up improvements

- Apply the same architecture-note / controlling-ADR split to other index rows where direct ADR links are still used
- Check whether any older index entries still mix navigation and control surfaces

## Candidate ADR or implementation topics

- Index row convention for `architecture.*` navigation notes
- Controlling-ADR link convention for `adr.<kebab>` targets

## Current status

`architecture.00` now points at `architecture.adr.names` for ADR naming, with `adr.adr-names` as the controlling ADR.
