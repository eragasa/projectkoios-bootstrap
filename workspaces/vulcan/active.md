```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "json-document-database-separation-validated",
  "datetime": "20260711.051951Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "src/python/projectkoios/bootstrap/control_surface/documents/",
    "src/python/projectkoios/bootstrap/control_surface/storage/",
    "src/python/projectkoios/bootstrap/control_surface/adr/",
    "tests/projectkoios/bootstrap/control_surface_storage/",
    "tests/projectkoios/bootstrap/control_surface_adr/",
    "dev/adr-json-database-one-adr-pilot/",
    "docs/implementation/json-document-database-separation.20260711.051951.md",
    "docs/AAR/aar.20260711.051951_json-document-database-separation.md"
  ],
  "scratch_directory": "scratch/",
  "source_brief": "docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md",
  "implementation_plan": "docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md",
  "latest_report": "docs/implementation/json-document-database-separation.20260711.051951.md"
}
```

# Vulcan active work

## Current priority stack

1. Await ATHENA/user/Hermes review of the validated JSON document database separation slice.
2. Preserve the explicit boundary: generic document store owns opaque JSON payload persistence; ADR layer owns ADR schema, projection, naming/lifecycle metadata, and evidence.
3. Keep the pilot bounded to one ADR; do not bulk migrate, promote database authority, or add reusable repo-level config without a new brief.

## Latest working material

- Architecture surface: `docs/architecture/architecture.json-adr-storage-topology.md`.
- Source brief: `docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md`.
- Approved implementation plan: `docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md`.
- Implementation report: `docs/implementation/json-document-database-separation.20260711.051951.md`.
- AAR: `docs/AAR/aar.20260711.051951_json-document-database-separation.md`.
- Generic document/storage code: `src/python/projectkoios/bootstrap/control_surface/documents/`, `src/python/projectkoios/bootstrap/control_surface/storage/`.
- ADR wrapper/code: `src/python/projectkoios/bootstrap/control_surface/adr/`.
- Tests: `tests/projectkoios/bootstrap/control_surface_storage/`, `tests/projectkoios/bootstrap/control_surface_adr/`.
- Pilot evidence: `dev/adr-json-database-one-adr-pilot/`.

## Latest validation evidence

- `uv run pytest tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/schema -q` => `29 passed in 0.16s`.
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/documents src/python/projectkoios/bootstrap/control_surface/storage src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr` => `Success: no issues found in 15 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/documents src/python/projectkoios/bootstrap/control_surface/storage src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 15 file(s)`.
- `git diff --check` => clean.
- `find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.
- `git status --short -- docs/adr` => no output.

## Implementation notes

- Implemented `DocumentType.ADR` rather than a dangling document-kind constant.
- Implemented enum/type ownership for introduced semantic evidence values.
- Removed duplicate hashing helper modules and encapsulated JSON payload serialization/hash behavior on `DocumentRecord`.
- Replaced Markdown parser constants with schema-derived section requirements and parser-owned legacy heading translation.
- Replaced old ADR-specific `adr_records` DDL with generic `json_documents` DDL.
- Removed ADR-specific query columns from the generic table.
- Generated SQLite DDL from `DocumentRecord` through `DocumentStoreSqlSchema`.
- Updated ADR parser/checkpoint behavior for the schema change that removed `routing`; source routing text is mapping evidence only.
- Removed YAGNI `AdrRecordComparer`, moved pilot evidence building into `AdrPilotEvidenceBuilder`, and introduced `PilotAdrSourceConfig`.
- Replaced `list_by_status` evidence with `list_by_kind(DocumentType.ADR)` evidence.
- Preserved source `.draft.md` path/hash, old pilot identity, and mapping provenance in migration evidence.

## Ignore for now

- Bulk ADR migration.
- Repository-level reusable ADR storage config.
- Database-authoritative repository policy.
- ADR naming/lifecycle policy changes.
- Product-facing document database architecture.

## Next expected artifact

- ATHENA as-built review or user/Hermes decision on next slice.
