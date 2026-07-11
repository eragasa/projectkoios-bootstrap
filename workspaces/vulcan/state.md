```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "adr-json-database-pilot-control-surface-package-validated",
  "datetime": "20260711.040819Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_architecture": "docs/architecture/architecture.json-adr-storage-topology.md",
  "source_brief": "docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md",
  "implementation_plan": "docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md",
  "latest_report": "docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md",
  "latest_aar": "docs/AAR/aar.20260711.035759_adr-json-database-one-adr-pilot.md",
  "control_files": ["state.md", "active.md"],
  "next_owner": "ATHENA_OR_USER_OR_HERMES",
  "blockers": []
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated ADR JSON/database one-ADR pilot.
- Architecture blueprint: `docs/architecture/architecture.json-adr-storage-topology.md`.
- Source brief: `docs/plans/adr-json-database-one-adr-pilot.implementation-brief.20260709.014124.md`.
- Implementation plan: `docs/plans/implementation-plan.20260711.033558_adr-json-database-one-adr-pilot.md`.
- Implementation report: `docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md`.
- AAR: `docs/AAR/aar.20260711.035759_adr-json-database-one-adr-pilot.md`.
- Representative ADR fixture: `docs/adr/adr.json-database-for-adr-storage.draft.md`.
- Schema: `docs/schemas/adr.schema.json`.

## Current status

- VULCAN implemented the approved bounded one-ADR pilot.
- VULCAN wrote code, tests, pilot evidence artifacts, implementation report, AAR, and workspace tracking updates.
- No hand-authored `docs/adr/*.md` files were modified by the pilot.
- No mutable `.sqlite` or `.db` file is committed under the pilot artifact directory.
- ATHENA completed conformance review and architecture as-built reconciliation.
- KOIOS reviewed the user-facing "JSON database" characterization and found it accurate only with bounded-pilot terminology qualifications.
- User approved implementing the KOIOS package-boundary watchpoint; code moved from `projectkoios.bootstrap.adr_records` to `projectkoios.bootstrap.control_surface.adr`.

## Implemented surfaces

- Pilot package: `src/python/projectkoios/bootstrap/control_surface/adr/`.
- Tests: `tests/projectkoios/bootstrap/control_surface_adr/`.
- Manifest/config and evidence index: `dev/adr-json-database-one-adr-pilot/manifest.json`.
- JSON checkpoint: `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.json`.
- Generated Markdown projection: `dev/adr-json-database-one-adr-pilot/adr.json-database-for-adr-storage.projected.md`.
- Mapping evidence: `dev/adr-json-database-one-adr-pilot/mapping.json`.
- Database evidence: `dev/adr-json-database-one-adr-pilot/database-evidence.md`.

## Latest validation evidence

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/schema -q` => `24 passed in 0.17s`.
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `Success: no issues found in 10 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 10 file(s)`.
- `git diff --check` => clean.
- `find dev/adr-json-database-one-adr-pilot -type f \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.

## Dirty tree caution

There are pre-existing and concurrent ATHENA/KOIOS/HERMES changes in the working tree. Treat the VULCAN-owned files/changes for this step as:

- `src/python/projectkoios/bootstrap/control_surface/adr/`
- `tests/projectkoios/bootstrap/control_surface_adr/`
- `dev/adr-json-database-one-adr-pilot/`
- `docs/implementation/adr-json-database-one-adr-pilot.20260711.035759.md`
- `docs/AAR/aar.20260711.035759_adr-json-database-one-adr-pilot.md`
- `workspaces/vulcan/state.md`
- `workspaces/vulcan/active.md`

Do not include unrelated ATHENA/KOIOS/HERMES workspace or architecture changes in a VULCAN implementation commit unless explicitly requested.

## KOIOS terminology update

Preferred user-facing wording:

> Yes, for the pilot: we stood up a SQLite operational store behind an ADR storage adapter that stores schema-backed ADR JSON records and exports a reviewable JSON checkpoint. We did not create a persistent or repository-authoritative database service.

Caveats: not a JSON-native/document database, not a persistent DB service, not repository-authoritative database state, not global ADR database config, and not bulk ADR migration. The JSON checkpoint remains pilot-derived/non-authoritative unless a later ADR/action promotes the storage model.

Package-boundary update: code was moved to `projectkoios.bootstrap.control_surface.adr` after user approval.

## Next transition

- Owner: USER_OR_HERMES.
- Expected action: decision on ADR revision/promotion/supersession, next architecture slice, or final packaging direction.
- Blockers: none from VULCAN.
