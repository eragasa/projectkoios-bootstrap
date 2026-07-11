```json
{
  "title": "Provenance note: Petri-net workflow status/queue consistency slice",
  "artifact_type": "provenance-note",
  "status": "koios-input-for-athena-hermes",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-workflow-status-queue-consistency",
  "output_owner": "KOIOS"
}
```

# Provenance note: Petri-net workflow status/queue consistency slice

## Purpose

This note preserves KOIOS provenance/requirements input for the next bounded workflow-engine slice: reconciling `workflow status` with `workflow queue` after accepted queue/activation work.

The gap exists because the project now has two mechanical workflow views with different fixture sources. `workflow queue` has advanced through Slice 4 and Slice 5 work, while `workflow status` still exposes the older Slice 2 token state. This creates the same operator confusion the workflow-engine effort is meant to reduce: agents can see one command saying there is an active Slice 2 user-decision token while another command says there is no active item and only `pi-skill-determinism-slice-0` is queued.

## Observed evidence

KOIOS ran from repository root on 20260711:

```bash
uv run projectkoios workflow status
uv run projectkoios workflow queue
```

Observed `workflow status` evidence:

```text
workflow: bootstrap-harness.slice-0
fixture: dev/workflow-nets/bootstrap-harness.workflow-net.json
active:
  user decision required: yes
...
tokens:
  - current-slice at user_decision color={active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2, kind=workflow-slice, requires_user_decision=true}
enabled transitions:
  - approve_next_slice: Approve next slice
user decision required: yes
```

`dev/workflow-nets/bootstrap-harness.workflow-net.json` confirms the marking still carries:

```json
"active_slice": "petrinet-workflow-current-slice-status-reconciliation-slice-2"
```

Observed `workflow queue` evidence:

```text
active:
  none

queued/proposed:
  1. pi-skill-determinism-slice-0 state=queued
...
completed/recent:
  - petrinet-workflow-queue-state-slice-4 state=accepted-committed-pushed commit=5f209114
...
next decision needed:
  Choose whether to activate pi-skill-determinism-slice-0 or define another workflow-engine control slice; do not implement queued work without explicit USER/HERMES activation.
```

`dev/workflow-nets/bootstrap-harness.queue-state.json` confirms `active_item` is `null`, `pi-skill-determinism-slice-0` remains queued, and Slice 4 is completed at `5f209114`.

HERMES state records Slice 5 as implemented, independently validated, and accepted with watchpoints, and local git history shows `d2739ef1 Add Petri net workflow activation command` after `5f209114 Add Petri net workflow queue view`.

Validated claim: queue/activation state has advanced, but the status fixture still represents an older user-decision token for Slice 2. A bounded consistency slice is warranted to prevent stale status output from acting as misleading workflow state.

## Minimum safe mutation claims

A first status/queue consistency slice should be narrow and fixture-oriented:

1. **Explicit consistency update only** — reconcile status output to the currently accepted queue/activation baseline; do not infer state from chat or agent memory.
2. **Deterministic static fixture edits** — if mutation is needed, it should be limited to the explicit static workflow fixtures required for consistency, likely `dev/workflow-nets/bootstrap-harness.workflow-net.json` and focused tests/docs for the status output. If queue fixture metadata needs a Slice 5 completed entry, that should be explicit and reviewed, not implicit.
3. **Queue state remains controlling for queue distinctions** — preserve `active_item: null`, `pi-skill-determinism-slice-0` as queued-only, completed Slice 4 provenance, and superseded/rejected history.
4. **Status output should not claim an obsolete active slice** — `workflow status` should not continue to report `petrinet-workflow-current-slice-status-reconciliation-slice-2` as active when the queue view has no active item.
5. **Visible before/after evidence** — implementation should show before/after `workflow status` and `workflow queue` output so HERMES/USER can see consistency restored.
6. **No implicit activation** — consistency reconciliation must not activate `pi-skill-determinism-slice-0`; it remains queued unless USER/HERMES explicitly activates it through the approved path.
7. **Preserve provenance** — completed, queued, superseded/rejected, and deferred items should remain visible; do not erase stale Slice 2 evidence without retaining artifact references in reports/tests where relevant.

## Boundary requirements and watchpoints

This slice should not introduce or authorize:

- Petri-net runtime firing, executor mutation, or token-transition semantics beyond static fixture reconciliation;
- general persistence/database/storage;
- git-history, chat-log, intercom, or workspace-prose reconstruction as state authority;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority or product/mothership workflow authority;
- global skill propagation;
- activation, implementation, or supersession of `pi-skill-determinism-slice-0`;
- broad workflow redesign beyond making the existing status and queue inspectability surfaces consistent.

## KOIOS assessment

The consistency slice is provenance-safe if it is framed as a bounded static-fixture reconciliation with visible command evidence. The target should be operator clarity: `workflow status` and `workflow queue` must no longer tell contradictory stories about whether an active slice exists. The slice should preserve the queue discipline established by Slices 4–5 and avoid converting fixture reconciliation into runtime firing, durable persistence, or product workflow authority.
