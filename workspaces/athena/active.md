```json
{
  "title": "Athena active work",
  "artifact_type": "workspace-active-priorities",
  "status": "skill-draft-conformance-reviewed",
  "datetime": "20260709.012745Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/athena/",
  "priority_count": 3,
  "active_working_items": [
    "docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md",
    "docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md",
    "docs/reviews/architecture-conformance.20260709.012745_template-record-roundtrip-skill.md"
  ]
}
```

# Athena active work

## Current priority stack

1. Package/commit decision for the validated parser slice plus draft/gated skill integration.
2. Optional KOIOS process trace update using VULCAN's skill implementation report and ATHENA's skill conformance review.
3. Preserve draft/gated status until an explicit future promotion review changes it.

## Waiting on

- User/Hermes packaging and commit direction.
- Optional KOIOS process trace update.

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
  - `docs/reviews/architecture-conformance.20260709.012745_template-record-roundtrip-skill.md`
  - `workspaces/athena/state.md`
  - `workspaces/athena/active.md`
- VULCAN-authored current-session artifacts include:
  - `agents/global/opencode/skills/template-record-roundtrip/SKILL.md`
  - `docs/skills/skill-register.md`
  - `docs/implementation/template-record-roundtrip-skill.20260709.012011.md`
  - `docs/AAR/aar.20260709.012011_template-record-roundtrip-skill.md`
  - `workspaces/vulcan/state.md`
  - `workspaces/vulcan/active.md`
- KOIOS has uncommitted process/provenance workspace artifacts in its domain.

## Ready follow-up candidates

- Hermes/user packages and commits the parser + skill integration.
- KOIOS updates process trace now that skill implementation and ATHENA review exist.
- A future explicit promotion review may evaluate whether `template-record-roundtrip` should move beyond `draft`; no such promotion is currently authorized.

## Ignore for now

- Product-domain template decisions that belong in the `projectkoios` mothership repository.
- Implementation code changes from the Athena workspace.
- Graphify/vault/source ingestion or a general-purpose ingestion package.

## Exit criteria

Athena state is stable: VULCAN implemented the skill, ATHENA reviewed it as conforming draft/gated work, and next owner is user/Hermes for packaging or KOIOS for optional trace capture.
