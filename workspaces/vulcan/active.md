```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "adr-json-authority-projectable-messy-canary-slice-3-implemented-validated-pending-review",
  "datetime": "20260711.150000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md",
    "docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md",
    "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md",
    "dev/adr-json-authority-inventory-review-overrides-slice-1/",
    "docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md",
    "docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md",
    "dev/adr-json-authority-projectable-messy-canary-slice-3/",
    "src/python/projectkoios/bootstrap/control_surface/adr/projectable_messy_canary.py",
    "tests/projectkoios/bootstrap/control_surface_adr/test__AdrProjectableMessyCanaryRunner__template_contract.py"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": null,
  "latest_report": "docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md",
  "latest_aar": "docs/AAR/aar.20260711.150000_adr-json-authority-projectable-messy-canary-slice-3.md"
}
```

# Vulcan active work

## Current priority stack

1. `adr-json-authority-projectable-messy-canary-slice-3`: implemented and validated; pending KOIOS provenance review and ATHENA architecture/conformance review.
2. Parent effort: ADR rationalization / JSON-authoritative ADR store.
3. Boundaries preserved: no `docs/adr` mutation; no `docs/schemas` mutation; no source status normalization; no authoritative JSON ADR record; no replacement projection; no file moves/renames/deletes/archives; no draft supersession; no authority cutover; no database/storage authority; no corpus conversion.

## Latest working material

- Brief: `docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md`.
- HERMES decision: `docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md`.
- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md`.
- Reviewed inventory input: `dev/adr-json-authority-inventory-review-overrides-slice-1/`.
- Slice 2 acceptance/watchpoints: `docs/reviews/hermes-acceptance.20260711.145000_adr-json-authority-messy-canary-slice-2.md`.
- Implementation report: `docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md`.
- AAR: `docs/AAR/aar.20260711.150000_adr-json-authority-projectable-messy-canary-slice-3.md`.

## Implemented outputs

- `AdrProjectableMessyCanaryRunner` and exported helper `run_adr_json_authority_projectable_messy_canary`.
- Evidence directory: `dev/adr-json-authority-projectable-messy-canary-slice-3/`.
- Candidate-only evidence with observed `Accepted` status preserved separately from normalized candidate `accepted`.
- KOIOS-identified wrapped-list lossiness corrected; candidate/projection now preserve `Workflow-bound ADRs can render optional gate fields without losing schema consistency.`
- Generated projection: `dev/adr-json-authority-projectable-messy-canary-slice-3/generated-projection.md`.
- Parse-back evidence confirms generated projection preserved `Accepted` and did not normalize status.
- Conflict/lossiness report keeps template/schema-contract and manual-review blockers active.

## Validation results

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Passed: `30 passed in 0.27s`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `Success: no issues found in 21 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `summary: 0 finding(s), 21 file(s)`.

Additional required checks passed: generated JSON validity, no `.sqlite`/`.db` files under Slice 3 evidence path, no `docs/adr` or `docs/schemas` status output, generated projection only under Slice 3 `dev/`, and `git diff --check` clean.

## Next expected artifact

- KOIOS provenance review.
- ATHENA architecture/conformance review.
- HERMES final acceptance only after those reviews.
