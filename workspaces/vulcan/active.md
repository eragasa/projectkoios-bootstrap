```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "adr-json-authority-inventory-classification-slice-0-implemented-validated",
  "datetime": "20260711.141200Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/adr/adr.json-authoritative-adr-store.draft.md",
    "docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md",
    "docs/plans/implementation-brief.20260711.140700_adr-json-authority-inventory-classification-slice-0.md",
    "docs/reviews/hermes-decision.20260711.141000_adr-json-authority-inventory-classification-slice-0.md",
    "docs/implementation/adr-json-authority-inventory-classification-slice-0.20260711.141200.md",
    "dev/adr-json-authority-inventory-classification-slice-0/",
    "src/python/projectkoios/bootstrap/control_surface/adr/inventory.py",
    "tests/projectkoios/bootstrap/control_surface_adr/test__AdrInventoryRunner__classification.py"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": null,
  "latest_report": "docs/implementation/adr-json-authority-inventory-classification-slice-0.20260711.141200.md",
  "latest_aar": "docs/AAR/aar.20260711.141200_adr-json-authority-inventory-classification-slice-0.md"
}
```

# Vulcan active work

## Current priority stack

1. `adr-json-authority-inventory-classification-slice-0`: implemented and validated.
2. Parent effort: ADR rationalization / JSON-authoritative ADR store.
3. Boundaries preserved: no `docs/adr` mutation by inventory generation; no `docs/schemas` mutation; no file moves/renames/deletes/archives; no source status normalization; no draft supersession; no authoritative JSON records; no corpus conversion; no replacement Markdown projections; no database/storage authority; no committed `.sqlite`/`.db`.

## Latest working material

- Source ADR: `docs/adr/adr.json-authoritative-adr-store.draft.md`.
- HERMES acceptance: `docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md`.
- Brief: `docs/plans/implementation-brief.20260711.140700_adr-json-authority-inventory-classification-slice-0.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.141000_adr-json-authority-inventory-classification-slice-0.md`.
- Implementation report: `docs/implementation/adr-json-authority-inventory-classification-slice-0.20260711.141200.md`.
- AAR: `docs/AAR/aar.20260711.141200_adr-json-authority-inventory-classification-slice-0.md`.

## Implemented outputs

- `AdrInventoryRunner` and exported helper `run_adr_json_authority_inventory`.
- Review-only inventory evidence directory: `dev/adr-json-authority-inventory-classification-slice-0/`.
- Manifest: `manifest.json`.
- Per-source inventory: `source-inventory.json`.
- Aggregate classification summary: `classification-summary.json`.
- Focused tests for review-only markers, required per-file fields, status preservation, index/control classification, deterministic generation, source non-mutation assumptions, and no database files.

## Validation results

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Passed: `18 passed in 0.21s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `summary: 0 finding(s), 15 file(s)`.

```bash
find dev/adr-json-authority-inventory-classification-slice-0 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-inventory-classification-slice-0 \( -name '*.sqlite' -o -name '*.db' \) -print
git diff --check
```

Passed. DB-file check produced no output.

Source/schema and evidence stability:

```text
stable_source_schema_hash=yes
stable_evidence_hash=yes
```

`git status --short -- docs/adr docs/schemas` currently includes `M docs/adr/adr.json-authoritative-adr-store.draft.md` as existing authorizing state; `docs/schemas` has no output.

## Next expected artifact

- HERMES/USER review of `dev/adr-json-authority-inventory-classification-slice-0/` before any conversion or authority-changing slice.
