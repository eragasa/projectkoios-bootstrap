```json
{
  "title": "Vulcan workspace state",
  "artifact_type": "workspace-state",
  "status": "adr-heading-parser-stable-format-slice-12-implemented-validated-pending-retrospective-acceptance",
  "datetime": "20260711.175500Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "document_domain": "implementation, tests, validation, implementation reports, deviation reports",
  "source_decision": null,
  "process_status": "original_workpackage_invalidated_pending_retrospective_acceptance",
  "slice_name": "adr-heading-parser-stable-format-slice-12",
  "latest_report": "docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md",
  "latest_aar": "docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md",
  "control_files": ["state.md", "active.md"],
  "next_owner": "ATHENA_KOIOS_HERMES_USER",
  "blockers": ["retrospective-athena-conformance-required", "koios-provenance-review-required", "hermes-user-acceptance-required"]
}
```

# Vulcan workspace state

## Current scope

- Current scope: implemented and validated ADR heading parser stable format Slice 12, pending retrospective acceptance.
- Slice name: `adr-heading-parser-stable-format-slice-12`.
- Original workpackage/decision reference was invalidated because it skipped ATHENA-owned brief and acceptance-criteria ownership.
- Report: `docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md`.
- AAR: `docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md`.

## Current status

- Implementation exists in working tree as implementation evidence only pending ATHENA retrospective conformance, KOIOS review, and HERMES/USER decision.
- Stable heading `# ADR: Title` is accepted by the control-surface ADR parser.
- Legacy heading `# ADR 20260711.000000Z: Title` remains accepted.
- Legacy heading-prefix stripping is recorded only for legacy prefixed headings.
- Projectable messy canary title parsing accepts stable and legacy headings.
- Stale timestamped filename docstring in `ArchitecturalDataRecord` is corrected.
- No source ADR, schema, lifecycle, successor, rename, migration, or projection replacement boundary changed.

## Validation evidence

From repository root:

- `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q` => `35 passed in 0.33s`.
- `uv run mypy src/python/projectkoios/bootstrap/control_surface/adr src/python/projectkoios/bootstrap/harness/data/adr.py tests/projectkoios/bootstrap/control_surface_adr` => `Success: no issues found in 24 source files`.
- `uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr src/python/projectkoios/bootstrap/harness/data/adr.py tests/projectkoios/bootstrap/control_surface_adr` => `summary: 0 finding(s), 24 file(s)`.
- `git status --short -- docs/adr docs/schemas` => no output.
- `git diff --check` => passed.

## Dirty tree caution

Treat VULCAN-owned changes for this slice as:

- `src/python/projectkoios/bootstrap/control_surface/adr/markdown.py`
- `src/python/projectkoios/bootstrap/control_surface/adr/projectable_messy_canary.py`
- `src/python/projectkoios/bootstrap/harness/data/adr.py`
- `tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py`
- `docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md`
- `docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md`
- `workspaces/vulcan/active.md`
- `workspaces/vulcan/state.md`

Known HERMES/ATHENA/KOIOS working-tree files may also exist. Keep commit boundaries explicit.

## Next transition

- Owner: ATHENA/KOIOS/HERMES/USER retrospective review and decision.
- Blockers: retrospective ATHENA conformance, KOIOS provenance review, and HERMES/USER acceptance are required before treating Slice 12 as accepted.
