# Implementation report 20260705.003351: Workspace-state protocol bootstrap reconciliation

## Status

Implementation complete for bounded policy/bootstrap reconciliation against the accepted canonical workspace-state and next-action protocol ADR.

## Provenance

- Acting-As: VULCAN
- Repository: projectkoios-bootstrap
- Workspace: `workspaces/vulcan/`
- Branch: `master`
- Request source: HERMES handoff authorized by user
- Controlling ADR: `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`
- Scope: stale policy/guidance/bootstrap surfaces only
- Next expected artifact: HERMES/user review or commit packaging decision

## Summary

Reconciled stale workspace protocol references and bootstrap workspace initialization behavior with the accepted ADR.

Changed policy and architecture surfaces:

- `docs/policies/workspace-layout.md`
  - Changed proposal/draft framing to accepted-ADR-aligned policy framing.
  - Points to the accepted ADR as the controlling decision.
  - Keeps workspace files framed as control surfaces, not authority replacements.
- `docs/architecture/architecture.00.md`
  - Updated the canonical workspace protocol row to link the accepted ADR.
- `docs/architecture/architecture.canonical-workspace-state-and-next-action-protocol.md`
  - Updated status/control links to the accepted ADR and marked the old draft as superseded provenance.
- `docs/architecture/architecture.workspaces.00.md`
  - Removed stale `handoffs/incoming/` and `handoffs/outgoing/` convention.
  - Aligned the workspace layout with `state.md`, `active.md`, `sessions/`, `working/`, `scratch/`, and `decisions/`.
  - Clarified that `working/` material is active only when named in `active.md`.
- `README.md`
  - Replaced proposed-workspace-state wording with accepted ADR and policy guidance.

Changed bootstrap code and tests:

- `src/python/projectkoios/bootstrap/commands/workspaces.py`
  - Replaced stale handoff-folder help text with workspace control-folder wording.
- `src/python/projectkoios/bootstrap/workspaces.py`
  - Added stable top JSON metadata blocks to generated `state.md` and `active.md` seed files.
  - Seeded required human-readable sections for resume state, blockers, validated state, handoff status, open questions, priority stack, waiting-on, active working material, ignored scope, exit criteria, and next expected artifact.
  - Fixed stale canonical reference path from `docs/architecture.00.md` to `docs/architecture/architecture.00.md`.
- `tests/test__workspaces_command.py`
  - Added coverage for top JSON metadata in generated `state.md` and `active.md`.
  - Added coverage for absence of deprecated `handoffs/`, `working/incoming/`, and `working/outgoing` directories.
  - Added coverage for the corrected architecture reference path.

## Validation evidence

Commands run from `/Users/eugene/repos/projectkoios-bootstrap`:

- `uv run pytest tests/test__workspaces_command.py -q` => `4 passed in 0.43s`
- `uv run mypy src/python/projectkoios/bootstrap/workspaces.py src/python/projectkoios/bootstrap/commands/workspaces.py tests/test__workspaces_command.py` => `Success: no issues found in 3 source files`
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/workspaces.py src/python/projectkoios/bootstrap/commands/workspaces.py` => `summary: 0 finding(s), 2 file(s)`
- `uv run pytest tests/test_bootstrap_flow.py tests/test__workspaces_command.py -q` => `6 passed in 0.58s`
- `uv run pytest -q` => `215 passed in 1.13s`

## Deviations and deferred work

- Did not edit product architecture.
- Did not broaden into unrelated workflow refactors.
- Did not reconcile existing Hermes workspace `state.md`/`active.md`; current bootstrap seeds are fixed for newly initialized/refreshed workspaces, and existing live workspace control files should be updated by their owning role when appropriate.
- Existing non-VULCAN dirty worktree changes outside this bounded patch were not modified intentionally.

## Current status

The requested stale policy/guidance/bootstrap surfaces are reconciled with the accepted workspace-state protocol ADR. Bootstrap workspace initialization now generates `state.md` and `active.md` with stable top JSON metadata and no deprecated mailbox directory convention.
