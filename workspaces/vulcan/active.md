```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "adr-json-database-pilot-control-surface-package-validated",
  "datetime": "20260711.040819Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "src/python/projectkoios/bootstrap/control_surface/adr/",
    "tests/projectkoios/bootstrap/control_surface_adr/",
    "dev/adr-json-database-one-adr-pilot/",
    "docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md",
    "docs/AAR/aar.20260711.035759_adr-json-database-one-adr-pilot.md"
  ],
  "scratch_directory": "scratch/",
  "source_brief": "docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md",
  "implementation_plan": "docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md",
  "latest_report": "docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md"
}
```

# Vulcan active work

## Current priority stack

1. Await user/Hermes decision on ADR revision/promotion/supersession, next architecture slice, or packaging direction.
2. Preserve KOIOS terminology caveat: this was a SQLite operational adapter storing schema-backed ADR JSON records and exporting a JSON checkpoint, not a persistent/repository-authoritative JSON database service.
3. Keep the pilot bounded to one ADR and do not overwrite `docs/adr/adr.json-database-for-adr-storage.draft.md` unless explicitly authorized.

## Latest working material

- Architecture blueprint: `docs/architecture/architecture.json-adr-storage-topology.md`.
- Source brief: `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`.
- Approved implementation plan: `docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md`.
- Implementation report: `docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md`.
- AAR: `docs/AAR/aar.20260711.035759_adr-json-database-one-adr-pilot.md`.
- Pilot code: `src/python/projectkoios/bootstrap/control_surface/adr/`.
- Pilot tests: `tests/projectkoios/bootstrap/control_surface_adr/`.
- Pilot evidence: `dev/adr-json-database-one-adr-pilot/`.

## Latest validation evidence

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/schema -q` => `24 passed in 0.17s`.
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `Success: no issues found in 10 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 10 file(s)`.
- `git diff --check` => clean.
- `find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.

## Implementation notes

- Implemented database-operational / JSON-checkpointed pilot mode.
- Implemented status-free canonical identity: `id = adr.json-database-for-adr-storage`, `slug = json-database-for-adr-storage`, and `status = draft` inside record content.
- Implemented committed pilot-local manifest/config and evidence index at `dev/adr-json-database-one-adr-pilot/manifest.json`.
- Implemented narrow storage adapter boundary; SQLite is the selected pilot adapter implementation and not a direct dependency for ADR mapping, validation, projection, or equality logic.
- Mutable SQLite `.sqlite`/`.db` files are generated/local only and are not committed.
- Source `.draft.md` filename is preserved as legacy/source evidence in mapping and manifest.
- KOIOS terminology update added to the implementation report and AAR.
- Package-boundary update implemented after user approval: code now lives under `projectkoios.bootstrap.control_surface.adr`.

## Ignore for now

- KOIOS ADR-lifecycle provenance-audit workspace artifact unless explicitly requested.
- Graphify ingestion daemon changes.
- Vault/PDF/source/evidence ingestion.
- `src/python/ingestion/`, `projectkoios.ingestion`, or generic ingestion framework.
- Product-facing template architecture.
- Broad migration of all templates.
- Runtime CLI integration.
- ADR lifecycle/status changes.

## Next expected artifact

- User/Hermes decision on ADR revision/promotion/supersession, next architecture slice, or packaging direction.
