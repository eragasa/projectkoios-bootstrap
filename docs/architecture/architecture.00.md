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

## Related bootstrap architecture

- `docs/agent-charter.md`
- `docs/workspaces.md`
- `docs/templates/incubator.brainstorm.template.md`
- `docs/architecture.repo-projections.md`
- Controlled by: `docs/architecture/adr/adr.idea-spike-adr-implementation-workflow.draft.md`
