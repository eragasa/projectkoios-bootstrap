```json
{
  "title": "Petri-net workflow activate slice 5 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-user-hermes-review",
  "datetime": "20260711.124950Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "Petri-net workflow harness / workflow inspectability",
  "previous_slice": "petrinet-workflow-queue-state-slice-4",
  "slice_name": "petrinet-workflow-activate-slice-5",
  "next_owner": "USER_HERMES"
}
```

# Implementation brief 20260711.124950: Petri-net workflow activate slice 5

## Purpose

Add the first explicit mechanical queue/activation control for the Petri-net workflow harness.

Slice 4 made workflow queue state visible through the static fixture-backed command:

```bash
uv run projectkoios workflow queue
```

Slice 5 should add a conservative mutation command that updates only the static queue fixture, by explicit command invocation, with deterministic JSON output and a clear before/after summary.

This remains part of the existing Petri-net workflow harness / workflow inspectability effort. It is not Petri-net runtime firing, not product workflow authority, and not a general workflow database.

## Current observed problem

HERMES observed that `uv run projectkoios workflow queue` now reports stale Slice 4 queue state:

- active: none;
- queued/proposed: `petrinet-workflow-queue-state-slice-4`, then `pi-skill-determinism-slice-0`;
- next decision still says review/accept Slice 4;
- but Slice 4 is now accepted/pushed as commit `5f209114`.

This proves the need for a controlled queue fixture update path.

## Slice name

`petrinet-workflow-activate-slice-5`

## Command surface

Preferred command:

```bash
uv run projectkoios workflow activate <item>
```

Recommended optional flag if low-cost:

```bash
uv run projectkoios workflow activate <item> --dry-run
```

If `--dry-run` would materially expand implementation complexity, defer dry-run and keep Slice 5 to one explicit mutation command plus tests.

## Required design decision: stale Slice 4 reconciliation

Slice 5 SHOULD include a deliberately narrow reconciliation behavior for the stale Slice 4 fixture state as part of the activation/update command surface, rather than creating another separate read-only reconciliation slice.

Rationale:

- the stale Slice 4 state is precisely the pressure that motivates activation/update mechanics;
- another manual fixture edit would postpone the mechanical-control goal;
- the command can make the state transition explicit and testable.

Minimum acceptable approach:

- `workflow activate <item>` may operate only on items already listed in `queued_items`;
- when activating an item, it removes that item from `queued_items`, writes it to `active_item`, and updates `next_decision_needed` deterministically;
- for already-completed stale items like `petrinet-workflow-queue-state-slice-4`, VULCAN may either:
  1. use a separate explicitly named command/subcommand such as `workflow activate <item> --complete-current --commit 5f209114` only if this stays small; or
  2. keep completion reconciliation manual in the fixture for Slice 5 setup and implement activation for the next queued item only.

ATHENA preference: keep Slice 5 smaller by implementing activation only, and in the same implementation update the static fixture initial state to reflect Slice 4 as completed (`5f209114`) so the command can be tested against a non-stale queue. Do not add completion mutation unless HERMES/USER explicitly requests it.

## Scope

In scope:

```text
dev/workflow-nets/bootstrap-harness.queue-state.json
src/python/projectkoios/cli/workflow.py
tests/projectkoios/cli/test__workflow_activate.py
tests/projectkoios/cli/test__workflow_queue.py
docs/implementation/<implementation-report>.md
docs/AAR/<aar-if-useful>.md
workspaces/vulcan/state.md and workspaces/vulcan/active.md if VULCAN implements
```

The command must write only:

```text
dev/workflow-nets/bootstrap-harness.queue-state.json
```

No other persistent workflow-state write is authorized.

## Initial fixture reconciliation requirement

Before or as part of implementation, the fixture should be brought to a sane baseline:

- move `petrinet-workflow-queue-state-slice-4` from `queued_items` to `completed_items` with commit `5f209114`;
- keep `pi-skill-determinism-slice-0` queued and not superseded;
- set `active_item` to null unless USER/HERMES names a concrete active next item before implementation;
- update `next_decision_needed` to indicate the next activation decision, not Slice 4 review.

