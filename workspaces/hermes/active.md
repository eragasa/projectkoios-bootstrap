```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.173500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/hermes/",
  "document_domain": "orchestration, repo-state reconciliation, cross-domain consistency",
  "control_files": ["state.md", "active.md"],
  "next_owner": "ATHENA",
  "blockers": []
}
```

# Hermes active work

## Current priority stack

1. Package/commit corrected Slice 10 handoff-only decision.
2. Await ATHENA successor-planning brief for `adr-template-schema-contract-successor-planning-slice-10`.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Corrected Slice 10 handoff

- Improper unpushed completion commit reset: `d197b3e5 Accept ADR template schema contract successor planning slice 10`.
- HERMES handoff decision: `docs/reviews/hermes-decision.20260711.173500_adr-template-schema-contract-successor-planning-slice-10.md`
- Process AAR: `docs/AAR/aar.20260711_hermes-athena-handoff-boundary.md`

## Next owner

ATHENA should produce the successor-planning brief.

Suggested output:

```text
docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md
```

## Waiting on

- Commit/push decision for corrected HERMES handoff state.
- ATHENA output before any HERMES acceptance of Slice 10.

## Exit criteria

Hermes state is stable when the corrected handoff is packaged and Athena receives the bounded Slice 10 planning task without Hermes producing Athena-owned artifacts directly.
