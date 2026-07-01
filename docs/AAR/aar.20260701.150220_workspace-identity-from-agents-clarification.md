# AAR 20260701.150220: Workspace identity from AGENTS clarification

## Scope

Clarified the next-stage goal for moving harness identity from runtime-based identity to workspace-local `AGENTS.md` identity.

## What happened

Updated the workspace-local harness instantiation ADR to state that identity should come from each workspace’s own `AGENTS.md`, with shared bootstrap config under `./*` and workspace-local state under `./$WORKSPACE$/*`.

## Process issues

The workspace naming contract is still underspecified at the directory-convention level.

## Proposed follow-up improvements

Write an implementation brief that defines the workspace contract, precedence rules, and migration sequence.

## Candidate ADR or implementation topics

- `./$WORKSPACE$/*` layout contract
- identity precedence between runtime and AGENTS.md
- shared vs workspace-local config separation
- compatibility/migration plan

## Current status

Planning updated; implementation should wait on a follow-up brief.
