# KOIOS review: ADR versus architecture-document split

## Metadata

- Type: provenance-review
- Status: advisory
- Captured: 20260704T024500Z
- Captured by: KOIOS
- Repository: projectkoios-bootstrap
- Scope: `docs/adr/`
- Related review: `workspaces/koios/handoffs/outgoing/architecture.document.control-surface.review.20260704T023500Z.md`

## Assessment

The active ADR directory mixes decision records, architecture blueprints, namespace control documents, lifecycle policies, templates, and implementation briefs.

This mixture makes it difficult to tell whether a file records a decision, defines a controlled architecture surface, or governs a repeated practice.

A split is likely needed before architecture-document authoring skills can be reliable.

## Classification rule used

A file is classified as `ADR` when it primarily records a bounded decision and its consequences.

A file is classified as `Architecture document` when it primarily defines a surface, namespace, protocol, lifecycle, template, policy, or reusable structure.

A file is classified as `Split` when it contains both a decision record and reusable architecture/control-surface material that should become a separate architecture document.

## Recommended target surfaces

| Surface | Purpose |
|---|---|
| ADR | Records a bounded decision and consequences. |
| Architecture document | Defines a controlled architectural surface or blueprint. |
| Policy | Governs repeated practice across artifacts or roles. |
| Template | Defines reusable document structure. |
| Implementation brief | Translates accepted architecture into implementation work. |

## Active ADR directory classification

