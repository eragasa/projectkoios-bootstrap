```json
{
  "title": "KOIOS provenance review: ADR JSON authority projectable messy canary slice 3",
  "artifact_type": "provenance-review",
  "status": "review-complete-provenance-adequate",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-projectable-messy-canary-slice-3",
  "reviewed_evidence_dir": "dev/adr-json-authority-projectable-messy-canary-slice-3/"
}
```

# KOIOS provenance review: ADR JSON authority projectable messy canary slice 3

## Verdict

KOIOS verdict: **provenance-adequate for HERMES final acceptance consideration, with no-authority boundaries preserved**.

This supersedes the earlier KOIOS acceptance blocker for Slice 3. VULCAN corrected the wrapped-list continuation lossiness, regenerated evidence, and updated the implementation report. KOIOS re-reviewed the corrected evidence and no longer sees the previous source-to-candidate lossiness blocker.

## Reviewed sources

- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_adr-json-authority-after-messy-canary-slice-2.md`
- Brief: `docs/plans/implementation-brief.20260711.145300_adr-json-authority-projectable-messy-canary-slice-3.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.145600_adr-json-authority-projectable-messy-canary-slice-3.md`
- VULCAN report: `docs/implementation/adr-json-authority-projectable-messy-canary-slice-3.20260711.150000.md`
- Evidence directory: `dev/adr-json-authority-projectable-messy-canary-slice-3/`
- Source: `docs/adr/adr.adr-template-contract.md`

## Correction verified

Earlier KOIOS review found that this source acceptance-criteria item lost the wrapped continuation `consistency.` during source-to-candidate conversion:

```text
- Workflow-bound ADRs can render optional gate fields without losing schema
  consistency.
```

Corrected `candidate-object.json` and `generated-projection.md` now preserve it as:

```text
Workflow-bound ADRs can render optional gate fields without losing schema consistency.
```

The implementation report also records the correction and the added wrapped-list preservation test. KOIOS considers the previous acceptance blocker resolved.

## Validation observed by KOIOS

During re-review, KOIOS observed:

- Source hash matched expected value: `2876dfbe031105d383fa9e33cec7d5dd49cf569cea6f43eae59e8fa1da502895`.
- `git status --short -- docs/adr docs/schemas` produced no output.
- All Slice 3 JSON files parsed successfully with `uv run python -m json.tool`.
- No `.sqlite` or `.db` files were found under `dev/adr-json-authority-projectable-messy-canary-slice-3/`.
- `git diff --check` passed.
- Focused test run passed: `uv run pytest tests/projectkoios/bootstrap/control_surface_adr -q` returned `30 passed`.

## Status-casing preservation

Status-casing handling is provenance-safe:

- Source `## Status` text is `Accepted`.
- Evidence preserves observed `Accepted` separately from normalized status candidate `accepted`.
- Normalization remains review-only / review-required.
- Source status was not rewritten.
- Projection parse-back preserves `Accepted` and reports `status_normalized_by_projection_or_parseback: false`.

## Template-contract and manual-review blockers

Template/schema-contract and manual-review blockers remain visible and unresolved:

- Reviewed category remains `template_schema_contract`.
- Reviewed disposition remains `manual_review_required`.
- `automatic_conversion_eligibility_candidate` remains `false`.
- Blocking reasons include `manual_review_required`, `template_schema_contract_ambiguity`, and `status_casing_or_text_would_normalize`.
- Outcome remains `projectable_candidate_blocked_pending_template_contract_and_status_review`.

## Projection safety and evidence-vs-authority clarity

Projection evidence is safely bounded for this slice:

- `generated-projection.md` is only under the dedicated Slice 3 `dev/` path.
- The projection begins with a non-authoritative generated-evidence warning.
- Metadata says authority mode is candidate evidence only, source mutation is false, schema change is false, and database authority is false.
- Parse-back evidence states `parseback_source: generated_projection_only`, `projection_introduced_authority: false`, and `projection_resolves_review_blockers: false`.
- Candidate/projection semantic equality is limited to candidate fields and does not resolve status-casing or template-contract authority questions.

## Residual watchpoints

- The evidence remains candidate-only and must not be promoted into JSON ADR authority without separate HERMES/USER/ATHENA decision.
- Template/schema-contract classification and status-casing normalization still require manual review before any authority promotion.
- Projection/parse-back equality should continue to be interpreted as evidence about this generated candidate only, not as corpus conversion readiness.
- The source contains existing prose/list oddities, including `fields.- The schema...`; Slice 3 preserves observed source text but does not resolve source cleanup or schema-contract policy.

## KOIOS recommendation to HERMES

HERMES may consider Slice 3 for final acceptance as a bounded, candidate-only, projectable messy-canary proof. Acceptance should explicitly preserve that this does not authorize corpus conversion, source mutation, schema publication/change, file moves/renames, status normalization, JSON authority cutover, database authority, or bulk migration.
