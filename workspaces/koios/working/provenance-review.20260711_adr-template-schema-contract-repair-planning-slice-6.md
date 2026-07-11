```json
{
  "title": "KOIOS provenance review: ADR template/schema contract repair planning slice 6",
  "artifact_type": "provenance-review",
  "status": "review-complete-provenance-adequate-with-minor-watchpoints",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-repair-planning-slice-6",
  "reviewed_artifact": "docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md"
}
```

# KOIOS provenance review: ADR template/schema contract repair planning slice 6

## Verdict

KOIOS verdict: **provenance-adequate for HERMES acceptance/packaging as proposal-only repair planning, with minor watchpoints**.

The repair plan's source claim inventory and support/staleness classifications are grounded in current control sources. The recommended successor-proposal path is provenance-safe because it avoids in-place mutation of the accepted-like source and preserves explicit future owner decisions for lifecycle/status/supersession/schema authority.

## Reviewed artifacts

- Repair plan: `docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md`
- ATHENA brief: `docs/plans/architecture-brief.20260711.155500_adr-template-contract-repair-planning-slice-6.md`
- HERMES decision: `docs/reviews/hermes-decision.20260711.160000_adr-template-schema-contract-repair-planning-slice-6.md`
- KOIOS input: `workspaces/koios/working/next-proof-input.20260711_template-schema-contract-repair-planning.md`
- Spot-checked sources: `docs/adr/adr.adr-template-contract.md`, `docs/adr/adr.adr.md`, `docs/schemas/adr.schema.json`, Slice 5 acceptance/review evidence, and current git status/diff checks.

## Provenance adequacy findings

- The plan covers exactly one target source: `docs/adr/adr.adr-template-contract.md`.
- The plan identifies the source as proposal/planning-only and explicitly denies source mutation, status normalization, lifecycle change, supersession, schema change, JSON/projection generation, migration, and cutover.
- The claim inventory addresses the expected risk claims: `Accepted` casing, JSON-vs-Markdown source-of-truth, `dcn`, `routing`, `workflow_binding`, schema canonicality, and mixed template/schema/decision role.
- The recommended primary path, a future successor template/schema contract proposal, is safer than in-place mutation and is consistent with prior Slice 5 semantic rationalization.

## Claim-support spot checks

KOIOS spot-checked the main classifications:

- **Status casing `Accepted`**: source has `## Status` value `Accepted`; current schema status enum is lowercase `proposal`, `draft`, `accepted`, `active`, `superseded`. Classification as `requires_owner_decision` and instruction to preserve observed casing is supported.
- **`routing` stale against schema**: `adr.adr-template-contract.md` lists `routing` as schema content and has a `## routing` section; current `docs/schemas/adr.schema.json` has no top-level `routing` property. Classification as stale/ahead-of-authority is supported.
- **`workflow_binding`**: current schema includes optional `workflow_binding`; plan's `current_with_boundary` classification is supported.
- **`dcn`**: `docs/adr/adr.adr.md` defines DOC CONTROL NUMBER and says `dcn` is the canonical record, while current `docs/schemas/adr.schema.json` has no top-level `dcn`. Classification as ambiguous/stale against current schema is supported.
- **JSON-vs-Markdown source-of-truth**: `adr.adr-template-contract.md` declares Markdown derived from JSON; current JSON-authoritative ADR work remains staged and no cutover/migration has occurred. Classification as partly current / ahead of authority is supported.
- **Mixed role**: the file combines ADR decision, template/schema contract, renderer/projection/source-of-truth policy, and workflow binding claims. The plan's mixed-role classification is supported by the source and Slice 5 review.

## Boundary review

The plan preserves required boundaries:

- no edit to `docs/adr/adr.adr-template-contract.md`;
- no edit to other ADR sources;
- no status normalization or lifecycle transition;
- no formal supersession, acceptance, activation, rejection, promotion, or demotion;
- no schema edit;
- no JSON conversion/projection generation;
- no generated projection replacement;
- no database/storage authority;
- no migration or JSON authority cutover.

KOIOS ran/observed:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Both produced no output / passed.

## Minor watchpoints

1. The phrase "current `docs/schemas/adr.schema.json` is the ADR content-shape schema surface" is acceptable for planning, but HERMES acceptance should avoid implying schema publication or JSON authority cutover beyond existing staged decisions.

2. If the next slice drafts `docs/adr/adr.adr-template-schema-contract.draft.md`, HERMES/USER should explicitly decide whether creating a new draft ADR is allowed in that slice. The stable semantic draft path reflects the current no-timestamp ADR filename convention; the Slice 6 plan only recommends future draft creation and does not authorize file creation.

3. The `dcn` decision may need coordination with `docs/adr/adr.adr.md` and schema authority. Do not resolve `dcn` by silently adding it to `docs/schemas/adr.schema.json` or by dropping it from namespace guidance.

4. The plan correctly prefers a successor proposal, but the old file's eventual relationship must remain explicit: retained source/provenance, accepted historical evidence, or formally superseded only after a later approved lifecycle decision.

## Unsupported-claim check

KOIOS did not find a blocking unsupported claim. The plan's support/staleness classifications are grounded in the target source, current schema, ADR namespace authority, Slice 5 semantic review, and JSON-authority staged-boundary context.

## KOIOS recommendation to HERMES

HERMES may accept/package Slice 6 as proposal-only repair planning. Acceptance should explicitly preserve that this plan does not authorize source edits, status normalization, supersession, schema changes, JSON conversion/projection generation, generated projection replacement, JSON authority/cutover, database/storage authority, or any repair execution.
