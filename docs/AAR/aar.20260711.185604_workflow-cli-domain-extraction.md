```json
{
  "title": "AAR: Workflow CLI domain extraction",
  "artifact_type": "after-action-report",
  "status": "captured",
  "datetime": "20260711.185604",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "scope": "workflow CLI layering fix"
}
```

# AAR: Workflow CLI domain extraction

## Scope

VULCAN responded to USER feedback that the CLI workflow surface did not appear built from the Petri-net/workflow pieces.

## What happened

- Graphify and source inspection showed `workflow status` used Petri-net runtime objects, but queue/activation/reconciliation services lived directly in the CLI module.
- VULCAN extracted the service logic to `projectkoios.workflow.fixtures` and left the CLI module as an argparse/service adapter.
- Full related CLI/workflow tests exposed stale assumptions about the live queue fixture's active item and completed-item ordering; tests were normalized to synthetic behavior fixtures where needed.

## Process issues

- The initial focused test set passed, but the broader related CLI suite revealed additional fixture-drift assumptions.
- Existing tests coupled behavior checks to the mutable live queue fixture, making unrelated workflow-state advancement look like implementation failure.

## Proposed follow-up improvements

- Prefer synthetic temp fixtures for behavior tests that require specific queue active/empty states.
- Keep live fixture tests limited to smoke/shape assertions rather than exact workflow progression details.
- Consider splitting `projectkoios.workflow.fixtures` into narrower workflow modules when another change needs the boundary.

## Candidate ADR or implementation topics

- Optional implementation cleanup: `projectkoios.workflow.status`, `projectkoios.workflow.queue_state`, and `projectkoios.workflow.reconciliation` module split.
- Optional workflow policy: test fixtures for workflow services should not depend on current live queue state unless the test explicitly names live-state behavior.

## Current status

Implemented and validated. No blocker remains for HERMES/USER review.
