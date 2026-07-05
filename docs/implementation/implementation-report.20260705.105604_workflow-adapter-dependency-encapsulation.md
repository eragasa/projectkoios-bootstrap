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

Review follow-up split the reusable Petri-net substrate from the workflow-specific net: generic behavior now lives in `petrinet.py`/`PetriNet`, while `workflownet.py` provides `WorkflowNet(PetriNet)` for workflow-domain specialization and later Petri-net extraction. Athena/user follow-ups also renamed bare `Marking` to `PetriNetMarking`, generic primitives to `PetriNetPlace`, `PetriNetTransition`, `PetriNetArc`, `PetriNetToken`, `PetriNetTransitionBinding`, and related names, and the handoff token DataObject from `HandoffArtifact` to `KoiosHandoff` while preserving `HandoffMarking = PetriNetMarking[KoiosHandoff]`.

## Changed files

- `src/python/projectkoios/workflow/petrinet.py`
  - Exports reusable canonical `PetriNet`, `PetriNetMarking`, and consistently prefixed generic Petri-net primitives for future extraction.
- `src/python/projectkoios/workflow/workflownet.py`
  - Adds `WorkflowNet(PetriNet)` and workflow semantic wrapper DataObjects.
- `src/python/projectkoios/bootstrap/harness/data/handoff.py`
  - Renames the domain handoff token DataObject to `KoiosHandoff`.
- `src/python/projectkoios/bootstrap/harness/data/marking.py`
  - Renames the generic handoff marking DataObject to `PetriNetMarking` and preserves `HandoffMarking = PetriNetMarking[KoiosHandoff]`.
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
- `tests/projectkoios/workflow/test__WorkflowNet__inherits_petrinet.py`
  - Added inheritance coverage proving `WorkflowNet` reuses `PetriNet` behavior.

## Validation

- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/harness/data/marking.py src/python/projectkoios/bootstrap/harness/data/handoff.py src/python/projectkoios/bootstrap/harness/handoffs src/python/projectkoios/workflow tests/projectkoios/bootstrap/harness tests/projectkoios/workflow` => `summary: 0 finding(s), 39 file(s)`.
- `uv run mypy src/python/projectkoios/bootstrap/harness/data/marking.py src/python/projectkoios/bootstrap/harness/data/handoff.py src/python/projectkoios/bootstrap/harness/handoffs src/python/projectkoios/workflow tests/projectkoios/bootstrap/harness tests/projectkoios/workflow` => `Success: no issues found in 39 source files`.
- `uv run pytest tests/projectkoios/bootstrap/harness tests/projectkoios/workflow -q` => `108 passed in 0.46s`.
- `uv run pytest -q` => `224 passed in 1.18s`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 118 file(s)`.
- `graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `9729 nodes, 10622 edges, 851 communities`.

## Residual risk

- This slice still does not implement concrete SNAKES or PM4Py object conversion.
- Optional dependencies are not added to `pyproject.toml`; callers must install them explicitly before using `backend_module()`.
- Full handoff/evaluator migration to `projectkoios.workflow` remains deferred.
