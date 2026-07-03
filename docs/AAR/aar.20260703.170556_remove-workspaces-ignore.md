# AAR: Remove workspaces ignore

## Scope
Repo-wide change to stop ignoring the `workspaces/` tree and allow workspace state files to be tracked.

## What happened
- Removed the broad `workspaces/` ignore rule.
- Replaced it with narrower ignores for workspace-local runtime artifacts.
- Added workspace state, active, inbox/outbox, and handoff files to version control.

## Process issues
None observed.

## Proposed follow-up improvements
- Keep workspace-local runtime caches out of git with targeted ignore rules.
- Decide whether additional workspace scratch prompts should remain tracked or move to a separate notes surface.

## Candidate ADR or implementation topics
- workspace layout policy for tracked vs local-only files
- canonical workspace-state surface

## Current status
Workspace files are now trackable and committed; the repo is clean.
