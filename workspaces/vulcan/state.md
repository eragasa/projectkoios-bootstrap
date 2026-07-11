```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "workflow-cli-domain-extraction-implemented-validated",
  "datetime": "20260711",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "slice_name": "workflow-cli-domain-extraction",
  "latest_report": "docs/implementation/workflow-cli-domain-extraction.20260711.md",
  "next_owner": "HERMES_USER",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

VULCAN implemented the workflow CLI layering fix requested by USER: workflow fixture loading, reporting, queue activation, and status reconciliation services now live in `projectkoios.workflow.fixtures` instead of the CLI adapter. VULCAN also corrected the Petri-net workflow status skill deadlock behavior so `user decision required: yes` gates workflow-state changes only, not unrelated user-delegated implementation, documentation, validation, review, or investigation work.

## Current status

- `src/python/projectkoios/cli/workflow.py` is now a thin argparse/service-composition adapter.
- `src/python/projectkoios/workflow/fixtures.py` owns the workflow fixture/service logic.
- CLI tests import domain services from `projectkoios.workflow.fixtures`.
- Queue/activation/reconciliation tests were hardened against live fixture advancement by using synthetic no-active copies where required and by avoiding brittle completed-item ordering assumptions.
- `src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md` now states that user-decision-required is a workflow-state gate only.
- Skill tests assert the corrected non-deadlocking gate language.

## Validation

- `uv run pytest tests/projectkoios/cli tests/projectkoios/workflow -q` → `34 passed in 0.09s`
- `uv run mypy src/python/projectkoios/cli/workflow.py src/python/projectkoios/workflow/fixtures.py tests/projectkoios/cli tests/projectkoios/workflow` → success
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli/workflow.py src/python/projectkoios/workflow/fixtures.py tests/projectkoios/cli tests/projectkoios/workflow` → `summary: 0 finding(s), 12 file(s)`

## Next expected owner

HERMES/USER review. Optional follow-up: split `projectkoios.workflow.fixtures` into narrower `status`, `queue`, and `reconciliation` modules if the workflow package keeps growing.
