```json
{
  "title": "Semantic rationalization: ADR six-entry slice 5",
  "artifact_type": "architecture-review",
  "status": "semantic-rationalization-review-only",
  "datetime": "20260711.155000Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-semantic-rationalization-six-entry-slice-5",
  "source_brief": "docs/plans/architecture-review-brief.20260711.154300_adr-semantic-rationalization-slice-5.md",
  "hermes_decision": "docs/reviews/hermes-decision.20260711.154700_adr-semantic-rationalization-six-entry-slice-5.md",
  "koios_input": "workspaces/koios/working/next-proof-input.20260711_adr-semantic-rationalization-after-slice-4.md",
  "source_slice_4_acceptance": "docs/reviews/hermes-acceptance.20260711.154100_adr-json-authority-corpus-dry-run-inventory-slice-4.md",
  "source_slice_4_evidence": "dev/adr-json-authority-corpus-dry-run-inventory-slice-4/",
  "authority_change": false,
  "source_mutation": false,
  "next_owner": "HERMES_USER"
}
```

# Semantic rationalization 20260711: ADR six-entry slice 5

## Verdict

Review complete. This is review-only semantic disposition input for HERMES/USER.

The six selected entries are heterogeneous and should not be treated uniformly as current ADR authority or JSON-authority migration candidates. The subset contains:

- one ADR directory/index control surface;
- one bounded accepted Petri-net decision that remains semantically coherent as current bootstrap workflow authority;
- one accepted-like ADR template/schema contract that is authority-relevant but needs revision before it can remain clean current schema/ADR-source-of-truth authority;
- one draft UI/core schema namespace candidate that is not ADR JSON authority;
- one missing-status schema/base architecture concept that needs lifecycle/status repair or architecture-surface relocation before current authority use;
- one lifecycle draft that is source/provenance for the accepted lifecycle/naming ADR, not current authority.

## Non-authority and non-mutation statement

This review does not mutate source Markdown, normalize status, accept, activate, supersede, reject, promote, demote, move, rename, delete, archive, convert, project, publish schemas, add DB/storage authority, run migration, or perform cutover.

All recommendations below are proposal input only and require HERMES/USER approval before execution.

## Reviewed subset and order

Exactly the HERMES-approved six entries were reviewed in KOIOS semantic order:

1. `docs/adr/README.md`
2. `docs/adr/adr.petrinet.20260705.132740Z.md`
3. `docs/adr/adr.adr-template-contract.md`
4. `docs/adr/adr.json-schemas.draft.md`
5. `docs/adr/adr.schema-base.md`
6. `docs/adr/adr.adr-lifecycle.draft.md`

No domain-review/product/future-system ADRs were added.

## Summary disposition table

| # | Source | Observed status | Slice 4 outcome | Primary semantic classification | Current authority assessment | Recommended next action |
|---:|---|---|---|---|---|---|
| 1 | `docs/adr/README.md` | missing / not ADR status | `index_control_surface_skipped` | `index_or_control_surface_exclude` | Current local ADR-directory control surface, not ADR decision authority | Keep as control/index surface; exclude from ADR-record JSON authority migration unless a separate control-surface record type is approved. |
| 2 | `docs/adr/adr.petrinet.20260705.132740Z.md` | `accepted` | `accepted_source_candidate_not_json_authority` | `current_coherent_authority_candidate` | Current bounded bootstrap Petri-net vocabulary/separation authority | Keep as current bounded authority; do not broaden into product/runtime authority or JSON authority by implication. |
| 3 | `docs/adr/adr.adr-template-contract.md` | `Accepted` | `projectable_candidate_blocked_pending_template_contract_and_status_review` | `template_or_schema_contract` | Authority-relevant but not clean current template/schema authority without revision | Review/revise as a template/schema contract; reconcile `routing`, Markdown-source-of-truth, and schema-canonical claims before migration. |
| 4 | `docs/adr/adr.json-schemas.draft.md` | `draft` | `candidate_projectable_pending_review` | `template_or_schema_contract` with draft/schema-namespace flag | Draft schema namespace candidate, not current ADR JSON authority | Keep as draft/proposal evidence or revise under schema/UI namespace; do not use as ADR-store authority. |
| 5 | `docs/adr/adr.schema-base.md` | missing top-level ADR status | `blocked_missing_status_pending_review` | `current_but_needs_revision` with missing-status/schema-family flags | Not current ADR authority until lifecycle/status and surface placement are resolved | Create a separate status/disposition repair or architecture-extraction proposal; do not infer status. |
| 6 | `docs/adr/adr.adr-lifecycle.draft.md` | `draft` plus accepted-control notice | `source_only_provenance_draft_skipped_or_blocked` | `source_only_provenance` | Provenance/source draft for accepted lifecycle/naming ADR, not current authority | Preserve as source/provenance; compare only when revising accepted lifecycle/naming authority. |

