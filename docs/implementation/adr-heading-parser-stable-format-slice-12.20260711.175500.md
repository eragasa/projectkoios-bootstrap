```json
{
  "title": "ADR heading parser stable format slice 12 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated-pending-retrospective-athena-koios-hermes-acceptance",
  "datetime": "20260711.175500Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "slice_name": "adr-heading-parser-stable-format-slice-12",
  "source_decision": null,
  "process_status": "original_workpackage_invalidated_pending_retrospective_acceptance",
  "next_owner": "ATHENA_KOIOS_HERMES_USER"
}
```

# Implementation report 20260711.175500: ADR heading parser stable format slice 12

## Process status correction

This report originally cited an invalid/nonexistent source decision:

```text
docs/reviews/hermes-decision.20260711.175000_adr-heading-parser-stable-format-slice-12.md
```

That workpackage was invalidated because it skipped ATHENA-owned brief and acceptance-criteria ownership. The implementation exists in the working tree but is pending retrospective review/acceptance based on ATHENA retrospective conformance, KOIOS review, and a final HERMES/USER decision.

Until accepted, this report is implementation evidence only and does not itself authorize the patch, establish architecture authority, or close Slice 12.

## Summary

Implemented the bounded tooling compatibility slice for stable ADR heading format, now marked pending retrospective acceptance.

Supported heading forms now include:

```text
# ADR: Title
# ADR 20260711.000000Z: Title
```

## Changes

- Updated `AdrMarkdownRecordParser.title()` to parse both stable `# ADR: Title` and legacy prefixed headings.
- Updated `AdrMarkdownRecordParser` mapping notes so legacy heading-prefix stripping is recorded only when a legacy prefixed heading is present.
- Updated `AdrProjectableMessyCanaryRunner.parse_title()` to accept both stable and legacy heading forms.
- Updated stale `ArchitecturalDataRecord` docstring to describe stable semantic ADR filenames.
- Added parser test coverage for stable `# ADR: Title` heading behavior.

## Boundaries preserved

No changes were made to:

- `docs/adr/`
- `docs/schemas/`
- ADR lifecycle/status policy
- successor ADR files
- supersession/source disposition
- ADR filenames or migrations
- projections/cutover/storage authority

## Retrospective acceptance dependency

Required before HERMES acceptance:

- ATHENA retrospective conformance / acceptance-criteria review;
- KOIOS provenance review;
- HERMES/USER decision accepting, rejecting, or revising the implementation state.

## Validation

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

```bash
git status --short -- docs/adr docs/schemas
```

Passed: no output.

```bash
git diff --check
```

Passed.
