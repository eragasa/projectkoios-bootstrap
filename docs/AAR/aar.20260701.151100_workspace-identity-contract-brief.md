# AAR 20260701.151100: Workspace identity contract brief

## Scope

Drafted the implementation brief for moving agent identity from runtime-based identity to workspace-local `AGENTS.md` identity.

## What happened

Created a new ADR brief stating that shared bootstrap config stays in `./*`, workspace-local state stays in `./$WORKSPACE$/*`, and the target workspace’s own `AGENTS.md` is the source of identity.

## Process issues

The exact target workspace directory convention is still abstracted as `./$WORKSPACE$/*`, which is fine for planning but will need implementation-specific naming later.

## Proposed follow-up improvements

Produce a concrete rollout plan with file-level ownership and compatibility notes.

## Candidate ADR or implementation topics

- workspace directory naming contract
- bootstrap vs workspace precedence rules
- AGENTS.md materialization flow
- validation for identity independence from runtime

## Current status

Implementation brief drafted; ready for review or follow-on planning.
