# AAR 20260702.130210Z: Closeout sequence clarified in AGENTS

## Scope

Repo session closeout rules across root, pi, opencode, and goose AGENTS files.

## What happened

The session closeout sequence was ambiguous during the prior wrap-up. The repository instructions were updated so the end-of-session flow is explicit: write the AAR, commit the files, request a push, and only consider the session ended after the push succeeds.

## Process issues

- The closeout rule was present in practice but not clearly visible in every relevant AGENTS file.
- The push/request boundary was easy to misread without a shared sequence.

## Proposed follow-up improvements

- Keep closeout steps mirrored in all harness AGENTS files.
- Prefer a single short numbered sequence for session end behavior.

## Candidate ADR or implementation topics

- Add a small shared closeout protocol note if the repo wants one canonical reference.

## Current status

The closeout sequence is now documented in the relevant AGENTS files and ready for commit/push.
