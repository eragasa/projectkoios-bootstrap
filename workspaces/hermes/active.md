```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.154100Z",
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

1. Package/commit accepted `adr-json-authority-corpus-dry-run-inventory-slice-4` when ready.
2. Choose the next bounded ADR JSON authority proof point, semantic ADR rationalization slice, or workflow-engine action.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Accepted Slice 4: ADR JSON authority corpus dry-run inventory

- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md`
- ATHENA brief: `docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.152000_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- Implementation report: `docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md`
- Evidence dir: `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`
- VULCAN AAR: `docs/AAR/aar.20260711.153000_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- ATHENA review: `docs/reviews/architecture-conformance.20260711.153400_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- KOIOS review: `workspaces/koios/working/provenance-review.20260711_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.154100_adr-json-authority-corpus-dry-run-inventory-slice-4.md`

## Slice 4 accepted meaning

- Accepted as a six-entry, candidate-only, corpus-style dry-run inventory proof.
- Approved subset only:
  - `docs/adr/adr.json-schemas.draft.md`
  - `docs/adr/adr.petrinet.20260705.132740Z.md`
  - `docs/adr/adr.adr-template-contract.md`
  - `docs/adr/adr.schema-base.md`
  - `docs/adr/adr.adr-lifecycle.draft.md`
  - `docs/adr/README.md`
- Reduced candidate objects are not source-complete; per-source omitted/sidecar-preserved sections are explicit and aggregate-counted.
- Projection equality is candidate-field-only and does not imply source-to-candidate completeness.
- README/index-control and lifecycle source/provenance rows remain skipped/blocked as appropriate.
- No source mutation, schema change, authoritative JSON ADR record, database/storage authority, corpus conversion, bulk migration, or authority cutover is accepted.

## Validation summary

HERMES reran/observed workflow status, focused tests, mypy, Python policy, JSON validity, DB-file scan, docs/adr/docs/schemas mutation check, aggregate consistency checks, and diff-check. Results passed: 34 tests, mypy clean, 0 policy findings, JSON valid, no DB files, no ADR/schema mutation, aggregate counts consistent, diff-check clean.

## Waiting on

- Packaging/commit decision for accepted Slice 4 changes.
- User/HERMES decision for next bounded proof point, semantic ADR review/rationalization slice, or workflow-engine action.

## Exit criteria

Hermes state is stable when accepted Slice 4 changes are packaged/committed and the next bounded action is chosen without implicitly authorizing corpus conversion or queued/deferred work.
