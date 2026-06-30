# AAR 20260701.014145: Promotion review routing

## Scope

This AAR covers the session that promoted the Graphify daemon ADR after an
Archon promotion review.

## What happened

The session started with a clean repository and one Draft ADR needing review:
`docs/architecture/adr/adr.20260701.004713_graphify-ingestion-daemon-bootstrap.md`.
After the user noted they could perform a Hermes review, Codex initially
described a manual Hermes review path. The user corrected the routing by
pointing out that an Archon promotion-review workflow already exists.

Codex then ran `athena_review-draft-for-promotion`, received a
`ready_for_hermes_acceptance_review` recommendation, recorded the user's
acceptance by changing the ADR status to `Accepted`, and pushed the status
change.

## Process issues

The session-start recommendation was directionally correct but underspecified.
For Draft ADRs that need review, Codex should prefer the existing
`athena_review-draft-for-promotion` workflow before suggesting an ad hoc manual
Hermes review, unless Hermes explicitly asks to bypass Archon.

This matters because the workflow encodes the promotion gate, checks lifecycle
context, and returns a reusable Athena artifact for Hermes to accept or reject.
Manual review remains Hermes authority, but the advisory Athena workflow is the
expected review path when available.

## Proposed follow-up improvements

- Update session-start guidance or repo-local skills to name
  `athena_review-draft-for-promotion` as the default next step for active Draft
  ADR promotion review.
- When recommending "Hermes review or Athena promotion," explicitly distinguish
  between human acceptance authority and the Archon advisory review workflow.

## Candidate ADR or implementation topics

- No new architecture ADR is required.
- Candidate documentation or skill update: Draft ADR promotion routing guidance.

## Current status

This AAR is a process observation artifact. It does not change architecture
authority, ADR status, or implementation routing by itself.
