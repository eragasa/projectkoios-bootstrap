```json
{
  "title": "Repair plan: ADR template/schema contract slice 6",
  "artifact_type": "repair-plan",
  "status": "planning-review-complete-proposal-only",
  "datetime": "20260711.160500Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-template-schema-contract-repair-planning-slice-6",
  "target_source": "docs/adr/adr.adr-template-contract.md",
  "source_brief": "docs/plans/architecture-brief.20260711.155500_adr-template-contract-repair-planning-slice-6.md",
  "hermes_decision": "docs/reviews/hermes-decision.20260711.160000_adr-template-schema-contract-repair-planning-slice-6.md",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_template-schema-contract-repair-planning.md",
  "authority_change": false,
  "source_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# Repair plan 20260711.155500: ADR template/schema contract slice 6

## Verdict

Planning review complete. This is proposal input only.

Recommended primary path: **draft a successor template/schema contract proposal in a future approved slice**, without editing `docs/adr/adr.adr-template-contract.md` in place first.

Fallback path: if HERMES/USER wants lower-risk staging before a successor proposal, produce a review-only errata/reconciliation note that explicitly marks stale/ahead-of-authority claims and migration exclusions. Do not mutate the source until a separate HERMES/USER-approved repair slice decides lifecycle/status and source disposition.

## Non-authority and non-mutation statement

This planning review does not edit `docs/adr/adr.adr-template-contract.md`, normalize status, change lifecycle state, supersede, accept, activate, reject, promote, demote, move, rename, delete, archive, split files, edit schemas, generate JSON/projections, replace Markdown, add DB/storage authority, migrate, or cut over authority.

All recommendations are proposal input only and require HERMES/USER approval before execution.

## Scope

Exactly one source was reviewed:

```text
docs/adr/adr.adr-template-contract.md
```

No other ADRs were added to the planning scope.

## Source claim inventory

| Source section | Claim / wording | Current support check | Classification | Safe repair recommendation |
|---|---|---|---|---|
| `## Status` | Observed status is `Accepted` with capital `A`. | Current lifecycle/schema vocabulary uses lowercase statuses: `proposal`, `draft`, `accepted`, `active`, `superseded`. Slice 4 preserved observed `Accepted` separately from normalized candidate `accepted`. | `requires_owner_decision` | Preserve exact casing in source/provenance. A future successor may use lowercase schema status, but this source should not be normalized as a side effect. |
| Context | `docs/schemas/adr.schema.json` is canonical source; Markdown is render target, not source of truth. | Current `docs/schemas/adr.schema.json` is the ADR content schema, but JSON authority is accepted staged direction only; repository-wide Markdown demotion/cutover is not executed. | `ahead_of_authority` | Successor should distinguish current authority from target end state: schema governs content shape; JSON authority/cutover requires later migration gates. |
| Context / architecture-spec | DOC CONTROL NUMBER standard is defined by `adr.adr.md`; template contract includes `dcn`. | `docs/adr/adr.adr.md` does define DOC CONTROL NUMBER and `dcn`, but current `docs/schemas/adr.schema.json` does not include a top-level `dcn` property. | `ambiguous/stale_against_schema` | Successor should decide whether `dcn` belongs in current ADR content schema, sidecar/envelope, naming/lifecycle metadata, or root ADR namespace guidance. No schema edit in this slice. |
| Decision | Adopt `docs/schemas/adr.schema.json` as canonical ADR schema and treat Markdown as derived rendering. | Schema file exists and is active content-shape surface; Markdown-as-derived is future/staged rather than current for all records. | `partly_current_partly_ahead_of_authority` | Successor should state that the schema is current content-shape reference while Markdown remains current source/control for unmigrated records. |
| Decision / architecture-spec | Schema should include required provenance, status, routing, renderable decision sections. | Current schema includes `status`, `context`, decision/consequence/spec/criteria/brief/resolved/non-goals/validation, `links`, optional `workflow_binding`; it does not include top-level `routing`. | `stale` | Successor should remove `routing` from current content-schema claims or classify it as sidecar/envelope/workflow metadata requiring separate decision. |
| Context / Decision | Optional `workflow_binding` block points at workflow ADRs and is lifecycle control extension. | Current schema contains optional `workflow_binding`; later workflow and Petri-net work did not promote routing as primary control model. | `current_with_boundary` | Retain optional workflow binding as schema-supported content only if successor preserves boundary: not a replacement for lifecycle or workflow authority. |
| architecture-spec | Canonical schema contains `routing`, `links`, and optional `workflow_binding` fields. | `links` and `workflow_binding` exist in current schema; top-level `routing` does not. | `mixed` | Successor should split currently supported fields from stale fields and avoid listing non-schema fields as canonical content. |
| acceptance-criteria | Criteria include provenance, routing, `dcn`, optional workflow-binding; line wrapping contains merged list item. | Slice 3/4 preserved the wrapped-list continuation, but `routing` and `dcn` are not current schema top-level fields. | `mixed/source_to_candidate_incomplete` | Successor should rewrite criteria in a new proposal, not patch this source silently. |
| `## routing` | Owner Athena; next phase accepted; governs JSON ADR source-of-truth surface. | Routing is not current schema content; staged JSON authority exists but not cutover. | `stale/ahead_of_authority` | Successor should use lifecycle/status and structured links rather than routing as controlling source-of-truth. Preserve this section as source/provenance until repair. |
| Overall role | File is an ADR decision, template contract, schema contract, renderer statement, and source-of-truth policy. | Slice 5 found it authority-relevant but semantically mixed/stale. README says templates/schema/architecture/policies belong on distinct surfaces when not bounded decisions. | `ambiguous_requires_owner_decision` | Prefer a successor template/schema contract proposal or architecture/schema extraction, rather than in-place mutation. |

