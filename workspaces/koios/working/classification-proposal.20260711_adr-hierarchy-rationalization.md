```json
{
  "title": "Classification proposal: ADR hierarchy rationalization",
  "artifact_type": "provenance-classification-proposal",
  "status": "koios-input-only-non-authoritative",
  "datetime": "20260711",
  "acting_as": "KOIOS",
  "repository": "projectkoios-bootstrap",
  "scope": "docs/adr hierarchy rationalization",
  "requires_promotion_by": ["ATHENA", "USER/HERMES"]
}
```

# Classification proposal: ADR hierarchy rationalization

## Authority boundary

This is KOIOS provenance/classification input only. It does not move, rename, edit, accept, supersede, or migrate any ADR. It does not change schemas, architecture, policy, source code, or document authority.

Any hierarchy, move/rename, status normalization, schema publication, or bulk migration requires ATHENA/USER promotion and a separate implementation/documentation handoff.

## Source basis

Inspected/used sources:

- `docs/adr/` file inventory: 42 Markdown files including `README.md`.
- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` — accepted lifecycle/naming consolidation.
- `docs/architecture/architecture.adr.00.md` — states ADRs live under `docs/adr/`, architecture documents under `docs/architecture/`, ADRs record bounded decisions, architecture documents describe controlled architectural surfaces or blueprints.
- `docs/architecture/architecture.adr.names.md` — title-vs-filename distinction, detailed naming rules still draft.
- `docs/policies/architecture.adr.lifecycle.md` — lifecycle consumption aid.
- Prior KOIOS notes: `provenance-index.20260704T175525Z_adr-control-surfaces.md`, `provenance-audit.20260709T012117Z_adr-lifecycle-followon-reconciliation.md`, `provenance-intake.20260711_adr-rationalization-json-md-object-track.md`.

Observed status scan from `docs/adr/` frontmatter/JSON/status headings:

| Observed status | Count |
|---|---:|
| `draft` | 31 |
| `Draft` | 1 |
| `active` | 2 parsed from JSON blocks, plus active-like frontmatter records observed in source list |
| `accepted` | 1 |
| `Accepted` | 1 |
| unknown/no parsed status | 6 |

KOIOS validation: the ADR directory is not a uniform hierarchy today. It mixes current decisions, draft/provenance sources, namespace/control-surface documents, templates/contracts, process/policy documents, implementation workflow documents, and product-ish/system architecture topics.

## Proposed hierarchy/categories

### A. Current decision records

Bounded decisions that appear accepted/active and may currently control behavior or interpretation.

Candidate subgroups:

- ADR control/lifecycle authority
- Harness/workspace authority
- Workflow/runtime decisions
- Template/schema namespace decisions

### B. Source/provenance drafts

Drafts retained as source/provenance for accepted decisions or future architecture work. These should not be silently superseded or deleted.

Candidate subgroups:

- lifecycle/naming source drafts
- control-surface/process source drafts
- workflow/source drafts
- review/skill/agent source drafts

### C. Architecture blueprints currently in ADR space

Documents that look like controlled architectural surfaces or system blueprints rather than bounded decision records. Some already have architecture counterparts or should be reconciled against `docs/architecture/` surfaces.

### D. Policy/process documents currently in ADR space

Documents that define operating policy, review procedures, lifecycle process, ownership, or workflow mechanics. Some may belong in `docs/policies/`, `docs/meta-harness.md`, or architecture/process-capture surfaces after ATHENA/USER decision.

### E. Templates/contracts/schema documents currently in ADR space

Documents that are closer to reusable template/schema/control-surface contracts than decisions. Some may belong under `docs/templates/`, `docs/schemas/`, or architecture surfaces, but only with promotion.

### F. Implementation brief/plan/workflow support concepts in ADR space

Documents about implementation briefs/plans, verification methods, spike packaging, or ADR-to-implementation workflows. These may remain provenance-only unless promoted into policy/workflow architecture.

### G. Product/domain or future-system topics in bootstrap ADR space

Documents that may belong to product/domain architecture or future subrepositories rather than bootstrap control surfaces. These need owner/domain review before promotion.

## File classification map

Uncertainty flags:

- `low` — category is strongly suggested by filename/title/status/source refs.
- `medium` — plausible category but needs ATHENA review.
- `high` — status/authority/domain unclear; do not move or promote without explicit review.

| File | Observed title/status | Proposed category | Topic/parent grouping | Uncertainty | Notes |
|---|---|---|---|---:|---|
| `docs/adr/README.md` | ADR control surface / unknown | E: index/control-surface note | ADR control surface | medium | README/index, not an ADR decision. |
| `docs/adr/adr.adr-lifecycle.20260705.011836Z.md` | ADR Lifecycle and Naming Consolidation / active | A: current decision record | ADR lifecycle + naming | low | Accepted canonical consolidation per prior KOIOS audit. |
| `docs/adr/adr.petrinet.20260705.132740Z.md` | Separate Petri-net Definition... / accepted | A: current decision record | Petri-net workflow runtime | low | Accepted decision; preserve as current authority unless superseded. |
| `docs/adr/adr.workspaces.20260705.105021Z.md` | Workspaces and Resume Control Surfaces / accepted | A: current decision record | Workspace/resume control | low | Accepted decision surface. |
| `docs/adr/adr.adr-template-contract.md` | Canonical ADR proposal template / Accepted | E or A: template contract decision | ADR templates | medium | Accepted-like, but template/contract surface. Needs authority review. |
| `docs/adr/adr.adr.md` | ADR Namespace Authority / active | A/E: namespace authority | ADR namespace | medium | Active namespace/control surface; may be more architecture/control than decision. |
| `docs/adr/adr.kernel.md` | ADR Kernel / active | C/F: implementation kernel blueprint | ADR implementation kernel | high | Active-like but likely architecture/process blueprint. |
| `docs/adr/adr.templates-adr.md` | Template ADR Control Surface / active | E/C: template control surface | Templates/ADR templates | medium | Template/control surface likely not pure decision record. |
| `docs/adr/adr.templates.md` | Template Representation Contract / active | E/C: template representation contract | Templates | medium | Contract/architecture-like; has template architecture relations. |
| `docs/adr/adr.schema-base.md` | Schema Base Class for ADR Records / unknown | E/C: schema/implementation contract | ADR schemas | high | Unknown status; likely schema/implementation concept. |
| `docs/adr/adr.20260703.000001_kernel.md` | ADR-Driven Implementation Kernel / draft | C/F: kernel blueprint draft | ADR implementation kernel | medium | Draft source; likely architecture/workflow process. |
| `docs/adr/adr.json-database-for-adr-storage.draft.md` | JSON ADR Storage Topology / draft | C: architecture blueprint in ADR space | ADR storage / JSON DB | low | Directly controlled by `architecture.json-adr-storage-topology.md`; source for pilot. |
| `docs/adr/adr.json-schemas.draft.md` | JSON Schemas Namespace / draft | E/C: schema namespace draft | JSON schemas | low | Used in conformance; active conformed record under `dev/`. |
| `docs/adr/adr.adr-lifecycle.draft.md` | ADR Lifecycle Policy / draft | B/D: lifecycle source draft | ADR lifecycle | low | Source/provenance for accepted lifecycle ADR. |
| `docs/adr/adr.adr-lifecycle-promotion-mechanics.md` | ADR Lifecycle Promotion Mechanics / draft | B/D: lifecycle source draft | ADR lifecycle | low | Source/provenance; not silently superseded. |
| `docs/adr/adr.adr-names.draft.md` | ADR Names / draft | B/D: naming source draft | ADR naming | low | Non-canonical detailed guidance. |
| `docs/adr/adr.adr-title-naming-convention.draft.md` | ADR Title Naming Convention / draft | B/D: naming source draft | ADR naming | low | Non-canonical child guidance. |
| `docs/adr/adr.adr-filename-naming-convention.draft.md` | ADR Filename Naming Convention / draft | B/D: naming source draft | ADR naming | low | Non-canonical child guidance. |
| `docs/adr/adr.adr-workflow.draft.md` | ADR-to-Workflow Binding / draft | D/F: workflow process draft | ADR workflow binding | medium | Process/workflow binding; may be superseded by Petri-net workflow work later. |
| `docs/adr/adr.workflow.draft.md` | Workflow Ontology for ADR Lifecycle / draft | C/D: workflow ontology draft | ADR workflow/lifecycle | medium | Blueprint/process hybrid. |
| `docs/adr/adr.idea-spike-adr-implementation-workflow.draft.md` | Idea → Spike → ADR → Implementation Workflow / draft | D/F: process draft | Idea/spike/implementation workflow | medium | Process flow, not bounded decision. |
| `docs/adr/adr.spike-entry-conditions.draft.md` | Spike Entry Conditions and Packaging / draft | D/F: process draft | Spike packaging | medium | Process/packaging. |
| `docs/adr/adr.implementation.draft.md` | Implementation Document Surface / draft | D/F: document-surface draft | Implementation docs | medium | Surface ownership/process. |
| `docs/adr/adr.implementation-brief-verification-method.draft.md` | Implementation Brief Verification Method / draft | D/F: process draft | Implementation verification | medium | Verification policy/process. |
| `docs/adr/adr.implementation-plan-ownership.draft.md` | Implementation Plan Ownership / draft | D/F: ownership/process draft | Implementation planning | medium | Ownership/process. |
| `docs/adr/adr.control-surfaces-and-ownership-boundaries.draft.md` | Control Surfaces and Ownership Boundaries / draft | C/D: control-surface blueprint/policy | Control surfaces | medium | Architecture/policy hybrid; compare `architecture.control-surfaces...`. |
| `docs/adr/adr.controlling-adr-join-protocol.draft.md` | Controlling ADR Join Protocol / draft | D: process/protocol draft | ADR joins | medium | Protocol/process; architecture counterpart exists. |
| `docs/adr/adr.draft-adr-comment-processing-protocol.draft.md` | Draft ADR Comment Processing Protocol / draft | D: process/protocol draft | ADR comments | medium | Review process; architecture counterpart exists. |
| `docs/adr/adr.comment-scope-and-control-boundary-review-rule.draft.md` | Comment Scope and Control-Boundary Review Rule / draft | D: review policy draft | Review/comment policy | medium | Policy/process. |
| `docs/adr/adr.decision-note-promotion-trigger.draft.md` | Decision Note Promotion Trigger / draft | D/F: process draft | Decision-note promotion | medium | Promotion trigger process. |
| `docs/adr/adr.brainstorm-capture-and-incubator-template.draft.md` | Brainstorm Capture and Incubator Note Template / draft | E/F: template/process draft | Brainstorm/incubator templates | medium | Template/process; likely not ADR decision. |
| `docs/adr/adr.skill-register-and-adr-binding-policy.draft.md` | Skill Register and ADR Binding Policy / draft | D/C: skill/ADR binding policy | Skill register | medium | Policy/architecture hybrid; architecture counterpart exists. |
| `docs/adr/adr.ownership-ledger-role-alignment.draft.md` | Ownership Ledger and Role Alignment / draft | D/C: ownership policy/architecture | Ownership/roles | medium | Policy/control-surface. |
| `docs/adr/adr.adversarial-two-plane-gate.draft.md` | Adversarial Two-Plane Gate / draft | D/C: review/control process | Review gates | medium | Review-process architecture. |
| `docs/adr/adr.20260702.043600_koios-adversarial-code-review-authority.draft.md` | Koios Adversarial Code Review Authority / draft | D/G: role/review authority draft | KOIOS review authority | medium | Role authority; ensure not product/domain authority. |
| `docs/adr/adr.unified-diff-review-surface.draft.md` | Unified Diff Review Surface / draft | C/D: review surface blueprint | Review/diff surface | medium | UI/review architecture-ish. |
| `docs/adr/adr.agent-windows-on-message-triggers.draft.md` | Agent Windows with `on_message` Triggers / draft | C/G: agent runtime/UI blueprint | Agent windows/triggers | high | Future system surface; domain unclear. |
| `docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md` | Agent Production Trace and Training Capture / Draft | G/C: future trace/training architecture | Agent trace/training | high | Product/training implications; casing mismatch. |
| `docs/adr/adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md` | Workflow-Compatible Petri-Net Executor... / draft | C/G: product workflow runtime draft | projectkoios-workflow Petri-net | high | Product/subrepo naming; bootstrap authority uncertain. |
| `docs/adr/adr.20260702.213000_template-representation-ingestion-scope.draft.md` | Template Representation Ingestion Scope / draft | C/E/G: template representation architecture | Templates/ingestion | medium | Prior KOIOS noted product ingestion boundary watchpoint. |
| `docs/adr/adr.ui-core.draft.md` | Shared UI Core Namespace / draft | C/G: UI architecture draft | UI core | high | Likely product/UI architecture, not bootstrap ADR control. |
| `docs/adr/adr.workflow-ui.draft.md` | Workflow UI Surface / draft | C/G: workflow UI architecture draft | Workflow UI | high | UI/product authority watchpoint. |

## Parent/child and topic grouping suggestions

These groupings are provenance suggestions only, not migration authority.

### ADR control surface

Parent/current authority candidate:

- `docs/adr/adr.adr-lifecycle.20260705.011836Z.md`
- `docs/adr/adr.adr.md`
- `docs/architecture/architecture.adr.00.md`

Children/source/provenance:

- lifecycle: `adr.adr-lifecycle.draft.md`, `adr.adr-lifecycle-promotion-mechanics.md`
- naming: `adr.adr-names.draft.md`, `adr.adr-title-naming-convention.draft.md`, `adr.adr-filename-naming-convention.draft.md`
- template contract: `adr.adr-template-contract.md`, `README.md`

### ADR storage / JSON object / schema rationalization

Parent architecture surface:

- `docs/architecture/architecture.json-adr-storage-topology.md`
- candidate/intake: `docs/plans/architecture-intake.20260711.131140_adr-bidirectional-json-markdown-objects.md`

ADR-space source/provenance:

- `adr.json-database-for-adr-storage.draft.md`
- `adr.json-schemas.draft.md`
- `adr.schema-base.md`

Evidence:

- `dev/adr-json-database-one-adr-pilot/`
- `dev/adr-json-schemas-conformance/`
- KOIOS `candidate-schema.20260711_adr-bidirectional-json-md-object.md`

### Template representation / template ADRs

Possible parent/control surfaces:

- `adr.templates.md`
- `adr.templates-adr.md`
- `architecture.adr.template.md` / template architecture surfaces if promoted

Children/source:

- `adr.20260702.213000_template-representation-ingestion-scope.draft.md`
- `adr.brainstorm-capture-and-incubator-template.draft.md`
- `adr.adr-template-contract.md`

Watchpoint: separate bootstrap template representation from product-domain ingestion.

### Workflow / Petri-net / ADR-to-workflow

Current accepted runtime decision:

- `adr.petrinet.20260705.132740Z.md`

Draft/source group:

- `adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md`
- `adr.adr-workflow.draft.md`
- `adr.workflow.draft.md`
- `adr.idea-spike-adr-implementation-workflow.draft.md`
- `adr.spike-entry-conditions.draft.md`

Watchpoint: do not merge ADR lifecycle workflow drafts with live Petri-net runtime/queue work without ATHENA/HERMES decision.

### Implementation process surfaces

Candidate parent/policy group:

- `adr.implementation.draft.md`
- `adr.implementation-brief-verification-method.draft.md`
- `adr.implementation-plan-ownership.draft.md`
- `adr.20260703.000001_kernel.md`
- `adr.kernel.md`

Watchpoint: may belong in meta-harness workflow/policies rather than ADR decision space.

### Review / comment / skill / role governance

Draft/source group:

- `adr.adversarial-two-plane-gate.draft.md`
- `adr.20260702.043600_koios-adversarial-code-review-authority.draft.md`
- `adr.comment-scope-and-control-boundary-review-rule.draft.md`
- `adr.controlling-adr-join-protocol.draft.md`
- `adr.draft-adr-comment-processing-protocol.draft.md`
- `adr.skill-register-and-adr-binding-policy.draft.md`
- `adr.ownership-ledger-role-alignment.draft.md`
- `adr.decision-note-promotion-trigger.draft.md`
- `adr.unified-diff-review-surface.draft.md`

Watchpoint: distinguish durable role/policy authority from review-surface experiments.

### UI / agent runtime / product-ish future surfaces

Draft/source group needing domain review:

- `adr.agent-windows-on-message-triggers.draft.md`
- `adr.20260702.144539_agent-production-trace-and-training-capture.draft.md`
- `adr.ui-core.draft.md`
- `adr.workflow-ui.draft.md`

Watchpoint: likely needs product/mothership or UI architecture ownership before promotion.

## What should remain provenance-only for now

- Lifecycle/naming source drafts unless ATHENA/USER explicitly promotes or supersedes them.
- Draft process/protocol documents that have architecture counterparts but no accepted consolidation.
- ADR JSON/database pilot and conformance artifacts under `dev/` as evidence, not repository-wide authority.
- Candidate bidirectional-object schema sketch under `workspaces/koios/working/`.
- Product-ish UI/agent/training drafts until domain ownership is clarified.
- Any status/casing scan results until a validated parser/tooling slice confirms them.

## What requires ATHENA/USER promotion before action

- Moving architecture blueprints out of `docs/adr/` or creating new hierarchy directories.
- Renaming ADR files or normalizing filename conventions.
- Changing `status` casing/vocabulary or adding structured disposition fields.
- Marking source drafts as superseded.
- Promoting JSON checkpoints or database state as ADR authority.
- Publishing a bidirectional ADR object schema under `docs/schemas/`.
- Bulk Markdown↔JSON conversion or bidirectional ingest.
- Treating `docs/adr/` as generated projection rather than editable source.

## KOIOS recommendation

Use this classification as intake for an ATHENA-owned architecture note or migration plan. The highest-leverage next architecture artifact would define the target document hierarchy and object authority model before any file movement:

1. accepted/current ADR decisions;
2. source/provenance drafts;
3. architecture blueprints;
4. policy/process surfaces;
5. templates/contracts/schema surfaces;
6. implementation workflow support documents;
7. product/future-system drafts needing domain ownership.

Only after ATHENA/USER accepts that hierarchy should VULCAN receive a bounded implementation/documentation brief for any moves, renames, status normalization, or schema work.
