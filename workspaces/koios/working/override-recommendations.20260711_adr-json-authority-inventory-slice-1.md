```json
{
  "title": "KOIOS override recommendations: ADR JSON authority inventory review/overrides slice 1",
  "artifact_type": "provenance-override-recommendations",
  "status": "koios-input-only-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "adr-json-authority-inventory-review-overrides-slice-1",
  "source_inventory": "dev/adr-json-authority-inventory-classification-slice-0/source-inventory.json",
  "requires_promotion_by": ["HERMES", "USER", "ATHENA"]
}
```

# KOIOS override recommendations: ADR JSON authority inventory review/overrides slice 1

## Authority boundary

This is KOIOS provenance/classification input only. It recommends review overrides for the Slice 0 inventory. It does not mutate ADR files, schemas, architecture, source code, or authority state.

No recommendation below is an authority decision. All values should remain `candidate_only: true` until HERMES/USER accepts override evidence.

## Sources reviewed

- `dev/adr-json-authority-inventory-classification-slice-0/source-inventory.json`
- `dev/adr-json-authority-inventory-classification-slice-0/classification-summary.json`
- `workspaces/koios/working/classification-proposal.20260711_adr-hierarchy-rationalization.md`
- `workspaces/koios/working/provenance-review.20260711_adr-json-authority-inventory-classification-slice-0.md`
- `docs/plans/implementation-brief.20260711.142200_adr-json-authority-inventory-review-overrides-slice-1.md`

Slice 0 generated 43 entries: 42 ADR-source candidates and 1 index/control surface. It marked 39 as `json_authority_candidate` and `proposed_authority`. KOIOS treats those labels as too authority-forward for direct consumption.

## Global override rules recommended

1. Preserve all Slice 0 observed status text/casing and source hashes unchanged.
2. Add `candidate_only: true` to every reviewed entry.
3. Do not use `authority_effect: proposed_authority` until HERMES/USER explicitly accepts a per-file authority plan. Prefer `authority_effect: candidate` for ordinary conversion candidates.
4. Treat `json_authority_candidate` as a conversion-planning candidate only. If document category/domain is unclear, override to `manual_review_required`, `domain_review_required`, `source_only_provenance_candidate`, or `excluded_pending_review`.
5. Any file with product/future-system, UI, training, or external subrepo implications should receive `domain_review_required` before conversion.
6. Any source/provenance draft that supports an accepted ADR should not be auto-promoted; prefer `source_only_provenance_candidate` or `manual_review_required`.
7. Current accepted/active decisions may be good conversion candidates, but conversion is not authority cutover; keep `authority_effect: candidate` pending separate cutover.

## Recommended per-file override groups

### A. Keep excluded / manual review

| Source path | Slice 0 values | Recommended override | Rationale |
|---|---|---|---|
| `docs/adr/README.md` | `index_or_control_surface`, `authority_effect: none`, auto false | Keep `index_or_control_surface`; keep auto false; `authority_effect: none`; owner/manual review true | Index/control surface, not an ADR record. |
| `docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md` | manual review, `status: Draft` | Keep manual review; add/keep domain review; category `product_future_system_draft` or `architecture_blueprint`; auto false | Status casing normalization plus training/product implications. |
| `docs/adr/adr.adr-template-contract.md` | manual review, `status: Accepted` | Keep manual review; category `template_schema_contract`; auto false until status/casing and authority reviewed | Accepted-like template contract, not plain ADR decision. |
| `docs/adr/adr.schema-base.md` | manual review, missing status | Keep manual review; category `template_schema_contract` + architecture aspect; auto false | Missing status and schema/implementation contract ambiguity. |

### B. Add domain/product review and remove automatic conversion eligibility

These were under-flagged in Slice 0. KOIOS recommends overriding to `disposition_candidate: domain_review_required` or `manual_review_required`, `authority_effect: domain_review_required` or `candidate`, and `automatic_conversion_eligibility_candidate: false` until owner/domain review.

