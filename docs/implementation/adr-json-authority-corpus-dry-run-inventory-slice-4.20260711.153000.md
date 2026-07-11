```json
{
  "title": "ADR JSON authority corpus dry-run inventory slice 4 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated-pending-koios-athena-review",
  "datetime": "20260711.153000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "slice_name": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "source_brief": "docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.152000_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md",
  "evidence_dir": "dev/adr-json-authority-corpus-dry-run-inventory-slice-4/",
  "next_owner": "KOIOS_ATHENA_REVIEW"
}
```

# Implementation report 20260711.153000: ADR JSON authority corpus dry-run inventory slice 4

## Summary

Implemented candidate-only corpus-style dry-run evidence for exactly the approved six-entry subset:

1. `docs/adr/adr.json-schemas.draft.md`
2. `docs/adr/adr.petrinet.20260705.132740Z.md`
3. `docs/adr/adr.adr-template-contract.md`
4. `docs/adr/adr.schema-base.md`
5. `docs/adr/adr.adr-lifecycle.draft.md`
6. `docs/adr/README.md`

Evidence path:

```text
dev/adr-json-authority-corpus-dry-run-inventory-slice-4/
```

This is a bounded subset dry run only. It does not authorize corpus conversion, source mutation, schema publication, JSON authority cutover, DB/storage authority, or bulk migration.

## Implemented changes

- Added `AdrCorpusDryRunRunner` and exported helper `run_adr_json_authority_corpus_dry_run`.
- Added focused tests for exact subset enforcement, Slice 2 missing-status behavior, Slice 3 status-casing/wrapped-list regression, README skip, lifecycle source/provenance skip, aggregate counts, projection parse-back, source non-mutation, no DB files, and JSON evidence validity.
- Generated Slice 4 evidence artifacts:
  - `manifest.json`
  - `selected-sources.json`
  - `per-source-results.json`
  - `conflict-lossiness-report.json`
  - `projection-parseback-report.json`
  - `skipped-or-blocked-sources.json`
  - `candidate-objects/`
  - `generated-projections/`
  - `sidecars/`

## Per-source outcomes

| Source | Outcome |
|---|---|
| `docs/adr/adr.json-schemas.draft.md` | `candidate_projectable_pending_review` |
| `docs/adr/adr.petrinet.20260705.132740Z.md` | `accepted_source_candidate_not_json_authority` |
| `docs/adr/adr.adr-template-contract.md` | `projectable_candidate_blocked_pending_template_contract_and_status_review` |
| `docs/adr/adr.schema-base.md` | `blocked_missing_status_pending_review` |
| `docs/adr/adr.adr-lifecycle.draft.md` | `source_only_provenance_draft_skipped_or_blocked` |
| `docs/adr/README.md` | `index_control_surface_skipped` |

## Aggregate counts

From `manifest.json` / `per-source-results.json`:

- Selected entries: `6`
- Generated candidate objects: `4`
- Generated projections: `3`
- Omitted/sidecar-preserved source sections: `48`
- Parse-back comparisons run: `3`
- Missing-status findings: `2`
- Status-casing/normalization-sensitive findings: `1`
- Source-only/provenance blockers: `1`
- Index/control-surface exclusions: `1`
- Manual-review blockers: `4`
- Sidecar/provenance required: `6`

Aggregate counts were checked against per-source records.

## Watchpoints preserved

- `docs/adr/README.md` is skipped/excluded as an index/control surface and is not converted into an ADR record.
- `docs/adr/adr.adr-lifecycle.draft.md` is source/provenance draft evidence only; it is not promoted, superseded, or treated as current lifecycle authority.
- `docs/adr/adr.schema-base.md` preserves missing status as missing and does not invent status.
- `docs/adr/adr.adr-template-contract.md` preserves observed `Accepted` separately from normalized candidate `accepted` and preserves the wrapped-list item: `Workflow-bound ADRs can render optional gate fields without losing schema consistency.`
- `docs/adr/adr.petrinet.20260705.132740Z.md` accepted/current source status remains source observation only, not accepted JSON authority.
- Projection parse-back parses generated projections only and does not resolve manual-review, source-only, index/control, authority blockers, or source-to-candidate completeness.
- Reduced candidate rows explicitly enumerate omitted/sidecar-preserved source sections per source and aggregate them across the dry run.

## KOIOS blocker correction

KOIOS provenance review found that reduced candidate objects did not make source-to-candidate omissions specific enough. VULCAN corrected the Slice 4 evidence so each per-source row and sidecar now includes `omitted_or_sidecar_preserved_source_sections`, and aggregate counts include `omitted_sidecar_preserved_source_sections_total` plus counts by section name.

Example: `docs/adr/adr.json-schemas.draft.md` now enumerates omitted/source-preserved sections such as `context`, `definitions`, `architecture_spec`, `implementation_brief`, `resolved_open_questions`, `non_goals`, `validation_expectations`, `routing`, and `links` rather than reporting projection equality alone.

The conflict/lossiness report now states that projection equality covers candidate fields only and does not imply source-to-candidate completeness. Candidate rows remain pending-review, candidate-only evidence; no row is promoted to source-complete or authoritative JSON.

## Authority boundaries preserved

No changes were made to:

- `docs/adr/`
- `docs/schemas/`
- ADR source Markdown status casing
- ADR source filenames or locations
- authoritative JSON ADR records
- database/storage authority
- corpus conversion or authority cutover

All candidate objects, projections, sidecars, reports, and manifests are under the Slice 4 `dev/` evidence path and marked candidate-only / non-authoritative.

## Validation

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

```bash
find dev/adr-json-authority-corpus-dry-run-inventory-slice-4 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
```

Passed.

```bash
find dev/adr-json-authority-corpus-dry-run-inventory-slice-4 \( -name '*.sqlite' -o -name '*.db' \) -print
```

Passed: no output.

```bash
git status --short -- docs/adr docs/schemas
```

Passed: no output.

```bash
find dev/adr-json-authority-corpus-dry-run-inventory-slice-4 -path '*/generated-projections/*.md' -print
```

Passed: generated projections exist only under the Slice 4 evidence path.

```bash
uv run python - <<'PY'
import json
m=json.load(open('dev/adr-json-authority-corpus-dry-run-inventory-slice-4/manifest.json'))
r=json.load(open('dev/adr-json-authority-corpus-dry-run-inventory-slice-4/per-source-results.json'))
assert m['selected_entry_count']==6
assert r['selected_entry_count']==6
assert m['aggregate_counts']==r['aggregate_counts']
assert len(r['results'])==6
print('aggregate_counts_match=yes')
PY
```

Passed: `aggregate_counts_match=yes`; `omitted_sections_total=48`.

```bash
git diff --check
```

Passed.

## Next required review

Pause for:

1. KOIOS provenance review focused on multi-file provenance, blocker specificity, source-to-candidate lossiness visibility, sidecar clarity, skipped/excluded row semantics, and no-authority signaling.
2. ATHENA architecture/conformance review focused on brief conformance, accepted Slice 2/Slice 3 watchpoints, exact subset enforcement, and no-authority boundaries.

HERMES acceptance should wait for those reviews.
