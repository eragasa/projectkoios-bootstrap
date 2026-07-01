# AAR 20260702.010828: Workspace Agent Guides Are Local Only

## Scope

Copied the root AGENTS guidance into the workspace-specific agent files and roughly adapted them for Hermes, Athena, Vulcan, and Koios.

## What happened

Updated `workspaces/hermes/AGENT.md`, `workspaces/vulcan/AGENT.md`, `workspaces/koios/AGENT.md`, and `workspaces/athena/AGENTS.md` with role-specific prose-plus-bullets guidance.

## Process issues

The workspace files are ignored by git via `.gitignore`, so these updates are local-only rather than versioned repo changes.

## Proposed follow-up improvements

If the workspace guides should be shared or versioned, move them to a tracked docs location or adjust the ignore rules intentionally.

## Candidate ADR or implementation topics

- Workspace guide ownership model
- Whether agent instructions should be tracked or local-only

## Current status

Workspace guides updated locally; repo tracking still excludes them.
