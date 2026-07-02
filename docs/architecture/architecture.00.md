---
status: draft
date: 20260701.131500Z
---

# Architecture index

## Purpose

This is the namespace index for bootstrap architecture notes.
Use it as the entry point for `architecture.*` documents and as the anchor
note for Obsidian-style navigation. It also serves as the top-level index for
process and lifecycle control surfaces when those are governed by a controlling
ADR.

## Scope

These notes describe the bootstrap-side workspace, repository-projection, and
harness-related architecture for `projectkoios-bootstrap`.
They do not replace `docs/architecture.md` in the mothership repo.

## Documentation system

The canonical architecture document for the documentation system lives at
`architecture.docs.md`.
That file is the stable active key for the docs architecture surface.
Replacement versions are archived under timestamped filenames.
The docs model is intentionally portable across Python 3, TypeScript, and Rust.

## Protection

Only Hermes may modify `docs/architecture*.md`, and only when Zeus explicitly
directs the change.

## Index

| note | controlling ADR |
|---|---|
| [architecture.documents](architecture.documents.md) | None |
| [architecture.adr.template](architecture.adr.template.md) | None |
| [architecture.lifecycle.00](architecture.lifecycle.00.md) | [ADR 20260702.000551: Idea → Spike → ADR → Implementation Workflow](adr/adr.idea-spike-adr-implementation-workflow.draft.md) |
| [ADR 20260701.131629: ADR template contract](adr/adr.adr-template-contract.md) | None |
| [ADR 20260702.000551: Idea → Spike → ADR → Implementation Workflow](adr/adr.idea-spike-adr-implementation-workflow.draft.md) | None |
| [ADR 20260702.004118: ADR Title Naming Convention](adr/adr.adr-title-naming-convention.draft.md) | None |
| [ADR 20260702.004300: ADR Filename Naming Convention](adr/adr.adr-filename-naming-convention.draft.md) | None |
| [ADR 20260702.005615: Brainstorm Capture and Incubator Note Template](adr/adr.brainstorm-capture-and-incubator-template.draft.md) | None |
| [ADR 20260702.012900: ADR Draft Comment and Promotion Workflow](adr/adr.draft-comment-and-promotion-workflow.draft.md) | None |
| [ADR 20260702.032100Z: Controlling ADR Join Protocol](adr/adr.controlling-adr-join-protocol.draft.md) | None |
| [ADR 20260702.032435Z: Draft ADR Comment Processing Protocol](adr/adr.draft-adr-comment-processing-protocol.draft.md) | None |
| [ADR 20260702.033824Z: Skill Register and ADR Binding Policy](adr/adr.skill-register-and-adr-binding-policy.draft.md) | None |
| [ADR 20260702.020440Z: Canonical Workspace State and Next-Action Protocol](adr/adr.canonical-workspace-state-next-action-protocol.draft.md) | None |
| [ADR 20260702.020818: Comment Scope and Control-Boundary Review Rule](adr/adr.comment-scope-and-control-boundary-review-rule.draft.md) | None |
| [ADR 20260701.181956Z: Control Surfaces and Ownership Boundaries](adr/adr.control-surfaces-and-ownership-boundaries.draft.md) | None |
| [ADR 20260702.020244Z: Hermes Sandbox Message Delivery](adr/adr.hermes-sandbox-message-delivery.draft.md) | None |
| [ADR 20260702.030200: Implementation Plan Ownership](adr/adr.implementation-plan-ownership.draft.md) | None |
| [ADR 20260702.043600: Koios Adversarial Code Review Authority](adr/adr.20260702.043600_koios-adversarial-code-review-authority.draft.md) | None |
| [ADR 20260702.121432Z: Adversarial Two-Plane Gate](adr/adr.adversarial-two-plane-gate.draft.md) | None |
| [ADR 20260702.121432Z: Ownership Ledger and Role Alignment](adr/adr.ownership-ledger-role-alignment.draft.md) | None |
| [ADR 20260702.121432Z: Agent Windows with `on_message` Triggers](adr/adr.agent-windows-on-message-triggers.draft.md) | None |
| [ADR 20260702.121432Z: JSON ADR Storage Topology](adr/adr.json-database-for-adr-storage.draft.md) | None |
| [ADR 20260702.121432Z: Spike Entry Conditions](adr/adr.spike-entry-conditions.draft.md) | None |
| [architecture.workspaces.00](architecture.workspaces.00.md) | None |
| [architecture.workspaces.git](architecture.workspaces.git.md) | None |
| [architecture.workspaces.obsidian](architecture.workspaces.obsidian.md) | None |
| [architecture.repositories.00](architecture.repositories.00.md) | None |
| [architecture.repos.git](architecture.repos.git.md) | None |
| [architecture.repos.obsidian](architecture.repos.obsidian.md) | None |
| [architecture.repo-projections](architecture.repo-projections.md) | None |

### Historic ADR archive
- `docs/archive/architecture/adr/` — all ADRs archived and marked historic

## Naming convention

- All bootstrap architecture notes use the `architecture.` prefix.
- Filenames stay unique and grep-friendly.
- Use Markdown links for navigation so grep, Graphify, and Obsidian all work.
- ADR filenames use `adr.<name>.md` for active notes and `adr.<name>.<status>.md` for non-active notes.
- The date slug, when present, lives under `## Status` and uses `YYYYMMDD.HHMMSSZ`.
- Related notes should link back here with `[architecture.00](architecture.00.md)`.
- Promoted ADRs should use concise decision titles aligned to this index; draft titles may remain provisional.

## ADR encapsulation and hierarchy

ADRs are encapsulated decision records and must be independently readable.

An ADR must contain only its own:
- context
- decision
- consequences
- acceptance criteria
- routing / next step

Hierarchy, readiness level, and promotion ordering are not encoded as nested ADR body structure.
Instead, those relationships are represented in `architecture.00` as the knowledge-organization layer for the repository.

`architecture.00` is authoritative for:
- parent / child relationships
- readiness tiers
- promotion paths
- package-extractable boundaries

In this model:
- ADRs remain self-contained
- `architecture.00` supplies structure
- the graph links decisions without making any ADR depend on hidden hierarchy
- gates are workflow-facing control surfaces
- ownership is treated as a higher-level architectural concern

## Related bootstrap architecture

- `docs/agent-charter.md`
- `docs/workspaces.md`
- `docs/templates/incubator.brainstorm.template.md`
- `docs/architecture.repo-projections.md`
- `docs/skills/skill-register.md`
- Controlled by: `docs/architecture/adr/adr.idea-spike-adr-implementation-workflow.draft.md`
