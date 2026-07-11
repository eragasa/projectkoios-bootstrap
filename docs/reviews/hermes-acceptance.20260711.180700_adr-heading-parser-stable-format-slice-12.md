```json
{
  "title": "HERMES acceptance: ADR heading parser stable format slice 12",
  "artifact_type": "completion-decision",
  "status": "accepted-retrospective-corrected-slice",
  "datetime": "20260711.180700Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-heading-parser-stable-format-slice-12",
  "implementation_report": "docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md",
  "athena_conformance": "docs/reviews/architecture-conformance.20260711.180500_adr-heading-parser-stable-format-slice-12.md",
  "koios_review": "workspaces/koios/working/provenance-review.20260711_adr-heading-parser-stable-format-slice-12.md",
  "vulcan_aar": "docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md",
  "hermes_aar": "docs/AAR/aar.20260711_premature-vulcan-tooling-handoff.md",
  "authority_change": false,
  "source_mutation": false,
  "schema_mutation": false,
  "retrospective_acceptance": true,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260711.180700: ADR heading parser stable format slice 12

## Decision

HERMES accepts `adr-heading-parser-stable-format-slice-12` as a corrected retrospective implementation slice.

This acceptance is explicitly **not** acceptance of the premature implementation workpackage path. The original HERMES implementation decision/workpackage was invalid because it skipped ATHENA ownership of the document-policy/tooling boundary.

## Accepted implementation evidence

```text
docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md
```

Accepted code/test surfaces:

```text
src/python/projectkoios/bootstrap/control_surface/adr/markdown.py
src/python/projectkoios/bootstrap/control_surface/adr/projectable_messy_canary.py
src/python/projectkoios/bootstrap/harness/data/adr.py
tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py
```

## Required retrospective reviews

ATHENA retrospective conformance:

```text
docs/reviews/architecture-conformance.20260711.180500_adr-heading-parser-stable-format-slice-12.md
```

Verdict: accepted with watchpoints.

KOIOS retrospective provenance review:

```text
workspaces/koios/working/provenance-review.20260711_adr-heading-parser-stable-format-slice-12.md
```

Verdict: retrospectively acceptable if accepted explicitly as a corrected retrospective slice and not as validation of the premature workpackage path.

VULCAN corrected its implementation report and AAR to remove the invalid source decision as authority and to mark the implementation as pending retrospective ATHENA/KOIOS/HERMES acceptance before this decision.

## Acceptance rationale

The implementation is bounded, validated, and now has the missing ATHENA and KOIOS review basis.

Accepted behavior:

- `AdrMarkdownRecordParser` accepts stable headings of the form `# ADR: Title`.
- Legacy prefixed headings such as `# ADR 20260711.000000Z: Title` remain accepted for compatibility/provenance.
- Mapping notes record legacy heading-prefix stripping only when a legacy prefixed heading is parsed.
- `AdrProjectableMessyCanaryRunner` title parsing accepts stable and legacy heading forms.
- `ArchitecturalDataRecord` implementation docstring now describes stable semantic ADR filenames.
- Focused test coverage exists for stable `# ADR: Title` parsing.

## Validation accepted

VULCAN and KOIOS reported/reran:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr src/python/projectkoios/bootstrap/harness/data/adr.py tests/projectkoios/bootstrap/control_surface_adr
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr src/python/projectkoios/bootstrap/harness/data/adr.py tests/projectkoios/bootstrap/control_surface_adr
git status --short -- docs/adr docs/schemas
git diff --check
```

Observed results:

- focused pytest: `35 passed`;
- mypy: success for 24 source files;
- Python policy: `0 finding(s), 24 file(s)`;
- no `docs/adr` or `docs/schemas` mutation;
- diff check passed.

## Process correction recorded

HERMES process AAR:

```text
docs/AAR/aar.20260711_premature-vulcan-tooling-handoff.md
```

VULCAN slice AAR:

```text
docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md
```

The HERMES AAR has been clarified to state that the invalid decision was removed, while the VULCAN implementation evidence was re-presented and accepted only through this retrospective review path.

## Boundaries preserved

This acceptance does not authorize:

- editing or rewriting source ADRs under `docs/adr/`;
- editing machine-readable schemas under `docs/schemas/`;
- renaming ADR files;
- changing ADR lifecycle/status policy;
- normalizing source status, source heading text, or source dates;
- creating the successor ADR draft;
- supersession/source disposition changes;
- generated projection replacement;
- JSON conversion/migration;
- database/storage authority;
- JSON authority cutover.

The patch is accepted only as parser/tooling compatibility for the current stable ADR heading convention plus legacy heading compatibility.

## Watchpoints carried forward

- Retrospective acceptance must not become precedent for bypassing ATHENA ownership on future document-policy/tooling changes.
- If additional ADR parsers/conversion runners are introduced, centralize heading parsing to avoid regex drift.
- Active naming-policy/documentation reconciliation remains needed for stable semantic ADR filenames, `# ADR: Title`, metadata-based timestamps, and collision policy.

## Recommended next actions

1. Package/commit the stable ADR filename/control-surface corrections and Slice 12 retrospective acceptance if USER approves.
2. Decide whether to activate `adr-template-schema-contract-successor-draft-slice-11` for ATHENA.
3. Create a separate ATHENA-owned naming-policy/documentation reconciliation slice for remaining active guidance.
