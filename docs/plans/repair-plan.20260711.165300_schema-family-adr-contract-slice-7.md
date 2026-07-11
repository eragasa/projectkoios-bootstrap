```json
{
  "title": "Repair plan: schema-family ADR contract slice 7",
  "artifact_type": "repair-plan",
  "status": "planning-review-complete-proposal-only",
  "datetime": "20260711.165300Z",
  "acting_as": "ATHENA",
  "delegated_operator": "HERMES/pi",
  "repository": "projectkoios-bootstrap",
  "scope": "schema-family-repair-planning-slice-7",
  "source_decision": "docs/reviews/hermes-decision.20260711.165218_schema-family-repair-planning-slice-7.md",
  "prior_slice": "docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md",
  "authority_change": false,
  "source_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# Repair plan 20260711.165300: schema-family ADR contract slice 7

## Verdict

Planning review complete. This artifact is proposal input only.

Recommended next concrete slice: **schema-base / ADR-contract reconciliation proposal**, not immediate schema mutation, source ADR mutation, projection replacement, migration, or authority cutover.

The highest-leverage repair is one ATHENA-authored successor/reconciliation proposal that defines the boundary between:

1. ADR content schema;
2. schema-backed record envelope;
3. source Markdown and generated projections;
4. sidecar/provenance evidence;
5. migration/cutover authority.

That proposal should then feed separate future slices for schema edits, source disposition/supersession, renderer/ingester behavior, and migration gates.

## Non-authority and non-mutation statement

This planning review does not edit `docs/adr/`, edit `docs/schemas/`, normalize source status or casing, change lifecycle state, supersede, accept, activate, reject, promote, demote, move, rename, delete, archive, split files, generate JSON records, generate or replace projections, add database/storage authority, migrate, or cut over authority.

All repair recommendations require separate HERMES/USER approval before execution.

## Scope reviewed

Approved Slice 7 surfaces:

```text
docs/adr/adr.adr-template-contract.md
docs/adr/adr.schema-base.md
docs/adr/adr.json-authoritative-adr-store.draft.md
docs/plans/schema-base-adr-records-workplan.md
docs/schemas/README.md
docs/schemas/adr.schema.json
docs/schemas/schema.record-base.json
docs/schemas/adr-draft.schema.json
docs/schemas/adr-active.schema.json
```

Context-only prior evidence:

- `docs/plans/repair-plan.20260711.155500_adr-template-schema-contract-slice-6.md`
- `docs/reviews/implementation-reality.20260711_adr-template-schema-contract-repair-planning-slice-6.md`
- `workspaces/koios/working/provenance-review.20260711_adr-template-schema-contract-repair-planning-slice-6.md`
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`

## Surface classification

| Surface | Current role | Support level | Repair relevance |
|---|---|---|---|
| `docs/schemas/adr.schema.json` | ADR content-shape schema | current but not full record envelope | Keep as content schema unless future slice replaces/renames it; do not force envelope metadata into it silently. |
| `docs/schemas/schema.record-base.json` | schema-backed record envelope | current draft/schema-family direction | Use for metadata/provenance/projection concepts; reconcile status vocabulary and relationship to content schema before implementation expansion. |
| `docs/schemas/adr-draft.schema.json` | draft ADR record-envelope family schema | draft/current candidate | Good composition pattern for future ADR record schemas; not a current migration/cutover authority. |
| `docs/schemas/adr-active.schema.json` | legacy/current ADR record schema candidate | compatibility/reconciliation marker | Preserve as candidate/legacy marker until reconciled into the base-envelope family or retired explicitly. |
| `docs/schemas/README.md` | schema namespace guide and migration table | current control surface for schema namespace | Keep as index/control, update only in a future approved schema-family doc slice. |
| `docs/adr/adr.schema-base.md` | draft architecture for base schema records | current draft architecture | Use as the primary architecture basis for envelope/provenance/projection repair. |
| `docs/plans/schema-base-adr-records-workplan.md` | workplan integrating reviews and concerns | planning/provenance | Use as source for unresolved/reconciled schema-family constraints, not as authority by itself. |
| `docs/adr/adr.json-authoritative-adr-store.draft.md` | accepted-staged-direction ADR proposal for JSON authority migration | staged direction only | Controls migration/cutover gates; does not change current Markdown authority or publish schemas by itself. |
| `docs/adr/adr.adr-template-contract.md` | accepted-like template/schema/source-of-truth contract | mixed/stale/ahead-of-authority | Do not mutate first; replace or reconcile through successor proposal and explicit lifecycle decision. |

## Current support summary

Supported/current:

