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

1. Package/commit accepted workflow-object Slice 0 and related architecture/review artifacts, or decide next bounded slice.
2. Before packaging, rerun validator if referenced workflow-object source artifacts changed.
3. Preserve authority boundaries during closeout.

## Accepted workflow-object Slice 0 artifacts

- `docs/architecture/architecture.workflow-object.md`
- `docs/plans/implementation-brief.20260711.102123_workflow-object-static-operator-console-record.md`
- `docs/plans/schema-proposal.workflow-object.static-record.20260711.102743.md`
- `docs/plans/example.workflow-object.operator-console-skeleton.20260711.103748.json`
- `docs/plans/roadmap.20260711.102324_workflow-object-future-slices.md`
- `docs/plans/implementation-plan.20260711.103626_workflow-object-static-operator-console-record.md`
- `dev/workflow-objects/operator-console-bootstrap-bundle.workflow-object.json`
- `tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py`
- `docs/implementation/workflow-object-static-operator-console-record.20260711.105117.md`
- `docs/reviews/architecture-conformance.20260711.105430_workflow-object-static-operator-console-record.md`
- `docs/reviews/implementation-review.20260711.105822_workflow-object-static-operator-console-record.md`

## Closeout watchpoints

- Do not promote candidate shape or test-only validator into schema/storage/production authority.
- Do not treat static record as completion authority.
- Do not treat static record as full Operator Console artifact closure.
- Rerun `uv run pytest tests/projectkoios/bootstrap/workflow_objects/test__operator_console_static_record.py -q` if referenced files changed before commit.

## Waiting on

- USER/HERMES packaging/commit or next-slice decision.

## Exit criteria

Hermes state is stable when the accepted workflow-object Slice 0 is packaged according to user direction, or the user explicitly starts the next bounded slice.
