```json
{
  "title": "Workflow status queue overlay durability review",
  "artifact_type": "implementation-report",
  "status": "reviewed-bounded-test-hardening-applied",
  "datetime": "20260712",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_hotfix_commit": "b13d7148 Show queue overlay in workflow status",
  "slice_name": "workflow-status-queue-overlay-hotfix-durability-review",
  "next_owner": "HERMES_USER"
}
```

# Workflow status queue overlay durability review

## Finding

The hotfix implementation is durable enough at code level, but the original regression tests had two implementation risks:

1. active-item warning was covered at reporter level, not through the `workflow status` command path;
2. some tests were brittle against live queue/status fixture changes, which could create false failures or false confidence as the queue advances.

## Bounded hardening applied

- Added a `workflow status` CLI-level test using temporary copied fixtures with `active_item` set.
- The new test asserts:
  - status output includes `queue control surface:`;
  - active item is displayed;
  - hard warning appears through the actual command path;
  - status fixture content is unchanged after command execution;
  - queue fixture content is unchanged after command execution.
- Loosened brittle assertions that assumed current fixture `active_slice=none` or no queue active item.
- Changed empty-section behavior coverage to use a synthetic fixture instead of relying on the live queue having no active item.

## Durability assessment

- `uv run projectkoios workflow status` is locked against silent token-only regression by CLI-level assertions for queue overlay output.
- Active-item warning is locked through both reporter behavior and status command behavior.
- Read-only access is now asserted by comparing fixture content before and after `workflow status` execution in a temporary fixture directory.
- Current queue fixture assertions are less brittle and focus on stable structural behavior plus current known queue item identity.
- No workflow mutation, activation/deactivation, transition logic, schema/fixture semantics, live adapter/session integration, Operator Console semantics, role model, `docs/adr`, or `docs/schemas` changes were made.

## Validation

```bash
uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py -q
```

Passed: `7 passed in 0.10s`.

```bash
uv run mypy src/python/projectkoios/cli/workflow.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py
```

Passed: `Success: no issues found in 3 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py
```

Passed: `summary: 0 finding(s), 2 file(s)`.

## Recommended next bounded action

No additional implementation slice is required for the hotfix to be durable as a read-only inspectability repair.

If HERMES/USER wants one more bounded follow-up later, make it a small mismatch-reporting slice: status should explicitly report when Petri-net `active_slice` and queue `active_item` disagree. That would still be inspectability-only and should not change activation, transition, schema, or authority semantics.
