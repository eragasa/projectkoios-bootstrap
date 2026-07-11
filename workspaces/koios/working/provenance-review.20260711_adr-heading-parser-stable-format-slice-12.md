```json
{
  "title": "KOIOS provenance review: ADR heading parser stable format slice 12",
  "artifact_type": "provenance-review",
  "status": "review-complete-retrospective-acceptable-with-process-watchpoints",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-heading-parser-stable-format-slice-12",
  "reviewed_implementation": "docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md",
  "athena_review": "docs/reviews/architecture-conformance.20260711.180500_adr-heading-parser-stable-format-slice-12.md",
  "retrospective_review": true
}
```

# KOIOS provenance review: ADR heading parser stable format slice 12

## Verdict

KOIOS verdict: **retrospectively acceptable for HERMES/USER acceptance, if accepted explicitly as a corrected retrospective slice and not as validation of the premature workpackage path**.

The implementation is bounded, validated, and provenance-safe after correction. ATHENA retrospective conformance now exists at `docs/reviews/architecture-conformance.20260711.180500_adr-heading-parser-stable-format-slice-12.md`, and VULCAN corrected its implementation report and slice AAR to record the invalidated original workpackage and pending retrospective acceptance path.

## Reviewed artifacts

- Implementation report: `docs/implementation/adr-heading-parser-stable-format-slice-12.20260711.175500.md`
- VULCAN AAR: `docs/AAR/aar.20260711.175500_adr-heading-parser-stable-format-slice-12.md`
- HERMES process AAR: `docs/AAR/aar.20260711_premature-vulcan-tooling-handoff.md`
- ATHENA retrospective conformance: `docs/reviews/architecture-conformance.20260711.180500_adr-heading-parser-stable-format-slice-12.md`
- Code/test changes in the working tree:
  - `src/python/projectkoios/bootstrap/control_surface/adr/markdown.py`
  - `src/python/projectkoios/bootstrap/control_surface/adr/projectable_messy_canary.py`
  - `src/python/projectkoios/bootstrap/harness/data/adr.py`
  - `tests/projectkoios/bootstrap/control_surface_adr/test__AdrConformanceRunner__json_schemas.py`

## Provenance correction status

Earlier KOIOS intercom review found that VULCAN's report cited an invalid/nonexistent `source_decision` and that the process record needed to acknowledge retrospective acceptance.

Current report correction is adequate:

- `source_decision` is now `null`.
- `process_status` is `original_workpackage_invalidated_pending_retrospective_acceptance`.
- The report states the original workpackage was invalidated because it skipped ATHENA-owned brief and acceptance-criteria ownership.
- The report states implementation evidence is pending ATHENA retrospective conformance, KOIOS review, and final HERMES/USER decision.

Current VULCAN AAR correction is adequate:

- It states the implementation proceeded from a premature/invalid HERMES workpackage.
- It states the implementation must be treated as pending retrospective ATHENA/KOIOS/HERMES acceptance.
- It preserves the process lesson that ATHENA-owned brief/acceptance criteria are required before VULCAN tooling compatibility patches.

ATHENA retrospective conformance provides the missing architecture/specification basis and explicitly warns that retrospective approval must not become permission to bypass ATHENA for future document-policy/tooling changes.

## Implementation behavior reviewed

The implemented behavior is bounded to parser/tooling compatibility:

- accepts stable `# ADR: Title` headings;
- preserves legacy `# ADR <prefix>: Title` / `# ADR 20260711.000000Z: Title` parsing compatibility;
- records legacy heading-prefix stripping only when a legacy prefixed heading is parsed;
- updates projectable messy canary title parsing for both stable and legacy heading forms;
- updates a stale implementation docstring from timestamped ADR filename convention to stable semantic filenames;
- adds focused test coverage for stable heading parsing.

This is consistent with the current stable ADR filename/heading direction and does not require source ADR mutation.

## KOIOS validation rerun

KOIOS reran validation from repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Observed: `35 passed`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr src/python/projectkoios/bootstrap/harness/data/adr.py tests/projectkoios/bootstrap/control_surface_adr
```

Observed: `Success: no issues found in 24 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr src/python/projectkoios/bootstrap/harness/data/adr.py tests/projectkoios/bootstrap/control_surface_adr
```

Observed: `summary: 0 finding(s), 24 file(s)`.

```bash
git status --short -- docs/adr docs/schemas
git diff --check
```

Observed: no `docs/adr` or `docs/schemas` output, and diff check passed.

## Authority and mutation boundaries

KOIOS found no evidence that Slice 12 mutates or authorizes mutation of:

- `docs/adr/` source ADRs;
- `docs/schemas/` machine-readable schemas;
- ADR lifecycle/status policy;
- supersession/source disposition;
- ADR filenames or migration state;
- JSON authority/cutover/storage authority;
- generated projections.

The patch should be accepted only as a tooling compatibility change. It must not be read as authority to rewrite legacy headings, normalize source status, rename ADR files, supersede records, change schema authority, or migrate records.

## Process/provenance watchpoints

- Final HERMES acceptance should explicitly state this is retrospective acceptance after invalid initial routing, based on ATHENA conformance, KOIOS provenance review, VULCAN evidence, and HERMES/USER decision.
- The retrospective acceptance should not cite the invalid workpackage as authority.
- HERMES process AAR `docs/AAR/aar.20260711_premature-vulcan-tooling-handoff.md` still says the invalid Slice 12 implementation artifacts/code were removed before commit. That was true for an earlier correction state but no longer describes the current retrospective path where VULCAN implementation evidence exists. HERMES should either add a short addendum or ensure final acceptance supersedes that current-status statement so future readers do not believe the Slice 12 implementation was removed.
- Future document-policy/tooling patches should receive ATHENA-owned brief/acceptance criteria before VULCAN implementation unless USER explicitly waives the order.
- Heading parsing now exists in both `AdrMarkdownRecordParser` and `AdrProjectableMessyCanaryRunner`; if more parsers appear, centralize parsing to avoid regex drift.

## KOIOS recommendation to HERMES

HERMES may accept/package Slice 12 retrospectively if final acceptance:

1. cites ATHENA retrospective conformance, this KOIOS review, and VULCAN's corrected report/AAR;
2. records that the original workpackage was invalid and not precedent;
3. preserves no-authority/no-mutation boundaries;
4. clarifies or supersedes the stale current-status statement in `docs/AAR/aar.20260711_premature-vulcan-tooling-handoff.md`.
