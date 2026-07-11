```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "adr-json-authority-inventory-review-overrides-slice-1-implemented-validated",
  "datetime": "20260711.143000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_brief": "docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md",
  "source_koios_recommendations": "workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.142700_adr-json-authority-inventory-review-overrides-slice-1.md",
  "source_inventory": "dev/adr-json-authority-inventory-classification-slice-0/",
  "slice_name": "adr-json-authority-inventory-review-overrides-slice-1",
  "latest_report": "docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md",
  "latest_aar": "docs/AAR/aar.20260711.143000_adr-json-authority-inventory-review-overrides-slice-1.md",
  "evidence_dir": "dev/adr-json-authority-inventory-review-overrides-slice-1/",
  "control_files": ["state.md", "active.md"],
  "next_owner": "HERMES_USER_REVIEW",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated ADR JSON authority inventory review/overrides Slice 1.
- Slice name: `adr-json-authority-inventory-review-overrides-slice-1`.
- Evidence directory: `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- Brief: `docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md`.
- KOIOS recommendations: `workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.142700_adr-json-authority-inventory-review-overrides-slice-1.md`.
- Source inventory: `dev/adr-json-authority-inventory-classification-slice-0/`.
- Report: `docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md`.

## Current status

- Review-only override artifacts exist under `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- All 43 Slice 0 entries were reviewed with explicit keep/override decisions and `candidate_only: true`.
- Authority-forward `proposed_authority` labels were downgraded to safer candidate/review labels.
- KOIOS domain-review, source/provenance, mixed-document, and auto-conversion exclusion recommendations were applied.
- Primary messy canary recommendation is `docs/adr/adr.schema-base.md`.
- No ADR source authority, schema authority, storage authority, lifecycle status, filenames, or Markdown source content is changed by override generation.

## Validation evidence

From repository root:

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q` => `22 passed in 0.22s`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 17 file(s)`.
- `find dev/adr-json-authority-inventory-review-overrides-slice-1 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null` => passed.
- `find dev/adr-json-authority-inventory-review-overrides-slice-1 \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.
- `git diff --check` => passed.
- Source/schema stability check around regeneration: before/after corpus hash matched, `stable_source_schema_hash=yes`.
- Evidence determinism check: repeated evidence hash matched, `stable_evidence_hash=yes`.
- `git status --short -- docs/adr docs/schemas` => no output during final validation.

## Dirty tree caution

Treat VULCAN-owned changes for this slice as:

- `dev/adr-json-authority-inventory-review-overrides-slice-1/`
- `src/python/projectkoios/bootstrap/control_surface/adr/overrides.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrInventoryOverrideRunner__review.py`
- `docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md`
- `docs/AAR/aar.20260711.143000_adr-json-authority-inventory-review-overrides-slice-1.md`
- `workspaces/vulcan/active.md`
- `workspaces/vulcan/state.md`

Known ATHENA/HERMES/KOIOS authorizing files and workspace state may also exist in the dirty tree. Keep commit boundaries explicit.

## Next transition

- Owner: HERMES/USER review.
- Expected action: review the review-only override evidence before any messy canary, conversion, or authority-changing slice consumes it.
- Blockers: none from VULCAN.
