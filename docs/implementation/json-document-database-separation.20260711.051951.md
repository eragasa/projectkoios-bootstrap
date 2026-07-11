```json
{
  "title": "JSON document database separation implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated-ready-for-athena-review",
  "datetime": "20260711.051951Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "source_architecture": "docs/architecture/architecture.json-adr-storage-topology.md",
  "source_brief": "docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md",
  "source_plan": "docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md"
}
```

# Implementation report 20260711.051951: JSON document database separation

## Summary

Implemented the approved separation slice for the one-ADR pilot.

- Added generic document model code under `projectkoios.bootstrap.control_surface.documents` and generic storage code under `projectkoios.bootstrap.control_surface.storage`.
- Refactored ADR storage into `DocumentStoreAdrStorageAdapter`, an ADR-facing wrapper over the generic storage protocol.
- Replaced the ADR-specific SQLite table shape with generic `json_documents` storage.
- Kept ADR mapping, validation, projection, equality, naming/lifecycle metadata, and evidence generation in the ADR layer.
- Added migration evidence preserving old adapter/table/package names, source `.draft.md` path/hash, old pilot identity, and prior mapping provenance.
- Used scoped enum/types for semantic values introduced by the slice, including `DocumentType`, `DocumentStoreBackend`, `ArtifactDisposition`, `ReplacementAction`, and `SourceOfTruthMode`.
- After user review, removed duplicate `*/hashing.py` helper modules and encapsulated canonical payload serialization/hash behavior on `DocumentRecord`; text hashing used by manifests is scoped to `PilotManifestBuilder`.
- Replaced dangling Markdown parser constants with schema-derived required section keys and parser methods for section-name translation and heading pattern behavior.
- Updated ADR parsing and pilot evidence for the revised ADR schema that no longer accepts `routing` as record content; source routing text is preserved only outside schema JSON as mapping evidence.

## Files changed

### Code

- `src/python/projectkoios/bootstrap/control_surface/documents/`
- `src/python/projectkoios/bootstrap/control_surface/storage/`
- `src/python/projectkoios/bootstrap/control_surface/document_store/` (removed after package split)
- `src/python/projectkoios/bootstrap/control_surface/adr/__init__.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/hashing.py` (removed)
- `src/python/projectkoios/bootstrap/control_surface/adr/manifest.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/models.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/pilot.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/storage.py`

### Tests

- `tests/projectkoios/bootstrap/control_surface_storage/`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrStoragePilot__run.py`

### Pilot evidence

- `dev/adr-json-database-one-adr-pilot/manifest.json`
- `dev/adr-json-database-one-adr-pilot/database-evidence.md`
- `dev/adr-json-database-one-adr-pilot/document-store-migration-evidence.json`

### Planning/policy artifacts touched in this session

- `docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md`
- `docs/policies/python-coding.md`

## Implementation details

Generic document store:

- `DocumentRecord` carries `document_id`, `document_kind`, canonical JSON payload, content hash, and caller-supplied timestamps.
- `DocumentType.ADR` is the enum boundary for the current pilot document family.
- `SqliteDocumentStore` persists only generic columns: `document_id`, `document_kind`, `content_hash`, `payload_json`, `created_at`, and `updated_at`.
- `MemoryDocumentStore` provides a non-SQLite implementation for boundary tests.
- Tests assert runtime protocol conformance for generic `DocumentStore` implementations and the ADR-facing `AdrStorageAdapter` wrapper.
- SQLite DDL is generated from `DocumentRecord` through `DocumentStoreSqlSchema`, with `payload` translated to the storage column `payload_json`.
- Removed the YAGNI `AdrRecordComparer`; pilot equality checks now use direct record comparison.
- Moved database and migration evidence construction from `AdrStoragePilot` into `AdrPilotEvidenceBuilder`.
- Added `PilotAdrSourceConfig` so pilot source identity/path/date values are explicit config instead of parser literals.

ADR layer:

- `DocumentStoreAdrStorageAdapter` converts ADR records into generic `DocumentRecord` instances and delegates persistence.
- ADR schema validation, Markdown projection, record comparison, and source mapping remain outside the generic store.
- The pilot now records generic document-store metadata in the manifest and database evidence.

Migration evidence:

- `document-store-migration-evidence.json` records old `SqliteAdrStorageAdapter`, `MemoryAdrStorageAdapter`, and `adr_records` table surfaces.
- The evidence records new `SqliteDocumentStore`, `MemoryDocumentStore`, `DocumentStoreAdrStorageAdapter`, and `json_documents` surfaces.
- The source `.draft.md` path/hash and old pilot identity remain preserved.

## Post-review refactors

User review identified two implementation style issues after the initial validation pass:

- duplicate `*/hashing.py` modules;
- dangling Markdown parser constants for section heading and required section keys.

VULCAN removed both `hashing.py` helper modules, moved canonical JSON payload behavior onto `DocumentRecord`, scoped manifest text hashing to `PilotManifestBuilder`, and replaced Markdown section constants with required section derivation from `docs/schemas/adr.schema.json` plus parser-owned heading translation.

## Validation evidence

Commands run from repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/schema -q
# 29 passed in 0.16s

uv run mypy src/python/projectkoios/bootstrap/control_surface/documents src/python/projectkoios/bootstrap/control_surface/storage src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr
# Success: no issues found in 15 source files

uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/documents src/python/projectkoios/bootstrap/control_surface/storage src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr
# summary: 0 finding(s), 15 file(s)

git diff --check
# clean

find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print
# no output
```

Additional guardrail:

- `git status --short -- docs/adr` produced no modified source ADR files.

## Deviations

No deviations from the approved implementation plan.

The JSON checkpoint payload hash remained unchanged because the ADR record payload did not change. Storage metadata and evidence artifacts changed.

## Boundaries preserved

- No backward-compatibility shim was added.
- No ADR-specific fields were added to the generic `json_documents` table.
- No bulk ADR migration was performed.
- No reusable repository-level config was added.
- No database-authority promotion was made.
- No source `docs/adr/*.md` file was modified.
- No mutable `.sqlite` or `.db` file is committed under the pilot directory.

## Next owner

ATHENA/user/Hermes for review of implementation evidence and architecture as-built reconciliation.
