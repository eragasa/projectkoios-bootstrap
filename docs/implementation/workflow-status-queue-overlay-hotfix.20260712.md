```json
{
  "title": "Workflow status queue overlay hotfix implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated",
  "datetime": "20260712",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "slice_name": "workflow-status-queue-overlay-hotfix",
  "authority_mode": "dirty-read-only-inspectability-repair",
  "athena_guidance": "intercom guidance: bounded dirty inspectability patch",
  "next_owner": "HERMES_USER"
}
```

# Implementation report: Workflow status queue overlay hotfix

## Summary

Implemented a dirty, bounded, read-only inspectability hotfix so:

```bash
uv run projectkoios workflow status
```

now renders the existing queue control surface alongside Petri-net token status.

This prevents operators from seeing only `user_decision` / `approve_next_slice` while missing queue state such as `active_item`, queued/proposed items, and `next_decision_needed`.

## Changes

- `workflow status` now loads `dev/workflow-nets/bootstrap-harness.queue-state.json` read-only and prints it as a `queue control surface` section after existing status output.
- `WorkflowQueueStateReporter` now prints a hard warning when `active_item` is set:

```text
WARNING: queue active_item is set; do not recommend or activate queued items until active item is cleared/accepted/rejected by HERMES/USER.
```

- Added regression coverage for:
  - status output including the queue control surface;
  - no warning when `active_item` is absent;
  - warning when `active_item` is present;
  - current queue fixture state after Slice 11 packaging.

## Boundaries

This hotfix is display-only:

- no workflow mutation;
- no queue activation/deactivation;
- no new persistence semantics;
- no schema or fixture format changes;
- no transition logic changes;
- no role permission model changes;
- no Operator Console/live adapter/session integration;
- no claim that the Petri-net token alone is complete workflow truth;
- no `docs/adr` or `docs/schemas` edits.

## Validation

From repository root:

```bash
uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py -q
```

Passed: `6 passed in 0.06s`.

```bash
uv run mypy src/python/projectkoios/cli/workflow.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py
```

Passed: `Success: no issues found in 3 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli/workflow.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py
```

Passed: `summary: 0 finding(s), 3 file(s)`.

Manual command check:

```bash
uv run projectkoios workflow status
```

Observed queue overlay includes `queued/proposed`, `completed/recent`, and `next decision needed` from the queue fixture.

## Follow-up

ATHENA should later decide whether a formal workflow status/queue consistency architecture or implementation brief is needed. This patch is intentionally a hotfix for operator safety.
