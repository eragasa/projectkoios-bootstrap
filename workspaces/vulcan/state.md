```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "adr-json-authority-corpus-dry-run-inventory-slice-4-implemented-validated-pending-review",
  "datetime": "20260711.153000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_brief": "docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.152000_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md",
  "slice_name": "adr-json-authority-corpus-dry-run-inventory-slice-4",
  "latest_report": "docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md",
  "latest_aar": "docs/AAR/aar.20260711.153000_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
  "evidence_dir": "dev/adr-json-authority-corpus-dry-run-inventory-slice-4/",
  "control_files": ["state.md", "active.md"],
  "next_owner": "KOIOS_ATHENA_REVIEW",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated ADR JSON authority corpus dry-run inventory Slice 4.
- Slice name: `adr-json-authority-corpus-dry-run-inventory-slice-4`.
- Exact subset: six approved entries only.
- Evidence directory: `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`.
- Brief: `docs/plans/implementation-brief.20260711.151500_adr-json-authority-corpus-dry-run-slice-4.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.152000_adr-json-authority-corpus-dry-run-inventory-slice-4.md`.
- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-corpus-dry-run-slice-4.md`.
- Report: `docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md`.
- AAR: `docs/AAR/aar.20260711.153000_adr-json-authority-corpus-dry-run-inventory-slice-4.md`.

## Current status

- Corpus-style dry-run evidence exists under `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`.
- Exactly six approved entries were processed and recorded; no other source is counted.
- README is skipped/excluded as index/control and not converted as an ADR record.
- Lifecycle draft is source/provenance skipped/blocked and not promoted or superseded.
- Schema-base missing status remains missing; no status invented.
- Template-contract Slice 3 behavior is preserved, including `Accepted` casing and wrapped-list continuation.
- Petrinet accepted/current status remains source observation only, not JSON authority.
- Candidate-only/no-authority markers are machine-visible in generated evidence.
- KOIOS-identified source-to-candidate omission visibility is corrected; per-source rows and sidecars enumerate omitted/source-preserved sections and aggregate omitted section count is `48`.

## Validation evidence

From repository root:

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q` => `34 passed in 0.29s`.
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `Success: no issues found in 23 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 23 file(s)`.
- `find dev/adr-json-authority-corpus-dry-run-inventory-slice-4 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null` => passed.
- `find dev/adr-json-authority-corpus-dry-run-inventory-slice-4 \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.
- `git status --short -- docs/adr docs/schemas` => no output.
- `find dev/adr-json-authority-corpus-dry-run-inventory-slice-4 -path '*/generated-projections/*.md' -print` => three projections, all under Slice 4 evidence path.
- Aggregate count check against per-source records => `aggregate_counts_match=yes`; `omitted_sections_total=48`.
- `git diff --check` => passed.

## Dirty tree caution

Treat VULCAN-owned changes for this slice as:

- `dev/adr-json-authority-corpus-dry-run-inventory-slice-4/`
- `src/python/projectkoios/bootstrap/control_surface/adr/corpus_dry_run.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrCorpusDryRunRunner__slice4.py`
- `docs/implementation/adr-json-authority-corpus-dry-run-inventory-slice-4.20260711.153000.md`
- `docs/AAR/aar.20260711.153000_adr-json-authority-corpus-dry-run-inventory-slice-4.md`
- `workspaces/vulcan/active.md`
- `workspaces/vulcan/state.md`

Known ATHENA/HERMES/KOIOS authorizing/review files and workspace state may also exist in the dirty tree. Keep commit boundaries explicit.

## Next transition

- Owner: KOIOS and ATHENA review, then HERMES acceptance.
- Expected action: KOIOS provenance review and ATHENA architecture/conformance review of Slice 4 evidence before HERMES final acceptance.
- Blockers: none from VULCAN.
