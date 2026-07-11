```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "live-petri-net-skeleton-slice-0-planned-awaiting-approval",
  "datetime": "20260711.114700Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_brief": "docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md",
  "source_architecture": [
    "docs/architecture/architecture.petrinet.00.md",
    "docs/adr/adr.petrinet.20260705.132740Z.md"
  ],
  "slice_name": "live-petri-net-skeleton-slice-0",
  "implementation_plan": "docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md",
  "latest_report": null,
  "latest_aar": null,
  "target_command": "uv run projectkoios workflow status",
  "control_files": ["state.md", "active.md"],
  "next_owner": "USER_HERMES_APPROVAL",
  "blockers": ["awaiting approval before coding"]
}
```

# Vulcan workspace state

## Current scope

- Current scope: planned Live Petri-net skeleton slice 0; paused before coding.
- Slice name: `live-petri-net-skeleton-slice-0`.
- Target command: `uv run projectkoios workflow status`.
- Brief: `docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md`.
- Plan: `docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md`.

## Current status

- VULCAN reviewed the ATHENA brief and existing Petri-net runtime substrate under `src/python/projectkoios/workflow/`.
- Existing runtime provides `PetriNet`, `PetriNetPlace`, `PetriNetTransition`, `PetriNetArc`, `PetriNetMarking`, `PetriNetToken`, `PetriNetState`, `PetriNetExecutor.enabled_bindings(...)`, and validation.
- VULCAN produced a concise implementation plan and is paused for USER/HERMES approval before implementation.

## Planned implementation

- Add `dev/workflow-nets/bootstrap-harness.workflow-net.json` as a narrow static fixture.
- Add `src/python/projectkoios/cli/workflow.py` with a command adapter, fixture loader, and deterministic status reporter.
- Register `workflow` in `src/python/projectkoios/cli/main.py`.
- Add `tests/projectkoios/cli/test__workflow_status.py`.

## Boundaries

- Use existing `projectkoios.workflow` Petri-net runtime classes.
- Compute enabled transitions through `PetriNetExecutor.enabled_bindings(...)`.
- Keep command read-only.
- Do not add firing, persistence, workflow-object integration, Operator Console integration, schema/product authority, role/permission expansion, or live adapters.

## Validation plan

- `uv run projectkoios workflow status`
- `uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q`
- `uv run mypy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli`
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli`
- `git diff --check`

## Dirty tree caution

Known uncommitted non-VULCAN/handoff surfaces exist in the working tree, including ATHENA/KOIOS workspace files and proposal material. Keep VULCAN implementation commit boundaries explicit.

## Next transition

- Owner: USER/HERMES.
- Expected action: approve implementation plan or request plan edits.
- Blocker: coding is paused until approval or direct authorization.