## Per-entry findings

### 1. `docs/adr/README.md`

- Observed status/casing: no ADR lifecycle status; this is not an ADR record.
- Slice 4 outcome: `index_control_surface_skipped`.
- Slice 4 omitted/source-preserved sections: `boundary`, `current_migration_note`, `purpose`, `required_minimum_structure`.
- Semantic classification: `index_or_control_surface_exclude`.
- Authority assessment: local control/index surface for the ADR directory, not ADR decision authority.

Rationale:

`README.md` defines directory purpose and boundary: ADRs record bounded decisions and are distinct from architecture documents, policies, templates, implementation reports, and process-chain records. It also notes some files in the directory may need later classification/splitting. This is exactly the semantic yardstick for the rest of this slice, but it is not itself an ADR decision.

Conflicts/stale claims:

- It says ADR JSON files should conform to schema files in this directory "when used". Current schema authority now lives under `docs/schemas/` and JSON authority remains staged/deferred; this README wording may need later cleanup but does not block using it as a control surface.

Recommended follow-up, proposal only:

- Keep as ADR directory control surface.
- Exclude from ADR-record JSON authority migration unless a future control-surface record type is explicitly approved.
- Later update README wording when schema/JSON-authority migration policy becomes durable.

### 2. `docs/adr/adr.petrinet.20260705.132740Z.md`

- Observed status/casing: `accepted`.
- Slice 4 outcome: `accepted_source_candidate_not_json_authority`.
- Slice 4 omitted/source-preserved sections: `context`, `implementation_brief`, `non_goals`, `normative_language`, `provenance`, `rejected`, `validation_expectations`.
- Semantic classification: `current_coherent_authority_candidate`.
- Authority assessment: current bounded authority for bootstrap-held Petri-net vocabulary/separation, not product/mothership workflow authority and not JSON-authority readiness.

Rationale:

The ADR explicitly limits authority to the bootstrap-held workflow implementation slice and separates static Petri-net definition, runtime marking, binding, execution request/state, executor/event behavior, and workflow-specific wrapper concerns. Current architecture surfaces confirm it remains the accepted context for Petri-net workflow architecture: `docs/architecture/architecture.petrinet.00.md` names this ADR as controlling accepted context, and `docs/architecture/architecture.workflows.00.md` indexes it as the applicable ADR for Petri-net architecture.

The accepted ADR also contains many follow-on obligations and boundaries. That means it is coherent current authority for the first-slice vocabulary and separation model, not a broad runtime/product workflow charter.

Conflicts/stale claims:

- It remains bounded and should not be used to decide Operator Console, product workflow engine, workflow-object runtime coupling, generalized persistence, or mothership workflow semantics.
- Its accepted status does not imply JSON authority or migration readiness; Slice 4 correctly preserved that distinction.

Recommended follow-up, proposal only:

- Keep as current accepted bootstrap Petri-net separation authority.
- Use later workflow-engine slices and architecture reconciliations to record as-built deltas, not this semantic review.
- If migrating to JSON later, preserve omitted/source sections and rejected/provenance material; do not reduce to candidate fields only.

### 3. `docs/adr/adr.adr-template-contract.md`

- Observed status/casing: `Accepted`.
- Slice 4 outcome: `projectable_candidate_blocked_pending_template_contract_and_status_review`.
- Slice 4 omitted/source-preserved sections: `architecture_spec`, `context`, `implementation_brief`, `links`, `non_goals`, `resolved_open_questions`, `routing`, `validation_expectations`.
- Semantic classification: `template_or_schema_contract`.
- Secondary flags: `current_but_needs_revision`, `source_to_candidate_incomplete`, `status_casing_or_text_would_normalize`.
- Authority assessment: authority-relevant template/schema contract, but not clean current authority without reconciliation.

Rationale:

This file declares `docs/schemas/adr.schema.json` canonical, Markdown as a render target, and routing as part of the schema. Those claims are semantically important but now interact with later decisions:

