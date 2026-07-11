```json
{
  "title": "Hermes workspace state",
  "artifact_type": "workspace-state",
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

# Hermes workspace state

## Current focus

Close out accepted `adr-json-authority-corpus-dry-run-inventory-slice-4`, then choose the next bounded ADR JSON authority proof point, semantic ADR rationalization slice, or workflow-engine action.

## Current validated state

- Petri-net workflow status inspected before acceptance:
  - workflow: `bootstrap-harness.slice-0`
  - current token/place: `current-slice` at `user_decision`
  - enabled transitions: `approve_next_slice`
  - user decision required: yes
  - recommendation: choose the next bounded workflow action before workflow-state advancement.
- ADR JSON authority prior slices are accepted:
  - Slice 0: bidirectional object canary accepted.
  - JSON authoritative ADR store architecture accepted.
  - Inventory classification Slice 0 accepted.
  - Inventory review overrides Slice 1 accepted.
  - Messy canary Slice 2 accepted and committed as `d015083e Accept ADR JSON messy canary slice 2`.
  - Projectable messy canary Slice 3 accepted and committed as `2f60837a Accept ADR JSON projectable messy canary slice 3`.
  - Corpus dry-run inventory Slice 4 accepted with watchpoints in `docs/reviews/hermes-acceptance.20260711.154100_adr-json-authority-corpus-dry-run-inventory-slice-4.md`.
- Slice 4 accepted evidence:
  - Implementation report: `docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md`
  - ATHENA review: `docs/reviews/architecture-conformance.20260711.153400_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
  - KOIOS review: `workspaces/koios/working/provenance-review.20260711_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
  - Evidence dir: `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`
- HERMES independently reran/observed:
  - `uv run projectkoios workflow status`
  - `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q`
  - `uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr`
  - `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr`
  - JSON validity for Slice 4 evidence JSON files
  - DB-file scan under Slice 4 evidence dir
  - `git status --short -- docs/adr docs/schemas`
  - aggregate-count consistency checks
  - `git diff --check`
- Validation passed: 34 tests, mypy clean, 0 policy findings, JSON valid, no DB files, no `docs/adr` or `docs/schemas` mutation, aggregate counts consistent, diff-check clean.

## Acceptance boundaries

- Slice 4 is accepted as a bounded six-entry candidate-only corpus-style dry-run inventory, not as source-complete conversion or authority promotion.
- Exactly six selected entries were processed; no all-ADR conversion is accepted.
- Reduced candidate objects are explicitly not source-to-candidate complete.
- Omitted/sidecar-preserved source sections are enumerated per source and aggregate-counted.
- Projection/parse-back equality remains candidate-field-only and does not imply source completeness or authority readiness.
- README/index-control and lifecycle source/provenance rows remain skipped/blocked as appropriate.
- Missing status remains missing for `docs/adr/adr.schema-base.md`.
- Accepted source status remains source observation only for `docs/adr/adr.petrinet.20260705.132740Z.md`.
- No source mutation, schema publication/change, authoritative JSON ADR record, file move/rename/delete/archive, status normalization, draft supersession, database/storage authority, corpus conversion, bulk migration, or authority cutover is accepted.

## Current blockers

- None for accepted Slice 4.

## Next owner

- HERMES_OR_USER for packaging/commit and choosing the next bounded proof point, semantic ADR rationalization slice, or workflow-engine action.

## Current status summary

`adr-json-authority-corpus-dry-run-inventory-slice-4` is implemented, corrected after KOIOS blocker, reviewed by ATHENA and KOIOS, independently validated by HERMES, and accepted with watchpoints. The working tree contains Slice 4 implementation/evidence/review artifacts plus role workspace state updates awaiting packaging/commit.
