```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "petrinet-separation-adr-remediation-validated",
  "datetime": "20260705.142149",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "docs/implementation/implementation-report.20260705.142149_petrinet-separation-adr-remediation.md",
    "docs/AAR/aar.20260705.142149_petrinet-separation-adr-remediation.md"
  ],
  "scratch_directory": "scratch/",
  "controlling_adr": "docs/adr/adr.petrinet.20260705.132740Z.md"
}
```

# Vulcan active work

## Current priority stack

1. Await ATHENA conformance review or user packaging direction for the Petri-net separation ADR remediation.
2. Package current VULCAN-only Petri-net/handoff naming and runtime remediation files for commit/push only if directed.
3. Avoid staging concurrent ATHENA/KOIOS workspace files, accepted ADR source files, or unrelated `dev/` content unless explicitly instructed.

## Latest working material

- Controlling ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`.
- Latest report: `docs/implementation/implementation-report.20260705.142149_petrinet-separation-adr-remediation.md`.
- Latest AAR: `docs/AAR/aar.20260705.142149_petrinet-separation-adr-remediation.md`.
- Latest all-target policy baseline: `0 finding(s), 118 file(s)`.

## Latest validation evidence

- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 11 file(s)`.
- `uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`.
- `uv run pytest tests/projectkoios/workflow -q` => `9 passed in 0.02s`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/harness/data/marking.py src/python/projectkoios/bootstrap/harness/data/handoff.py src/python/projectkoios/bootstrap/harness/handoffs src/python/projectkoios/workflow tests/projectkoios/bootstrap/harness tests/projectkoios/workflow` => `summary: 0 finding(s), 39 file(s)`.
- `uv run mypy src/python/projectkoios/bootstrap/harness/data/marking.py src/python/projectkoios/bootstrap/harness/data/handoff.py src/python/projectkoios/bootstrap/harness/handoffs src/python/projectkoios/workflow tests/projectkoios/bootstrap/harness tests/projectkoios/workflow` => `Success: no issues found in 39 source files`.
- `uv run pytest tests/projectkoios/bootstrap/harness tests/projectkoios/workflow -q` => `108 passed in 0.42s`.
- `uv run pytest -q` => `224 passed in 1.16s`.
- `uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 118 file(s)`.
- `graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `9848 nodes, 10742 edges, 860 communities`.

## Implementation notes

- `PetriNetBinding` is remediated to `PetriNetTransitionBinding`.
- `PetriNetFiringRule` is remediated to `PetriNetFiringRequest`.
- `PetriNetExecutionState` is remediated to `PetriNetState`.
- Runtime service is now `PetriNetExecutor`.
- In-process debug events are `PetriNetTransitionFiredEvent`, `PetriNetMarkingChangedEvent`, and `PetriNetEventCollection`.
- `PetriNetArc` plus `PetriNetArcKind` is retained per accepted YAGNI boundary.
- Prior dirty handoff renames remain validated: `KoiosHandoff` and `PetriNetMarking` with `HandoffMarking = PetriNetMarking[KoiosHandoff]`.

## Ignore for now

- Product architecture changes.
- Concrete SNAKES/PM4Py conversion without an implementation brief.
- Older workflow ADR/plan control-surface reconciliation unless explicitly routed.
- ATHENA/HERMES/KOIOS-owned workspace files unless explicitly directed.
- Source-authority changes outside accepted ADR implementation.
- Concurrent dirty files unrelated to VULCAN implementation work.

## Next expected artifact

- ATHENA conformance review, VULCAN-only commit/push instruction, or follow-up workflow implementation slice.
