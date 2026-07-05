```json
{
  "title": "Workflow adapter dependency encapsulation",
  "artifact_type": "implementation-report",
  "status": "validated",
  "datetime": "20260705.105604",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "src/python/projectkoios/workflow/adapters.py and workflow adapter tests",
  "source_artifact": "user follow-up after workflow first slice",
  "validation_status": "pass"
}
```

# Workflow adapter dependency encapsulation

## Summary

VULCAN strengthened the workflow adapter boundary so optional SNAKES and PM4Py dependencies are encapsulated behind lazy adapter methods while core workflow petrinet/runtime imports remain dependency-free. The adapter-neutral net representation now uses explicit PetriNet payload DataObjects plus a `PetriNetPayloadBuilder` ActionObject instead of a free helper function returning an untyped dictionary.

Review follow-up renamed the canonical Petri-net module and class from `model.py`/`WorkflowNet` to `petrinet.py`/`PetriNet`.

## Changed files

- `src/python/projectkoios/workflow/petrinet.py`
  - Renamed from `model.py` and now exports canonical `PetriNet` instead of `WorkflowNet`.
- `src/python/projectkoios/workflow/adapters.py`
  - Added `AdapterUnavailableError` for clear optional dependency failures.
  - Added deterministic library-neutral payload DataObjects: `PetriNetPlacePayload`, `PetriNetTransitionPayload`, `PetriNetArcPayload`, and `PetriNetPayload`.
  - Added `PetriNetPayloadBuilder` as the ActionObject that converts canonical `PetriNet` objects into payload DataObjects.
  - Updated SNAKES and PM4Py adapters to expose typed payload exports without requiring external libraries.
  - Added lazy `backend_module()` loading methods for optional backend access.
- `src/python/projectkoios/workflow/__init__.py`
  - Exported the adapter error, payload DataObjects, and payload builder ActionObject.
- `tests/projectkoios/workflow/test__WorkflowAdapters__encapsulate_dependencies.py`
  - Added tests for library-neutral payload DataObject construction and adapter export payloads.
  - Added tests for lazy backend loading and clear unavailable dependency errors.

## Validation

- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 9 file(s)`.
- `uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 9 source files`.
- `uv run pytest tests/projectkoios/workflow -q` => `8 passed in 0.02s`.
- `uv run pytest -q` => `223 passed in 1.20s`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 116 file(s)`.
- `graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `9720 nodes, 10563 edges, 860 communities`.

## Residual risk

- This slice still does not implement concrete SNAKES or PM4Py object conversion.
- Optional dependencies are not added to `pyproject.toml`; callers must install them explicitly before using `backend_module()`.
- Full handoff/evaluator migration to `projectkoios.workflow` remains deferred.
