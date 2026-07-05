```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "petrinet-followups-validated",
  "datetime": "20260705.173808",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "controlling_adr": "docs/adr/adr.petrinet.20260705.132740Z.md",
  "source_review": "docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md",
  "latest_report": "docs/implementation/implementation-report.20260705.173808_petrinet-followups.md",
  "python_coding_policy": "docs/policies/python-coding.md",
  "python_testing_policy": "docs/policies/python-testing.md",
  "control_files": ["state.md", "active.md"],
  "next_owner": "user-or-ATHENA",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Latest completed scope: bounded follow-ups from ATHENA's Petri-net conformance review.
- Controlling ADR: `docs/adr/adr.petrinet.20260705.132740Z.md`.
- Source review: `docs/reviews/architecture-conformance.20260705.144506_petrinet-separation-adr-remediation.md`.
- Current implementation status: validated.
- Authority boundary: implementation remains limited to bootstrap-held workflow Petri-net implementation and related control-surface reconciliation.

## Latest validated state

Latest completed report:

- `docs/implementation/implementation-report.20260705.173808_petrinet-followups.md`.

Session AAR:

- `docs/AAR/aar.20260705.173808_petrinet-followups.md`.

Latest validation evidence:

- `cd ../.. && uv run pytest tests/projectkoios/workflow -q` => `9 passed in 0.02s`.
- `cd ../.. && uv run mypy src/python/projectkoios/workflow tests/projectkoios/workflow` => `Success: no issues found in 11 source files`.
- `cd ../.. && uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/workflow tests/projectkoios/workflow` => `summary: 0 finding(s), 11 file(s)`.
- `cd ../.. && uv run pytest -q` => `224 passed in 1.15s`.
- `cd ../.. && uv run projectkoios bootstrap validate-python-policy --all` => `summary: 0 finding(s), 118 file(s)`.
- `cd ../.. && uv run mypy src/python tests` => `Success: no issues found in 118 source files`.
- Raw-string executor fire search over `src/python` and `tests` => no remaining direct string fire calls found.
- `cd ../.. && graphify update /Users/eugene/repos/projectkoios-bootstrap` => rebuilt graph with `9888 nodes, 10781 edges, 861 communities`.

## Implementation notes

- `PetriNetExecutor.fire()` now accepts `PetriNetFiringRequest` directly.
- Workflow executor tests construct `PetriNetFiringRequest` before firing.
- Older workflow executor draft ADR and implementation plan now contain current-control notes that point to the accepted Petri-net separation ADR for first-slice vocabulary.
- Event timestamps remain runtime-generated, consistent with ATHENA's accepted first-slice residual risk.

## Dirty tree caution

- VULCAN has uncommitted validated follow-up files.
- ATHENA workspace files are dirty and outside VULCAN scope:
  - `workspaces/athena/active.md`.
  - `workspaces/athena/state.md`.
- KOIOS workspace files are dirty/untracked and outside VULCAN scope:
  - `workspaces/koios/active.md`.
  - `workspaces/koios/state.md`.
  - `workspaces/koios/working/provenance-index.20260704T175525Z_adr-control-surfaces.md`.
- Root `AGENTS.md`, accepted ADR/dev source files, and conformance review are present in the dirty tree; stage them only with explicit packaging direction.

## Next transition

- Owner: user if packaging/commit/push is desired.
- Owner: ATHENA if a second conformance review of these follow-ups is desired.
- Highest-leverage next action: package the validated VULCAN-owned follow-up files plus any explicitly authorized ADR/review/dev provenance files.
- Blockers: none currently.