| Source path | Slice 0 category | KOIOS recommended category/aspect | Rationale |
|---|---|---|---|
| `docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md` | implementation workflow support | `product_future_system_draft` / `architecture_blueprint` | Names `projectkoios-workflow`; product/subrepo authority unclear. |
| `docs/adr/adr.agent-windows-on-message-triggers.draft.md` | architecture blueprint | `product_future_system_draft` / agent runtime architecture | Future agent runtime/UI behavior; bootstrap authority unclear. |
| `docs/adr/adr.ui-core.draft.md` | template schema contract | `product_future_system_draft` / UI architecture | Shared UI core likely product/UI architecture, not ADR-store migration authority. |
| `docs/adr/adr.workflow-ui.draft.md` | template schema contract | `product_future_system_draft` / workflow UI architecture | UI/product authority watchpoint. |

Optional additional domain-review candidates:

- `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md` — template/ingestion boundary may touch product ingestion; recommend at least manual review before conversion.
- `docs/adr/adr.unified-diff-review-surface.draft.md` — review UI/surface implications; recommend manual review if UI authority matters.

### C. Source/provenance drafts: do not auto-promote

These are known source/provenance or detailed guidance surfaces. Recommended override: `disposition_candidate: source_only_provenance_candidate` or `manual_review_required`; `authority_effect: candidate` or `none`; `automatic_conversion_eligibility_candidate: false` unless HERMES/USER explicitly wants them as JSON authority records.

| Source path | Rationale |
|---|---|
| `docs/adr/adr.adr-lifecycle.draft.md` | Source/provenance for accepted lifecycle/naming ADR. |
| `docs/adr/adr.adr-lifecycle-promotion-mechanics.md` | Source/provenance for accepted lifecycle/naming ADR. |
| `docs/adr/adr.adr-names.draft.md` | Non-canonical detailed naming guidance. |
| `docs/adr/adr.adr-title-naming-convention.draft.md` | Non-canonical child guidance. |
| `docs/adr/adr.adr-filename-naming-convention.draft.md` | Non-canonical child guidance. |

These may be converted later for archival/queryability, but they should not become proposed JSON authority by default.

### D. Current accepted/active decisions: good conversion candidates, but not final authority labels

Recommended override for these: keep as conversion candidates, but set `authority_effect: candidate` rather than `proposed_authority`; retain `json_authority_candidate` only if `candidate_only: true` is explicit. They should be early clean canaries after mechanics are proven.

| Source path | Slice 0 status | Recommended note |
|---|---|---|
| `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` | active | Current controlling lifecycle/naming decision; high-value conversion candidate but risky because status authority matters. |
| `docs/adr/adr.petrinet.20260705.132740Z.md` | accepted | Accepted Petri-net separation decision; good later canary for accepted ADR. |
| `docs/adr/adr.workspaces.20260705.105021Z.md` | accepted | Accepted workspace/resume decision; good later canary. |
| `docs/adr/adr.adr.md` | active | Namespace/control-surface authority; needs template/control-surface review. |
| `docs/adr/adr.kernel.md` | active | Likely architecture/process blueprint; manual review before authority conversion. |
| `docs/adr/adr.templates.md` | active | Template representation contract; conversion candidate after template authority review. |
| `docs/adr/adr.templates-adr.md` | active | Template ADR control surface; conversion candidate after template authority review. |

### E. Architecture/policy/process/template mixed documents needing category override review

Slice 0 over-concentrated categories in `template_schema_contract` and `implementation_workflow_support`. KOIOS recommends these category corrections or review flags:

