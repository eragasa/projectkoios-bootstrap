---
status: draft
date: 20260701.131500Z
---

# Architecture index

## Purpose

This is the namespace index for bootstrap architecture notes.
Use it as the entry point for `architecture.*` documents and as the anchor
note for Obsidian-style navigation.

## Scope

These notes describe the bootstrap-side workspace, repository-projection, and
harness-related architecture for `projectkoios-bootstrap`.
They do not replace `docs/architecture.md` in the mothership repo.

## Protection

Only Hermes may modify `docs/architecture*.md`, and only when Zeus explicitly
directs the change.

## Index

### Workspace notes
- [architecture.workspaces.00](architecture.workspaces.00.md)
- [architecture.workspaces.git](architecture.workspaces.git.md)
- [architecture.workspaces.obsidian](architecture.workspaces.obsidian.md)

### Repository projection notes
- [architecture.repositories.00](architecture.repositories.00.md)
- [architecture.repos.git](architecture.repos.git.md)
- [architecture.repos.obsidian](architecture.repos.obsidian.md)
- [architecture.repo-projections](architecture.repo-projections.md)

## Naming convention

- All bootstrap architecture notes use the `architecture.` prefix.
- Filenames stay unique and grep-friendly.
- Use Markdown links for navigation so grep, Graphify, and Obsidian all work.
- The date slug lives under `## Status` and uses `YYYYMMDD.HHMMSSZ`.
- Related notes should link back here with `[architecture.00](architecture.00.md)`.

## Related bootstrap architecture

- `docs/agent-charter.md`
- `docs/workspaces.md`
- `docs/architecture.repo-projections.md`


```text
   docs/
   ├── README.md
   ├── index.md
   ├── architecture/
   │   ├── adr/
   │   ├── specs/
   │   └── briefs/
   ├── workflows/
   │   ├── process/
   │   ├── runbooks/
   │   └── templates/
   ├── skills/
   │   ├── specs/
   │   └── design/
   ├── governance/
   │   ├── policies/
   │   ├── roles/
   │   └── decisions/
   ├── handoffs/
   ├── archive/
   │   ├── handoffs/
   │   └── superseded/
   ├── AAR/
   └── notes/
 ```