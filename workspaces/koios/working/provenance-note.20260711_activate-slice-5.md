```json
{
  "title": "Provenance note: Petri-net workflow activate slice 5",
  "artifact_type": "provenance-note",
  "status": "koios-input-for-athena-hermes",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-workflow-activate-slice-5",
  "output_owner": "KOIOS"
}
```

# Provenance note: Petri-net workflow activate slice 5

## Purpose

This note preserves KOIOS provenance/requirements input for `petrinet-workflow-activate-slice-5`.

The activation/update control exists because Slice 4 made queue state visible but did not give the harness a controlled way to reconcile that state after acceptance. The current queue fixture can expose stale state: after USER said `go` and Slice 4 was accepted/committed/pushed as `5f209114 Add Petri net workflow queue view`, `uv run projectkoios workflow queue` still reports `petrinet-workflow-queue-state-slice-4` as `proposed-next` and asks to review/accept/revise Slice 4.

Validated claim: static queue inspectability is useful but insufficient. Without an explicit mechanical update/activation command, agents can fall back to chat-inferred activation and manual prose reconciliation, which is the chaos this workflow effort is trying to eliminate.

## Evidence observed

### Slice 4 implementation and commit

`docs/implementation/petrinet-workflow-queue-state-slice-4.20260711.124549.md` reports that Slice 4 implemented:

```bash
uv run projectkoios workflow queue
```

The command loads `dev/workflow-nets/bootstrap-harness.queue-state.json` and prints active, queued/proposed, completed/recent, superseded/rejected, deferred, and next-decision-needed sections. The report confirms no activation or queue mutation command was added.

Local git history confirms latest relevant commit:

```text
5f209114 Add Petri net workflow queue view
```

### Current queue fixture/output

`dev/workflow-nets/bootstrap-harness.queue-state.json` currently has:

- `active_item: null`;
- first queued/proposed item: `petrinet-workflow-queue-state-slice-4` with `state: proposed-next`;
- second queued item: `pi-skill-determinism-slice-0` with `state: queued`;
- completed items through Slice 3 and the VULCAN state fix;
- next decision: review/accept/revise Slice 4.

On 20260711, KOIOS ran:

```bash
uv run projectkoios workflow queue
```

Observed output still reports:

```text
active:
  none

queued/proposed:
  1. petrinet-workflow-queue-state-slice-4 state=proposed-next
...
next decision needed:
  Review and accept or revise petrinet-workflow-queue-state-slice-4; do not activate or implement pi-skill-determinism-slice-0 unless USER/HERMES explicitly switches priority.
```

Validated claim: the view is now stale relative to HERMES/USER state because Slice 4 has been accepted/pushed, but the explicit fixture has not advanced.

### HERMES state

`workspaces/hermes/state.md` records that Slice 4 is implemented, validated, accepted by HERMES with watchpoints, and that the next recommended direction is a bounded activation/transition-control slice so queue state can advance through explicit commands rather than chat inference.

`workspaces/hermes/active.md` records accepted Slice 4 artifacts and says the next workflow-engine activation/control slice should be queued/briefed without replacing existing queued work.

Validated claim: HERMES has already identified this as the next workflow-engine control gap, but KOIOS should preserve the provenance boundary: this is controlled fixture update/activation, not broad runtime authority.

## Minimum safe mutation claims

A first activation/update slice should support only these mutation claims:

1. **Explicit command invocation only** — state changes happen only when an operator/agent runs a named command, not because a chat message, intercom message, or workspace prose implies activation.
2. **Narrow deterministic target** — update only `dev/workflow-nets/bootstrap-harness.queue-state.json` for this slice.
3. **Deterministic update semantics** — the command should move/update known fixture entries in a predictable way, e.g. mark the accepted Slice 4 as completed/accepted with commit `5f209114`, remove it from proposed-next, preserve `pi-skill-determinism-slice-0` as queued, and set the next decision toward Slice 5 review/approval.
4. **Before/after visible summary** — command output should show what changed before and after, including active, queued/proposed, completed/recent, superseded/rejected, deferred, and next decision where affected.
5. **No implicit activation from chat/intercom** — USER/HERMES `go` is authority to proceed, but the repository state changes only through the explicit command/edit performed under the approved slice.
6. **Preserve provenance** — completed, queued, superseded, rejected, and deferred items must not be erased. Mutation should add/reclassify with source artifact/commit refs rather than dropping history.
7. **Auditable fixture edit** — the resulting JSON should remain small, readable, and reviewable by `git diff` and `uv run python -m json.tool`.

## Boundary requirements

For provenance safety, Slice 5 should not introduce:

- Petri-net runtime transition firing or token execution semantics;
- a general persistence/database layer;
- git-history-derived, chat-log-derived, or intercom-derived state reconstruction;
- live adapter/session reads;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority under `docs/schemas/`;
- product/mothership workflow authority;
- global skill propagation;
- replacement, supersession, or implementation of `pi-skill-determinism-slice-0`.

## KOIOS assessment

The activation slice is provenance-safe if it is framed as a narrow, explicit, command-driven fixture update mechanism for the existing queue-state file. It should close the observed Slice 4 stale-state gap without claiming Petri-net runtime firing, durable workflow database authority, or product workflow authority.
