```json
{
  "title": "Architecture conformance review: Petri-net follow-ups",
  "artifact_type": "architecture-conformance-review",
  "status": "conforms",
  "datetime": "20260705.174118",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "source_review": "docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md",
  "implementation_report": "docs/implementation/implementation-report.20260705.173808_petrinet-followups.md",
  "scope": "bounded Petri-net follow-up slice"
}
```

# Architecture conformance review 20260705.174118: Petri-net follow-ups

## Outcome

`conforms`

The bounded follow-up slice conforms to accepted ADR `docs/adr/adr.petrinet.20260705.132740Z.md` and closes the actionable follow-ups named in ATHENA review `docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md`.

## Reviewed scope

- `src/python/projectkoios/workflow/runtime.py`
- `tests/projectkoios/workflow/test__PetriNetExecutor__fire.py`
- `docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md`
- `docs/plans/projectkoios-workflow-petri-net-executor.md`
- `docs/implementation/implementation-report.20260705.173808_petrinet-followups.md`
- Controlling ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`

## Findings

| Requirement / follow-up | Finding | Status |
|---|---|---|
| `PetriNetExecutor.fire()` should use `PetriNetFiringRequest` rather than raw transition strings | `runtime.py` now imports `PetriNetFiringRequest`; `fire()` accepts `request: PetriNetFiringRequest`; implementation extracts `request.transition_id`. | conforms |
| Workflow executor tests should exercise request DataObject | `test__PetriNetExecutor__fire.py` constructs `PetriNetFiringRequest(transition_id="submit")` and passes it to `runtime.fire(state, request)`. | conforms |
| Older workflow executor draft should point current first-slice vocabulary to accepted ADR | `docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md` now has a current-control note pointing to `docs/adr/adr.petrinet.20260705.132740Z.md` and naming accepted first-slice vocabulary. | conforms |
| Older workflow implementation plan should point current first-slice vocabulary to accepted ADR | `docs/plans/projectkoios-workflow-petri-net-executor.md` now has a current-control note pointing to `docs/adr/adr.petrinet.20260705.132740Z.md` and naming accepted implementation targets. | conforms |
| Preserve older draft/plan material as provenance rather than silently rewriting broader workflow proposal | The added current-control notes preserve the old documents as provenance and explicitly scope current control to first-slice vocabulary. | conforms |
| Avoid broad workflow/product architecture expansion | Follow-up is limited to request API cleanup and control-surface notes; no external event bus, broad orchestration, adapter/backend selection, or product-domain semantics are introduced. | conforms |

## Validation performed by ATHENA

- `uv run pytest tests/projectkoios/workflow -q` => `9 passed in 0.02s`
- `uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`
- Search for raw-string executor fire calls:
  - `rg -n "\.fire\(state, \"|runtime\.fire\(state, \"|PetriNetExecutor\(\)\.fire\(.*\"" src/python tests -S || true`
  - result: no matches

VULCAN also reported broader validation in `docs/implementation/implementation-report.20260705.173808_petrinet-followups.md`, including full pytest, full policy, full mypy, and Graphify update.

## Residual risks

- Broader workflow adapter, restart, persistence, and product-domain architecture remain outside this bounded follow-up.
- Event timestamps remain runtime-generated as accepted by the prior conformance review.
- This review does not evaluate unrelated dirty ATHENA/KOIOS/root files.

## Packaging recommendation

This bounded follow-up slice may be packaged/committed with:

- the VULCAN implementation changes and report,
- this ATHENA conformance review,
- the accepted Petri-net ADR/source package if not already packaged,
- and related state/control updates,

while preserving unrelated workspace changes as separate packaging concerns.
