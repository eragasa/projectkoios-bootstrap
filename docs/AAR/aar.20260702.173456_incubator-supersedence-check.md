# AAR: Incubator supersedence check

## Scope
Incubator note cleanup in `projectkoios-bootstrap`.

## What happened
- Deleted two incubator notes too early.
- User corrected the process and requested restoration.
- Restored the requested notes and confirmed matching draft ADRs already exist for the same topics.

## Process issues
- I did not verify explicit supersedence before deleting incubator notes.
- Deletion based on loose topic matching is too aggressive.

## Proposed follow-up improvements
- Require an explicit supersedence check before removing incubator notes.
- Prefer retaining incubator notes until the matching ADR draft is confirmed.

## Candidate ADR or implementation topics
- Incubator-to-ADR promotion policy.
- Supersedence validation rule for note cleanup.

## Current status
- Requested incubator notes restored.
- Matching ADR drafts are present.
- One unrelated incubator deletion remains intentionally in place.
