```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "live-petri-net-skeleton-slice-0-implemented-validated",
  "datetime": "20260711.114916Z",
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
  "latest_report": "docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md",
  "latest_aar": "docs/AAR/aar.20260711.114916_live-petri-net-skeleton-slice-0.md",
  "target_command": "uv run projectkoios workflow status",
  "control_files": ["state.md", "active.md"],
  "next_owner": "USER_HERMES_ATHENA_REVIEW",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated Live Petri-net skeleton slice 0.
- Slice name: `live-petri-net-skeleton-slice-0`.
- Target command: `uv run projectkoios workflow status`.
- Brief: `docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md`.
- Plan: `docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md`.
- Report: `docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md`.

## Current status

- VULCAN added a static bootstrap Petri-net fixture at `dev/workflow-nets/bootstrap-harness.workflow-net.json`.
- VULCAN added the read-only workflow CLI command adapter at `src/python/projectkoios/cli/workflow.py`.
- `src/python/projectkoios/cli/main.py` now registers the top-level `workflow` command group.
- `uv run projectkoios workflow status` prints workflow id, fixture path, places, token locations/color, enabled transitions, and user-decision-required status.
- Enabled transitions are computed via `PetriNetExecutor.enabled_bindings(...)`.
- The fixture remains static bootstrap inspectability material, not canonical workflow authority.

## Validation evidence

From repository root:

- `uv run projectkoios workflow status` => passed; printed expected status.
- `uv run pytest tests/projectkoios/cli/test__workflow_status.py tests/projectkoios/workflow -q` => `15 passed in 0.06s`.
- `uv run mypy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli` => `Success: no issues found in 12 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/cli src/python/projectkoios/workflow tests/projectkoios/cli` => `summary: 0 finding(s), 12 file(s)`.
- `git diff --check` => clean.

## Boundaries preserved

No transition firing command, persistence, mutable workflow state, runtime event-log persistence, Operator Console integration, workflow-object integration, Petri-net graph UI, `docs/schemas/` authority, generalized workflow-net loader framework, role/permission expansion, live intercom/session adapters, or product/mothership workflow authority was added.

## Dirty tree caution

Treat VULCAN-owned changes for this slice as:

- `dev/workflow-nets/bootstrap-harness.workflow-net.json`
- `src/python/projectkoios/cli/workflow.py`
- `src/python/projectkoios/cli/main.py`
- `tests/projectkoios/cli/test__workflow_status.py`
- `docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md`
- `docs/AAR/aar.20260711.114916_live-petri-net-skeleton-slice-0.md`
- `workspaces/vulcan/active.md`
- `workspaces/vulcan/state.md`

Known non-VULCAN handoff/planning files may also exist in the dirty tree. Keep commit boundaries explicit.

## Next transition

- Owner: USER/HERMES/ATHENA review.
- Expected action: review status output and conformance, or request closeout/commit.
- Blockers: none from VULCAN.
