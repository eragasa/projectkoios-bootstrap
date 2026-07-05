```json
{
  "title": "Architecture conformance review: Petri-net separation ADR remediation",
  "artifact_type": "architecture-conformance-review",
  "status": "conforms-with-followups",
  "datetime": "20260705.144506",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "implementation_report": "docs/implementation/implementation-report.20260705.142149_petrinet-separation-adr-remediation.md",
  "scope": "bootstrap-held workflow Petri-net implementation naming and runtime separation"
}
```

# Architecture conformance review 20260705.144506: Petri-net separation ADR remediation

## Outcome

`conforms-with-followups`

The VULCAN remediation conforms to the accepted architecture authority in `docs/adr/adr.petrinet.20260705.132740Z.md` for the first implementation slice.

This review does not mark broader workflow/product architecture complete and does not cover the separate older workflow ADR/plan documentation-control follow-on.

## Reviewed artifacts

- Accepted ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`
- Implementation report: `docs/implementation/implementation-report.20260705.142149_petrinet-separation-adr-remediation.md`
- Source implementation surfaces:
  - `src/python/projectkoios/workflow/petrinet.py`
  - `src/python/projectkoios/workflow/runtime.py`
  - `src/python/projectkoios/workflow/events.py`
  - `src/python/projectkoios/workflow/workflownet.py`
  - `src/python/projectkoios/workflow/__init__.py`
- Workflow tests: `tests/projectkoios/workflow/`

## Conformance findings

| ADR requirement | Review finding | Status |
|---|---|---|
| Mandatory prefixed implementation names | `PetriNetPlace`, `PetriNetToken`, `PetriNetTransition`, `PetriNetArc`, `PetriNetArcKind`, `PetriNetMarking`, `PetriNetTransitionBinding`, `PetriNetFiringRequest`, `PetriNetState`, `PetriNetTransitionFiredEvent`, and `PetriNetMarkingChangedEvent` exist/export where expected. | conforms |
| `PetriNetFiringRule` superseded by `PetriNetFiringRequest` | No live workflow implementation/test reference to `PetriNetFiringRule` remains outside historical/report text. | conforms |
| `PetriNetExecutionState` superseded by `PetriNetState` | `PetriNetState` is the generic net-plus-marking state; no live workflow implementation/test reference to `PetriNetExecutionState` remains outside historical/report text. | conforms |
| `PetriNetBinding` refined to `PetriNetTransitionBinding` | Runtime enabledness and firing use `PetriNetTransitionBinding`. | conforms |
| Keep `PetriNetArc + PetriNetArcKind` under YAGNI | Implementation retains kinded arcs and does not split input/output arc classes. | conforms |
| Preserve generic `PetriNet` and workflow wrapper boundary | `WorkflowNet(PetriNet)` exists as the workflow-domain wrapper while `PetriNet` remains generic. | conforms |
| Include bounded in-process event emission for debugging | `PetriNetEventCollection`, `PetriNetTransitionFiredEvent`, and `PetriNetMarkingChangedEvent` exist; `PetriNetExecutor.fire()` returns emitted events with the new state. | conforms |
| Avoid external event bus / broad observability | Implementation uses in-process event collection only. | conforms |
| Place/Transition do not own tokens or mutate state | Token distribution remains in `PetriNetMarking`; firing returns a new `PetriNetState`. | conforms |

## Validation performed by ATHENA

- `uv run pytest tests/projectkoios/workflow -q` => `9 passed in 0.02s`
- `uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`
- Search for rejected live workflow names/patterns:
  - `PetriNetBinding`
  - `PetriNetFiringRule`
  - `PetriNetExecutionState`
  - bare `FiringRule`
  - bare `ExecutionState`
  - `place.tokens`
  - `on_update`
  - `fire_mutating_state`

  Result: no live workflow implementation/test references found; only implementation-report historical rename notes matched.

## Follow-ups / residual risks

- `PetriNetFiringRequest` exists as the accepted request DataObject, but `PetriNetExecutor.fire()` currently accepts `transition_id: str` directly. The accepted first-slice implementation brief required the rename/introduction of `PetriNetFiringRequest`; it did not strictly require executor API adoption. A later runtime API cleanup may choose to accept `PetriNetFiringRequest` directly.
- Event DataObjects include `created_at` timestamps, so event ordering and serialization shape are deterministic, but timestamp values are runtime-generated. This is acceptable for debugging in the first slice; tests should avoid relying on wall-clock equality unless a later decision requires deterministic clocks.
- Older workflow executor ADR/plan reconciliation remains a separate documentation/control-surface follow-on required by the accepted ADR.

## Decision

ATHENA accepts VULCAN's implementation evidence as conforming to the accepted Petri-net separation ADR for this bounded implementation/remediation slice.

Implementation may be packaged/committed with its implementation report and this conformance review, subject to repository dirty-state packaging rules.