- `docs/schemas/` is the durable namespace for machine-readable schema artifacts.
- `docs/schemas/adr.schema.json` defines an ADR content model with lowercase lifecycle status enum and optional `links` / `workflow_binding`.
- `docs/schemas/schema.record-base.json` defines a `metadata` + `content` envelope with provenance and projection metadata.
- `docs/schemas/adr-draft.schema.json` demonstrates the intended `$ref` + `allOf` family-schema composition path.
- `docs/adr/adr.schema-base.md` and `docs/schemas/README.md` distinguish schema-backed records from Markdown render/projection surfaces.
- `docs/adr/adr.json-authoritative-adr-store.draft.md` defines staged migration gates and preserves Markdown authority for unmigrated records.

Stale/ahead-of-authority:

- `docs/adr/adr.adr-template-contract.md` says Markdown is a derived rendering of JSON as if that is already universal current authority; current authority remains source/control Markdown for unmigrated records.
- `docs/adr/adr.adr-template-contract.md` lists `routing` as ADR content schema, but `docs/schemas/adr.schema.json` has no top-level `routing` and `additionalProperties: false`.
- `docs/adr/adr.adr-template-contract.md` treats `dcn` as part of the template/schema contract, but current ADR content schema and Python tooling do not implement `dcn`.
- `docs/schemas/adr-active.schema.json` still carries legacy `$id` value `adr.schema-adr.json`, so its identity is not yet reconciled with the project-local `$id` strategy used by newer schemas.

Ambiguous/mixed:

- `status` appears in both the old content schema and the base record metadata model; future record-envelope design must decide whether ADR lifecycle status lives in metadata, content, or both with a strict mirroring rule.
- `routing` could be legacy prose, record-envelope metadata, workflow metadata, sidecar/provenance evidence, or intentionally excluded source material.
- `dcn` could be namespace guidance, metadata identity, content field, filename convention, or deferred compatibility concept.
- `workflow_binding` exists in ADR content schema but is not operational workflow authority.
- `docs/adr/adr.adr-template-contract.md` combines template, schema contract, source-of-truth policy, rendering statement, and ADR decision roles.

## Contradiction inventory

| Topic | Conflict | Current safe interpretation | Required future decision |
|---|---|---|---|
| Content schema vs envelope schema | `adr.schema.json` is a flat ADR content object; `schema.record-base.json` and `adr-draft.schema.json` use `metadata` + `content`. | Treat `adr.schema.json` as current content-shape schema and base schemas as record-envelope direction. | Decide whether a successor ADR-family record schema wraps/replaces flat content schema or keeps both as separate layers. |
| Markdown authority | Template contract says Markdown is derived; migration ADR says this is future after gates. | Markdown remains source/control for unmigrated records; generated projections are evidence unless cutover accepted. | Define per-category Markdown disposition and projection markers before migration. |
| Status placement | ADR content schema has top-level `status`; record-base metadata also has `metadata.status`. | Preserve current observed statuses and do not normalize by implication. | Decide canonical record status location and any mirroring/normalization rule. |
| Status vocabulary | Lifecycle ADR uses `proposal`, `draft`, `accepted`, `active`, `superseded`; schema-base workplan mentions older `proposed`, `completed`, `rejected`; current base schema uses canonical five values. | Canonical current vocabulary is the five lifecycle states unless changed later. | Reconcile stale workplan language by note/update, not by schema mutation in this slice. |
| `routing` | Template contract lists it as schema field; current schema excludes it; tooling preserves it outside content. | `routing` is not current ADR content schema. | Decide legacy-only vs sidecar/provenance vs envelope/workflow field. |
| `dcn` | Namespace ADR mentions DOC CONTROL NUMBER; current schema/tooling omit it. | `dcn` is unresolved namespace/control metadata. | Decide whether it maps to `record_id`, filename convention, metadata field, content field, or deferred guidance. |
| `workflow_binding` | Schema supports optional field; workflow runtime does not operationally use it. | Optional content extension only. | Decide whether workflow authority ever consumes it, or keep it documentary. |
| Legacy schema markers | `adr-active.schema.json` differs from newer `$id`/envelope strategy. | Candidate/compatibility marker, not co-authoritative base-family schema. | Reconcile, retire, or wrap in a future schema-family slice. |

## Repair options evaluated

### Option A: Immediate successor for only `adr.adr-template-contract.md`

Assessment: safer than in-place mutation, but narrower than the USER-selected option.

Pros:

- Directly resolves the stale accepted-like template contract.
- Preserves old source as provenance until lifecycle relation is decided.

Cons:

- Risks solving `routing`, `dcn`, projection, and status placement locally before schema-family boundaries are decided.
- May require immediate supersession/lifecycle decisions.

Use after a schema-family reconciliation proposal, not as the first Slice 7 follow-up.

### Option B: Non-mutating errata/index note

Assessment: low-risk interim fallback.

Pros:

- Warns readers about stale/ahead-of-authority claims without source mutation.
- Useful if HERMES/USER wants no successor ADR yet.

Cons:

- Does not settle schema-family boundaries.
- Adds another surface readers must discover.

