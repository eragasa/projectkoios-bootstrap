```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260712",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES_USER",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. Validate and package workflow queue reconciliation for ADR successor next-action visibility.
2. Decide whether to activate `adr-template-schema-contract-successor-draft-slice-11` for ATHENA.
3. Preserve `pi-skill-determinism-slice-0` as queued unless USER/HERMES explicitly reprioritizes it.

## Active reconciliation update

Updated in working tree:

```text
dev/workflow-nets/bootstrap-harness.queue-state.json
tests/projectkoios/cli/test__workflow_queue.py
docs/implementation/workflow-queue-adr-successor-reconciliation.20260712.md
workspaces/hermes/state.md
workspaces/hermes/active.md
```

Intended visible queue result:

- active: none
- queued/proposed #1: `adr-template-schema-contract-successor-draft-slice-11` state=`recommended-next`
- queued/proposed #2: `pi-skill-determinism-slice-0` state=`queued`
- next decision: activate Slice 11 for ATHENA or explicitly reprioritize

## Waiting on

- Validation.
- Packaging/commit decision after validation.
- USER/HERMES decision whether to activate Slice 11 after packaging.

## Exit criteria

Hermes state is stable when the queue fixture and tests reflect accepted ADR successor next-action state, validation passes, and the reconciliation is packaged or explicitly revised.
