# AAR 20260701.142022: Hermes workspace AGENT file

## Scope

Wrote the local Hermes workspace instruction file.

## What happened

Updated `workspaces/hermes/AGENT.md` to define Hermes workspace behavior,
local file expectations, and canonical references.

## Process issues

- Workspace-local instruction files need to stay concise and explicit.
- The Hermes workspace should point to the routing authority and formatting
  template rather than repeating broader policy prose.

## Proposed follow-up improvements

- Add matching `AGENT.md` files for the other workspaces if their local
  instructions need refinement.
- Consider generating workspace AGENT files from a template helper.

## Candidate ADR or implementation topics

- Workspace-local AGENT file generation.

## Current status

Complete.
