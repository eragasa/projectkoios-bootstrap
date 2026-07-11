```json
{
  "title": "Workflow CLI domain extraction implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated",
  "datetime": "20260711",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "workflow CLI fixture services extraction"
}
```

# Workflow CLI domain extraction implementation report

## Scope

VULCAN addressed the workflow CLI layering issue where `projectkoios.cli.workflow` carried fixture loading, queue activation, status reconciliation, and Petri-net-backed reporting logic directly inside the CLI adapter.

## Changes

- Added `src/python/projectkoios/workflow/fixtures.py` as the workflow-owned fixture/service module.
- Moved workflow status fixture loading/reporting, queue fixture loading/reporting, queue activation, and status reconciliation services out of `src/python/projectkoios/cli/workflow.py`.
- Reduced `src/python/projectkoios/cli/workflow.py` to argument parsing, fixed fixture path selection, service composition, and printing.
- Updated CLI tests to import workflow services from `projectkoios.workflow.fixtures` instead of the CLI module.
- Hardened queue/activation/reconciliation tests against live queue fixture advancement by using synthetic no-active fixture state where the behavior under test requires it, and by keying completed-item assertions by item name.
- Corrected the Petri-net workflow status skill gate so `user decision required: yes` blocks workflow-state changes only, not unrelated user-delegated implementation, documentation, validation, review, or investigation work.
- Updated skill test coverage for the non-deadlocking workflow-state gate language.

## Boundary notes

- No Petri-net execution semantics were changed.
- No workflow fixture JSON was intentionally mutated by this implementation.
- No ADR, schema, role model, workflow authority, or product-domain decision was introduced.
- Skill guidance changed only agent behavior around the workflow-state gate; it does not authorize workflow mutation or transition firing.
- Queue activation remains a static fixture update service; it is now workflow-owned rather than CLI-owned.

## Validation

- `uv run pytest tests/projectkoios/cli tests/projectkoios/workflow -q` → `34 passed in 0.09s`
- `uv run mypy src/python/projectkoios/cli/workflow.py src/python/projectkoios/workflow/fixtures.py tests/projectkoios/cli tests/projectkoios/workflow` → success
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli/workflow.py src/python/projectkoios/workflow/fixtures.py tests/projectkoios/cli tests/projectkoios/workflow` → `summary: 0 finding(s), 12 file(s)`

## Result

The CLI workflow surface is now built as a thin adapter over workflow package services. The Petri-net-backed status path and the static queue/reconciliation/activation services live under `projectkoios.workflow`, so future work can evolve workflow services without adding domain logic to the CLI layer.
