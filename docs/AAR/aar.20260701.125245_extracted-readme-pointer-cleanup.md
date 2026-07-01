# AAR 20260701.125245: Extracted README pointer cleanup

## Scope

Trimmed the extracted repository READMEs so they point to the canonical routing doc instead of repeating role policy.

## What happened

Updated the READMEs in the extracted repos to include a short pointer to `projectkoios-bootstrap/docs/agent-charter.md`.

## Process issues

- Even short README role blurbs can drift from the canonical routing doc.
- Pointer-only docs reduce duplication and make future role changes cheaper.

## Proposed follow-up improvements

- Keep extracted repo READMEs as ownership summaries only.
- Centralize any future role/routing changes in the bootstrap charter.

## Candidate ADR or implementation topics

- README pointer template for extracted repos.

## Current status

Complete.
