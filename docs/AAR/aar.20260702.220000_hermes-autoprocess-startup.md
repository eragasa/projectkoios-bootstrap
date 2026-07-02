# AAR — Hermes autoprocess startup

## Scope
Hermes workspace-state startup support.

## What happened
Added a durable autoprocess startup note and updated Hermes state/active files so future sessions can resume from workspace files rather than chat history.

## Process issues
The repo already has workspace-state conventions, but they were not yet consolidated into a single startup checklist file.

## Proposed follow-up improvements
Consider linking the startup checklist from the Hermes workspace instructions so it is easier to find after restarts.

## Candidate ADR or implementation topics
Workspace startup checklist binding.

## Current status
No blocking issue observed.
