```json
{
  "title": "Reconciliation proposal: ADR schema-family contract",
  "artifact_type": "reconciliation-proposal",
  "status": "proposal-only",
  "datetime": "20260711.170000Z",
  "acting_as": "ATHENA",
  "delegated_operator": "HERMES/pi",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-schema-family-contract-reconciliation-slice-8",
  "source_decision": "docs/reviews/hermes-decision.20260711.170500_adr-schema-family-contract-reconciliation-slice-8.md",
  "source_plan": "docs/plans/repair-plan.20260711.165300_schema-family-adr-contract-slice-7.md",
  "authority_change": false,
  "source_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# Reconciliation proposal 20260711.170000: ADR schema-family contract

## Proposal status

This is a non-mutating reconciliation proposal. It does not change repository authority by itself.

It proposes the contract boundary that should govern future ADR schema-family repair slices.

## Problem statement

Current ADR schema-family surfaces are internally useful but not yet cleanly layered:

- `docs/schemas/adr.schema.json` is a flat ADR content-shape schema.
- `docs/schemas/schema.record-base.json` and `docs/schemas/adr-draft.schema.json` express a newer `metadata` + `content` record-envelope pattern.
- `docs/schemas/adr-active.schema.json` preserves an older ADR record schema candidate with legacy identity and shape.
- `docs/adr/adr.adr-template-contract.md` says Markdown is already derived from JSON and lists fields such as `routing` and `dcn` as canonical template/schema content, but current schemas/tooling do not support those claims as current content authority.
- `docs/adr/adr.json-authoritative-adr-store.draft.md` accepts JSON authority only as staged direction after explicit migration gates, not as current cutover.

Without a contract boundary, future implementation or migration slices could silently choose whether status, routing, dcn, projections, and provenance belong in content, metadata, sidecars, or legacy source evidence.

## Proposed layer contract

### Layer 1: ADR content schema

`docs/schemas/adr.schema.json` should be treated as the current ADR **content-shape** schema until a future approved schema-change slice replaces, wraps, or retires it.

The content schema owns fields that are part of the decision body or its rendered ADR sections, including current fields such as:

- `title`
- `status` as current flat-schema lifecycle value until envelope reconciliation is implemented
- `context`
- `decision`
- `consequences`
- `architecture_spec`
- `acceptance_criteria`
- `implementation_brief`
- `resolved_open_questions`
- `non_goals`
- `validation_expectations`
- `links`
- optional `workflow_binding`

It must not be assumed to own `routing`, `dcn`, source hashes, projection metadata, source/candidate disposition, migration conflict state, or unsupported-field preservation unless a future schema-change slice explicitly adds those fields.

### Layer 2: schema-backed record envelope

`docs/schemas/schema.record-base.json` should be treated as the current draft direction for a schema-backed record envelope.

The envelope owns record identity, schema identity/versioning, provenance, derivation, evidence, projections, repository/domain typing, and source-of-truth metadata.

The envelope should remain exactly two top-level keys unless changed later:

```text
metadata
content
```

Family schemas such as `adr-draft.schema.json` should constrain `content` and may narrow metadata constants such as `schema_id` and `status`.

### Layer 3: rendered/source Markdown

Markdown under `docs/adr/` remains source/control for unmigrated records unless a later accepted migration/cutover decision changes the specific file's disposition.

Generated Markdown projections are evidence or review/navigation surfaces unless and until a cutover package marks them as generated projections for migrated records.

Markdown files must not be overwritten, generated, moved, renamed, or demoted by implication from this proposal.

### Layer 4: sidecar/provenance evidence

Unsupported or out-of-contract source material should be preserved in sidecar/provenance evidence rather than forced into ADR content.

This includes source hashes, observed source status/casing, omitted source sections, conversion warnings, unsupported fields, inferred fields and rationale, generated projection hashes, and migration conflict classifications.

### Layer 5: migration/cutover authority

JSON authority remains staged direction only until the gates in `docs/adr/adr.json-authoritative-adr-store.draft.md` are satisfied and HERMES/USER accepts a cutover package.

Review-only `dev/` evidence, candidate JSON, generated projections, and dry-run records are not durable authority by themselves.

## Status placement proposal

Current safe rule:

- Preserve observed source status/casing exactly in source/provenance evidence.
- Use canonical lifecycle vocabulary from `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` for normalized candidates: `proposal`, `draft`, `accepted`, `active`, `superseded`.
- Do not normalize source Markdown status as a side effect of schema-family repair.

Future envelope rule to decide in a schema-change slice:

- Prefer `metadata.status` as the canonical record lifecycle status for schema-backed records.
- If ADR `content.status` remains for flat-schema compatibility or rendering, it must mirror `metadata.status` and any mismatch must be a validation error or blocked migration conflict.
- Generated projections may render status from the canonical record status but must preserve original observed source status/casing in provenance when migrated from Markdown.

This proposal does not edit schemas to implement that rule.

## `routing` disposition proposal

`routing` should not be treated as current ADR content-schema data.

Future repair should choose one of these explicit dispositions:

1. `legacy_source_only`: keep old `routing` prose/sections only as historical source evidence.
2. `sidecar_provenance`: preserve parsed routing values in migration sidecars/evidence.
3. `workflow_metadata`: map routing-like intent into a workflow-specific metadata surface only after a workflow authority decision.
4. `record_envelope_metadata`: add a bounded routing/provenance field to a record envelope only through a schema-change slice.
5. `excluded`: record that routing is not migrated into current records.

Recommended default: preserve `routing` as sidecar/provenance evidence, not content schema, until a separate workflow/envelope decision promotes a replacement.

## `dcn` disposition proposal

`dcn` should be treated as unresolved namespace/control metadata.

Future repair should decide whether `dcn` is:

1. alias or predecessor of `metadata.record_id`;
2. a filename/title convention governed by ADR naming policy;
3. a separate metadata field on schema-backed ADR records;
4. a content field in the ADR payload;
5. deferred legacy terminology retained only in older source/provenance.

Recommended default: map current identity needs to `metadata.record_id` / filename conventions and preserve `dcn` mentions as legacy namespace guidance until a dedicated namespace/schema decision is approved.

## `workflow_binding` boundary proposal

`workflow_binding` is currently schema-supported optional content in `docs/schemas/adr.schema.json`.

It should remain documentary/schema content unless a later workflow authority decision gives it operational semantics.

No current repair slice should imply that Petri-net workflow runtime, ADR lifecycle state, or operator-console state is controlled by `workflow_binding`.

## Legacy schema marker proposal

`docs/schemas/adr-active.schema.json` should be treated as a compatibility/reconciliation candidate.

Future schema repair should either:

1. wrap it under the base envelope;
2. replace it with a new active-ADR family schema;
3. retire it as a legacy marker with documented old/new mapping; or
4. preserve it temporarily only for compatibility tests.

Its legacy `$id` value should not be silently treated as the final project-local schema identity.

## Template contract disposition proposal

Do not mutate `docs/adr/adr.adr-template-contract.md` in place as the first repair.

After this reconciliation proposal is accepted, the next source-facing repair should be one of:

1. a successor template/schema contract ADR proposal under an explicitly approved ADR-creation slice;
2. a non-mutating errata/index note warning readers about stale/ahead-of-authority claims;
3. a lifecycle/source-disposition slice deciding whether the old template contract is retained as historical source, linked as provenance, or formally superseded.

Recommended default: draft a successor ADR/template-schema contract only after HERMES/USER explicitly approves ADR creation and lifecycle relation handling.

## Future staged repair sequence

### Stage A: accept or revise this reconciliation proposal

Owner: HERMES/USER.

Effect: proposal-only. No source/schema mutation.

### Stage B: documentation/index clarification

Owner: ATHENA, with HERMES approval.

Possible outputs:

- update `docs/schemas/README.md` to state content-schema vs envelope-schema layering;
- add a non-mutating errata/reconciliation note for `adr.adr-template-contract.md`;
- record legacy marker handling for `adr-active.schema.json`.

Requires explicit doc-edit approval.

### Stage C: schema-change slice

Owner: ATHENA for schema authority; VULCAN if implementation/tests are included.

Possible outputs:

- new ADR record-envelope schema;
- explicit `metadata.status` / `content.status` rule;
- replacement or retirement path for `adr-active.schema.json`;
- `$id` and versioning update.

Requires explicit `docs/schemas/` mutation approval.

### Stage D: successor template/schema contract

Owner: ATHENA, with HERMES/USER lifecycle approval.

Possible outputs:

- successor ADR draft or proposal for ADR template/schema/source/projection contract;
- explicit relation to old `docs/adr/adr.adr-template-contract.md`;
- no supersession/status mutation unless separately approved.

### Stage E: implementation/migration continuation

Owner: VULCAN for implementation; KOIOS for provenance; HERMES for acceptance.

Possible outputs:

- renderer/ingester implementation brief and patch;
- dry-run evidence using settled schema/envelope boundaries;
- migration package only after JSON-authority gates are met.

## Proposed next action after this proposal

If HERMES accepts this proposal, the next highest-leverage bounded action is:

```text
schema-family-doc-index-clarification-slice-9
```

Purpose: edit only planning/control documentation, not schemas or ADR source authority, to make the content-schema vs envelope-schema boundary visible to readers.

Alternative: if USER wants to move directly toward source repair, approve a successor template/schema contract ADR creation slice instead.

## Non-goals

This proposal does not:

- edit `docs/adr/`;
- edit `docs/schemas/`;
- create a new ADR draft;
- normalize status casing;
- supersede or retire any source;
- generate JSON records or projections;
- replace Markdown authority;
- add database/storage authority;
- run migration or cutover.

## Validation expectations

HERMES closeout should verify:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result: no source/schema/dry-run evidence mutation and clean whitespace validation.
