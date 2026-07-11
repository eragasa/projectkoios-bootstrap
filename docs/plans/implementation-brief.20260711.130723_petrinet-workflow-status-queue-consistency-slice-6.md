```json
{
  "title": "Petri-net workflow status queue consistency slice 6 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "draft-pending-user-hermes-review",
  "datetime": "20260711.130723Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "parent_effort": "Petri-net workflow harness / workflow inspectability",
  "previous_slice": "petrinet-workflow-activate-slice-5",
  "slice_name": "petrinet-workflow-status-queue-consistency-slice-6",
  "next_owner": "USER_HERMES"
}
```

# Implementation brief 20260711.130723: Petri-net workflow status queue consistency slice 6

## Purpose

Reconcile the Petri-net workflow status fixture with the machine-visible queue/control state introduced by Slices 4 and 5.

Current problem observed by HERMES:

- `uv run projectkoios workflow status` still reports:
  - token `current-slice` at `user_decision`;
  - `active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2`.
- `uv run projectkoios workflow queue` reports:
  - Slice 4 completed;
  - Slice 5 accepted/pushed;
  - active none;
  - `pi-skill-determinism-slice-0` queued-only.

These surfaces now disagree. This slice should make status reflect the current accepted queue/control state through an explicit static-fixture update path.

## Slice name

`petrinet-workflow-status-queue-consistency-slice-6`

## Design direction

Keep `workflow status` read-only.

Add a conservative fixture-only reconciliation command that updates only the status fixture from the queue fixture’s accepted control state.

Preferred command:

```bash
uv run projectkoios workflow reconcile-status
```

Preferred dry-run form if low-cost:

```bash
uv run projectkoios workflow reconcile-status --dry-run
```

Alternative acceptable command if VULCAN finds it cleaner:

```bash
uv run projectkoios workflow status --reconcile
```

ATHENA preference is a separate `workflow reconcile-status` command so status inspection remains clearly read-only.

## Scope

In scope:

```text
dev/workflow-nets/bootstrap-harness.workflow-net.json
dev/workflow-nets/bootstrap-harness.queue-state.json
src/python/projectkoios/cli/workflow.py
tests/projectkoios/cli/test__workflow_reconcile_status.py
tests/projectkoios/cli/test__workflow_status.py
tests/projectkoios/cli/test__workflow_queue.py
docs/implementation/<implementation-report>.md
docs/AAR/<aar-if-useful>.md
```

Command execution may write only:

```text
dev/workflow-nets/bootstrap-harness.workflow-net.json
```

It may read:

```text
dev/workflow-nets/bootstrap-harness.queue-state.json
dev/workflow-nets/bootstrap-harness.workflow-net.json
```

No other runtime, workspace, chat, git, or intercom state may be used to infer workflow state.

## Reconciliation semantics

The command should derive the status fixture’s `active_slice` from the explicit queue fixture using this precedence:

1. If `active_item` exists in `bootstrap-harness.queue-state.json`, status `active_slice` should become that active item’s `name`.
2. If `active_item` is null, status should represent no active workflow-engine item without activating queued work.

Minimum representation for no active item:

- keep token `current-slice` at `user_decision`;
- set token color `active_slice` to a clear sentinel such as `none` or `no-active-item`;
- keep `requires_user_decision=true`;
- keep decision reason aligned with queue state, e.g.:

  ```text
  USER/HERMES decision is required to activate a queued item or define the next workflow-engine control slice.
  ```

ATHENA preference: use `active_slice="none"` because the queue surface already prints `active: none` and the value is human-readable in the existing status output. If VULCAN finds an existing vocabulary convention requiring `no-active-item`, it may propose that in the plan/report.

This slice must not activate `pi-skill-determinism-slice-0` just because it is queued.

## Required command behavior

For `uv run projectkoios workflow reconcile-status`:

1. Load queue fixture and status fixture.
2. Determine expected status active-slice value from queue `active_item`:
   - active item name if present;
   - `none` when queue active item is null.
