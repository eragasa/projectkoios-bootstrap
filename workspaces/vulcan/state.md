```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "json-document-database-separation-validated",
  "datetime": "20260711.051951Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_architecture": "docs/architecture/architecture.json-adr-storage-topology.md",
  "source_brief": "docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md",
  "implementation_plan": "docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md",
  "latest_report": "docs/implementation/json-document-database-separation.20260711.051951.md",
  "latest_aar": "docs/AAR/aar.20260711.051951_json-document-database-separation.md",
  "control_files": ["state.md", "active.md"],
  "next_owner": "ATHENA_OR_USER_OR_HERMES",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated JSON document database separation of concerns for the one-ADR pilot.
- Architecture surface: `docs/architecture/architecture.json-adr-storage-topology.md`.
- Source brief: `docs/plans/implementation-brief.20260711.045012_json-document-database-separation.md`.
- Implementation plan: `docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md`.
- Implementation report: `docs/implementation/json-document-database-separation.20260711.051951.md`.
- AAR: `docs/AAR/aar.20260711.051951_json-document-database-separation.md`.

## Current status

- VULCAN implemented the approved separation slice.
- Generic document-store code now lives under `src/python/projectkoios/bootstrap/control_surface/documents/` and `src/python/projectkoios/bootstrap/control_surface/storage/`.
- SQLite DDL is generated from `DocumentRecord` through `DocumentStoreSqlSchema`.
- ADR parser/checkpoint behavior now conforms to the schema change that removed `routing`; source routing text is mapping evidence only.
- YAGNI cleanup removed `AdrRecordComparer`, moved pilot evidence construction into `AdrPilotEvidenceBuilder`, and added `PilotAdrSourceConfig` for pilot source values.
- ADR-specific storage now delegates through `DocumentStoreAdrStorageAdapter` in `src/python/projectkoios/bootstrap/control_surface/adr/storage.py`.
- Generic SQLite table is `json_documents` with no ADR-specific fields.
- Scoped enum/type values are used for introduced semantic values; no dangling semantic constants were introduced.
- Duplicate hashing helper modules were removed; JSON payload hashing is encapsulated on `DocumentRecord`.
- Markdown parser section requirements derive from `docs/schemas/adr.schema.json`; parser methods handle legacy heading translation.
- Pilot migration evidence was added at `dev/adr-json-database-one-adr-pilot/document-store-migration-evidence.json`.

## Latest validation evidence

- `uv run pytest tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/schema -q` => `29 passed in 0.16s`.
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/documents src/python/projectkoios/bootstrap/control_surface/storage src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr` => `Success: no issues found in 15 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/documents src/python/projectkoios/bootstrap/control_surface/storage src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 15 file(s)`.
- `git diff --check` => clean.
- `find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.
- `git status --short -- docs/adr` => no output.

## Dirty tree caution

There are concurrent ATHENA workspace and architecture changes in the working tree. Treat VULCAN-owned changes for this slice as:

- `src/python/projectkoios/bootstrap/control_surface/documents/` and `src/python/projectkoios/bootstrap/control_surface/storage/`
- `src/python/projectkoios/bootstrap/control_surface/adr/`
- `tests/projectkoios/bootstrap/control_surface_storage/`
- `tests/projectkoios/bootstrap/control_surface_adr/`
- `dev/adr-json-database-one-adr-pilot/`
- `docs/plans/implementation-plan.20260711.050606_json-document-database-separation.md`
- `docs/policies/python-coding.md`
- `docs/implementation/json-document-database-separation.20260711.051951.md`
- `docs/AAR/aar.20260711.051951_json-document-database-separation.md`
- `workspaces/vulcan/state.md`
- `workspaces/vulcan/active.md`

Do not include unrelated ATHENA/KOIOS/HERMES workspace or architecture changes in a VULCAN implementation commit unless explicitly requested.

## Next transition

- Owner: ATHENA_OR_USER_OR_HERMES.
- Expected action: review implementation evidence and reconcile architecture as-built state.
- Blockers: none from VULCAN.
