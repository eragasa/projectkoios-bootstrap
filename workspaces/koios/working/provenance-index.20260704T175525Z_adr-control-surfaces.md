# KOIOS provenance index: ADR control surfaces

## Metadata

- Type: provenance-index
- Status: captured
- Captured: 20260704T175525Z
- Captured by: KOIOS
- Repository: projectkoios-bootstrap
- Scope: ADR lifecycle/naming consolidation and template representation namespace split

## Authority boundary

This index is a KOIOS knowledge/provenance artifact.

It does not create architecture authority, implementation authority, product-domain authority, or workflow completion decisions.

It records source mappings and authority-boundary observations for existing ATHENA-owned ADR surfaces.

## Indexed artifacts

| Artifact | Status | Owner | Path |
|---|---|---|---|
| ADR Lifecycle and Naming Consolidation | accepted | ATHENA | `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` |
| Template Representation and Namespace Split | proposed | ATHENA | `dev/template-representation-namespace-split/adr.template-representation.20260705.014135Z.proposed.md` |

## Lifecycle and naming consolidation provenance

| Claim | Source artifacts | KOIOS provenance assessment |
|---|---|---|
| ADR record statuses are `draft`, `proposed`, `accepted`, `completed`, `superseded`, and `rejected`. | `docs/adr/adr.adr-lifecycle.draft.md`; `docs/policies/architecture.adr.lifecycle.md`; `docs/schemas/schema.record-base.json` | Accepted ADR explicitly reconciles older lifecycle vocabulary with current schema/status practice. |
| Older `active` language maps to accepted authority or completed rollout, not review activity. | `docs/adr/adr.adr-lifecycle.draft.md`; `docs/policies/architecture.adr.lifecycle.md`; `docs/schemas/schema.record-base.json` | Accepted ADR preserves distinction between ADR authority and workspace live-work state. |
| Spike packaging is draft ADR plus `ADR_implementation_plan` under `spike/<spike-id>/`. | `docs/adr/adr.adr-lifecycle.draft.md`; `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`; `docs/architecture/architecture.lifecycle.00.md` | Accepted ADR preserves the concept and normalizes the path to repo-relative wording. |
| Proposed ADRs use `dev/<proposal-id>/` as the review surface. | `docs/adr/adr.adr-lifecycle-promotion-mechanics.md`; `docs/architecture/architecture.lifecycle.00.md` | Accepted ADR maps older “active review” wording to `proposed`. |
| ADR titles and filenames are separate naming layers. | `docs/adr/adr.adr-names.draft.md`; `docs/architecture/architecture.adr.names.md` | Accepted ADR promotes only the umbrella distinction. |
| Detailed title and filename rules remain non-canonical draft guidance. | `docs/adr/adr.adr-title-naming-convention.draft.md`; `docs/adr/adr.adr-filename-naming-convention.draft.md` | Accepted ADR does not silently promote the child naming drafts. |
| Policy/index/source-draft updates require separate handoff. | Accepted ADR source-draft disposition and implementation brief. | Boundary is explicit; acceptance alone does not authorize policy/index edits, schema/tooling changes, status migration, or file renames. |

## Template representation namespace split provenance

| Claim | Source artifacts | KOIOS provenance assessment |
|---|---|---|
| The proposal is a narrow JSON↔Markdown template/document representation slice. | `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`; `docs/plans/template-representation-and-implementation-namespace-split.md`; `docs/architecture/architecture.templates.md` | Current proposal includes a source traceability table and bounds the slice to template/document representation. |
| Presentation-only Markdown variance may normalize when semantic meaning is preserved. | `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`; `docs/plans/template-representation-and-implementation-namespace-split.md` | Current proposal adds typed parse/equivalence-error expectations for meaning-changing differences. |
| `docs/templates/` is the reusable template namespace. | `docs/templates/templates.00.md`; `docs/architecture/architecture.templates.md`; `docs/adr/adr.templates.md` | Current proposal now includes the controlling template draft as source context and does not accept it wholesale. |
| `docs/implementation/` is the implementation-linked records namespace. | `docs/implementation/implementation.00.md`; `docs/adr/adr.implementation.draft.md` | Current proposal now includes the controlling implementation draft as source context and does not accept it wholesale. |
| Future implementation target is inside `src/python/projectkoios/bootstrap/`, not `src/python/ingestion/` or `projectkoios.ingestion`. | `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`; `docs/plans/template-representation-and-implementation-namespace-split.md`; repository source layout inspection. | Source inspection confirmed `src/python/projectkoios/bootstrap/` exists and `src/python/ingestion/` does not. This remains future implementation-target guidance only. |
| General ingestion, Graphify/source ingestion, vault/PDF/evidence ingestion, and product-domain template semantics are excluded. | `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md`; `docs/plans/template-representation-and-implementation-namespace-split.md`; current proposal non-goals. | Boundary is explicit and protects bootstrap scope from product-domain authority expansion. |
| Existing implementation plan is a candidate Vulcan handoff only. | `docs/plans/template-representation-and-implementation-namespace-split.md`; current proposal implementation brief. | Current proposal states the plan is not accepted architecture beyond constraints restated in the ADR. |

## Silent-authority watchpoints

| Watchpoint | Current status | Owning next action |
|---|---|---|
| Lifecycle policy/index updates after accepted ADR | Explicitly not authorized by acceptance alone. | ATHENA/HERMES only if user requests follow-on documentation/control-surface reconciliation. |
| Lifecycle source-draft supersession | Explicitly not silently performed. | Separate accepted action required. |
| Template representation proposal acceptance | Would create bootstrap architecture/control-surface boundary only if accepted. | HERMES/user review decision. |
| Template/implementation controlling drafts | Current proposal uses them as source context only. | Separate action required to accept, supersede, or migrate those drafts. |
| Product-domain template authority | Explicitly excluded for `~/projectkoios/` and future product repositories. | Separate product-domain acceptance required outside bootstrap. |
| Implementation plan promotion | Current proposal keeps plan as candidate handoff, not architecture authority. | Vulcan handoff only after acceptance or explicit user direction. |

## Current KOIOS assessment

The accepted lifecycle/naming ADR has adequate claim/source provenance and strong non-authority boundaries.

The revised template representation proposal now satisfies the main KOIOS provenance requests: claim/source traceability, inclusion of controlling namespace drafts, narrowed implementation scope, avoidance of broad ingestion terminology, product-domain exclusion, and implementation-plan non-promotion.

KOIOS has no provenance objection to HERMES/user reviewing the revised template representation proposal for acceptance, revision, or rejection.
