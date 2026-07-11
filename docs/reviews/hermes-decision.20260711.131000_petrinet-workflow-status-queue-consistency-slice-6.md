```json
{
  "title": "HERMES decision: Petri-net workflow status/queue consistency slice 6",
  "artifact_type": "workflow-decision",
  "status": "approved-for-vulcan-implementation",
  "datetime": "20260711.131000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-workflow-status-queue-consistency-slice-6",
  "reviewed_artifact": "docs/plans/implementation-brief.20260711.130723_petrinet-workflow-status-queue-consistency-slice-6.md",
  "next_owner": "VULCAN"
}
```

# HERMES decision 20260711.131000: Petri-net workflow status/queue consistency slice 6

## Decision

HERMES approves `petrinet-workflow-status-queue-consistency-slice-6` for VULCAN implementation.

## Rationale

The current workflow inspectability surfaces disagree:

- `uv run projectkoios workflow status` still reports `active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2` at `user_decision`.
- `uv run projectkoios workflow queue` reports no active item, Slice 4 completed, Slice 5 accepted/pushed, and `pi-skill-determinism-slice-0` queued-only.

This stale-status inconsistency is now a workflow-engine bug because it can mislead operators and agents about whether a current active slice exists. A narrow static-fixture reconciliation command is the smallest coherent next repair.

## Approved implementation direction

- Keep `workflow status` read-only.
- Add a separate conservative command, preferably:

  ```bash
  uv run projectkoios workflow reconcile-status [--dry-run]
  ```

- Command execution may read only:
  - `dev/workflow-nets/bootstrap-harness.workflow-net.json`
  - `dev/workflow-nets/bootstrap-harness.queue-state.json`
- Command execution may write only:
  - `dev/workflow-nets/bootstrap-harness.workflow-net.json`
- Derive status `active_slice` from queue `active_item`:
  - active item name when queue has an active item;
  - `none` when queue `active_item` is null.
- Preserve status fixture topology, token id/place, enabled transition behavior, and `requires_user_decision=true`.
- Do not activate, implement, or supersede `pi-skill-determinism-slice-0`.
- Print a before/after summary and static-fixture/non-canonical authority warning.
- Include dry-run if low-cost; otherwise document deferral.

## Watchpoints

Do not add Petri-net transition firing, executor/runtime mutation, queue activation, generalized persistence/database/storage, git/chat/intercom/workspace-prose reconstruction, Operator Console integration, workflow-object runtime coupling, schema/product authority, global skill propagation, or implicit activation of queued work.

## Required validation

VULCAN should validate with queue output, reconcile dry-run if implemented, status output after reconciliation, focused tests, Python policy validation, JSON validity checks for both fixtures, and `git diff --check`. Any deviation from the brief must be reported explicitly.
