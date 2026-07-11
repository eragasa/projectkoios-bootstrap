```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "workflow-status-queue-overlay-hotfix-implemented-validated",
  "datetime": "20260712",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "slice_name": "workflow-status-queue-overlay-hotfix",
  "latest_report": "docs/implementation/workflow-status-queue-overlay-hotfix.20260712.md",
  "latest_aar": "docs/AAR/aar.20260712_workflow-status-queue-overlay-hotfix.md",
  "next_owner": "HERMES_USER",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

VULCAN implemented and validated the dirty read-only `workflow-status-queue-overlay-hotfix`.

## Current status

- `uv run projectkoios workflow status` preserves existing Petri-net status output.
- It now appends the queue control surface from `dev/workflow-nets/bootstrap-harness.queue-state.json`.
- Queue reporter emits a hard warning when `active_item` is set.
- No workflow mutation, activation/deactivation, schema/fixture semantics, transition logic, role model, live adapter, `docs/adr`, or `docs/schemas` changes were introduced.

## Validation

- `uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py -q` → `6 passed in 0.06s`
- `uv run mypy src/python/projectkoios/cli/workflow.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py` → success
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli/workflow.py tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/cli/test__workflow_queue.py` → `summary: 0 finding(s), 3 file(s)`
- Manual `uv run projectkoios workflow status` check showed queue overlay and next decision needed.

## Next expected owner

HERMES/USER review. Optional ATHENA follow-up can formalize workflow status/queue consistency architecture later.
