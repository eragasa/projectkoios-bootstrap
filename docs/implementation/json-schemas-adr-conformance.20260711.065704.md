```json
{
  "title": "JSON schemas ADR conformance implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated-ready-for-athena-review",
  "datetime": "20260711.065704Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_plan": "docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md",
  "target_source": "docs/adr/adr.json-schemas.draft.md",
  "schema": "docs/schemas/adr.schema.json"
}
```

# Implementation report 20260711.065704: JSON schemas ADR conformance

## Summary

VULCAN implemented the approved one-document active YAGNI conformance slice for:

- `docs/adr/adr.json-schemas.draft.md`

The source Markdown was not mutated. A schema-valid active conformed JSON checkpoint was produced under a target-specific conformance directory, with conversion provenance preserved in sidecars.

## Files changed

### Code

- `src/python/projectkoios/bootstrap/control_surface/adr/conformance.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/markdown.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`

### Tests

- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py`

### Conformance artifacts

- `dev/adr-json-schemas-conformance/adr.json-schemas.json`
- `dev/adr-json-schemas-conformance/adr.json-schemas.projected.md`
- `dev/adr-json-schemas-conformance/conversion-evidence.json`
- `dev/adr-json-schemas-conformance/mapping.json`
- `dev/adr-json-schemas-conformance/manifest.json`
- `dev/adr-json-schemas-conformance/database-evidence.md`

## Behavior implemented

- Added `AdrConformanceRunner` and `AdrConformancePaths` for the single approved target.
- Reused `DocumentStoreAdrStorageAdapter` over `SqliteDocumentStore` and the generic `json_documents` substrate.
- Generated the active conformed record at `dev/adr-json-schemas-conformance/adr.json-schemas.json`.
- Preserved source `routing.owner`, `routing.next_phase`, `routing.notes`, source date/status/path/hash, and `links.related` in sidecar evidence outside the schema record.
- Kept `routing` absent from the schema record.
- Kept `links.related` absent from the schema record because the current schema does not define it.
- Generated a projection and round-tripped its embedded record through schema validation.
- Added a non-destructive round-trip test proving source Markdown remains byte-for-byte unchanged while checkpoint, storage export, and projection parse records match.
- Removed generated SQLite state after evidence capture.

## Constraint checks

- `docs/adr/adr.json-schemas.draft.md` was not modified.
- `docs/schemas/adr.schema.json` was not modified.
- No `routing` field is present in `dev/adr-json-schemas-conformance/adr.json-schemas.json`.
- Source routing and related-link material is preserved in `dev/adr-json-schemas-conformance/conversion-evidence.json` and `mapping.json`.
- The new record is framed as `active-conformance-record`, not historical-only/non-authoritative migration evidence.
- No generated `.sqlite` or `.db` files are present under `dev/adr-json-schemas-conformance/`.

## Validation evidence

Commands run from repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py -q
# 4 passed in 0.09s

uv run pytest tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/schema -q
# 33 passed in 0.20s

uv run pytest -q
# 256 passed in 1.25s

uv run mypy src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage
# Success: no issues found in 18 source files

uv run ruff check src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage
# All checks passed!

uv run projectkoios bootstrap validate-python-policy tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py
# summary: 0 finding(s), 1 file(s)

uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage
# summary: 0 finding(s), 18 file(s)

git diff --check
# clean

find dev/adr-json-schemas-conformance -type f \( -name '*.sqlite' -o -name '*.db' \) -print
# no output

git status --short -- docs/adr
# no output
```

## Deviations

No intentional deviations from the approved plan.

Implementation note: `AdrProjectionRenderer` was made tolerant of either legacy pilot metadata or new conformance metadata so the existing projection behavior could be reused without creating a new projection policy.

## Residual watchpoints for ATHENA

- Confirm the active artifact framing in `manifest.json` and `conversion-evidence.json` matches the intended review vocabulary.
- Confirm that preserving `links.related` exclusively in sidecar evidence is sufficient until/unless the ADR schema grows a related-link field.
- Confirm that projection text remaining generated/non-authoritative is acceptable while the JSON checkpoint is the active conformed record artifact.

## Next owner

ATHENA/user/Hermes for review of the conformed record and sidecar evidence.
