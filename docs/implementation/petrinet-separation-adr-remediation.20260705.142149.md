```json
{
  "title": "Petri-net separation ADR remediation",
  "artifact_type": "implementation-report",
  "status": "validated-needs-athena-conformance-review",
  "datetime": "20260705.142149",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "bootstrap-held workflow Petri-net implementation naming and runtime separation",
  "source_artifact": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "validation_status": "pass"
}
```

# Petri-net separation ADR remediation

## Summary

VULCAN remediated the workflow Petri-net implementation toward accepted ADR `docs/adr/adr.petrinet.20260705.132740Z.md`.

This implementation preserves prefixed generic Petri-net names, keeps `PetriNetArc` plus `PetriNetArcKind` for the first slice, preserves `WorkflowNet(PetriNet)` as the workflow-domain wrapper, and adds bounded in-process event collection for debugging.

## Changed files

- `src/python/projectkoios/workflow/petrinet.py`
  - Renamed `PetriNetBinding` to `PetriNetTransitionBinding`.
  - Renamed `PetriNetFiringRule` to `PetriNetFiringRequest`.
  - Renamed `PetriNetExecutionState` to `PetriNetState`.
  - Retained `PetriNetArc` and `PetriNetArcKind` under the accepted first-slice YAGNI boundary.
- `src/python/projectkoios/workflow/events.py`
  - Added `PetriNetTransitionFiredEvent`.
  - Added `PetriNetMarkingChangedEvent`.
  - Added immutable `PetriNetEventCollection` for bounded in-process event capture.
- `src/python/projectkoios/workflow/runtime.py`
  - Renamed runtime service to `PetriNetExecutor`.
  - Updated firing to return `PetriNetState` and emitted event collection through `PetriNetFiringResult`.
  - Emits transition-fired and marking-changed event DataObjects during `fire()`.
- `src/python/projectkoios/workflow/__init__.py`
  - Updated public exports for the accepted vocabulary.
- `tests/projectkoios/workflow/test__PetriNetExecutor__fire.py`
  - Updated runtime tests for `PetriNetExecutor`, `PetriNetState`, and prefixed event DataObjects.
- `docs/implementation/workflow-petri-net-executor-first-slice.20260705.102506.md`
  - Updated prior implementation vocabulary references to current accepted names.
- `docs/implementation/workflow-adapter-dependency-encapsulation.20260705.105604.md`
  - Updated current remediation summary and validation evidence.
- `docs/AAR/aar.20260705.105604_workflow-adapter-dependency-encapsulation.md`
  - Updated process capture with accepted ADR remediation notes.
- Existing dirty handoff naming refactors remain part of the current validated VULCAN batch:
  - `KoiosHandoff` replaces `HandoffArtifact`.
  - `PetriNetMarking` replaces bare `Marking` while preserving `HandoffMarking = PetriNetMarking[KoiosHandoff]`.

## Validation

- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 11 file(s)`.
- `uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`.
- `uv run pytest tests/projectkoios/workflow -q` => `9 passed in 0.03s`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/harness/data/marking.py src/python/projectkoios/bootstrap/harness/data/handoff.py src/python/projectkoios/bootstrap/harness/handoffs src/python/projectkoios/workflow tests/projectkoios/bootstrap/harness tests/projectkoios/workflow` => `summary: 0 finding(s), 39 file(s)`.
- `uv run mypy src/python/projectkoios/bootstrap/harness/data/marking.py src/python/projectkoios/bootstrap/harness/data/handoff.py src/python/projectkoios/bootstrap/harness/handoffs src/python/projectkoios/workflow tests/projectkoios/bootstrap/harness tests/projectkoios/workflow` => `Success: no issues found in 39 source files`.
- `uv run pytest tests/projectkoios/bootstrap/harness tests/projectkoios/workflow -q` => `108 passed in 0.42s`.
- `uv run pytest -q` => `224 passed in 1.16s`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 118 file(s)`.
- `graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `9848 nodes, 10742 edges, 860 communities`.

## Residual risk

- Athena conformance review remains required before this implementation is marked complete.
- Input/output arc class split remains deferred under the accepted first-slice YAGNI boundary.
- No external event bus was added; event capture is intentionally in-process only.
- Older workflow ADR/plan reconciliation is a separate documentation/control-surface follow-on and was not bundled here.
