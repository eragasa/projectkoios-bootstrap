```json
{
  "title": "ADR JSON authority projectable messy canary slice 3 implementation report",
  "artifact_type": "implementation-report",
  "status": "implemented-validated-pending-koios-athena-review",
  "datetime": "20260711.150000Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "slice_name": "adr-json-authority-projectable-messy-canary-slice-3",
  "source_brief": "docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md",
  "source_decision": "docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md",
  "evidence_dir": "dev/adr-json-authority-projectable-messy-canary-slice-3/",
  "next_owner": "KOIOS_ATHENA_REVIEW"
}
```

# Implementation report 20260711.150000: ADR JSON authority projectable messy canary slice 3

## Summary

Implemented Slice 3 as candidate-only evidence for exactly one source:

```text
docs/adr/adr.adr-template-contract.md
```

The slice produced projectable messy-canary evidence under:

```text
dev/adr-json-authority-projectable-messy-canary-slice-3/
```

Outcome:

```text
projectable_candidate_blocked_pending_template_contract_and_status_review
```

## Implemented changes

- Added `AdrProjectableMessyCanaryRunner` and `run_adr_json_authority_projectable_messy_canary`.
- Exported the runner from `projectkoios.bootstrap.control_surface.adr`.
- Added focused tests for status-casing preservation, projection/parse-back safety, sidecar provenance, reviewed inventory preservation, source non-mutation, source wrapped-list preservation, and stable JSON artifacts.
- Corrected wrapped-list parsing after KOIOS provenance review found undisclosed lossiness in the source acceptance-criteria continuation line.
- Regenerated Slice 3 evidence artifacts:
  - `manifest.json`
  - `candidate-object.json`
  - `generated-projection.md`
  - `projection-parseback-evidence.json`
  - `conversion-evidence.json`
  - `conflict-lossiness-report.json`
  - `sidecar-provenance.json`

## Evidence findings

- Exactly one source is in scope: `docs/adr/adr.adr-template-contract.md`.
- Source hash is preserved as `2876dfbe031105d383fa9e33cec7d5dd49cf569cea6f43eae59e8fa1da502895`.
- Observed Markdown status is preserved as `Accepted`.
- Normalized status candidate is recorded separately as `accepted` and marked review-only.
- Projection was generated only under the Slice 3 `dev/` evidence path and is visibly non-authoritative.
- Parse-back reads only the generated projection's embedded JSON record.
- Parse-back preserved status casing: `Accepted` remained `Accepted`.
- Projection/parse-back semantic equality for candidate fields is true, but it does not resolve review blockers.
- Source wrapped-list continuation is preserved in the content candidate: `Workflow-bound ADRs can render optional gate fields without losing schema consistency.`
- Template/schema-contract ambiguity remains explicit.
- Manual review remains blocking before any authority promotion.

## Authority boundaries preserved

No changes were made to:

- `docs/adr/`
- `docs/schemas/`
- ADR source Markdown status casing
- ADR source filenames or locations
- authoritative JSON ADR records
- database/storage authority
- corpus conversion or authority cutover

Generated projection evidence is not a replacement source and does not authorize status normalization or JSON authority promotion.

## KOIOS blocker correction

KOIOS provenance review found that the original Slice 3 evidence dropped the continuation `consistency.` from this source acceptance-criteria item:

```text
- Workflow-bound ADRs can render optional gate fields without losing schema
  consistency.
```

VULCAN corrected the list parser to preserve wrapped continuation lines, added a focused regression assertion, regenerated all Slice 3 evidence, and reran validation. The candidate/projection evidence now records:

```text
Workflow-bound ADRs can render optional gate fields without losing schema consistency.
```

The existing status-casing, template/schema-contract, manual-review, candidate-only, and no-authority blockers remain preserved.

## Validation

From repository root:

```bash
uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q
```

Passed: `30 passed in 0.27s`.

```bash
uv run mypy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `Success: no issues found in 21 source files`.

```bash
uv run projectkoios bootstrap validate-python-policy src/python/projectkoios/bootstrap/control_surface/adr tests/projectkoios/bootstrap/control_surface_adr
```

Passed: `summary: 0 finding(s), 21 file(s)`.

```bash
find dev/adr-json-authority-projectable-messy-canary-slice-3 -name '*.json' -print -exec uv run python -m json.tool {} \; >/dev/null
```

Passed.

```bash
find dev/adr-json-authority-projectable-messy-canary-slice-3 \( -name '*.sqlite' -o -name '*.db' \) -print
```

Passed: no output.

```bash
git status --short -- docs/adr docs/schemas
```

Passed: no output.

```bash
find dev/adr-json-authority-projectable-messy-canary-slice-3 -name 'generated-projection.md' -print
```

Passed: only `dev/adr-json-authority-projectable-messy-canary-slice-3/generated-projection.md`.

```bash
git diff --check
```

Passed.

## Next required review

Pause for:

1. KOIOS provenance review focused on status-casing preservation, template-contract/manual-review blockers, projection safety, and evidence-vs-authority clarity.
2. ATHENA architecture/conformance review focused on brief conformance and no-authority boundaries.

HERMES acceptance should wait for those reviews. This implementation does not authorize corpus dry-run, source mutation, schema publication, JSON authority cutover, bulk conversion, or migration.