- user/HERMES removed `routing` from the current ADR schema direction earlier in this workstream;
- `docs/adr/adr.json-authoritative-adr-store.draft.md` accepts JSON authority only as staged direction and explicitly does not execute migration or demote Markdown authority yet;
- `docs/architecture/architecture.adr-bidirectional-objects.md` defines candidate object/projection semantics without current schema/authority cutover.

The file is accepted-like and useful, but it mixes a decision record with template/schema contract behavior. Its observed status casing `Accepted` should be preserved exactly until a separate lifecycle/status normalization decision.

Conflicts/stale claims:

- Claims that Markdown is derived from JSON are ahead of current repository-wide authority state.
- The `routing` field appears stale relative to current ADR schema direction.
- It is unclear whether this file is an ordinary ADR decision, a template contract, or a schema-control decision.

Recommended follow-up, proposal only:

- Draft a bounded revision/replacement proposal for the ADR template/schema contract after semantic review acceptance.
- Preserve this file as authority-relevant source until the replacement is approved.
- Do not bulk-migrate this file without preserving all omitted/source-preserved sections and the status-casing issue.

### 4. `docs/adr/adr.json-schemas.draft.md`

- Observed status/casing: `draft`.
- Slice 4 outcome: `candidate_projectable_pending_review`.
- Slice 4 omitted/source-preserved sections: `architecture_spec`, `context`, `definitions`, `implementation_brief`, `links`, `non_goals`, `resolved_open_questions`, `routing`, `validation_expectations`.
- Semantic classification: `template_or_schema_contract` with `draft_schema_namespace_candidate` refinement.
- Secondary flags: `source_to_candidate_incomplete`, `defer_domain_review` for UI/core-family applicability.
- Authority assessment: draft schema namespace candidate, not current ADR-store schema authority.

Rationale:

The source describes a JSON schema namespace for the UI/core family. It says the namespace holds schemas/contracts only and should not define UI concept, renderer behavior, workflow UI surface, marshalling, framework choices, transport, or runtime internals. Despite the filename, this is not the current controlling ADR JSON authority decision. It is draft, UI/core-family adjacent, and semantically separate from the later ADR JSON authority migration path.

Slice 4 showed it is mechanically projectable but source-to-candidate incomplete. Conversion cleanliness must not be mistaken for semantic authority.

Conflicts/stale claims:

- `routing` says proposed, but routing is not current ADR control model for this migration work.
- The name may cause confusion with ADR schema authority even though the content is UI/core-family namespace guidance.
- It may be stale or incomplete relative to later schema namespace/storage topology work.

Recommended follow-up, proposal only:

- Keep as draft schema-namespace/source evidence.
- Do not treat as ADR JSON-authority control surface.
- If still relevant, revise/promote through a bounded schema/UI namespace review; otherwise leave as provenance.

### 5. `docs/adr/adr.schema-base.md`

- Observed status/casing: missing top-level ADR status; embedded JSON metadata includes `status: draft`.
- Slice 4 outcome: `blocked_missing_status_pending_review`.
- Slice 4 omitted/source-preserved sections: `architecture_spec`, `comments`, `content`, `context`, `implementation_brief`, `links`, `non_goals`, `open_questions`, `resolved_open_questions`, `routing`, `validation_expectations`.
- Semantic classification: `current_but_needs_revision` with missing-status/schema-family flags.
- Secondary flags: `insufficient_evidence`, `template_or_schema_contract`, `source_to_candidate_incomplete`.
- Authority assessment: not current ADR authority until lifecycle/status and document-surface placement are resolved.

Rationale:

The document contains substantial schema-family architecture: shared base record contract, metadata/content envelope, family-specific record contracts, rendered document surfaces, and Markdown renderer/ingester behavior. However, it lacks a top-level ADR `## Status`; the embedded JSON says `draft`, but Slice 2/4 correctly preserved that as source metadata rather than inventing lifecycle status.

The content may be valuable architecture/schema material, but its current ADR-control status is unsafe. It also overlaps later architecture surfaces (`architecture.adr-bidirectional-objects.md`, `architecture.json-adr-storage-topology.md`) and schema direction.

Conflicts/stale claims:

- Missing top-level status blocks ordinary ADR authority interpretation.
- The document is closer to schema-family architecture/spec than a clean ADR decision.
- Some schema/renderer/ingester claims may be stale relative to the later staged JSON authority path and current no-schema-change boundaries.

Recommended follow-up, proposal only:

