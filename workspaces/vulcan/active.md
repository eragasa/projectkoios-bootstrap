```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "adr-json-authority-inventory-review-overrides-slice-1-implemented-validated",
  "datetime": "20260711.143000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md",
    "workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md",
    "docs/reviews/hermes-decision.20260711.142700_adr-json-authority-inventory-review-overrides-slice-1.md",
    "docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md",
    "dev/adr-json-authority-inventory-review-overrides-slice-1/",
    "src/python/projectkoios/bootstrap/control_surface/adr/overrides.py",
    "tests/projectkoios/bootstrap/control_surface_adr/test__AdrInventoryOverrideRunner__review.py"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": null,
  "latest_report": "docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md",
  "latest_aar": "docs/AAR/aar.20260711.143000_adr-json-authority-inventory-review-overrides-slice-1.md"
}
```

# Vulcan active work

## Current priority stack

1. `adr-json-authority-inventory-review-overrides-slice-1`: implemented and validated.
2. Parent effort: ADR rationalization / JSON-authoritative ADR store.
3. Boundaries preserved: no `docs/adr` mutation; no `docs/schemas` mutation; no authoritative JSON records; no Markdown-to-JSON conversion; no replacement projections; no file moves/renames/deletes/archives; no source status normalization; no draft supersession; no database/storage authority; no committed `.sqlite`/`.db`.

## Latest working material

- Brief: `docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md`.
- KOIOS recommendations: `workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.142700_adr-json-authority-inventory-review-overrides-slice-1.md`.
- Implementation report: `docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md`.
- AAR: `docs/AAR/aar.20260711.143000_adr-json-authority-inventory-review-overrides-slice-1.md`.

## Implemented outputs

- `AdrInventoryOverrideRunner` and exported helper `run_adr_json_authority_inventory_overrides`.
- Review-only override evidence directory: `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- Manifest: `manifest.json`.
- Reviewed inventory: `reviewed-inventory.json`.
- Explicit decisions: `overrides.json`.
- Aggregate review summary: `review-summary.json`.
- Focused tests for authority-forward label downgrades, KOIOS domain/provenance recommendations, messy canary recommendation, deterministic generation, valid artifacts, and no database files.

## Validation results

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Passed: `22 passed in 0.22s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `summary: 0 finding(s), 17 file(s)`.

```bash
find dev/adr-json-authority-inventory-review-overrides-slice-1 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-inventory-review-overrides-slice-1 \( -name '*.sqlite' -o -name '*.db' \) -print
git diff --check
```

Passed. DB-file check produced no output.

Source/schema and evidence stability:

```text
stable_source_schema_hash=yes
stable_evidence_hash=yes
```

`git status --short -- docs/adr docs/schemas` produced no output during final validation.

## Next expected artifact

- HERMES/USER review of `dev/adr-json-authority-inventory-review-overrides-slice-1/` before any messy canary or authority-changing slice consumes the reviewed inventory.
