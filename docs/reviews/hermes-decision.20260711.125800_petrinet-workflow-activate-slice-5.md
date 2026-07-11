```json
{
  "title": "HERMES decision: Petri-net workflow activate slice 5",
  "artifact_type": "workflow-decision",
  "status": "approved-for-vulcan-implementation",
  "datetime": "20260711.125800Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-workflow-activate-slice-5",
  "reviewed_artifact": "docs/plans/implementation-brief.20260711.124950_petrinet-workflow-activate-slice-5.md",
  "next_owner": "VULCAN"
}
```

# HERMES decision 20260711.125800: Petri-net workflow activate slice 5

## Decision

HERMES approves `petrinet-workflow-activate-slice-5` for VULCAN implementation.

## Rationale

The brief addresses the current document-domain inconsistency: Slice 4 is accepted and committed as `5f209114`, but the static queue fixture still reports Slice 4 as proposed-next. A narrow activation/queue-fixture update command is the smallest coherent next state because it changes future queue advancement from chat/prose inference to explicit command-driven fixture mutation.

## Approved implementation direction

- Add `uv run projectkoios workflow activate <item>`.
- Mutate only `dev/workflow-nets/bootstrap-harness.queue-state.json` during command execution.
- Reconcile the baseline fixture so `petrinet-workflow-queue-state-slice-4` is completed with commit `5f209114` and no longer queued/proposed.
- Keep `pi-skill-determinism-slice-0` queued and not superseded unless USER/HERMES explicitly activates it.
- Implement activation for queued/proposed items only: move exactly one named item from `queued_items` to `active_item` with state `active` when no active item exists.
- Fail safely without writing when an active item already exists or the requested item is not queued/proposed.
- Write deterministic valid JSON and print a before/after summary with static-fixture/non-canonical authority warning.
- Include dry-run only if low-cost; otherwise document deferral.

## Watchpoints

Do not add Petri-net transition firing, runtime executor mutation, generalized persistence/database/storage, git/chat/intercom reconstruction, Operator Console integration, workflow-object runtime coupling, schema/product authority, global skill propagation, or implementation/supersession of `pi-skill-determinism-slice-0`.

## Required validation

VULCAN should run the validation set from the brief, including focused activation/queue/status tests, Python policy validation, JSON validity check, and `git diff --check`, and report any deviation explicitly.
