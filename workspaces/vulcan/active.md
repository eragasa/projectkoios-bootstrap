```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "adr-heading-parser-stable-format-slice-12-implemented-validated-pending-retrospective-acceptance",
  "datetime": "20260711.175500Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 1,
  "working_directory": "working/",
  "active_working_items": [
    "docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md",
    "docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md",
    "src/python/projectkoios/bootstrap/control_surface/adr/markdown.py",
    "src/python/projectkoios/bootstrap/control_surface/adr/projectable_messy_canary.py",
    "src/python/projectkoios/bootstrap/harness/data/adr.py",
    "tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py"
  ],
  "scratch_directory": "scratch/",
  "implementation_plan": null,
  "latest_report": "docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md",
  "latest_aar": "docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md"
}
```

# Vulcan active work

## Current priority stack

1. `adr-heading-parser-stable-format-slice-12`: implemented and validated, pending retrospective ATHENA/KOIOS/HERMES acceptance because the original workpackage was invalidated.
2. Parent effort: ADR filename/heading stable semantic convention compatibility.
3. Boundaries preserved: no `docs/adr` mutation; no `docs/schemas` mutation; no lifecycle/status policy change; no successor ADR creation; no supersession; no ADR renames; no migration/cutover/projection replacement.

## Implemented outputs

These outputs are working-tree implementation evidence only until retrospective acceptance.

- `AdrMarkdownRecordParser.title()` accepts stable `# ADR: Title` and legacy `# ADR <prefix>: Title` headings.
- Mapping normalized fields record legacy heading-prefix stripping only when a legacy prefixed heading is present.
- `AdrProjectableMessyCanaryRunner.parse_title()` accepts both stable and legacy headings.
- `ArchitecturalDataRecord` docstring now describes stable semantic ADR filenames.
- Control-surface ADR test coverage includes stable `# ADR: Title` parsing.

## Validation results

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Passed: `35 passed in 0.33s`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr src/python/projectkoios/bootstrap/harness/data/adr.py tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `Success: no issues found in 24 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr src/python/projectkoios/bootstrap/harness/data/adr.py tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `summary: 0 finding(s), 24 file(s)`.

Additional checks passed: `git status --short -- docs/adr docs/schemas` produced no output and `git diff --check` passed.

## Next expected artifact

- ATHENA retrospective conformance / acceptance-criteria review.
- KOIOS provenance review.
- HERMES/USER decision accepting, rejecting, or revising Slice 12.