This baseline update is allowed because it is direct reconciliation of the Slice 4 accepted/pushed state and prepares the static fixture for the activation command. It must be recorded in the implementation report.

## Activation behavior

For `uv run projectkoios workflow activate <item>`:

1. Load `dev/workflow-nets/bootstrap-harness.queue-state.json`.
2. Find exactly one queued/proposed item by `name`.
3. If `active_item` is not null, fail safely with a clear message and do not write.
4. If the named item is not found in `queued_items`, fail safely with a clear message and do not write.
5. Remove the item from `queued_items`.
6. Set `active_item` to the selected item with state updated to `active`.
7. Preserve completed/recent, superseded/rejected, and deferred sections unchanged.
8. Update `next_decision_needed` deterministically, e.g.:

   ```text
   Complete or review active item <item>; do not activate another item until active_item is cleared.
   ```

9. Write deterministic pretty JSON back to the fixture.
10. Print before/after summary including:
    - previous active item;
    - activated item;
    - remaining queued items;
    - next decision needed;
    - fixture path;
    - static fixture / non-canonical authority warning.

## Dry-run behavior, if included

If `--dry-run` is included:

- perform all validation and before/after rendering;
- do not write the fixture;
- visibly print `dry run: no changes written`;
- tests must prove the fixture content is unchanged.

Dry-run is preferred if small, but not required for acceptance if VULCAN justifies deferral.

## Boundaries

This slice must not add:

- Petri-net transition firing;
- Petri-net executor/runtime mutation;
- generalized persistence/database/storage;
- writes to any file other than `dev/workflow-nets/bootstrap-harness.queue-state.json` for command execution;
- git-history, chat, intercom, or workspace-prose reconstruction;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority under `docs/schemas/`;
- product/mothership workflow authority;
- global skill propagation;
- implementation or supersession of `pi-skill-determinism-slice-0`.

This is the first mutation slice, so implementation must be conservative and narrow.

## Acceptance criteria

1. `uv run projectkoios workflow activate <item>` exists.
2. The command operates only on the static queue fixture.
3. The command fails without writing if an active item already exists.
4. The command fails without writing if the requested item is not queued/proposed.
5. On success, the requested item moves from `queued_items` to `active_item` with state `active`.
6. Completed/recent, superseded/rejected, and deferred sections are preserved.
7. JSON output is deterministic and valid.
8. The command prints a before/after summary and exact next decision needed.
9. The fixture is reconciled so Slice 4 is completed with commit `5f209114`, not still queued/proposed.
10. `pi-skill-determinism-slice-0` remains queued and not superseded unless explicitly activated by USER/HERMES.
11. Tests cover success, active-item conflict, missing item, deterministic fixture write, and optional dry-run if implemented.
12. No Petri-net runtime firing/mutation, persistence/database, git/chat/intercom reconstruction, Operator Console, workflow-object coupling, schema/product authority, or global skill propagation is introduced.

## Suggested validation

From repository root:

```bash
uv run projectkoios workflow queue
uv run pytest tests/projectkoios/cli/test__workflow_activate.py tests/projectkoios/cli/test__workflow_queue.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow src/python/projectkoios/cli tests/projectkoios/workflow tests/projectkoios/cli
uv run python -m json.tool dev/workflow-nets/bootstrap-harness.queue-state.json >/dev/null
git diff --check
```

If tests use temporary fixture copies to avoid mutating the repo fixture during pytest, VULCAN should document that in the implementation report.

## Pause triggers

Pause and ask USER/HERMES if implementation would require:

- activating an item not already present in `queued_items`;
- clearing or completing an active item;
- changing completed/superseded/deferred semantics beyond preserving them;
- writing any file other than the queue fixture during command execution;
- Petri-net transition firing or runtime mutation;
- persistence/database/storage abstractions;
- deriving state from git, chat, intercom, or workspace prose;
- Operator Console or workflow-object integration;
- schema/product authority;
- global skill propagation;
- implementing or superseding `pi-skill-determinism-slice-0`.

## Handoff

This is a brief only. Pause for USER/HERMES review before routing to VULCAN planning or implementation.
