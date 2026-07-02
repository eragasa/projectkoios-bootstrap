# AAR 20260702.180350: ADR Names Umbrella and Child-Link Encapsulation

## Scope

ATHENA session in `projectkoios-bootstrap` adding an umbrella ADR for naming semantics and linking the existing title/filename naming ADRs underneath it.

## What happened

- Created `docs/architecture/adr/adr.adr-names.draft.md`
- Updated `docs/architecture/architecture.00.md` so ADR title/filename naming now point at the umbrella naming ADR
- Added child links from the umbrella ADR to the existing title and filename naming ADRs

## Process issues

- The naming discussion needed a semantic title layer separate from filename storage
- The umbrella ADR makes the naming surface easier to navigate for JSON-backed ADR work

## Proposed follow-up improvements

- Review whether the title and filename ADRs should eventually be folded into the umbrella as subsections
- Check other docs for any remaining title/filename conflation

## Candidate ADR or implementation topics

- JSON ADR title-as-data contract
- Promotion workflow for semantic ADR titles vs storage filenames

## Current status

Umbrella ADR drafted and indexed. Working tree updated with architecture index changes.
