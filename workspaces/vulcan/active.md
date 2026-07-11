```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "json-schemas-adr-conformance-planned-paused",
  "datetime": "20260711.062654Z",
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
    "src/python/projectkoios/bootstrap/control_surface/documents/",
    "src/python/projectkoios/bootstrap/control_surface/storage/",
    "src/python/projectkoios/bootstrap/control_surface/adr/",
    "dev/adr-json-schemas-conformance/"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": "docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md",
  "previous_report": "docs/implementation/control-surface-cleanup-and-schema-conformance.20260711.061724.md"
}
```

# Vulcan active work

## Current priority stack

1. Await ATHENA/user/Hermes approval or revision of `docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md`.
2. Preserve the hard constraints: do not mutate `docs/adr/adr.json-schemas.draft.md`, do not populate `routing` in the schema record, and preserve `routing.*` plus `links.related` in sidecar evidence.
3. If approved, implement only the YAGNI conformance slice for this one ADR-shaped source using the existing document/storage substrate.

## Latest working material

- Target source: `docs/adr/adr.json-schemas.draft.md`.
- Target schema: `docs/schemas/adr.schema.json`.
- Plan: `docs/plans/implementation-plan.20260711.062654_json-schemas-adr-conformance.md`.
- Planned output directory: `dev/adr-json-schemas-conformance/`.
- Prior validated substrate report: `docs/implementation/control-surface-cleanup-and-schema-conformance.20260711.061724.md`.

## Planned outputs if approved

- `dev/adr-json-schemas-conformance/adr.json-schemas.json`
- `dev/adr-json-schemas-conformance/adr.json-schemas.projected.md`
- `dev/adr-json-schemas-conformance/conversion-evidence.json`
- `dev/adr-json-schemas-conformance/mapping.json`
- `dev/adr-json-schemas-conformance/manifest.json`
- `dev/adr-json-schemas-conformance/database-evidence.md`

## Pause state

Coding is paused. Approval or requested revisions are required before implementation.

## Ignore for now

- Bulk ADR migration.
- Source Markdown mutation under `docs/adr/`.
- ADR schema redesign.
- Lifecycle/workflow/routing redesign.
- Projection policy redesign.
- Reusable repository-level ADR storage config.
- Database-authoritative repository policy.