| Source path | Slice 0 category | KOIOS recommended category/disposition |
|---|---|---|
| `docs/adr/adr.json-database-for-adr-storage.draft.md` | template_schema_contract | `architecture_blueprint`; manual review or source/provenance until storage authority resolved. |
| `docs/adr/adr.json-authoritative-adr-store.draft.md` | template_schema_contract | `current_decision` or `architecture_blueprint` candidate depending on acceptance state; manual review before conversion. |
| `docs/adr/adr.json-schemas.draft.md` | template_schema_contract | Keep `template_schema_contract`; preferred clean canary; candidate only. |
| `docs/adr/adr.control-surfaces-and-ownership-boundaries.draft.md` | implementation_workflow_support | `policy_process` or `architecture_blueprint`; manual review. |
| `docs/adr/adr.controlling-adr-join-protocol.draft.md` | policy_process | Keep policy/process; candidate only; not auto authority. |
| `docs/adr/adr.draft-adr-comment-processing-protocol.draft.md` | policy_process | Keep policy/process; candidate only; not auto authority. |
| `docs/adr/adr.skill-register-and-adr-binding-policy.draft.md` | policy_process | Keep policy/process; manual review due skill/harness authority. |
| `docs/adr/adr.idea-spike-adr-implementation-workflow.draft.md` | implementation_workflow_support | `policy_process` / implementation workflow support; manual review before authority. |
| `docs/adr/adr.implementation.draft.md` | template_schema_contract | `implementation_workflow_support` / policy-process; manual review. |
| `docs/adr/adr.implementation-brief-verification-method.draft.md` | template_schema_contract | `implementation_workflow_support`; manual review. |
| `docs/adr/adr.brainstorm-capture-and-incubator-template.draft.md` | template_schema_contract | template/process; manual review. |

## Recommended exclusions from automatic conversion for Slice 1 reviewed inventory

At minimum, KOIOS recommends automatic conversion false for:

- `docs/adr/README.md`
- `docs/adr/adr.schema-base.md`
- `docs/adr/adr.adr-template-contract.md`
- `docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md`
- all four under-flagged product/future-system files listed in section B
- lifecycle/naming source drafts listed in section C unless HERMES/USER explicitly chooses archival JSON conversion

This does not mean never convert; it means do not feed them into an automatic JSON-authority conversion without reviewed disposition.

## Recommended messy canary candidates

### Clean/control canary already preferred

- `docs/adr/adr.json-schemas.draft.md`
  - Category: `template_schema_contract`, secondary architecture/schema aspect.
  - Rationale: schema-adjacent, prior conformance evidence, unsupported field preservation already tested.

### Messy canary candidates after clean canary

1. `docs/adr/adr.schema-base.md`
   - Why: missing status, schema/implementation contract ambiguity.
   - Tests: missing status handling, manual review disposition, sidecar/source provenance.

2. `docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md`
   - Why: non-canonical status casing `Draft`, product/training implications.
   - Tests: status casing preservation, domain-review flag, no automatic authority.

3. `docs/adr/adr.adr-template-contract.md`
   - Why: `Accepted` casing, template contract vs decision ambiguity.
   - Tests: accepted-like casing preservation and template authority review.

4. `docs/adr/adr.agent-windows-on-message-triggers.draft.md`
   - Why: future agent runtime/domain ambiguity despite parseable draft status.
   - Tests: domain-review override even when parse confidence is high.

KOIOS recommendation: use `adr.schema-base.md` as first messy canary because it is contained within ADR/schema rationalization and has missing-status ambiguity without broader product-domain implications.

## Implementation guidance for Slice 1 override evidence

For every reviewed entry, include:

- original Slice 0 category/disposition/authority-effect/auto-conversion values;
- reviewed values;
- `candidate_only: true`;
- rationale source: KOIOS classification, KOIOS provenance review, HERMES watchpoint, or deterministic rule;
- `authority_change: false`;
- `source_mutation: false`.

Recommended default reviewed values for most entries:

```json
{
  "authority_effect": "candidate",
  "candidate_only": true,
  "authority_change": false,
  "source_mutation": false
}
```

Only HERMES/USER should elevate any entry back toward `proposed_authority` for a later cutover plan.
