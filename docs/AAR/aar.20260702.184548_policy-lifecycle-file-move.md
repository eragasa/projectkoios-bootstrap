# AAR 20260702.184548: Policy Lifecycle File Move

## Scope

ATHENA session in `projectkoios-bootstrap` moving the ADR lifecycle policy note into the dot-named policy filename and linking it from the ADR architecture index.

## What happened

- Moved `docs/policies/adr-lifecycle.md` to `docs/policies/architecture.adr.lifecycle.md`
- Added `architecture.adr.lifecycle` to `docs/architecture/architecture.adr.00.md`
- Updated lifecycle ADR and review template references to the new policy path

## Process issues

- The lifecycle policy path needed to match the repository's dot-named index style
- The move briefly created stale references that had to be rewritten

## Proposed follow-up improvements

- Search for any remaining stale references to the old lifecycle policy filename in older notes or archives
- Decide whether more policy docs should adopt the same `architecture.*` filename style

## Candidate ADR or implementation topics

- Policy filename normalization for active policy surfaces
- Indexing rules for human-facing policy notes

## Current status

Policy file moved and references updated.
