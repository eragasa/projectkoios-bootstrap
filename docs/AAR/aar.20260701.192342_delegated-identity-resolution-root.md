# AAR 20260701.192342: Delegated identity resolution moved to root AGENTS

## Scope

Moved the delegated identity resolution rule from `workspaces/hermes/AGENTS.md` into the repo root `AGENTS.md`.

## What happened

The user identified the rule as global, not Hermes-specific. I moved the rule block and removed it from the Hermes workspace file.

## Process issues

- None observed.
- The user requested better analysis before making the choice, which was applied.

## Proposed follow-up improvements

- Keep cross-harness identity rules in the root AGENTS file only.
- Keep workspace AGENTS files focused on workspace-specific constraints and behavior.

## Candidate ADR or implementation topics

- Global vs workspace AGENTS policy partition
- Identity resolution and delegation provenance rules
- Precision-edit workflow for AGENTS maintenance

## Current status

The delegated identity resolution rule now lives in the repo root AGENTS file.
