```json
{
  "title": "Petri-net workflow activate slice 5 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated",
  "datetime": "20260711.125832Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_brief": "docs/plans/implementation-brief.20260711.124950_petrinet-workflow-activate-slice-5.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.125800_petrinet-workflow-activate-slice-5.md",
  "slice_name": "petrinet-workflow-activate-slice-5",
  "parent_effort": "Petri-net workflow harness / workflow inspectability"
}
```

# Implementation report 20260711.125832: Petri-net workflow activate slice 5

## Summary

Implemented the approved conservative activation command:

```bash
uv run projectkoios workflow activate <item>
```

The command mutates only `dev/workflow-nets/bootstrap-harness.queue-state.json`, fails safely without writing when an active item exists or the named item is not queued/proposed, writes deterministic valid JSON on success, and prints a before/after summary with static-fixture/non-canonical authority warning.

`--dry-run` was included because it was low-cost and useful for validation.

## Changed files

- `dev/workflow-nets/bootstrap-harness.queue-state.json` — reconciled baseline so Slice 4 is completed with commit `5f209114`; `pi-skill-determinism-slice-0` remains queued.
- `src/python/projectkoios/cli/workflow.py` — activation data/result object, activator, reporter, CLI registration, and `--dry-run` support.
- `tests/projectkoios/cli/test__workflow_activate.py` — focused tests for success, active-item conflict, missing item, deterministic write, and dry-run no-write behavior.
- `tests/projectkoios/cli/test__workflow_queue.py` — updated queue expectations for reconciled Slice 4 baseline.
- `docs/implementation/petrinet-workflow-activate-slice-5.20260711.125832.md` — this report.
- `docs/AAR/aar.20260711.125832_petrinet-workflow-activate-slice-5.md` — process note.
- `workspaces/vulcan/active.md` and `workspaces/vulcan/state.md` — VULCAN workspace state updates.

## Baseline reconciliation

The static queue fixture now records:

- `petrinet-workflow-queue-state-slice-4` as `accepted-committed-pushed` with commit `5f209114`;
- `pi-skill-determinism-slice-0` remains `queued`, not superseded and not implemented;
- `active_item` remains `null`;
- `next_decision_needed` now asks whether to activate `pi-skill-determinism-slice-0` or define another workflow-engine control slice.

## Activation behavior

On success, `workflow activate <item>`:

- loads the static queue fixture;
- finds exactly one matching queued/proposed item by name;
- requires `active_item` to be null;
- removes the item from `queued_items`;
- sets it as `active_item` with state `active`;
- preserves completed/recent, superseded/rejected, and deferred sections;
- updates `next_decision_needed` deterministically;
- writes pretty JSON back to the queue fixture;
- prints previous active item, activated item, remaining queued items, next decision needed, fixture path, write status, and non-canonical warning.

Safe no-write failures are implemented for active-item conflict and missing/nonqueued item.

## Boundary confirmation

This slice did not add:

- Petri-net transition firing;
- Petri-net executor/runtime mutation;
- generalized persistence/database/storage;
- writes to files other than `dev/workflow-nets/bootstrap-harness.queue-state.json` during command execution;
- git-history, chat, intercom, or workspace-prose reconstruction;
- Operator Console integration;
- workflow-object runtime coupling;
- schema authority under `docs/schemas/`;
- product/mothership workflow authority;
- global skill propagation;
- implementation or supersession of `pi-skill-determinism-slice-0`.

Tests use temporary fixture copies for mutation scenarios so pytest does not mutate the repository fixture.

## Validation results

From repository root:

```bash
uv run projectkoios workflow queue
```

Result: passed; queue output shows Slice 4 completed with commit `5f209114`, `pi-skill-determinism-slice-0` queued, active none, static/read-only caveat, and updated next decision.

```bash
uv run projectkoios workflow activate pi-skill-determinism-slice-0 --dry-run
```

Result: passed; printed activation before/after summary and `dry run: no changes written`.

```bash
uv run pytest tests/projectkoios/cli/test__workflow_activate.py tests/projectkoios/cli/test__workflow_queue.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q
```

Result: passed, `28 passed in 0.08s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow src/python/projectkoios/cli tests/projectkoios/workflow tests/projectkoios/cli
```

Result: passed, `summary: 0 finding(s), 20 file(s)`.

```bash
uv run python -m json.tool dev/workflow-nets/bootstrap-harness.queue-state.json >/dev/null
```

Result: passed.

```bash
git diff --check
```

Result: passed with no output.
