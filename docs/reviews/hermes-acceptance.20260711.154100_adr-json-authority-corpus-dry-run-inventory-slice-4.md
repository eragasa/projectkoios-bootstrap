```json
{
  "title": "HERMES acceptance: ADR JSON authority corpus dry-run inventory slice 4",
  "artifact_type": "completion-decision",
  "status": "accepted-with-watchpoints",
  "datetime": "20260711.154100Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "implementation_report": "docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md",
  "athena_review": "docs/reviews/architecture-conformance.20260711.153400_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
  "koios_review": "workspaces/koios/working/provenance-review.20260711_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
  "evidence_dir": "dev/adr-json-authority-corpus-dry-run-inventory-slice-4/",
  "next_owner": "HERMES_OR_USER"
}
```

# HERMES acceptance 20260711.154100: ADR JSON authority corpus dry-run inventory slice 4

## Decision

HERMES accepts `adr-json-authority-corpus-dry-run-inventory-slice-4` with watchpoints.

## Accepted scope

This acceptance covers exactly the approved six-entry subset:

```text
docs/adr/adr.json-schemas.draft.md
docs/adr/adr.petrinet.20260705.132740Z.md
docs/adr/adr.adr-template-contract.md
docs/adr/adr.schema-base.md
docs/adr/adr.adr-lifecycle.draft.md
docs/adr/README.md
```

Accepted evidence lives under:

```text
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/
```

This is accepted as a bounded, candidate-only, corpus-style dry-run inventory proof. It is not accepted as corpus conversion, source-complete conversion, migration readiness, or JSON authority cutover.

## Acceptance basis

HERMES reviewed the implementation report, corrected evidence, KOIOS revised provenance review, and ATHENA revised architecture/conformance review.

The previous KOIOS blocker is resolved: source-to-candidate omissions are now visible per source and in aggregate. Evidence records `omitted_or_sidecar_preserved_source_sections`, `source_to_candidate_complete: false`, aggregate omitted/source-preserved section counts, and explicitly states projection equality does not imply source-to-candidate completeness.

Accepted findings:

- Exactly the approved six entries were processed, with no extras.
- Source hashes match reviewed Slice 1 values.
- `docs/adr/README.md` is skipped as an index/control surface and is not converted into an ADR record.
- `docs/adr/adr.adr-lifecycle.draft.md` remains source/provenance-only and is not promoted or superseded.
- `docs/adr/adr.schema-base.md` preserves missing status as missing and does not invent status.
- `docs/adr/adr.adr-template-contract.md` preserves observed `Accepted` separately from normalized candidate `accepted` and preserves the Slice 3 wrapped-list continuation.
- `docs/adr/adr.petrinet.20260705.132740Z.md` accepted source status remains source observation only and does not imply accepted JSON authority.
- Aggregate counts match per-source records.
- Candidate/projection equality is scoped to candidate fields only.
- Every source is marked not source-to-candidate complete.
- Evidence remains `candidate_only: true` and `authority_change: false`.

## Independent HERMES validation

HERMES independently reran or observed clean validation for:

- `uv run projectkoios workflow status`
- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q`
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr`
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr`
- JSON validity for Slice 4 evidence JSON files
- DB-file scan under Slice 4 evidence path
- `git status --short -- docs/adr docs/schemas`
- aggregate-count consistency checks
- `git diff --check`

Validation passed: 34 tests, mypy clean, 0 policy findings, JSON valid, no DB files, no `docs/adr` or `docs/schemas` mutation, aggregate counts consistent, diff-check clean.

Petri-net workflow status remained at user decision and HERMES did not mutate workflow state.

## Watchpoints

This acceptance is bounded and does not authorize:

- corpus conversion or all-ADR conversion;
- conversion or projection of files beyond the approved six-entry subset;
- authoritative JSON ADR records;
- source Markdown mutation;
- source status normalization;
- schema publication or schema changes;
- file moves, renames, deletes, or archives;
- draft supersession;
- database/storage authority;
- mutable `.sqlite` or `.db` files;
- JSON authority cutover;
- treating `dev/` evidence as durable authority.

The manifest still contains `validation_command_summary` values marked pending closeout validation. HERMES accepts this as a traceability polish issue, not a blocker, because the implementation report, KOIOS review, ATHENA review, and HERMES validation record completed validation.

Remaining review questions before broader migration:

- whether reduced candidate objects should become source-complete or remain paired with explicit sidecar/omission reports;
- how semantic ADR rationalization should decide whether each ADR still makes sense as current authority;
- how larger corpus dry-runs should sample or sequence ADRs;
- how final authority location/cutover should be gated.
