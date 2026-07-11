```json
{
  "title": "ADR JSON authority inventory review/overrides slice 1 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated",
  "datetime": "20260711.143000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_brief": "docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md",
  "source_koios_recommendations": "workspaces/koios/working/override-recommendations.20260711_adr-json-authority-inventory-slice-1.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.142700_adr-json-authority-inventory-review-overrides-slice-1.md",
  "source_inventory": "dev/adr-json-authority-inventory-classification-slice-0/",
  "slice_name": "adr-json-authority-inventory-review-overrides-slice-1",
  "evidence_dir": "dev/adr-json-authority-inventory-review-overrides-slice-1/",
  "next_owner": "HERMES_USER_REVIEW"
}
```

# Implementation report 20260711.143000: ADR JSON authority inventory review/overrides slice 1

## Summary

Implemented review-only override evidence for the accepted Slice 0 ADR inventory.

The slice reviews all 43 Slice 0 entries, including every `authority_effect: proposed_authority` and `disposition_candidate: json_authority_candidate` entry, and emits explicit keep/override decisions with `candidate_only: true`.

Output path:

```text
dev/adr-json-authority-inventory-review-overrides-slice-1/
```

## Changed files

Implementation and tests:

- `src/python/projectkoios/bootstrap/control_surface/adr/overrides.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrInventoryOverrideRunner__review.py`

Generated review-only evidence:

- `dev/adr-json-authority-inventory-review-overrides-slice-1/manifest.json`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/reviewed-inventory.json`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/overrides.json`
- `dev/adr-json-authority-inventory-review-overrides-slice-1/review-summary.json`

Workspace/reporting:

- `docs/implementation/adr-json-authority-inventory-review-overrides-slice-1.20260711.143000.md`
- `docs/AAR/aar.20260711.143000_adr-json-authority-inventory-review-overrides-slice-1.md`
- `workspaces/vulcan/state.md`
- `workspaces/vulcan/active.md`

## Evidence summary

`review-summary.json` reports:

- Total reviewed: 43.
- Changed decisions: 43.
- Reviewed authority effects:
  - `candidate`: 37
  - `domain_review_required`: 5
  - `none`: 1
- Reviewed dispositions:
  - `json_authority_candidate`: 17
  - `manual_review_required`: 15
  - `source_only_provenance_candidate`: 5
  - `domain_review_required`: 5
  - `index_or_control_surface`: 1
- Automatic conversion eligibility candidate count reduced to 17.
- Primary messy canary recommendation: `docs/adr/adr.schema-base.md`.

All values are candidate/review-only and do not authorize conversion or authority cutover.

## Validation

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Result: `22 passed in 0.22s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `summary: 0 finding(s), 17 file(s)`.

```bash
find dev/adr-json-authority-inventory-review-overrides-slice-1 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
```

Result: passed for all generated JSON evidence files.

```bash
find dev/adr-json-authority-inventory-review-overrides-slice-1 \( -name '*.sqlite' -o -name '*.db' \) -print
```

Result: no output.

```bash
git diff --check
```

Result: passed.

Source/schema non-mutation and deterministic evidence check:

```text
source_schema_hash_before=ca79b7f67852dd3d42cdce7dabc919831e49a0577a6ed7bae2b5e3694d4da3fa
source_schema_hash_after=ca79b7f67852dd3d42cdce7dabc919831e49a0577a6ed7bae2b5e3694d4da3fa
stable_source_schema_hash=yes
evidence_hash_first=08b05b7b52cca79c3d7fa70d62dd4c9749a2e443f76d435dfbd0bf43b80505b1
evidence_hash_second=08b05b7b52cca79c3d7fa70d62dd4c9749a2e443f76d435dfbd0bf43b80505b1
stable_evidence_hash=yes
```

`git status --short -- docs/adr docs/schemas` produced no output during final validation.

## Boundary confirmation

Preserved boundaries:

- No `docs/adr` mutation.
- No `docs/schemas` changes.
- No authoritative JSON ADR records.
- No Markdown-to-JSON conversion.
- No replacement projections.
- No file moves, renames, deletes, or archives.
- No source status normalization.
- No draft supersession.
- No database/storage authority.
- No mutable `.sqlite` or `.db` evidence files.

## Next owner

HERMES/USER review of `dev/adr-json-authority-inventory-review-overrides-slice-1/` before any messy canary, corpus dry-run, source mutation, schema publication, JSON authority cutover, or migration slice consumes the reviewed inventory.
