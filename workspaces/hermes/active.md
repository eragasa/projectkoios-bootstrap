```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.110000Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "USER_OR_HERMES",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. Package/commit accepted live Petri-net skeleton Slice 0 and related planning/implementation artifacts, or decide next bounded inspectability slice.
2. Preserve authority boundaries during closeout.
3. If packaging also includes workflow-object Slice 0 or changed workflow-object refs, rerun the workflow-object validator as needed.

## Accepted live Petri-net skeleton Slice 0 artifacts

- `docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md`
- `docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md`
- `dev/workflow-nets/bootstrap-harness.workflow-net.json`
- `src/python/projectkoios/cli/workflow.py`
- `src/python/projectkoios/cli/main.py`
- `tests/projectkoios/cli/test__workflow_status.py`
- `docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md`

## Closeout watchpoints

- Keep `workflow status` read-only.
- Keep the static bootstrap workflow-net fixture non-authoritative.
- Do not treat this as transition firing, persistence, Operator Console integration, workflow-object runtime coupling, schema authority, role/permission expansion, or product/mothership workflow authority.
- Treat the current output as a first inspectability skeleton, not a complete control surface.

## Waiting on

- USER/HERMES packaging/commit or next bounded inspectability slice decision.

## Exit criteria

Hermes state is stable when the accepted live Petri-net skeleton Slice 0 is packaged according to user direction, or the user explicitly starts the next bounded inspectability slice.
