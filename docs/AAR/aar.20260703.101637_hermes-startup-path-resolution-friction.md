# AAR 20260703.101637: Hermes startup path resolution friction

## Scope
Hermes session startup in `projectkoios-bootstrap`.

## What happened
I followed the Hermes start sequence, read `state.md`, `active.md`, the newest session note, and confirmed the inbox was empty. The Archon DB showed no running or paused workflow runs. The first attempt to run `./scripts/hermes-startup new` from the workspace directory failed because the script lives at repo root; rerunning it from the repo root succeeded and created a new session marker.

## Process issues
The workspace-level instructions and repo-root script location were easy to mismatch during startup.

## Proposed follow-up improvements
Document the repo-root invocation more prominently in the Hermes workspace notes or add a workspace-local wrapper.

## Candidate ADR or implementation topics
Hermes startup ergonomics.

## Current status
Complete.
