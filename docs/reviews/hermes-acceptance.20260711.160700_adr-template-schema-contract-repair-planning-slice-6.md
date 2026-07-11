```json
{
  "title": "HERMES acceptance: ADR template/schema contract repair planning slice 6",
  "artifact_type": "completion-decision",
  "status": "accepted-proposal-only-with-watchpoints",
  "datetime": "20260711.160700Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-repair-planning-slice-6",
  "repair_plan": "docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md",
  "athena_brief": "docs/plans/architecture-brief.20260711.155500_adr-template-contract-repair-planning-slice-6.md",
  "hermes_decision": "docs/reviews/hermes-decision.20260711.160000_adr-template-schema-contract-repair-planning-slice-6.md",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_template-schema-contract-repair-planning.md",
  "koios_review": "workspaces/koios/working/provenance-review.20260711_adr-template-schema-contract-repair-planning-slice-6.md",
  "vulcan_implementation_reality": "docs/reviews/implementation-reality.20260711_adr-template-schema-contract-repair-planning-slice-6.md",
  "next_owner": "HERMES_OR_USER"
}
```

# HERMES acceptance 20260711.160700: ADR template/schema contract repair planning slice 6

## Decision

HERMES accepts `adr-template-schema-contract-repair-planning-slice-6` as proposal-only repair planning.

## Accepted scope

This acceptance covers exactly one target source:

```text
docs/adr/adr.adr-template-contract.md
```

Accepted repair plan:

```text
docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md
```

This acceptance does not execute repair, mutate source, change lifecycle state, or create a successor ADR.

## Accepted recommendation

HERMES accepts the repair plan recommendation as proposal input:

- Primary next path: draft a successor ADR/template-schema contract proposal in a future approved slice.
- Fallback path: produce a review-only errata/reconciliation note first if HERMES/USER wants lower-risk staging.
- Do not mutate `docs/adr/adr.adr-template-contract.md` in place as the first repair action.

## Accepted findings

- Observed source status is `Accepted`; casing must be preserved and not normalized as a side effect.
- `routing` claims in the source are stale or ahead-of-authority relative to current `docs/schemas/adr.schema.json`, which lacks a top-level `routing` property.
- Markdown-as-derived / JSON-source-of-truth claims are ahead of current repository authority because JSON authority remains staged and no cutover has occurred.
- `dcn` is supported by `docs/adr/adr.adr.md` but ambiguous against current `docs/schemas/adr.schema.json`, which lacks a top-level `dcn` property.
- Optional `workflow_binding` is supported by current schema but must remain bounded.
- The target file is a mixed template/schema contract, renderer/projection/source-of-truth policy, and decision record; it is not a clean ordinary ADR decision.

## Acceptance basis

HERMES reviewed the ATHENA repair plan, ATHENA brief, HERMES routing decision, KOIOS provenance input, KOIOS provenance review, and VULCAN implementation-reality check.

KOIOS found the plan provenance-adequate for acceptance/packaging as proposal-only repair planning with minor watchpoints. HERMES incorporates those watchpoints here:

- Do not treat the current schema as broader published/cutover JSON authority beyond existing staged decisions.
- A future successor draft file must be explicitly authorized by HERMES/USER; Slice 6 only recommends it.
- `dcn` disposition requires explicit coordination with `docs/adr/adr.adr.md` and schema authority.
- The old file's future relationship must be explicit: retained source/provenance, accepted historical evidence, or formally superseded only by later approved lifecycle decision.

VULCAN implementation-reality input supports the repair plan. Current code/schema/tooling does not treat `routing` as ADR content, does not implement `dcn`, supports `workflow_binding` only as optional schema content without operational workflow use, and treats hand-authored Markdown as source/control material while generated projections remain non-authoritative `dev/` evidence.

## Validation

ATHENA and KOIOS reported, and HERMES observed, that no source ADRs, schemas, Slice 4 evidence, or code were intentionally modified by the planning slice.

Validation commands:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Both passed / produced no output.

## Watchpoints

This acceptance is proposal-only and does not authorize:

- editing `docs/adr/adr.adr-template-contract.md`;
- editing any source ADR;
- status normalization or lifecycle state changes;
- formal supersession, acceptance, activation, rejection, promotion, or demotion;
- schema changes;
- file moves, renames, deletes, archives, or splits;
- JSON conversion or projection generation;
- generated projection replacement;
- authoritative JSON ADR records;
- database/storage authority;
- migration or JSON authority cutover;
- creating a successor ADR draft without a future explicit approval.

A future successor proposal brief should explicitly distinguish current ADR content schema fields from envelope/sidecar metadata; `routing` as current sidecar/provenance rather than schema content; `dcn` as unresolved namespace/control metadata; optional `workflow_binding` as schema-supported but not workflow authority; Markdown source/control for unmigrated records versus generated projection evidence; and observed `Accepted` versus schema-valid `accepted`.

## Recommended next decision

The highest-leverage follow-up is the primary path recommended by ATHENA and cleared by KOIOS:

```text
adr-template-schema-contract-successor-proposal-slice-7
```

That future slice should be explicitly authorized before creating any new draft/proposal file and should define current ADR content-schema truths versus future JSON authority target, `routing` disposition, `dcn` disposition, optional `workflow_binding` boundary, and the relationship to `docs/adr/adr.adr-template-contract.md`.
