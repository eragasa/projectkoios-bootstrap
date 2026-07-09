```json
{
  "title": "Athena active work",
  "artifact_type": "workspace-active-priorities",
  "status": "schema-backed-conformance-reviewed",
  "datetime": "20260709.011055Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "priority_count": 3,
  "active_working_items": [
    "docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md",
    "docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md"
  ]
}
```

# Athena active work

## Current priority stack

1. Return schema-backed conformance review to VULCAN.
2. Let VULCAN proceed with draft/gated skill integration from `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md` if user wants skill integration before packaging.
3. Otherwise let VULCAN/Hermes/user package the schema-backed parser slice.

## Waiting on

- VULCAN decision/execution for draft/gated skill integration.
- User/Hermes packaging and commit direction.
- Optional KOIOS process trace update after skill implementation or packaging decision.

## Current repo state

- ATHENA-authored current-session artifacts include:
  - `docs/plans/implementation-brief.20260708.041245_template-representation-roundtrip.md`
  - `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md`
  - `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md`
  - `docs/AAR/aar.20260708.041331_template-representation-vulcan-handoff.md`
  - `docs/AAR/aar.20260709.010343_template-record-roundtrip-skill-brief.md`
  - `docs/AAR/aar.20260709.010828_koios-comments-skill-brief-update.md`
  - `docs/reviews/architecture-conformance.20260708.052436_template-representation-roundtrip.md`
  - `docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md`
  - `workspaces/athena/state.md`
  - `workspaces/athena/active.md`
- VULCAN and KOIOS also have uncommitted implementation/process artifacts in their domains.

## Ready follow-up candidates

- VULCAN adds `agents/global/opencode/skills/template-record-roundtrip/SKILL.md` and updates `docs/skills/skill-register.md` as draft/gated.
- ATHENA reviews the skill draft after implementation.
- Hermes/user packages and commits the schema-backed parser slice if skill integration is deferred.

## Ignore for now

- Product-domain template decisions that belong in the `projectkoios` mothership repository.
- Implementation code changes from the Athena workspace.
- Graphify/vault/source ingestion or a general-purpose ingestion package.

## Exit criteria

Athena state remains stable when VULCAN has received the schema-backed conformance review and next owner is clear.
