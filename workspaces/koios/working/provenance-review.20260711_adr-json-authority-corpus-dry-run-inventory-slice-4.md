```json
{
  "title": "KOIOS provenance review: ADR JSON authority corpus dry-run inventory slice 4",
  "artifact_type": "provenance-review",
  "status": "review-complete-provenance-adequate",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "reviewed_evidence_dir": "dev/adr-json-authority-corpus-dry-run-inventory-slice-4/"
}
```

# KOIOS provenance review: ADR JSON authority corpus dry-run inventory slice 4

## Verdict

KOIOS verdict: **provenance-adequate for HERMES final acceptance consideration, with no-authority boundaries preserved**.

This supersedes the earlier KOIOS acceptance blocker for Slice 4. VULCAN corrected the source-to-candidate lossiness visibility gap by enumerating omitted/source-preserved sections per source and in aggregate. KOIOS re-reviewed the corrected evidence and no longer sees the previous lossiness-reporting blocker.

## Reviewed sources

- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md`
- Brief: `docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.152000_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- VULCAN report: `docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md`
- Evidence: `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`

## Correction verified

Earlier KOIOS review found that reduced candidate objects omitted source sections without specific per-source lossiness visibility.

Corrected evidence now includes:

- `omitted_or_sidecar_preserved_source_sections` in `per-source-results.json` for every selected source;
- matching omitted/source-preserved section lists in per-source sidecars;
- per-source omitted section lists in `conflict-lossiness-report.json`;
- aggregate counts in `manifest.json` and `per-source-results.json`, including `omitted_sidecar_preserved_source_sections_total: 48` and `by_omitted_sidecar_preserved_source_section`;
- explicit `source_to_candidate_complete: false` for every source;
- explicit `projection_parseback_scope: candidate_fields_only_not_source_completeness` for per-source rows.

The example KOIOS called out is now handled: `docs/adr/adr.json-schemas.draft.md` lists omitted/source-preserved sections including `architecture_spec`, `context`, `definitions`, `implementation_brief`, `links`, `non_goals`, `resolved_open_questions`, `routing`, and `validation_expectations`.

KOIOS considers the previous source-to-candidate lossiness visibility blocker resolved.

## Validation observed by KOIOS

During re-review, KOIOS observed:

- The selected subset remains exactly the approved six entries.
- All six source hashes match reviewed Slice 1 values.
- `git status --short -- docs/adr docs/schemas` produced no output.
- All Slice 4 JSON files parsed successfully with `uv run python -m json.tool`.
- No `.sqlite` or `.db` files were found under the Slice 4 evidence path.
- `manifest.json` and `per-source-results.json` aggregate counts match.
- `omitted_sidecar_preserved_source_sections_total` is `48`.
- `git diff --check` passed.
- Focused tests passed: `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q` returned `34 passed`.

## Multi-file provenance and aggregate preservation

The corrected evidence preserves per-source distinctions and aggregate counts:

- `docs/adr/adr.json-schemas.draft.md` — `candidate_projectable_pending_review`, reduced candidate with omitted/source-preserved sections enumerated.
- `docs/adr/adr.petrinet.20260705.132740Z.md` — `accepted_source_candidate_not_json_authority`, accepted source status remains source observation only.
- `docs/adr/adr.adr-template-contract.md` — `projectable_candidate_blocked_pending_template_contract_and_status_review`, `Accepted` casing and Slice 3 wrapped-list preservation remain visible.
- `docs/adr/adr.schema-base.md` — `blocked_missing_status_pending_review`, missing status remains missing and no status is invented.
- `docs/adr/adr.adr-lifecycle.draft.md` — `source_only_provenance_draft_skipped_or_blocked`, not promoted or superseded.
- `docs/adr/README.md` — `index_control_surface_skipped`, not converted as an ADR record.

Aggregate reporting distinguishes projectable, accepted-source-not-authority, manual-review, missing-status, source-only, and index/control outcomes.

## Sidecar clarity and source-to-candidate lossiness

Sidecar/lossiness clarity is now adequate for a candidate-only dry run:

- Every source has a sidecar.
- Every source is marked `source_to_candidate_complete: false`.
- Omitted/source-preserved sections are named per source rather than hidden behind projection equality.
- Projection equality is explicitly scoped to candidate fields only and does not imply source-to-candidate completeness.
- The reduced candidate-object shape remains visible as evidence-only, not source-complete authority.

## Skipped/excluded row semantics

Skipped/excluded row semantics remain provenance-safe:

- `README.md` has no candidate object or projection and remains an index/control surface.
- `adr.adr-lifecycle.draft.md` has no candidate object or projection and remains source/provenance draft evidence only.
- `adr.schema-base.md` may have a candidate object, but projection is blocked, missing status is preserved, and authority promotion remains blocked.

## No-authority signaling

No-authority signaling is clear and machine-visible:

- `authority_change: false`
- `candidate_only: true`
- `corpus_dry_run: true`
- `bounded_subset_only: true`
- `bulk_migration: false`
- `cutover_authorized: false`
- `database_authority: false`
- `conversion_completed_as_authoritative_record: false`

Generated projections remain under `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/generated-projections/`, and parse-back evidence states generated projections only were parsed.

## Minor watchpoint

`manifest.json` still contains `validation_command_summary` values marked `pending closeout validation`, while the implementation report and KOIOS re-validation show validation was completed. This is a traceability polish issue, not a provenance blocker for HERMES acceptance if acceptance cites the report and review evidence.

## KOIOS recommendation to HERMES

HERMES may consider Slice 4 for final acceptance as a bounded, candidate-only, six-entry corpus-style dry-run proof. Acceptance should explicitly preserve that this slice does not authorize corpus conversion, source mutation, schema publication/change, source status normalization, authoritative JSON ADR records, database/storage authority, file moves/renames/deletes, draft supersession, JSON authority cutover, or treating `dev/` evidence as durable authority.
