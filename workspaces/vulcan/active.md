```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "json-schemas-adr-conformance-implemented-validated",
  "datetime": "20260711.065704Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "docs/adr/adr.json-schemas.draft.md",
    "docs/schemas/adr.schema.json",
    "docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md",
    "src/python/projectkoios/bootstrap/control_surface/adr/conformance.py",
    "tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py",
    "dev/adr-json-schemas-conformance/",
    "docs/implementation/json-schemas-adr-conformance.20260711.065704.md",
    "docs/AAR/aar.20260711.065704_json-schemas-adr-conformance.md"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": "docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md",
  "latest_report": "docs/implementation/json-schemas-adr-conformance.20260711.065704.md",
  "latest_aar": "docs/AAR/aar.20260711.065704_json-schemas-adr-conformance.md"
}
```

# Vulcan active work

## Current priority stack

1. Await ATHENA/user/Hermes review of `docs/implementation/json-schemas-adr-conformance.20260711.065704.md` and `dev/adr-json-schemas-conformance/`.
2. Preserve the hard constraints: do not mutate `docs/adr/adr.json-schemas.draft.md`, do not populate `routing` in the schema record, and preserve `routing.*` plus `links.related` in sidecar evidence.
3. Keep the slice bounded to this one ADR-shaped source; no bulk migration, schema redesign, lifecycle redesign, reusable config, or storage-authority change.

## Latest working material

- Target source: `docs/adr/adr.json-schemas.draft.md`.
- Target schema: `docs/schemas/adr.schema.json`.
- Approved plan: `docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md`.
- Implementation report: `docs/implementation/json-schemas-adr-conformance.20260711.065704.md`.
- AAR: `docs/AAR/aar.20260711.065704_json-schemas-adr-conformance.md`.
- Output directory: `dev/adr-json-schemas-conformance/`.

## Implemented outputs

- `dev/adr-json-schemas-conformance/adr.json-schemas.json`
- `dev/adr-json-schemas-conformance/adr.json-schemas.projected.md`
- `dev/adr-json-schemas-conformance/conversion-evidence.json`
- `dev/adr-json-schemas-conformance/mapping.json`
- `dev/adr-json-schemas-conformance/manifest.json`
- `dev/adr-json-schemas-conformance/database-evidence.md`

## Latest validation evidence

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py -q` => `4 passed in 0.09s`.
- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage tests/projectkoios/bootstrap/schema -q` => `33 passed in 0.20s`.
- `uv run pytest -q` => `256 passed in 1.25s`.
- `uv run mypy src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage` => `Success: no issues found in 18 source files`.
- `uv run ruff check src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage` => `All checks passed!`.
- `uv run projectkoios bootstrap validate-python-policy tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py` => `summary: 0 finding(s), 1 file(s)`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface tests/projectkoios/bootstrap/control_surface_adr tests/projectkoios/bootstrap/control_surface_storage` => `summary: 0 finding(s), 18 file(s)`.
- `git diff --check` => clean.
- `find dev/adr-json-schemas-conformance -type f \( -name '*.sqlite' -o -name '*.db' \) -print` => no output.
- `git status --short -- docs/adr` => no output.

## Ignore for now

- Bulk ADR migration.
- Source Markdown mutation under `docs/adr/`.
- ADR schema redesign.
- Lifecycle/workflow/routing redesign.
- Projection policy redesign.
- Reusable repository-level ADR storage config.
- Database-authoritative repository policy.

## Next expected artifact

- ATHENA review or user/Hermes decision on the conformed record and provenance sidecars.
