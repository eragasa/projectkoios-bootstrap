```json
{
  "title": "ADR JSON authority inventory/classification slice 0 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated",
  "datetime": "20260711.141200Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_adr": "docs/adr/adr.json-authoritative-adr-store.draft.md",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.140500_json-authoritative-adr-store.md",
  "source_brief": "docs/plans/implementation-brief.20260711.140700_adr-json-authority-inventory-classification-slice-0.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.141000_adr-json-authority-inventory-classification-slice-0.md",
  "slice_name": "adr-json-authority-inventory-classification-slice-0",
  "evidence_dir": "dev/adr-json-authority-inventory-classification-slice-0/",
  "next_owner": "HERMES_USER_REVIEW"
}
```

# Implementation report 20260711.141200: ADR JSON authority inventory/classification slice 0

## Summary

Implemented Phase 0 review-only inventory/classification for ADR-space Markdown files.

The slice inspects `docs/adr/*.md`, records per-file source hash/status/title/classification evidence, and writes review-only JSON artifacts under:

```text
dev/adr-json-authority-inventory-classification-slice-0/
```

No ADR source authority, schema authority, storage authority, lifecycle status, filenames, or Markdown sources are changed by this implementation.

## Changed files

Implementation and tests:

- `src/python/projectkoios/bootstrap/control_surface/adr/inventory.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrInventoryRunner__classification.py`

Generated review-only evidence:

- `dev/adr-json-authority-inventory-classification-slice-0/manifest.json`
- `dev/adr-json-authority-inventory-classification-slice-0/source-inventory.json`
- `dev/adr-json-authority-inventory-classification-slice-0/classification-summary.json`

Workspace/reporting:

- `docs/implementation/adr-json-authority-inventory-classification-slice-0.20260711.141200.md`
- `docs/AAR/aar.20260711.141200_adr-json-authority-inventory-classification-slice-0.md`
- `workspaces/vulcan/state.md`
- `workspaces/vulcan/active.md`

## Evidence summary

`classification-summary.json` reports:

- Total inspected Markdown files: 43.
- File kind counts: 42 `adr_source_candidate`, 1 `index_or_control_surface`.
- Parse confidence counts: 39 `high`, 4 `medium`.
- Automatic-conversion eligibility candidate count: 39.
- Review required count: 4.

All values are candidate/review-only and do not change authority.

## Validation

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Result: `18 passed in 0.21s`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Result: `summary: 0 finding(s), 15 file(s)`.

```bash
find dev/adr-json-authority-inventory-classification-slice-0 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
```

Result: passed for all generated JSON evidence files.

```bash
find dev/adr-json-authority-inventory-classification-slice-0 \( -name '*.sqlite' -o -name '*.db' \) -print
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
evidence_hash_first=c3e484c67fbc23f4076727e8901d4c6e56bb6b4a2a86d4e8cdfc3b2ec1fb5cc7
evidence_hash_second=c3e484c67fbc23f4076727e8901d4c6e56bb6b4a2a86d4e8cdfc3b2ec1fb5cc7
stable_evidence_hash=yes
```

`git status --short -- docs/adr docs/schemas` at validation time showed:

```text
 M docs/adr/adr.json-authoritative-adr-store.draft.md
```

That modified ADR is the authorizing JSON-authority direction already present in the tree for this slice. The source/schema hash check above proves the inventory generation did not change the ADR/schema corpus during validation. `docs/schemas` had no status output.

## Boundary confirmation

Preserved boundaries:

- No `docs/adr` mutation by inventory generation.
- No `docs/schemas` changes.
- No file moves, renames, deletes, or archives.
- No source status normalization.
- No draft supersession.
- No authoritative JSON ADR records.
- No corpus conversion.
- No replacement Markdown projections.
- No database/storage authority.
- No mutable `.sqlite` or `.db` evidence files.

## Next owner

HERMES/USER review of the review-only inventory/classification manifest before any conversion, source mutation, schema publication, JSON authority cutover, or migration slice proceeds.
