```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "workflow-cli-domain-extraction-implemented-validated",
  "datetime": "20260711",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "latest_report": "docs/implementation/workflow-cli-domain-extraction.20260711.md"
}
```

# Vulcan active work

## Current priority stack

1. `workflow-cli-domain-extraction`: implemented and validated.
2. User concern addressed: CLI workflow no longer owns the workflow/Petri-net fixture services directly.
3. Skill deadlock concern addressed: `user decision required: yes` now gates workflow-state changes only, not unrelated user-delegated work.
4. Boundaries preserved: no fixture authority change, no Petri-net firing semantics change, no ADR/schema/product changes.

## Implemented changes

- Moved status fixture loading/reporting, queue fixture loading/reporting, queue activation, and status reconciliation into `src/python/projectkoios/workflow/fixtures.py`.
- Kept `src/python/projectkoios/cli/workflow.py` as the CLI adapter over workflow services.
- Updated tests to import workflow services from the workflow package.
- Removed brittle assumptions tied to the live queue fixture's current active item and completed-item order.
- Updated Petri-net workflow status skill language and tests so decision-gated workflow state does not block delegated implementation/docs/review/investigation tasks.

## Validation results

- `uv run pytest tests/projectkoios/cli tests/projectkoios/workflow -q` → `34 passed in 0.09s`
- `uv run mypy src/python/projectkoios/cli/workflow.py src/python/projectkoios/workflow/fixtures.py tests/projectkoios/cli tests/projectkoios/workflow` → success
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli/workflow.py src/python/projectkoios/workflow/fixtures.py tests/projectkoios/cli tests/projectkoios/workflow` → `summary: 0 finding(s), 12 file(s)`

## Next expected artifact

HERMES/USER review. Optional future bounded cleanup: split `projectkoios.workflow.fixtures` into more granular workflow modules once another slice needs it.
