```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "adr-json-authority-messy-canary-slice-2-implemented-validated",
  "datetime": "20260711.144500Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md",
    "docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md",
    "dev/adr-json-authority-inventory-review-overrides-slice-1/",
    "docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md",
    "dev/adr-json-authority-messy-canary-slice-2/",
    "src/python/projectkoios/bootstrap/control_surface/adr/messy_canary.py",
    "tests/projectkoios/bootstrap/control_surface_adr/test__AdrMessyCanaryRunner__schema_base.py"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": null,
  "latest_report": "docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md",
  "latest_aar": "docs/AAR/aar.20260711.144500_adr-json-authority-messy-canary-slice-2.md"
}
```

# Vulcan active work

## Current priority stack

1. `adr-json-authority-messy-canary-slice-2`: implemented and validated.
2. Parent effort: ADR rationalization / JSON-authoritative ADR store.
3. Boundaries preserved: no `docs/adr` mutation; no `docs/schemas` mutation; no conversion of any other file; no authoritative JSON records; no replacement projections; no file moves/renames/deletes/archives; no source status normalization; no draft supersession; no authority cutover; no database/storage authority; no committed `.sqlite`/`.db`.

## Latest working material

- Brief: `docs/plans/implementation-brief.20260711.143800_adr-json-authority-messy-canary-slice-2.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.144200_adr-json-authority-messy-canary-slice-2.md`.
- Reviewed inventory input: `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- Implementation report: `docs/implementation/adr-json-authority-messy-canary-slice-2.20260711.144500.md`.
- AAR: `docs/AAR/aar.20260711.144500_adr-json-authority-messy-canary-slice-2.md`.

## Implemented outputs

- `AdrMessyCanaryRunner` and exported helper `run_adr_json_authority_messy_canary`.
- Messy canary evidence directory: `dev/adr-json-authority-messy-canary-slice-2/`.
- Manifest: `manifest.json`.
- Candidate object: `adr.schema-base.candidate-object.json`.
- Conversion evidence: `conversion-evidence.json`.
- Conflict/lossiness report: `conflict-lossiness-report.json`.
- Sidecar/provenance: `sidecar-provenance.json`.
- Focused tests for missing-status preservation, sidecar provenance, reviewed inventory values, source non-mutation, no projection/DB files, deterministic generation, and valid JSON artifacts.

## Validation results

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Passed: `26 passed in 0.23s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `summary: 0 finding(s), 19 file(s)`.

```bash
find dev/adr-json-authority-messy-canary-slice-2 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
find dev/adr-json-authority-messy-canary-slice-2 \( -name '*.sqlite' -o -name '*.db' \) -print
git status --short -- docs/adr docs/schemas
git diff --check
```

Passed. DB-file and `docs/adr docs/schemas` status checks produced no output.

Source/schema and evidence stability:

```text
stable_source_schema_hash=yes
stable_evidence_hash=yes
```

## Next expected artifact

- HERMES/USER review of `dev/adr-json-authority-messy-canary-slice-2/` before any corpus dry-run or authority-changing slice.
