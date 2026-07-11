```json
{
  "title": "Control surface cleanup and schema conformance report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated-ready-for-athena-review",
  "datetime": "20260711.061724Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_brief": "docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md",
  "source_plan": "docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md",
  "related_report": "docs/implementation/json-document-database-separation.20260711.051951.md"
}
```

# Implementation report 20260711.061724: Control surface cleanup and schema conformance

## Summary

VULCAN completed post-approval cleanup and conformance work on the ADR control-surface pilot after user and ATHENA review.

Implemented changes:

- Split generic document concerns from storage concerns:
  - `src/python/projectkoios/bootstrap/control_surface/documents/`
  - `src/python/projectkoios/bootstrap/control_surface/storage/`
- Kept ADR-specific behavior under:
  - `src/python/projectkoios/bootstrap/control_surface/adr/`
- Updated ADR parsing and pilot evidence to conform to the revised ADR schema with no `routing` property.
- Preserved the source Markdown `routing` section only as mapping evidence outside schema JSON.
- Added runtime protocol conformance tests for `DocumentStore` and `AdrStorageAdapter`.
- Generated SQLite DDL from `DocumentRecord` via `DocumentStoreSqlSchema`.
- Removed YAGNI `AdrRecordComparer`/`equality.py`; equality checks are direct record comparisons.
- Moved database/migration evidence building into `AdrPilotEvidenceBuilder`.
- Added `PilotAdrSourceConfig` for pilot source values instead of parser literals.
- Renamed/reduced jargon per KOIOS/user feedback:
  - singular enum class names (`DocumentType`, `DocumentStoreBackend`, etc.);
  - `AdrStoragePilot` instead of `AdrJsonDatabasePilot`;
  - `document-store-migration-evidence.json` instead of replacement evidence wording;
  - `AdrMarkdownRecordParser` for Markdown-to-record parsing.

## Schema conformance note

ATHENA removed `routing` from `docs/schemas/adr.schema.json`.

VULCAN updated implementation behavior accordingly:

- Generated ADR JSON checkpoint no longer contains `routing`.
- `AdrMarkdownRecordParser` no longer populates `routing` for ADR schema conformance.
- Generated projection no longer renders `routing` from record content.
- Mapping evidence preserves source routing text under `preserved_outside_schema.routing_section`.
- Tests assert `routing` is absent from parsed and checkpoint ADR records.

Remaining `routing` text appears only as:

- historical/source prose inside the representative ADR content;
- mapping/migration evidence preserving source or old-table history;
- tests proving ADR-specific routing columns are absent from generic storage.

## Files changed

### Code

- `src/python/projectkoios/bootstrap/control_surface/__init__.py`
- `src/python/projectkoios/bootstrap/control_surface/documents/`
- `src/python/projectkoios/bootstrap/control_surface/storage/`
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/evidence.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/manifest.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/markdown.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/models.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/pilot.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/storage.py`
- Removed: `src/python/projectkoios/bootstrap/control_surface/adr/equality.py`
- Removed: `src/python/projectkoios/bootstrap/control_surface/adr/hashing.py`

### Tests

- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrStoragePilot__run.py`
- `tests/projectkoios/bootstrap/control_surface_storage/test__DocumentStore__sqlite_and_memory.py`
- Removed old test path: `tests/projectkoios/bootstrap/control_surface_adr/test__AdrJsonDatabasePilot__run.py`

### Pilot evidence

- `dev/adr-json-database-one-adr-pilot/manifest.json`
- `dev/adr-json-database-one-adr-pilot/database-evidence.md`
- `dev/adr-json-database-one-adr-pilot/mapping.json`
- `dev/adr-json-database-one-adr-pilot/document-store-migration-evidence.json`
- `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json`
- `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md`

## Boundary preservation

Preserved boundaries:

- No bulk ADR migration.
- No database-authority promotion.
- No reusable repository-level config beyond pilot/test-local scaffolding.
- No source `docs/adr/*.md` file modified.
- No mutable `.sqlite` or `.db` files committed.
- Generic storage table has no ADR-specific fields.
- Petri-net workflow state was not redesigned into ADR `routing` metadata.

## Validation evidence

Commands run from repository root:

```bash
uv run pytest -q
# 253 passed in 1.27s

uv run mypy src/python tests
# Success: no issues found in 139 source files

uv run ruff check src/python tests
# All checks passed!

uv run projectkoios bootstrap validate-python-policy src/python tests
# summary: 0 finding(s), 139 file(s)

git diff --check
# clean

find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print
# no output
```

Graphify was updated after code movement.

## Deviations

No intentional deviations from user-approved implementation direction.

One conformance adjustment was required after ATHENA changed the ADR schema: `routing` was removed from generated ADR JSON and preserved only as source mapping evidence.

## Residual watchpoints for ATHENA

- Confirm whether preserving the old source Markdown `routing` section in mapping evidence is the desired provenance treatment.
- Confirm whether `workflow_binding` should remain untouched until a real Petri-net workflow integration brief exists.
- Confirm whether the split into `documents/`, `storage/`, and `adr/` matches the intended architecture vocabulary.
- Decide later whether `DocumentStoreSqlSchema` should stay as a small generator or be simplified if no second storage table appears.

## Next owner

ATHENA/user/Hermes for architecture review and as-built reconciliation.
