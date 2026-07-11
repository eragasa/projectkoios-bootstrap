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

1. Package/commit accepted Petri-net workflow agent status skill Slice 1, including project discovery symlink.
2. Preserve queue discipline: new topics are queued, not substituted for active work.
3. After packaging, choose the next queued follow-up only by USER/HERMES direction.

## Accepted Petri-net workflow inspectability artifacts

### Slice 0: live Petri-net skeleton

- `docs/plans/implementation-brief.20260711.114600_live-petri-net-skeleton-slice-0.md`
- `docs/plans/implementation-plan.20260711.114700_live-petri-net-skeleton-slice-0.md`
- `dev/workflow-nets/bootstrap-harness.workflow-net.json`
- `src/python/projectkoios/cli/workflow.py`
- `src/python/projectkoios/cli/main.py`
- `tests/projectkoios/cli/test__workflow_status.py`
- `docs/implementation/live-petri-net-skeleton-slice-0.20260711.114916.md`

### Slice 1: Petri-net workflow agent status skill

- `docs/plans/slicing.20260711.121500_petrinet-workflow-agent-affordances.md`
- `docs/plans/implementation-brief.20260711.121600_petrinet-workflow-agent-status-skill-slice-1.md`
- `src/python/projectkoios/workflow/skills/README.md`
- `src/python/projectkoios/workflow/skills/manifest.json`
- `src/python/projectkoios/workflow/skills/petrinet-workflow-status/SKILL.md`
- `.agents/skills/petrinet-workflow-status`
- `tests/projectkoios/workflow/test__PetriNetWorkflowSkills__status_skill.py`
- `docs/implementation/petrinet-workflow-agent-status-skill-slice-1.20260711.121800.md`
- `docs/reviews/architecture-conformance.20260711.122300_petrinet-workflow-agent-status-skill-slice-1.md`

## Queued follow-ups

- `docs/plans/queued-slice.20260711.122000_pi-skill-determinism-slice-0.md` — queued only; must not supersede active/accepted Petri-net Slice 1.
- Petri-net workflow interactive-control affordance — deferred Slice 2 candidate.

## Closeout watchpoints

- Keep `workflow status` read-only.
- Keep the static bootstrap workflow-net fixture non-authoritative.
- Keep canonical skill source under `src/python/projectkoios/workflow/skills/`; `.agents/skills/petrinet-workflow-status` is discovery exposure only.
- Do not treat this as transition firing, persistence, Operator Console integration, workflow-object runtime coupling, schema authority, role/permission expansion, or product/mothership workflow authority.
- Preserve active/queued/superseded/deferred distinctions.

## Waiting on

- USER/HERMES packaging/commit, then next queued-slice decision.

## Exit criteria

Hermes state is stable when accepted Petri-net workflow agent status skill Slice 1 is packaged according to user direction and the next queued follow-up is left queued unless explicitly activated.
