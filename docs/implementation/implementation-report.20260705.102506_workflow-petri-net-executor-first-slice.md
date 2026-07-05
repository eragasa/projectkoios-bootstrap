```json
{
  "title": "Workflow Petri-net executor first slice",
  "artifact_type": "implementation-report",
  "status": "validated-partial-slice",
  "datetime": "20260705.102506",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "src/python/projectkoios/workflow and tests/projectkoios/workflow",
  "source_artifact": "docs/plans/projectkoios-workflow-petri-net-executor.md",
  "source_adr": "docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md",
  "validation_status": "pass"
}
```

# Workflow Petri-net executor first slice

## Summary

VULCAN implemented the first bounded slice of the workflow-compatible Petri-net executor despite the controlling ADR remaining in draft, per explicit user selection.

This slice creates the canonical `projectkoios.workflow` package boundary and validates a minimal executable substrate. It does not complete the full migration or third-party adapter implementations from the larger plan.

## Changed files

- `src/python/projectkoios/workflow/__init__.py`
  - Exports the canonical workflow API.
- `src/python/projectkoios/workflow/petrinet.py`
  - Adds `PetriNetPlace`, `PetriNetTransition`, `PetriNetToken`, `PetriNetArc`, `PetriNetMarking`, `PetriNet`, `PetriNetTransitionBinding`, `PetriNetFiringRequest`, `PetriNetSchema`, `PetriNetState`, and semantic wrapper types.
- `src/python/projectkoios/workflow/runtime.py`
  - Adds `PetriNetExecutor` enabled-binding and transition-firing behavior.
- `src/python/projectkoios/workflow/validation.py`
  - Adds workflow net validation and validation errors.
- `src/python/projectkoios/workflow/events.py`
  - Adds event, trace, and event-log inspection types.
- `src/python/projectkoios/workflow/adapters.py`
  - Adds SNAKES and PM4Py adapter-boundary placeholders without third-party imports.
- `tests/projectkoios/workflow/test__PetriNetExecutor__fire.py`
  - Covers enabled transition firing, marking movement, trace emission, and guard filtering.
- `tests/projectkoios/workflow/test__WorkflowValidator__validate.py`
  - Covers endpoint validation and adapter import-boundary enforcement.

## Validation

- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 8 file(s)`.
- `uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 8 source files`.
- `uv run pytest tests/projectkoios/workflow -q` => `4 passed in 0.01s`.
- `uv run pytest -q` => `219 passed in 1.19s`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 115 file(s)`.

## Residual risk and deferred work

- The source ADR is still draft; this implementation is user-authorized but should not be treated as accepted architecture authority.
- This is a first executable substrate slice, not the full plan completion.
- Existing handoff/evaluator code has not yet been migrated or wrapped under `projectkoios.workflow`.
- SNAKES and PM4Py integrations are adapter-boundary placeholders only; no third-party adapter behavior is implemented.
- Restart/checkpoint persistence hooks are limited to immutable execution state and event trace inspection; durable restart persistence remains deferred.