| File | Current title | Classification | Recommended action |
|---|---|---|---|
| `adr.20260702.042300_projectkoios-workflow-petri-net-executor.draft.md` | Workflow-Compatible Petri-Net Executor | ADR | Keep as ADR if it records the executor choice; split detailed executor shape into architecture document. |
| `adr.20260702.043600_koios-adversarial-code-review-authority.draft.md` | Koios Adversarial Code Review Authority | Split | Keep authority decision as ADR; move review authority model into architecture/policy document. |
| `adr.20260702.144539_agent-production-trace-and-training-capture.draft.md` | Agent Production Trace and Training Capture | Split | Keep trace-capture decision as ADR; move capture schema and workflow into architecture document. |
| `adr.20260702.213000_template-representation-ingestion-scope.draft.md` | Template Representation Ingestion Scope | ADR | Keep as ADR if it chooses ingestion scope; move reusable template representation rules into architecture document. |
| `adr.20260703.000001_kernel.md` | ADR-Driven Implementation Kernel | Architecture document | Move to architecture document because it defines a kernel model rather than only recording a decision. |
| `adr.adr-filename-naming-convention.draft.md` | ADR Filename Naming Convention | Policy | Move to ADR policy or template convention. |
| `adr.adr-lifecycle-promotion-mechanics.md` | ADR Lifecycle Promotion Mechanics | Policy | Move to ADR lifecycle policy. |
| `adr.adr-lifecycle.draft.md` | ADR Lifecycle Policy | Policy | Move to ADR lifecycle policy. |
| `adr.adr-names.draft.md` | ADR Names | Architecture document | Move to ADR namespace architecture document. |
| `adr.adr-template-contract.md` | Canonical ADR proposal template | Template | Move to template/control-surface document. |
| `adr.adr-title-naming-convention.draft.md` | ADR Title Naming Convention | Policy | Move to ADR policy or naming convention document. |
| `adr.adr-workflow.draft.md` | ADR-to-Workflow Binding | Split | Keep binding choice as ADR; move workflow binding model into architecture document. |
| `adr.adr.md` | ADR Namespace Authority | Architecture document | Move to namespace/control-surface architecture document. |
| `adr.adversarial-two-plane-gate.draft.md` | Adversarial Two-Plane Gate | Architecture document | Move gate model into architecture document; create ADR only if a specific gate decision is being accepted. |
| `adr.agent-windows-on-message-triggers.draft.md` | Agent Windows with on_message Triggers | ADR | Keep as ADR if it decides to use message-trigger windows; split protocol details if extensive. |
| `adr.brainstorm-capture-and-incubator-template.draft.md` | Brainstorm Capture and Incubator Note Template | Template | Move to template or process document. |
| `adr.canonical-workspace-state-next-action-protocol.draft.md` | Canonical Workspace State and Next-Action Protocol | Policy | Move to workflow/process policy. |
| `adr.comment-scope-and-control-boundary-review-rule.draft.md` | Comment Scope and Control-Boundary Review Rule | Policy | Move to review policy. |
| `adr.control-surfaces-and-ownership-boundaries.draft.md` | Control Surfaces and Ownership Boundaries | Architecture document | Move to control-surface architecture document. |
| `adr.controlling-adr-join-protocol.draft.md` | Controlling ADR Join Protocol | Policy | Move to ADR workflow policy. |
| `adr.decision-note-promotion-trigger.draft.md` | Decision Note Promotion Trigger | Policy | Move to promotion policy. |
| `adr.draft-adr-comment-processing-protocol.draft.md` | Draft ADR Comment Processing Protocol | Policy | Move to ADR review/comment policy. |
| `adr.idea-spike-adr-implementation-workflow.draft.md` | Idea → Spike → ADR → Implementation Workflow | Architecture document | Move to workflow architecture document; create ADR only for the choice to adopt this lifecycle. |
| `adr.implementation-brief-verification-method.draft.md` | Implementation Brief Verification Method | Policy | Move to implementation-brief policy or verification standard. |
| `adr.implementation-plan-ownership.draft.md` | Implementation Plan Ownership | Policy | Move to ownership policy. |
| `adr.implementation.draft.md` | Implementation Document Surface | Architecture document | Move to implementation document control-surface architecture document. |
| `adr.json-database-for-adr-storage.draft.md` | JSON ADR Storage Topology | Split | Keep storage-topology choice as ADR; move JSON storage model into architecture document. |
| `adr.json-schemas.draft.md` | JSON Schemas Namespace | Architecture document | Move to schema namespace architecture document. |
| `adr.kernel.md` | ADR Kernel | Architecture document | Move to kernel architecture document. |
| `adr.ownership-ledger-role-alignment.draft.md` | Ownership Ledger and Role Alignment | Architecture document | Move to ownership architecture document. |
| `adr.skill-register-and-adr-binding-policy.draft.md` | Skill Register and ADR Binding Policy | Split | Keep binding decision as ADR; move skill register policy/model into architecture or policy document. |
| `adr.spike-entry-conditions.draft.md` | Spike Entry Conditions and Packaging | Policy | Move to spike workflow policy. |
| `adr.templates.draft.md` | Template Representation Contract | Architecture document | Move to template architecture document. |
| `adr.ui-core.draft.md` | Shared UI Core Namespace | Architecture document | Move to UI namespace architecture document. |
| `adr.unified-diff-review-surface.draft.md` | Unified Diff Review Surface | Architecture document | Move to review-surface architecture document. |
| `adr.workflow-ui.draft.md` | Workflow UI Surface | Architecture document | Move to workflow UI architecture document. |
| `adr.workflow.draft.md` | Workflow Ontology for ADR Lifecycle | Architecture document | Move to workflow ontology architecture document. |

## Summary counts

| Classification | Count |
|---|---:|
| ADR | 4 |
| Split | 6 |
| Architecture document | 15 |
| Policy | 10 |
| Template | 2 |

## Interpretation

Only a small minority of files in the active ADR directory are clean ADRs.

Most files are better understood as architecture documents, policy documents, templates, or split candidates.

This supports the user's diagnosis that the architecture-document and ADR surfaces are currently conflated.

## Recommended next step

ATHENA should define the target directory map before moving files.

Suggested map:

| Target directory | Content |
|---|---|
| `docs/adr/` | Bounded decision records only. |
| `docs/architecture/` | Architecture documents and controlled blueprints. |
| `docs/policies/` | Lifecycle, naming, ownership, review, and workflow policies. |
| `docs/templates/` | Reusable document templates and contracts. |
| `docs/implementation/` | Implementation reports and implementation-surface records. |

ATHENA should then choose one cluster to split first.

The ADR-lifecycle cluster is the best first split because it contains ADR naming, title, lifecycle, template, workflow, and promotion mechanics files.

## Non-authority statement

This classification is KOIOS advisory provenance only.

This classification does not move files.

This classification does not change ADR status.

This classification does not create architecture or policy authority.
