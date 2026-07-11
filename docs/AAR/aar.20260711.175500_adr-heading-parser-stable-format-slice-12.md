# AAR 20260711.175500: ADR heading parser stable format slice 12

## Scope

VULCAN implemented a bounded compatibility patch for stable ADR heading format.

## What happened

- VULCAN implemented Slice 12 from a premature workpackage that was later invalidated because it skipped ATHENA-owned brief and acceptance-criteria ownership.
- Parser support was added for `# ADR: Title` while preserving legacy `# ADR <prefix>: Title` support.
- Legacy heading-prefix stripping is now reported only for legacy prefixed headings.
- Projectable messy canary title parsing was aligned with the stable heading convention.
- A stale implementation docstring about timestamped ADR filenames was corrected.
- Focused control-surface ADR tests, mypy, Python policy validation, `docs/adr`/`docs/schemas` status check, and diff hygiene passed.

## Process issues

- Process breach: VULCAN proceeded from an invalid HERMES workpackage before ATHENA produced the owning brief/acceptance criteria and before renewed HERMES/USER approval.
- VULCAN completion messaging briefly conflicted with the corrected control-surface state and required retrospective correction.
- The implementation must be treated as pending retrospective ATHENA/KOIOS/HERMES acceptance, not as a normally authorized completed slice.
- The stable filename/heading convention exposed a small parser assumption that had been safe only for legacy timestamped ADR headings.
- Historical docs and tests still contain legacy timestamped headings. That is acceptable as compatibility evidence but future parser tests should cover stable format first.

## Proposed follow-up improvements

- Require ATHENA-owned brief/acceptance criteria before VULCAN tooling compatibility patches, even when the patch appears small.
- Retrospective acceptance should explicitly decide whether to retain, revise, or revert the existing implementation patch.
- Naming-policy/document reconciliation should align remaining active prose surfaces with stable ADR filenames and `# ADR: Title` headings.
- If more ADR parsers are introduced, centralize heading parsing to avoid repeated regex drift.

## Candidate ADR or implementation topics

- Dedicated naming-policy reconciliation remains ATHENA-owned and should not be inferred from this compatibility patch.

## Current status

Slice 12 implementation exists as working-tree implementation evidence but is pending retrospective ATHENA conformance, KOIOS provenance review, and HERMES/USER acceptance. No source ADR, schema, lifecycle, migration, or cutover authority changed.
