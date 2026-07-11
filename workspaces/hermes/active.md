```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.145000Z",
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

1. Package/commit accepted `adr-json-authority-messy-canary-slice-2` when ready.
2. Choose the next bounded ADR JSON authority proof point or workflow-engine action.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Accepted Slice 2: ADR JSON authority messy canary

- Brief: `docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md`
- Implementation report: `docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md`
- Evidence dir: `dev/adr-json-authority-messy-canary-slice-2/`
- VULCAN AAR: `docs/AAR/aar.20260711.144500_adr-json-authority-messy-canary-slice-2.md`
- ATHENA review: `docs/reviews/architecture-conformance.20260711.144800_adr-json-authority-messy-canary-slice-2.md`
- KOIOS review: `workspaces/koios/working/provenance-review.20260711_adr-json-authority-messy-canary-slice-2.md`
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md`

## Slice 2 accepted meaning

- Accepted as a one-source evidence-only messy canary.
- Source: `docs/adr/adr.schema-base.md` only.
- Outcome: `conversion_candidate_blocked_pending_review`.
- Missing Markdown/ADR status remains missing.
- Embedded JSON `status: draft` remains sidecar/source metadata only.
- No source mutation, schema change, projection, authoritative JSON ADR record, database/storage authority, or authority cutover.

## Validation summary

HERMES reran status, focused tests, mypy, Python policy, JSON validity, DB-file scan, docs/adr/docs/schemas mutation check, and diff-check. Results passed: 26 tests, mypy clean, 0 policy findings, JSON valid, no DB files, no ADR/schema mutation, diff-check clean.

## Waiting on

- Packaging/commit decision for accepted Slice 2 changes.
- User/HERMES decision for next bounded proof point.

## Exit criteria

Hermes state is stable when accepted Slice 2 changes are packaged/committed and the next bounded ADR JSON authority proof point or workflow-engine action is chosen without implicitly authorizing corpus conversion or queued/deferred work.
