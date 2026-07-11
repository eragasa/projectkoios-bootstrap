```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "adr-json-authority-corpus-dry-run-inventory-slice-4-implemented-validated-pending-review",
  "datetime": "20260711.153000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md",
    "docs/reviews/hermes-decision.20260711.152000_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
    "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md",
    "docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md",
    "docs/AAR/aar.20260711.153000_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
    "dev/adr-json-authority-corpus-dry-run-inventory-slice-4/",
    "src/python/projectkoios/bootstrap/control_surface/adr/corpus_dry_run.py",
    "tests/projectkoios/bootstrap/control_surface_adr/test__AdrCorpusDryRunRunner__slice4.py"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": null,
  "latest_report": "docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md",
  "latest_aar": "docs/AAR/aar.20260711.153000_adr-json-authority-corpus-dry-run-inventory-slice-4.md"
}
```

# Vulcan active work

## Current priority stack

1. `adr-json-authority-corpus-dry-run-inventory-slice-4`: implemented and validated; pending KOIOS provenance review and ATHENA architecture/conformance review.
2. Parent effort: ADR rationalization / JSON-authoritative ADR store.
3. Boundaries preserved: no `docs/adr` mutation; no `docs/schemas` mutation; no source status normalization; no authoritative JSON ADR record; no files outside approved six-entry subset converted/projected/parsed as candidates; no database/storage authority; no bulk migration/cutover.

## Latest working material

- Brief: `docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.152000_adr-json-authority-corpus-dry-run-inventory-slice-4.md`.
- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md`.
- Implementation report: `docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md`.
- AAR: `docs/AAR/aar.20260711.153000_adr-json-authority-corpus-dry-run-inventory-slice-4.md`.

## Implemented outputs

- `AdrCorpusDryRunRunner` and exported helper `run_adr_json_authority_corpus_dry_run`.
- Evidence directory: `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`.
- Per-source results for exactly six selected entries.
- KOIOS-identified source-to-candidate omission visibility corrected; per-source rows and sidecars now enumerate omitted/source-preserved sections and aggregate omitted section counts.
- Candidate objects for four candidate rows.
- Generated projections/parse-back for three projectable rows.
- Sidecars for all six rows.
- Skipped/blocked report for manual-review, source/provenance, index/control, and missing-status rows.

## Validation results

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Passed: `34 passed in 0.29s`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `Success: no issues found in 23 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `summary: 0 finding(s), 23 file(s)`.

Additional checks passed: generated JSON validity, no `.sqlite`/`.db` files under Slice 4 evidence path, no `docs/adr` or `docs/schemas` status output, generated projections only under Slice 4 `dev/`, aggregate counts match per-source records, omitted sections total is `48`, and `git diff --check` clean.

## Next expected artifact

- KOIOS provenance review.
- ATHENA architecture/conformance review.
- HERMES final acceptance only after those reviews.
