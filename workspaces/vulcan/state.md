```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "petrinet-separation-adr-remediation-validated",
  "datetime": "20260705.142149",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "controlling_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "python_coding_policy": "docs/policies/python-coding.md",
  "python_testing_policy": "docs/policies/python-testing.md",
  "control_files": ["state.md", "active.md"],
  "next_owner": "ATHENA-or-user",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Latest completed scope: accepted Petri-net separation ADR implementation remediation plus prior naming corrections.
- Controlling ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`.
- Current implementation status: validated; awaiting Athena conformance review before completion claim.
- Authority boundary: implementation is limited to bootstrap-held workflow Petri-net implementation and related harness naming surfaces; older workflow ADR/plan reconciliation remains a separate follow-on.

## Latest validated state

Latest completed report:

- `docs/implementation/implementation-report.20260705.142149_petrinet-separation-adr-remediation.md`.

Session AAR:

- `docs/AAR/aar.20260705.142149_petrinet-separation-adr-remediation.md`.

Latest validation evidence:

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
- `PetriNet` remains reusable/generic; `WorkflowNet(PetriNet)` contains workflow-domain specialization.
- Handoff token naming is now `KoiosHandoff`; `HandoffMarking = PetriNetMarking[KoiosHandoff]` is preserved.

## Dirty tree caution

- VULCAN has uncommitted validated remediation files.
- ATHENA workspace files are dirty and outside VULCAN scope:
  - `workspaces/athena/active.md`.
  - `workspaces/athena/state.md`.
- KOIOS workspace files are dirty/untracked and outside VULCAN scope:
  - `workspaces/koios/active.md`.
  - `workspaces/koios/state.md`.
  - `workspaces/koios/working/provenance-index.20260704T175525Z_adr-control-surfaces.md`.
- Accepted ADR/dev source files are present but should be staged only if explicitly included in a packaging instruction.
- Any commit should deliberately stage VULCAN-owned files only unless the user explicitly directs otherwise.

## Next transition

- Owner: ATHENA for conformance review.
- Owner: user if packaging/push is desired before review.
- Highest-leverage next action: request or await Athena conformance review, then package VULCAN-owned remediation files only.
- Expected successor artifact: ATHENA conformance review, VULCAN-only commit/push, or follow-up workflow implementation slice.
- Blockers: none currently.