Use only if HERMES/USER wants temporary documentation before the main reconciliation proposal.

### Option C: Schema-base / ADR-contract reconciliation proposal

Assessment: recommended.

Pros:

- Matches USER-selected broader schema-family planning.
- Settles layer boundaries before source/schema mutation.
- Can explicitly decide which future slices create successor ADRs, schema edits, source disposition, and migration gates.
- Preserves current Markdown authority and staged JSON cutover boundaries.

Cons:

- Requires a future separate execution slice before any concrete repair.

Recommended.

### Option D: Direct schema edits under `docs/schemas/`

Assessment: not safe as next step.

Pros:

- Could make schemas internally consistent quickly.

Cons:

- Would silently choose status placement, `routing`, `dcn`, and envelope/content semantics.
- Violates Slice 7 planning-only boundary.

Do not use without a future HERMES/USER-approved schema-change slice.

### Option E: Migration/cutover preparation

Assessment: premature.

Pros:

- Advances JSON-authoritative ADR end state.

Cons:

- Migration gates require schema authority decisions and per-record disposition first.
- Known stale/mixed template-schema claims could contaminate migration assumptions.

Defer until after schema-family reconciliation and accepted migration package gates.

## Recommended staged repair sequence

### Stage 1: schema-family reconciliation proposal

Owner: ATHENA.

Output options:

```text
docs/plans/reconciliation-proposal.<timestamp>_adr-schema-family-contract.md
```

or, if HERMES/USER approves ADR creation in that slice:

```text
docs/adr/adr.adr-schema-family-contract.<timestamp>.draft.md
```

Required decisions:

- define `adr.schema.json` as content schema, legacy schema, or payload under a record envelope;
- define record-envelope schema relationship to ADR content schemas;
- decide canonical status location and allowed mirroring rule;
- classify `routing`, `dcn`, and `workflow_binding`;
- define projection/source-authority language that respects migration gates;
- name the future disposition path for `adr.adr-template-contract.md`.

No schema/source mutation in Stage 1 unless separately approved.

### Stage 2: schema docs / README reconciliation

Owner: ATHENA, with HERMES approval.

Potential outputs:

- update `docs/schemas/README.md`;
- update or create a schema-family architecture note;
- document legacy marker status for `adr-active.schema.json` and old `$id` values.

This stage may edit docs only if explicitly approved.

### Stage 3: machine-readable schema repair

Owner: ATHENA for schema authority and VULCAN for implementation if code/tests are involved.

Potential outputs:

- new or revised ADR record-envelope schema;
- compatibility or retirement plan for `adr-active.schema.json`;
- explicit versioning and `$id` policy;
- tests/validation if implementation changes occur.

Requires separate HERMES/USER-approved schema-change slice.

### Stage 4: template contract source disposition

Owner: ATHENA for lifecycle/source proposal, HERMES for cross-domain acceptance.

Potential outputs:

- successor template/schema contract ADR;
- explicit `supersedes` / `superseded_by` relation if approved;
- retained source/provenance decision for `docs/adr/adr.adr-template-contract.md`;
- optional non-mutating errata/index note if source mutation remains deferred.

Requires explicit lifecycle/source mutation approval before editing the old source.

### Stage 5: renderer/ingester and migration proof continuation

Owner: VULCAN for implementation, KOIOS for provenance review, HERMES for acceptance.

Potential outputs:

- implementation brief after schema-family contract is settled;
- round-trip renderer/ingester tests;
- dry-run corpus evidence that uses the settled schema/envelope boundaries;
- no authority cutover until Phase 4/5 migration gates from the JSON-authority ADR are met.

## Recommended next concrete slice

Recommended next slice: **Stage 1 schema-family reconciliation proposal**.

Suggested HERMES decision name:

```text
adr-schema-family-contract-reconciliation-slice-8
```

Suggested output:

```text
docs/plans/reconciliation-proposal.20260711.170000_adr-schema-family-contract.md
```

Scope should include the same Slice 7 surfaces and may additionally cite `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` for status vocabulary. It should not edit `docs/adr/`, `docs/schemas/`, generate projections, or run migration unless separately approved.

## Future owner decisions required

HERMES/USER must approve before any of the following:

- creating a new ADR draft under `docs/adr/`;
- editing `docs/adr/adr.adr-template-contract.md`;
- changing lifecycle status, status casing, or supersession links;
- editing any JSON schema under `docs/schemas/`;
- retiring, renaming, replacing, or wrapping `adr-active.schema.json`;
- adding `routing` or `dcn` to any schema;
- changing `workflow_binding` from optional content to operational workflow authority;
- generating or replacing Markdown projections;
- creating authoritative JSON ADR records;
- migrating or cutting over authority;
- promoting database/storage authority.

## Closeout checks

Required planning-only validation:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Expected result: no `docs/adr`, `docs/schemas`, or dry-run evidence mutations, and whitespace check clean.
