```json
{
  "title": "Provenance note: Petri-net workflow queue state slice 4",
  "artifact_type": "provenance-note",
  "status": "koios-input-for-athena-hermes",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-workflow-queue-state-slice-4",
  "output_owner": "KOIOS"
}
```

# Provenance note: Petri-net workflow queue state slice 4

## Purpose

This note preserves KOIOS provenance/requirements input for `petrinet-workflow-queue-state-slice-4`.

The slice exists because recent workflow state was still being inferred from chat, workspace prose, and agent memory. That created user-visible chaos: agents could replace the active queue with new topics, confuse active work with queued work, and lose track of superseded or deferred items. The next useful improvement is a mechanical read-only queue/status surface that makes active/queued/completed/superseded/deferred state inspectable by command.

## Evidence observed

### `uv run projectkoios workflow status`

From repository root on 20260711, KOIOS ran:

```bash
uv run projectkoios workflow status
```

Observed output:

```text
workflow: bootstrap-harness.slice-0
fixture: dev/workflow-nets/bootstrap-harness.workflow-net.json

active:
  user decision required: yes
  reason: USER/HERMES approval is required before the next implementation transition.

places:
  - intake: Intake
  - user_decision: User decision
  - implementation: Implementation
  - validated: Validated

tokens:
  - current-slice at user_decision color={active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2, kind=workflow-slice, requires_user_decision=true}

enabled transitions:
  - approve_next_slice: Approve next slice

user decision required: yes
```

Validated claim: current status output is useful but insufficient for queue state. It reports one token/current slice and an enabled transition, but it does not report queued/proposed items, completed recent slices, superseded/deferred items, or the exact queue-order decision.

### Queued slice artifact

`docs/plans/queued-slice.20260711.122000_pi-skill-determinism-slice-0.md` records `pi-skill-determinism-slice-0` as `queued-not-active`, with `queue_position` after the Petri-net workflow status skill slice and an explicit `must_not_supersede` boundary. Its non-goals forbid replacing the active Petri-net workflow inspectability slice, changing Petri-net runtime/status, transition firing, persistence, cross-harness propagation, or broad ADR/process expansion.

Validated claim: the repo already needs durable distinction between queued and active work, and queued work must not silently supersede active workflow-engine work.

### Interactive-control brief and implementation evidence

`docs/plans/implementation-brief.20260711.123305_petrinet-workflow-interactive-control-skill-slice-3.md` requires agents to preserve active/queued/superseded/deferred distinctions when known, ask before active/queued-state changes, and not activate queued work without explicit USER/HERMES direction.

`docs/implementation/petrinet-workflow-interactive-control-skill-slice-3.20260711.123801.md` reports that Slice 3 implemented `inspect → summarize → recommend → ask/act`, including queue discipline and asking before active/queued-state changes. HERMES state records Slice 3 as implemented, validated, and accepted with watchpoints.

Validated claim: Slice 3 improved agent behavior, but it remains guidance/prose. It does not by itself create a machine-visible queue state.

### HERMES/ATHENA/VULCAN workspace evidence

- `workspaces/hermes/active.md` lists accepted Petri-net slices 0–3 and a queued follow-up `docs/plans/queued-slice.20260711.122000_pi-skill-determinism-slice-0.md`; it recommends mechanical workflow queue/activate controls as the next priority.
- `workspaces/hermes/state.md` states the next recommended direction is a mechanical workflow queue/activate control slice so active vs queued state becomes machine-visible rather than chat-inferred.
- `workspaces/athena/active.md` contains a queue discipline rule: do not replace current active work with new incoming topics unless USER/HERMES explicitly says to switch; always distinguish active vs queued vs superseded vs deferred.
- `workspaces/vulcan/active.md` records Slice 3 implemented/validated and preserves boundaries: no runtime/CLI behavior changes, no transition firing, no persistence, no live adapters, no Operator Console/workflow-object coupling, no global skill directories, and `pi-skill-determinism-slice-0` remains queued.

Validated claim: the role workspaces agree on the need for queue discipline, but today that discipline is distributed across prose files rather than a single command-readable queue view.

### Draft Slice 4 brief

`docs/plans/implementation-brief.20260711.124106_petrinet-workflow-queue-state-slice-4.md` already names the desired surface: a read-only queue/status command, preferably:

```bash
uv run projectkoios workflow queue
```

It requires reporting active item, queued/proposed items, completed/accepted recent slices, superseded/rejected/deferred items, exact next decision needed, fixture/source reference, and a visible static/read-only non-authority label.

## Minimum claims the queue view must support

A first read-only queue view must support at least these operator claims:

1. **Active item** — the current active item, or an explicit `none`.
2. **Queued/proposed items** — ordered future/proposed work, including dependencies/blockers and recommendations where known.
3. **Completed/accepted recent slices** — recent accepted/completed workflow slices, ideally with artifact and commit references when known.
4. **Superseded/rejected/deferred items** — items known not to be active or queued, without erasing that they occurred.
5. **Exact next decision needed** — one clear decision/action needed from USER/HERMES before state advances.
6. **Source/mode** — fixture path or source reference, plus a clear statement that the first surface is a static read-only fixture and not canonical workflow/product authority.

## Boundary requirements

For provenance safety, this slice should remain read-only first.

Do not introduce in this slice:

- transition firing, simulation, activation mutation, or queue mutation;
- persistence-as-authority beyond an explicit static fixture committed to the repo;
- generalized workflow database/storage or schema authority;
- live intercom/session reads, git-history reconstruction, or chat-log inference;
- Operator Console integration;
- workflow-object runtime coupling;
- product/mothership workflow authority;
- global skill propagation;
- replacement, activation, or supersession of `pi-skill-determinism-slice-0`.

## KOIOS assessment

The queue-state slice is provenance-safe if it is framed as mechanical inspectability over an explicit static fixture, not as workflow authority. It addresses the observed chaos directly by turning queue distinctions into command-visible state while preserving USER/HERMES control over activation and next decisions.
