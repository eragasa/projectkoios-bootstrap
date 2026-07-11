```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.130500Z"
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES_OR_USER",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. Package/commit accepted `petrinet-workflow-activate-slice-5` when ready.
2. Choose the next bounded workflow-engine slice after packaging.
3. Preserve `pi-skill-determinism-slice-0` as queued-only unless USER/HERMES explicitly switches priority.

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

### Slice 2: current-slice status reconciliation

- `docs/plans/implementation-brief.20260711.122048_petrinet-workflow-current-slice-status-reconciliation.md`
- `docs/plans/implementation-plan.20260711.122325_petrinet-workflow-current-slice-status-reconciliation.md`
- `dev/workflow-nets/bootstrap-harness.workflow-net.json`
- `tests/projectkoios/cli/test__workflow_status.py`
- `docs/implementation/petrinet-workflow-current-slice-status-reconciliation-slice-2.20260711.122814.md`

### Slice 3: interactive-control skill

- `docs/plans/implementation-brief.20260711.123305_petrinet-workflow-interactive-control-skill-slice-3.md`
- `src/python/projectkoios/workflow/skills/README.md`
- `src/python/projectkoios/workflow/skills/manifest.json`
- `src/python/projectkoios/workflow/skills/petrinet-workflow-interactive-control/SKILL.md`
- `tests/projectkoios/workflow/test__PetriNetWorkflowSkills__interactive_control_skill.py`
- `docs/implementation/petrinet-workflow-interactive-control-skill-slice-3.20260711.123801.md`

### Slice 4: queue state command

- `docs/plans/implementation-brief.20260711.124106_petrinet-workflow-queue-state-slice-4.md`
- `dev/workflow-nets/bootstrap-harness.queue-state.json`
- `src/python/projectkoios/cli/workflow.py`
- `tests/projectkoios/cli/test__workflow_queue.py`
- `docs/implementation/petrinet-workflow-queue-state-slice-4.20260711.124549.md`
- `workspaces/koios/working/provenance-note.20260711_queue-state-slice-4.md`

## Accepted Slice 5: activation command

- `docs/plans/implementation-brief.20260711.124950_petrinet-workflow-activate-slice-5.md` — ATHENA brief approved by USER/HERMES.
- `docs/reviews/hermes-decision.20260711.125800_petrinet-workflow-activate-slice-5.md` — HERMES approval decision.
- `workspaces/koios/working/provenance-note.20260711_activate-slice-5.md` — KOIOS provenance input complete enough for routing.
- `docs/implementation/petrinet-workflow-activate-slice-5.20260711.125832.md` — VULCAN implementation report.
- `docs/AAR/aar.20260711.125832_petrinet-workflow-activate-slice-5.md` — VULCAN process note.
- `docs/reviews/hermes-acceptance.20260711.130500_petrinet-workflow-activate-slice-5.md` — HERMES acceptance.
- Live queue fixture is reconciled: Slice 4 is completed at commit `5f209114`, `active_item` remains null, and `pi-skill-determinism-slice-0` remains queued-only.

## Queued follow-ups

- `docs/plans/queued-slice.20260711.122000_pi-skill-determinism-slice-0.md` — queued only; must not supersede accepted Petri-net slices.

## Closeout watchpoints

- Keep `workflow status` read-only until a specific transition-firing/activation slice is approved.
- Keep the static bootstrap workflow-net fixture non-authoritative.
- Keep canonical skill source under `src/python/projectkoios/workflow/skills/`; `.agents/skills/petrinet-workflow-status` is discovery exposure only.
- Do not treat skill guidance as mechanical workflow-state authority.
- Preserve active/queued/superseded/deferred distinctions.

## Waiting on

- Packaging/commit decision for accepted Slice 5 changes.

## Exit criteria

Hermes state is stable when accepted Slice 5 changes are packaged/committed and the next bounded workflow-engine control slice is chosen without implicitly activating `pi-skill-determinism-slice-0`.
