```json
{
  "title": "Hermes workspace state",
  "artifact_type": "workspace-state",
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

# Hermes workspace state

## Current focus

Reconcile startup workflow queue/status visibility with accepted ADR successor-planning state, then choose whether to activate Slice 11.

## Current validated state

- Stable ADR filename convention/control-surface corrections and corrected retrospective Slice 12 acceptance were committed and pushed as `d9aa360c Stabilize ADR filename convention and parser compatibility`.
- Initial Hermes control-surface guardrails were committed and pushed as `92556ac9 Harden Hermes control-surface guardrails`.
- Hermes normative-language guardrail tightening was committed as `4fba6224 Tighten Hermes guardrails with normative language`.
- Accepted Slice 10 records proposal-only successor planning for the ADR template/schema contract:
  - `docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md`
  - `docs/reviews/hermes-acceptance.20260711.174500_adr-template-schema-contract-successor-planning-slice-10.md`
- Accepted Slice 10 recommends the next bounded action `adr-template-schema-contract-successor-draft-slice-11`, with intended output `docs/adr/adr.adr-template-schema-contract.draft.md`.
- User observed the Petri-net workflow status skill may be incomplete because the queue/status surface hid the ADR successor next action.
- USER said `go` to HERMES recommendation to reconcile the queue/status gap before activating Slice 11.

## Current coherent state

Current working-tree reconciliation updates:

```text
dev/workflow-nets/bootstrap-harness.queue-state.json
tests/projectkoios/cli/test__workflow_queue.py
docs/implementation/workflow-queue-adr-successor-reconciliation.20260712.md
workspaces/hermes/state.md
workspaces/hermes/active.md
```

The queue fixture should now show `adr-template-schema-contract-successor-draft-slice-11` as `recommended-next` while preserving `pi-skill-determinism-slice-0` as queued.

## Active boundaries

This reconciliation does not authorize creating the successor ADR draft, editing existing `docs/adr/` files, editing `docs/schemas/`, changing source status or casing, supersession, lifecycle changes, migration, generated projection replacement, database/storage authority, or cutover.

## Current blockers

- Validation and packaging are pending.

## Next owner

HERMES for validation/package, then HERMES_USER for deciding whether to activate Slice 11.
