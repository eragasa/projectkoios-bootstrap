# AAR 20260701.141728: Workspace command and Koios skill

## Scope

Added a bootstrap command to materialize per-agent workspaces and refined the
Koios workspace-bootstrap skill to match the new tool.

## What happened

Implemented `projectkoios bootstrap workspaces init`, which seeds
`workspaces/hermes`, `workspaces/athena`, `workspaces/vulcan`, and
`workspaces/koios` with local `AGENT.md`, `state.md`, `active.md`, and the
expected handoff/session/decision directories. Updated the Koios skill and the
workspace template instructions to reflect that each workspace has its own
local `AGENT.md`.

## Process issues

- The workspace bootstrap needed to be a real command, not just a manual layout.
- The Koios skill needed to name the actual bootstrap command it should use.
- Per-workspace `AGENT.md` files make the runtime instructions less ambiguous.

## Proposed follow-up improvements

- Add a tiny command to show workspace status or validate that the local
`AGENT.md` files exist.
- Consider generating the workspace `AGENT.md` files from a dedicated template
file if the wording changes often.

## Candidate ADR or implementation topics

- Workspace command lifecycle and validation.
- Template-driven generation of per-agent `AGENT.md` files.

## Current status

Complete.
