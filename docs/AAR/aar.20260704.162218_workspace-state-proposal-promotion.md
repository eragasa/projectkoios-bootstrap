# AAR 20260704.162218: workspace-state proposal promotion

## Scope

Athena session in `projectkoios-bootstrap` advancing the canonical workspace-state / next-action protocol from draft state toward proposed review.

## What happened

- Read Athena workspace state and active priority surfaces.
- User selected priority 3: promote or reconcile the canonical workspace-state / next-action protocol draft.
- Created proposed review surface at `dev/canonical-workspace-state-next-action-protocol/adr.canonical-workspace-state-next-action-protocol.proposed.md`.
- Marked the historical draft `docs/adr/adr.canonical-workspace-state-next-action-protocol.draft.md` as superseded by the proposal without rewriting it in place.
- Updated Athena `state.md` and `active.md` to record the proposal and next review owner.

## Process issues

- The repository had unrelated Vulcan-owned uncommitted implementation/test changes while Athena performed this bounded ADR promotion work.
- ADR promotion mechanics are still themselves draft-level guidance, so the proposal used the documented `dev/<proposal-id>/` shape but should receive Hermes/user review before being treated as accepted authority.

## Proposed follow-up improvements

- Hermes/user should review whether this proposal should be accepted and whether `docs/policies/workspace-layout.md` should point to it as the controlling decision.
- A future validator can check the required `state.md`/`active.md` top JSON metadata and workspace directory shape.
- Workspace startup guidance should continue to emphasize the read order: `state.md`, then `active.md`, then only named working material.

## Candidate ADR or implementation topics

- Accept canonical workspace-state / next-action protocol ADR.
- Implement lightweight workspace-state validator after acceptance.
- Reconcile `docs/policies/workspace-layout.md` with the accepted ADR if needed.

## Current status

Proposal created and awaiting Hermes/user review. No implementation authority was created.