## Current support summary

Supported or partly supported:

- `docs/schemas/adr.schema.json` is a current ADR content-shape schema surface.
- Current schema supports `status`, `context`, decision/consequences/spec/criteria/brief/resolved/non-goals/validation, `links`, and optional `workflow_binding`.
- `docs/adr/adr.adr.md` defines a `dcn` concept for ADR namespace control.
- Optional workflow binding exists in schema and should remain bounded.

Stale or ahead of current authority:

- `routing` as top-level ADR schema content is stale against current `docs/schemas/adr.schema.json`.
- Markdown as universally derived rendering is ahead of current repository authority; JSON-authoritative ADR migration is staged but not cut over.
- `dcn` as canonical current schema field is ambiguous because the root namespace ADR defines it but the current schema does not carry it.
- The file's `Accepted` status casing is noncanonical for current schema/lifecycle values and must not be silently normalized.

Ambiguous/mixed:

- The file acts as a template/schema contract and source-of-truth policy, not merely an ordinary ADR decision.
- The future home of routing-like data is unresolved: possible sidecar/envelope, workflow binding, lifecycle/policy surface, or intentionally excluded provenance.

## Repair options evaluated

### Option A: Leave as-is with explicit classification

Assessment: safe as a temporary state only.

Pros:

- No mutation risk.
- Preserves provenance and accepted-like source text.

Cons:

- Leaves readers with an accepted-like file that overstates JSON/Markdown authority and routing schema membership.
- Requires every future migration/tooling slice to remember exclusions and sidecar rules.

Use only as interim watchpoint, not as the preferred repair path.

### Option B: Revise in place later

Assessment: not preferred as first repair action.

Pros:

- Could directly make the current file less misleading.

Cons:

- Mutating an accepted-like source with `Accepted` status risks silent lifecycle/status semantics.
- Source carries useful provenance about older schema/routing/source-of-truth intent.
- In-place repair would need careful diff review and possibly status normalization/supersession decisions.

Use only after HERMES/USER explicitly approves source mutation and lifecycle handling.

### Option C: Replacement ADR / successor contract proposal later

Assessment: preferred primary path.

Pros:

- Avoids editing accepted-like source in place.
- Makes the new current truth explicit while preserving the old file as source/provenance or later supersession candidate.
- Allows HERMES/USER to explicitly decide lifecycle relation (`supersedes`, source/provenance, or retained accepted historical evidence).
- Fits the staged JSON-authority posture: successor can distinguish content schema, envelope/sidecar, projection, and migration authority.

Cons:

- Requires a later owner decision about whether and how to supersede/narrow the old file.
- Must avoid silently demoting the current source before successor acceptance.

Recommended.

