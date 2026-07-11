```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.155200Z",
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

1. Package/commit accepted `adr-semantic-rationalization-six-entry-slice-5` when ready.
2. Choose the next bounded action: template/schema repair planning, schema-base status/surface repair planning, broader semantic rationalization, or workflow-engine automation.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Accepted Slice 5: ADR semantic rationalization

- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_adr-semantic-rationalization-after-slice-4.md`
- ATHENA brief: `docs/plans/architecture-review-brief.20260711.154300_adr-semantic-rationalization-slice-5.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.154700_adr-semantic-rationalization-six-entry-slice-5.md`
- ATHENA review: `docs/reviews/semantic-rationalization.20260711_adr-six-entry-slice-5.md`
- KOIOS review: `workspaces/koios/working/provenance-review.20260711_adr-semantic-rationalization-six-entry-slice-5.md`
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.155200_adr-semantic-rationalization-six-entry-slice-5.md`

## Slice 5 accepted meaning

- Accepted as review-only semantic disposition evidence.
- Covers exactly six entries:
  1. `docs/adr/README.md`
  2. `docs/adr/adr.petrinet.20260705.132740Z.md`
  3. `docs/adr/adr.adr-template-contract.md`
  4. `docs/adr/adr.json-schemas.draft.md`
  5. `docs/adr/adr.schema-base.md`
  6. `docs/adr/adr.adr-lifecycle.draft.md`
- Does not mutate source files, normalize statuses, supersede/promote/demote ADRs, convert JSON, or perform cutover.
- Recommendations are proposal input only.

## Key accepted dispositions

- `README.md`: index/control surface, not ADR decision authority.
- `adr.petrinet.20260705.132740Z.md`: current bounded bootstrap Petri-net authority, not product/runtime or JSON authority by implication.
- `adr.adr-template-contract.md`: template/schema contract, authority-relevant but needs revision before clean current authority.
- `adr.json-schemas.draft.md`: draft schema namespace/template-contract candidate, not current ADR JSON authority.
- `adr.schema-base.md`: schema-family concept pending status/surface review; needs lifecycle/status and surface-placement repair before current ADR authority use.
- `adr.adr-lifecycle.draft.md`: source/provenance only, subordinate to accepted active lifecycle/naming ADR.

## Waiting on

- Packaging/commit decision for accepted Slice 5 changes.
- User/HERMES decision for next bounded action.

## Exit criteria

Hermes state is stable when accepted Slice 5 changes are packaged/committed and the next bounded action is chosen without implicitly authorizing source mutation, status changes, supersession, migration, or queued/deferred work.
