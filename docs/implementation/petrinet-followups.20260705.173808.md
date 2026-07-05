```json
{
  "title": "Petri-net ADR follow-up implementation report",
  "artifact_type": "implementation-report",
  "status": "validated",
  "datetime": "20260705.173808",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "source_review": "docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md",
  "source_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "scope": "bounded follow-ups from ATHENA conformance review"
}
```

# Implementation report 20260705.173808: Petri-net ADR follow-ups

## Summary

Implemented the actionable follow-ups from ATHENA's conformance review for the accepted Petri-net separation ADR.

## Changes

- Updated `PetriNetExecutor.fire()` to accept `PetriNetFiringRequest` directly instead of a raw `transition_id: str`.
- Updated workflow executor tests to construct and pass `PetriNetFiringRequest`.
- Added current-control notes to the older workflow executor draft ADR and implementation plan so they point to `docs/adr/adr.petrinet.20260705.132740Z.md` for first-slice vocabulary.
- Preserved older workflow draft/plan material as provenance rather than silently rewriting the original broader workflow substrate proposal.

## Files changed

- `src/python/projectkoios/workflow/runtime.py`
- `tests/projectkoios/workflow/test__PetriNetExecutor__fire.py`
- `docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md`
- `docs/plans/projectkoios-workflow-petri-net-executor.md`

## Validation

- `cd ../.. && uv run pytest tests/projectkoios/workflow -q` => `9 passed in 0.02s`.
- `cd ../.. && uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`.
- `cd ../.. && uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 11 file(s)`.
- `cd ../.. && uv run pytest -q` => `224 passed in 1.15s`.
- `cd ../.. && uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 118 file(s)`.
- `cd ../.. && uv run mypy src/python tests` => `Success: no issues found in 118 source files`.
- `cd ../.. && grep -R "runtime.fire(state, \\\"\|\\.fire(state, \\\"\|PetriNetExecutor().fire" -n src/python tests || true` => no remaining raw-string fire calls found.
- `cd ../.. && graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `9888 nodes, 10781 edges, 861 communities`.

## Residual risks

- Event timestamps remain runtime-generated as accepted by the ATHENA conformance review for this first slice.
- Broader workflow adapter, restart, persistence, and product-domain architecture remain outside this bounded follow-up.
- Concurrent dirty ATHENA/KOIOS/root files remain outside this VULCAN implementation scope.
