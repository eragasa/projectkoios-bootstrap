```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.174500Z",
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

1. Package/commit accepted Slice 10 successor planning, review artifacts, and corrected handoff artifacts.
2. Decide whether to activate recommended `adr-template-schema-contract-successor-draft-slice-11`.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Accepted Slice 10: ADR template/schema contract successor planning

- HERMES handoff decision: `docs/reviews/hermes-decision.20260711.173500_adr-template-schema-contract-successor-planning-slice-10.md`
- ATHENA brief: `docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md`
- KOIOS review: `workspaces/koios/working/provenance-review.20260711_adr-template-schema-contract-successor-planning-slice-10.md`
- VULCAN review: `docs/reviews/implementation-reality.20260711_adr-template-schema-contract-successor-planning-slice-10.md`
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.174500_adr-template-schema-contract-successor-planning-slice-10.md`
- Process AAR: `docs/AAR/aar.20260711_hermes-athena-handoff-boundary.md`

## Accepted Slice 10 meaning

- The old source `docs/adr/adr.adr-template-contract.md` remains unedited source/provenance.
- No new successor ADR has been created yet.
- A future successor draft should preserve old-source status/casing `Accepted` as provenance.
- The future draft should distinguish content schema, record envelope, Markdown source/control, generated projections, sidecar/provenance, `routing`, `dcn`, and `workflow_binding` boundaries.
- The future draft should defer supersession, source mutation, schema edits, migration, and cutover to later HERMES/USER-approved slices.
- KOIOS packaging watchpoint on `workspaces/athena/active.md` metadata punctuation was corrected before acceptance.

## Accepted next recommendation

Primary recommended next bounded action:

```text
adr-template-schema-contract-successor-draft-slice-11
```

Recommended future draft path pattern:

```text
docs/adr/adr.adr-template-schema-contract.<YYYYMMDD.HHMMSSZ>.draft.md
```

## Waiting on

- Packaging/commit decision for accepted Slice 10 changes.
- HERMES/USER decision to activate Slice 11 or choose a different bounded repair action.

## Exit criteria

Hermes state is stable when accepted Slice 10 changes are packaged/committed and the next bounded action is chosen without implicitly authorizing old-source mutation, schema changes, lifecycle/status changes, supersession, migration, generated projection replacement, database/storage authority, or cutover.
