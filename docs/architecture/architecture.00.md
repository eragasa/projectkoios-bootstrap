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


## Index

| note | controlling ADR |
|---|---|
| [architecture.documents](architecture.documents.md) | None |
| [architecture.adr.00](architecture.adr.00.md) | [adr.adr](../adr/adr.adr.md) |
| [architecture.adr.template](architecture.adr.template.md) | [adr.adr-template-contract](../adr/adr.adr-template-contract.md) |
| [architecture.lifecycle.00](architecture.lifecycle.00.md) | [adr.idea-spike-adr-implementation-workflow](../adr/adr.idea-spike-adr-implementation-workflow.draft.md) |
| [architecture.adr.names](architecture.adr.names.md) | [adr.adr-names](../adr/adr.adr-names.draft.md) |
| [architecture.brainstorm-capture-and-incubator-note-template](architecture.brainstorm-capture-and-incubator-note-template.md) | [adr.brainstorm-capture-and-incubator-template](../adr/adr.brainstorm-capture-and-incubator-template.draft.md) |
| [architecture.draft-comment-and-promotion-workflow](architecture.draft-comment-and-promotion-workflow.md) | [archived adr-draft-comment-and-promotion-workflow](../archive/architecture/adr/adr.20260702.012900_adr-draft-comment-and-promotion-workflow.md) |
| [architecture.controlling-adr-join-protocol](architecture.controlling-adr-join-protocol.md) | [adr.controlling-adr-join-protocol](../adr/adr.controlling-adr-join-protocol.draft.md) |
| [architecture.draft-adr-comment-processing-protocol](architecture.draft-adr-comment-processing-protocol.md) | [adr.draft-adr-comment-processing-protocol](../adr/adr.draft-adr-comment-processing-protocol.draft.md) |
| [architecture.skill-register-and-adr-binding-policy](architecture.skill-register-and-adr-binding-policy.md) | [adr.skill-register-and-adr-binding-policy](../adr/adr.skill-register-and-adr-binding-policy.draft.md) |
| [architecture.canonical-workspace-state-and-next-action-protocol](architecture.canonical-workspace-state-and-next-action-protocol.md) | [adr.canonical-workspace-state-and-next-action-protocol](../adr/adr.canonical-workspace-state-next-action-protocol.draft.md) |
| [architecture.comment-scope-and-control-boundary-review-rule](architecture.comment-scope-and-control-boundary-review-rule.md) | [adr.comment-scope-and-control-boundary-review-rule](../adr/adr.comment-scope-and-control-boundary-review-rule.draft.md) |
| [architecture.control-surfaces-and-ownership-boundaries](architecture.control-surfaces-and-ownership-boundaries.md) | [adr.control-surfaces-and-ownership-boundaries](../adr/adr.control-surfaces-and-ownership-boundaries.draft.md) |
| [architecture.implementation-plan-ownership](architecture.implementation-plan-ownership.md) | [adr.implementation-plan-ownership](../adr/adr.implementation-plan-ownership.draft.md) |
| [architecture.templates](architecture.templates.md) | [adr.templates](../adr/adr.templates.draft.md) |
| [architecture.koios-adversarial-code-review-authority](architecture.koios-adversarial-code-review-authority.md) | [adr.koios-adversarial-code-review-authority](../adr/adr.20260702.043600_koios-adversarial-code-review-authority.draft.md) |
| [architecture.adversarial-two-plane-gate](architecture.adversarial-two-plane-gate.md) | [adr.adversarial-two-plane-gate](../adr/adr.adversarial-two-plane-gate.draft.md) |
| [architecture.ownership-ledger-role-alignment](architecture.ownership-ledger-role-alignment.md) | [adr.ownership-ledger-role-alignment](../adr/adr.ownership-ledger-role-alignment.draft.md) |
| [architecture.unified-diff-review-surface](architecture.unified-diff-review-surface.md) | [adr.unified-diff-review-surface](../adr/adr.unified-diff-review-surface.draft.md) |
| [architecture.ui-core](architecture.ui-core.md) | [adr.ui-core](../adr/adr.ui-core.draft.md) |
| [architecture.workflow-ui](architecture.workflow-ui.md) | [adr.workflow-ui](../adr/adr.workflow-ui.draft.md) |
| [architecture.json-schemas](architecture.json-schemas.md) | [adr.json-schemas](../adr/adr.json-schemas.draft.md) |
| [architecture.agent-windows-with-on-message-triggers](architecture.agent-windows-with-on-message-triggers.md) | [adr.agent-windows-on-message-triggers](../adr/adr.agent-windows-on-message-triggers.draft.md) |
| [architecture.json-adr-storage-topology](architecture.json-adr-storage-topology.md) | [adr.json-database-for-adr-storage](../adr/adr.json-database-for-adr-storage.draft.md) |
| [architecture.spike-entry-conditions](architecture.spike-entry-conditions.md) | [adr.spike-entry-conditions](../adr/adr.spike-entry-conditions.draft.md) |
| [architecture.workspaces.00](architecture.workspaces.00.md) | None |
| [architecture.workspaces.git](architecture.workspaces.git.md) | None |
| [architecture.workspaces.obsidian](architecture.workspaces.obsidian.md) | None |
| [architecture.repositories.00](architecture.repositories.00.md) | None |
| [architecture.repos.git](architecture.repos.git.md) | None |
| [architecture.repos.obsidian](architecture.repos.obsidian.md) | None |
| [architecture.repo-projections](architecture.repo-projections.md) | None |
| [implementation.00](../implementation/implementation.00.md) | [adr.implementation](../adr/adr.implementation.draft.md) |

### ADR locations

- `docs/adr/` — active ADR control surface for bounded decision records.
- `docs/archive/architecture/adr/` — historic ADR archive.

## Naming convention

- All bootstrap architecture notes use the `architecture.` prefix.
- Filenames stay unique and grep-friendly.
- Use Markdown links for navigation so grep, Graphify, and Obsidian all work.
- ADR filenames live under `docs/adr/`.
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

- `docs/agents/agent-charter.md`
- `docs/workspaces.md`
- `docs/templates/incubator.brainstorm.template.md`
- `docs/architecture.repo-projections.md`
- `docs/skills/skill-register.md`
- Controlled by: `docs/adr/adr.idea-spike-adr-implementation-workflow.draft.md`