3. Update only the status fixture token color `active_slice` and, if needed, the status fixture decision reason.
4. Preserve status fixture net topology, places, transitions, arcs, token id, token place, enabled transition behavior, and `requires_user_decision=true`.
5. Write deterministic pretty JSON back to `dev/workflow-nets/bootstrap-harness.workflow-net.json` unless `--dry-run` is used.
6. Print before/after summary including:
   - queue active item;
   - previous status active_slice;
   - new status active_slice;
   - whether write occurred;
   - status fixture path;
   - queue fixture path;
   - static fixture / non-canonical authority warning;
   - next decision needed from queue fixture.

## Dry-run behavior, if included

If `--dry-run` is included:

- perform all validation and before/after rendering;
- do not write the status fixture;
- visibly print `dry run: no changes written`;
- tests must prove the status fixture content is unchanged.

Dry-run is preferred if small, following Slice 5 precedent.

## Required status behavior after reconciliation

After the fixture is reconciled and `uv run projectkoios workflow status` is run, expected output should include:

```text
current-slice at user_decision
active_slice=none
requires_user_decision=true
user decision required: yes
```

The command should no longer report:

```text
active_slice=petrinet-workflow-current-slice-status-reconciliation-slice-2
```

unless the queue fixture later explicitly sets that item as active.

## Boundaries

This slice must not add:

- Petri-net transition firing;
- Petri-net executor/runtime mutation;
- activation of queued items;
- implementation or supersession of `pi-skill-determinism-slice-0`;
- generalized persistence/database/storage;
- writes to queue fixture during reconciliation;
- writes to any file other than the status fixture during command execution;
- git-history, chat, intercom, or workspace-prose reconstruction;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority under `docs/schemas/`;
- product/mothership workflow authority;
- global skill propagation.

This is a fixture consistency slice, not a runtime execution slice.

## Acceptance criteria

1. A reconciliation command exists, preferably:

   ```bash
   uv run projectkoios workflow reconcile-status
   ```

2. `workflow status` remains read-only.
3. Reconciliation reads queue fixture and status fixture only.
4. Reconciliation writes only `dev/workflow-nets/bootstrap-harness.workflow-net.json`.
5. When queue `active_item` is null, status fixture `active_slice` becomes `none` or an approved equivalent sentinel.
6. Queued `pi-skill-determinism-slice-0` remains queued and is not activated, implemented, or superseded.
7. Status fixture topology, token place, enabled transition behavior, and user-decision requirement remain unchanged.
8. Command prints before/after summary and non-canonical static-fixture warning.
9. Dry-run is included or explicitly deferred with rationale.
10. Tests cover successful reconciliation, dry-run/no-write if implemented, no queue write, and status output after reconciliation.
11. No Petri-net runtime firing/mutation, queue activation, persistence/database, git/chat/intercom reconstruction, Operator Console, workflow-object coupling, schema/product authority, or global skill propagation is introduced.

## Suggested validation

From repository root:

```bash
uv run projectkoios workflow queue
uv run projectkoios workflow reconcile-status --dry-run
uv run projectkoios workflow status
uv run pytest tests/projectkoios/cli/test__workflow_reconcile_status.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py tests/projectkoios/workflow -q
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow src/python/projectkoios/cli tests/projectkoios/workflow tests/projectkoios/cli
uv run python -m json.tool dev/workflow-nets/bootstrap-harness.workflow-net.json >/dev/null
uv run python -m json.tool dev/workflow-nets/bootstrap-harness.queue-state.json >/dev/null
git diff --check
```

If tests use temporary fixture copies to avoid mutating repo fixtures during pytest, VULCAN should document that in the implementation report.

## Pause triggers

Pause and ask USER/HERMES if implementation would require:

- activating or modifying `pi-skill-determinism-slice-0`;
- changing queue fixture content from the reconciliation command;
- firing or simulating Petri-net transitions;
- changing Petri-net executor/runtime semantics;
- changing status fixture topology or token place;
- writing any file other than the status fixture during command execution;
- deriving state from git, chat, intercom, or workspace prose;
- adding persistence/database/storage abstractions;
- Operator Console or workflow-object integration;
- schema/product authority;
- global skill propagation.

## Handoff

This is a brief only. Pause for USER/HERMES review before routing to VULCAN planning or implementation.
