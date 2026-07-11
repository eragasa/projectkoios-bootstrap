```json
{
  "title": "HERMES decision: ADR template/schema contract successor planning slice 10",
  "artifact_type": "workflow-decision",
  "status": "approved-for-athena-handoff",
  "datetime": "20260711.173500Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-successor-planning-slice-10",
  "source_acceptance": "docs/reviews/hermes-acceptance.20260711.172000_schema-family-doc-index-clarification-slice-9.md",
  "next_owner": "ATHENA"
}
```

# HERMES decision 20260711.173500: ADR template/schema contract successor planning slice 10

## Decision

HERMES approves `adr-template-schema-contract-successor-planning-slice-10` for ATHENA handoff.

## Rationale

Slice 9 recommended a source-facing planning step for `docs/adr/adr.adr-template-contract.md`. The next coherent action is not for HERMES to draft the Athena-owned successor plan directly, but to hand the bounded architecture/planning slice to ATHENA.

## Handoff target

ATHENA should produce one proposal-only planning brief for a future successor template/schema contract.

Suggested output path:

```text
docs/plans/successor-brief.20260711.172500_adr-template-schema-contract.md
```

## Approved planning scope

Primary target source:

```text
docs/adr/adr.adr-template-contract.md
```

Planning inputs:

```text
docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md
docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md
docs/reviews/hermes-acceptance.20260711.172000_schema-family-doc-index-clarification-slice-9.md
docs/schemas/README.md
docs/adr/adr.adr-lifecycle.20260705.011836Z.md
```

## Required ATHENA output content

ATHENA should define what a future successor ADR/template-schema contract draft should contain without creating that draft yet.

The brief should specify:

- intended future draft path and status;
- source/provenance relationship to `docs/adr/adr.adr-template-contract.md`;
- exact authority boundaries for current content schema, record envelope, Markdown source/control, projections, `routing`, `dcn`, and `workflow_binding`;
- acceptance criteria for a future ADR-creation slice;
- explicit exclusions and owner decisions required before supersession, source mutation, schema edits, migration, or cutover.

## Boundaries

This HERMES decision does not authorize HERMES to produce the ATHENA planning artifact directly.

This decision also does not authorize creating a new ADR draft under `docs/adr/`, editing `docs/adr/`, editing `docs/schemas/`, changing source status or casing, supersession, acceptance, activation, rejection, promotion, demotion, file moves/renames/deletes/archives/splits, JSON conversion/projection generation, generated projection replacement, authoritative JSON ADR records, database/storage authority, migration, or cutover.

## Required closeout for ATHENA output

ATHENA/HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```
