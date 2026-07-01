# AAR 20260702.002233: Architecture Index Table

## Scope
Hermes normalized the `docs/architecture/architecture.00.md` index into a table of architecture notes and controlling ADRs.

## What happened
Replaced the sectioned bullet index with a two-column table: note and controlling ADR. The lifecycle note now points to the workflow ADR, and all other listed `architecture.<sub>` notes currently show `None`.

## Process issues
None observed.

## Proposed follow-up improvements
If more architecture notes gain controlling ADRs, the table can serve as the single place to review ownership.

## Candidate ADR or implementation topics
- Whether to add more controlling ADRs for other architecture notes
- Whether `architecture.00` should also list archive-only notes

## Current status
`docs/architecture/architecture.00.md` updated and graphify refreshed.
