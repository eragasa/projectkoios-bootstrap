```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.160700Z",
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

1. Package/commit accepted `adr-template-schema-contract-repair-planning-slice-6` when ready.
2. Choose the next bounded action: successor template/schema contract proposal slice, errata/reconciliation note slice, or broader schema-family repair planning.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Accepted Slice 6: template/schema contract repair planning

- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_template-schema-contract-repair-planning.md`
- ATHENA brief: `docs/plans/architecture-brief.20260711.155500_adr-template-contract-repair-planning-slice-6.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.160000_adr-template-schema-contract-repair-planning-slice-6.md`
- ATHENA repair plan: `docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md`
- KOIOS review: `workspaces/koios/working/provenance-review.20260711_adr-template-schema-contract-repair-planning-slice-6.md`
- VULCAN implementation-reality check: `docs/reviews/implementation-reality.20260711_adr-template-schema-contract-repair-planning-slice-6.md`
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.160700_adr-template-schema-contract-repair-planning-slice-6.md`

## Slice 6 accepted meaning

- Accepted as proposal-only repair planning for exactly `docs/adr/adr.adr-template-contract.md`.
- Primary recommended next path: successor ADR/template-schema contract proposal in a future approved slice.
- Fallback: review-only errata/reconciliation note if HERMES/USER wants lower-risk staging.
- In-place mutation is not recommended as the first repair action.
- No source mutation, status normalization, lifecycle change, supersession/promotion/demotion, schema change, file move/split, JSON conversion/projection, DB/storage authority, migration, or cutover is authorized.

## Key accepted findings

- Preserve source status casing `Accepted`.
- `routing` is stale or ahead-of-authority relative to current schema.
- Markdown-derived/JSON-source-of-truth claims are ahead of current repository authority.
- `dcn` is supported by `adr.adr.md` but ambiguous against current schema.
- `workflow_binding` is supported by current schema but must remain bounded.
- The file is a mixed template/schema contract and source-of-truth policy, not a clean ordinary ADR decision.
- VULCAN confirmed current tooling treats `routing` as outside ADR content, does not implement `dcn`, treats `workflow_binding` as schema-supported but non-operational, and keeps Markdown source/control separate from generated projection evidence.

## Waiting on

- Packaging/commit decision for accepted Slice 6 changes.
- User/HERMES decision for next bounded action.

## Exit criteria

Hermes state is stable when accepted Slice 6 changes are packaged/committed and the next bounded action is chosen without implicitly authorizing source mutation, successor creation, status changes, schema changes, supersession, migration, or cutover.
