```json
{
  "title": "Hermes active work",
  "artifact_type": "workspace-active-priorities",
  "status": "active",
  "datetime": "20260711.151000Z",
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

1. Package/commit accepted `adr-json-authority-projectable-messy-canary-slice-3` when ready.
2. Choose the next bounded ADR JSON authority proof point or workflow-engine action.
3. Preserve queued/deferred work as queued-only unless USER/HERMES explicitly activates it.

## Accepted Slice 3: ADR JSON authority projectable messy canary

- Brief: `docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md`
- Implementation report: `docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md`
- Evidence dir: `dev/adr-json-authority-projectable-messy-canary-slice-3/`
- VULCAN AAR: `docs/AAR/aar.20260711.150000_adr-json-authority-projectable-messy-canary-slice-3.md`
- ATHENA prior review: `docs/reviews/architecture-conformance.20260711.150300_adr-json-authority-projectable-messy-canary-slice-3.md`
- ATHENA post-remediation review: `docs/reviews/architecture-conformance.20260711.150700_adr-json-authority-projectable-messy-canary-slice-3-post-remediation.md`
- KOIOS review: `workspaces/koios/working/provenance-review.20260711_adr-json-authority-projectable-messy-canary-slice-3.md`
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.151000_adr-json-authority-projectable-messy-canary-slice-3.md`

## Slice 3 accepted meaning

- Accepted as a one-source, candidate-only, evidence-only projectable messy canary.
- Source: `docs/adr/adr.adr-template-contract.md` only.
- Outcome: `projectable_candidate_blocked_pending_template_contract_and_status_review`.
- Observed `Accepted` status casing remains preserved separately from normalized candidate `accepted`.
- Corrected wrapped-list preservation is accepted; the prior dropped `consistency.` blocker is resolved.
- Projection/parse-back evidence remains dev-only and non-authoritative.
- Template/schema-contract ambiguity and manual-review blockers remain unresolved and blocking.
- No source mutation, schema change, authoritative JSON ADR record, database/storage authority, corpus conversion, bulk migration, or authority cutover is accepted.

## Validation summary

HERMES reran/observed workflow status, focused tests, mypy, Python policy, JSON validity, DB-file scan, docs/adr/docs/schemas mutation check, and diff-check. Results passed: 30 tests, mypy clean, 0 policy findings, JSON valid, no DB files, no ADR/schema mutation, diff-check clean.

## Waiting on

- Packaging/commit decision for accepted Slice 3 changes.
- User/HERMES decision for next bounded proof point or workflow-engine action.

## Exit criteria

Hermes state is stable when accepted Slice 3 changes are packaged/committed and the next bounded ADR JSON authority proof point or workflow-engine action is chosen without implicitly authorizing corpus conversion or queued/deferred work.
