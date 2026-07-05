```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "petrinet-followups-validated",
  "datetime": "20260705.173808",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "docs/implementation/implementation-report.20260705.173808_petrinet-followups.md",
    "docs/AAR/aar.20260705.173808_petrinet-followups.md"
  ],
  "scratch_directory": "scratch/",
  "controlling_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "source_review": "docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md"
}
```

# Vulcan active work

## Current priority stack

1. Package current validated VULCAN follow-up files for commit/push only if directed.
2. Request ATHENA follow-up conformance review only if the user wants an additional architecture check.
3. Avoid staging concurrent ATHENA/KOIOS workspace files, root `AGENTS.md`, accepted ADR source/dev files, or unrelated surfaces unless explicitly instructed.

## Latest working material

- Controlling ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`.
- Source conformance review: `docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md`.
- Latest report: `docs/implementation/implementation-report.20260705.173808_petrinet-followups.md`.
- Latest AAR: `docs/AAR/aar.20260705.173808_petrinet-followups.md`.

## Latest validation evidence

- `cd ../.. && uv run pytest tests/projectkoios/workflow -q` => `9 passed in 0.02s`.
- `cd ../.. && uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`.
- `cd ../.. && uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 11 file(s)`.
- `cd ../.. && uv run pytest -q` => `224 passed in 1.15s`.
- `cd ../.. && uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 118 file(s)`.
- `cd ../.. && uv run mypy src/python tests` => `Success: no issues found in 118 source files`.
- `cd ../.. && graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `9888 nodes, 10781 edges, 861 communities`.

## Implementation notes

- `PetriNetExecutor.fire()` now accepts `PetriNetFiringRequest` directly.
- Workflow executor tests now use `PetriNetFiringRequest`.
- Older workflow executor ADR/plan surfaces now explicitly defer first-slice vocabulary authority to the accepted Petri-net separation ADR.
- Runtime-generated event timestamps remain accepted first-slice behavior.

## Ignore for now

- Product architecture changes.
- Concrete SNAKES/PM4Py conversion without an implementation brief.
- Broader workflow adapter/restart/persistence expansion.
- ATHENA/HERMES/KOIOS-owned workspace files unless explicitly directed.
- Source-authority changes outside accepted ADR implementation.
- Concurrent dirty files unrelated to VULCAN implementation work.

## Next expected artifact

- VULCAN-only commit/push instruction, ATHENA follow-up conformance review, or new bounded implementation slice.
