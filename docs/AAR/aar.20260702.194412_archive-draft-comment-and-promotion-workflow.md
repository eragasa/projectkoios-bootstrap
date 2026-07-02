# AAR 20260702.194412: Archive Draft Comment and Promotion Workflow

## Scope

ATHENA session in `projectkoios-bootstrap` moving the draft comment/promotion workflow ADR to historical archive status.

## What happened

- Marked `adr.draft-comment-and-promotion-workflow` as historical
- Archived it under `docs/archive/architecture/adr/`
- Pointed its `superseded_by` link at `adr.adr-lifecycle-promotion-mechanics`
- Removed it from the active lifecycle overview note

## Process issues

- The workflow note had been superseded by the lifecycle and promotion-mechanics ADRs
- The user wanted it explicitly marked historical before archival

## Proposed follow-up improvements

- Check whether any other active lifecycle notes are now redundant after the archive move
- Consider folding the remaining comment-open wording into lifecycle guidance if needed

## Candidate ADR or implementation topics

- Historical archive conventions for superseded ADRs
- Active vs archived lifecycle-note cleanup

## Current status

Historical archive completed.
