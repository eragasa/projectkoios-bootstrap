# AAR 20260701.193907: Hermes AGENTS pruned to Hermes-local scope

## Scope

Reduced `workspaces/hermes/AGENTS.md` to Hermes-local instructions and moved global policy content into the repo root `AGENTS.md`.

## What happened

The user requested a forest-level pass instead of continued line-by-line edits. I moved global identity/delegation/policy sections out of the Hermes workspace file, kept the Hermes workspace header and session protocol, and left Hermes-specific operating guidance in place.

## Process issues

- The earlier line-by-line approach was too narrow for the file’s scope.
- Some edits required a broader structural pass to avoid duplication and policy drift.

## Proposed follow-up improvements

- Keep Hermes workspace files limited to Hermes-local behavior and session protocol.
- Keep shared policy blocks centralized in the repo root AGENTS file.
- Use major-revision checkpoints for future large scope changes.

## Candidate ADR or implementation topics

- AGENTS file scope partitioning
- Hermes workspace contract
- Major-revision workflow for policy docs

## Current status

Hermes-local content remains in the workspace AGENTS file; global policy was moved out.