### Option D: Split surfaces later

Assessment: useful as part of the successor design, not as an immediate file operation.

Potential split:

- successor ADR for the ADR template/schema contract decision;
- architecture/schema note for ADR content schema vs bidirectional envelope;
- JSON authority migration policy remains under `docs/adr/adr.json-authoritative-adr-store.draft.md` and related architecture;
- README/control-surface update later to point readers to the successor.

Pros:

- Matches README boundary guidance for ADRs vs architecture/templates/policies.
- Separates content schema from envelope/projection/migration policy.

Cons:

- Actual file splits/moves are out of scope and need later approval.

Use as design guidance for the successor proposal.

### Option E: Defer pending broader schema-base repair

Assessment: acceptable fallback but not highest leverage.

Pros:

- Avoids duplicating schema-family decisions that may also affect `adr.schema-base.md`.

Cons:

- Leaves a known accepted-like stale authority surface unresolved.
- Blocks clean use of this file in JSON-authority migration planning.

Use only if HERMES/USER prefers a broader schema-family repair package.

## Recommended path

Primary recommendation: **prepare a successor ADR/template-schema contract proposal in the next approved slice**.

Recommended next slice type: review-only / drafting slice, not source mutation.

Recommended output of next slice:

```text
docs/adr/adr.adr-template-schema-contract.<timestamp>.draft.md
```

or another HERMES/USER-approved proposal path under `docs/plans/` or `dev/` if HERMES wants a non-ADR proposal first.

The successor proposal should decide current truth for:

1. ADR content schema fields currently supported by `docs/schemas/adr.schema.json`.
2. The relationship between ADR content schema and bidirectional object envelope/sidecar evidence.
3. Markdown source authority for unmigrated records versus future generated projection state after cutover.
4. `routing` disposition: stale content field, sidecar/provenance, workflow metadata, or excluded legacy field.
5. `dcn` disposition: root ADR namespace guidance, schema field proposal, sidecar/envelope field, or deferred.
6. Optional `workflow_binding` boundary.
7. Relationship to old `docs/adr/adr.adr-template-contract.md`: retained source/provenance until an explicit HERMES/USER lifecycle decision, not silently superseded.

Fallback recommendation: if HERMES/USER does not want a successor proposal yet, create a review-only errata/reconciliation note that is cited by future migration slices. This fallback still must not edit source or change status.

## Required owner decisions before any repair execution

Before any source mutation or successor acceptance, HERMES/USER must decide:

- whether the old file will be superseded, retained as accepted historical/source evidence, or left unchanged with errata;
- whether lowercase `accepted` will be used in successor metadata while preserving source `Accepted` as observed provenance;
- whether `routing` belongs nowhere in content schema, in sidecar/envelope, in workflow binding, or in a separate policy/control surface;
- whether `dcn` should be added to schema in a later schema-change slice or remain namespace/control metadata;
- whether successor should be an ADR, architecture document, schema-contract document, or staged proposal first.

## Migration implications

Until repair is accepted:

- `docs/adr/adr.adr-template-contract.md` should remain excluded from automatic authoritative migration.
- Candidate conversion evidence may be used only with sidecar/provenance and source-to-candidate incomplete markers.
- Generated projection parse-back equality must remain candidate-field-only and must not imply semantic/source completeness.
- Any future JSON migration must preserve omitted/source-preserved sections: `architecture_spec`, `context`, `implementation_brief`, `links`, `non_goals`, `resolved_open_questions`, `routing`, and `validation_expectations`.

## Proposed follow-up brief

If HERMES/USER accepts this plan, the next brief should be:

```text
adr-template-schema-contract-successor-proposal-slice-7
```

Purpose:

- draft a successor template/schema contract proposal without editing the current source;
- explicitly mark it as proposal/draft until HERMES/USER accepts;
- define current ADR content-schema truths vs future JSON authority target;
- define relationship to `docs/adr/adr.adr-template-contract.md` as source/provenance or supersession candidate;
- preserve no schema/source mutation unless separately approved.

## Closeout validation

ATHENA ran:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Observed result: both commands produced no output / passed.

## Remaining HERMES/USER decision

Decide whether to accept this repair plan and activate a successor-proposal slice, an errata note slice, or a broader schema-family repair path.