- Create a separate status/disposition repair or architecture-extraction proposal if HERMES/USER wants to preserve it as current design input.
- Do not infer `draft`, `accepted`, or `active` from embedded JSON.
- Consider moving the durable idea into an architecture/schema surface in a future approved slice rather than treating this file as current ADR authority.

### 6. `docs/adr/adr.adr-lifecycle.draft.md`

- Observed status/casing: `draft`, with explicit `Accepted control` notice.
- Slice 4 outcome: `source_only_provenance_draft_skipped_or_blocked`.
- Slice 4 omitted/source-preserved sections: `accepted_control`, `architecture_spec`, `context`, `implementation_brief`, `links`, `non_goals`, `resolved_open_questions`, `routing`, `validation_expectations`.
- Semantic classification: `source_only_provenance`.
- Authority assessment: source/provenance draft for accepted lifecycle/naming consolidation ADR, not current authority.

Rationale:

The file explicitly says it is retained as source/provenance for accepted ADR `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` and is not canonical where it conflicts with that accepted ADR. The accepted lifecycle/naming ADR is `active` and controls canonical statuses `proposal`, `draft`, `accepted`, `active`, and `superseded`, along with compatibility mappings for older terms.

The draft remains useful for provenance and detailed older lifecycle thinking, but it must not override the active lifecycle/naming ADR.

Conflicts/stale claims:

- Draft states older status values (`Draft`, `Proposed`, `Active`, `Historical`, `Rejected`) that differ from accepted active lifecycle vocabulary.
- It includes role ownership and required proposed sections that the active ADR explicitly leaves out of scope or deferred.

Recommended follow-up, proposal only:

- Preserve as source/provenance.
- If useful claims remain, route a bounded lifecycle/naming amendment or guidance extraction; do not silently promote this draft.
- Exclude from automatic JSON authority promotion unless a future migration explicitly marks it source/provenance-only.

## Cross-entry findings

1. Semantic authority and JSON conversion readiness diverge. `adr.json-schemas.draft.md` was mechanically projectable but is only draft UI/core schema namespace material; `adr.petrinet...` is semantically coherent current authority but not automatically JSON-authoritative.
2. `docs/adr/README.md` correctly warns that some files in `docs/adr/` need classification/splitting. This six-entry subset confirms that warning: the directory contains ADR decisions, drafts, source/provenance, template/schema contracts, schema architecture concepts, and control surfaces.
3. Accepted-like status does not make a document clean authority. `adr.adr-template-contract.md` has `Accepted` but contains stale or unresolved claims about schema/routing/source-of-truth behavior.
4. Missing status must remain a blocker. `adr.schema-base.md` should not be rationalized into current authority without an explicit status/disposition repair.
5. Source/provenance drafts should remain provenance until a separate owner decision. `adr.adr-lifecycle.draft.md` is already subordinate to the active lifecycle/naming ADR.
6. Slice 4 omitted/source-preserved sections are semantically important. Every selected source was `source_to_candidate_complete: false`; reduced candidate objects are not enough to decide authority.

## Proposed next actions

These are proposal input only:

1. Approve this semantic rationalization as a review-only disposition matrix for the six-entry subset.
2. Next high-leverage slice: draft a bounded repair/revision brief for `docs/adr/adr.adr-template-contract.md` and `docs/adr/adr.schema-base.md`, because they are authority-relevant but semantically unsafe as-is.
3. Keep `docs/adr/README.md` and `docs/adr/adr.adr-lifecycle.draft.md` out of ADR-record JSON authority migration by default: README as control surface, lifecycle draft as source/provenance.
4. Treat `docs/adr/adr.petrinet.20260705.132740Z.md` as a good current-authority migration candidate only after a future JSON migration slice preserves its omitted/provenance/rejected material.
5. Treat `docs/adr/adr.json-schemas.draft.md` as schema-namespace draft/provenance, not as ADR JSON authority, unless HERMES/USER separately selects a schema namespace revision path.

## Closeout validation

This review created only this review artifact. No source ADRs, schemas, Slice 4 evidence, or code were intentionally modified.

ATHENA ran:

```bash
git status --short -- docs/adr docs/schemas dev/adr-json-authority-corpus-dry-run-inventory-slice-4
git diff --check
```

Observed result: both commands produced no output / passed.

## Remaining HERMES/USER decisions

- Whether to accept this six-entry semantic disposition matrix as review evidence.
- Whether to pursue a template/schema repair slice, a schema-base status/disposition repair slice, or another semantic rationalization subset next.
- Whether any recommendations should become actual ADR lifecycle/status/source changes in a future approved slice.
