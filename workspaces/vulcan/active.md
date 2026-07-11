```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "workflow-status-queue-overlay-hotfix-implemented-validated",
  "datetime": "20260712",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "src/python/projectkoios/cli/workflow.py",
    "tests/projectkoios/cli/test__workflow_status.py",
    "tests/projectkoios/cli/test__workflow_queue.py",
    "docs/implementation/workflow-status-queue-overlay-hotfix.20260712.md",
    "docs/AAR/aar.20260712_workflow-status-queue-overlay-hotfix.md"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": null,
  "latest_report": "docs/implementation/workflow-status-queue-overlay-hotfix.20260712.md",
  "latest_aar": "docs/AAR/aar.20260712_workflow-status-queue-overlay-hotfix.md"
}
```

# Vulcan active work

## Current priority stack

1. `workflow-status-queue-overlay-hotfix`: implemented and validated.
2. Parent issue: Petri-net workflow status hid queue control-surface state and misled HERMES/operator.
3. Boundaries preserved: read-only display only; no workflow mutation; no activation/deactivation; no new persistence/schema semantics; no transition logic changes; no role permission model; no Operator Console/live adapter/session integration; no `docs/adr` or `docs/schemas` edits.

## Implemented outputs

- `uv run projectkoios workflow status` now prints queue control surface state after existing Petri-net status output.
- Queue overlay includes active item, queued/proposed items, completed/recent items, deferred/superseded sections, and next decision needed.
- Hard warning is rendered when queue `active_item` is set.
- Focused tests cover queue overlay in status output and active-item warning behavior.

## Validation results

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

Manual `uv run projectkoios workflow status` check showed queue overlay and next decision needed.

## Next expected artifact

- HERMES/USER review of hotfix.
- Optional ATHENA follow-up for formal workflow status/queue consistency architecture.
