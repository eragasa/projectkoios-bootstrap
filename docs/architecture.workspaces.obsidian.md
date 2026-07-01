---
status: draft
date: 20260701.131500Z
---

# Workspaces Obsidian projection

See `[architecture.00](architecture.00.md)`.

## Context


Architecture documents, decisions, and session notes should be navigable like an
Obsidian repository while still living in git.

## Decision


Use Obsidian-friendly Markdown conventions for workspace notes:
- unique filenames prefixed with `architecture.`
- wiki links for note-to-note navigation
- optional aliases for human-friendly labels
- plain Markdown files, not a separate database

Workspace notes may treat architecture docs as a vault-like surface, but only for
navigation and persistence — not as a replacement for the canonical repo maps or
harness charter.

## Consequences

- Notes are easy to find with grep and Graphify.
- Obsidian navigation stays simple because filenames are unique.
- The workspace layer can reuse the same Markdown conventions as architecture
  docs.

## Related notes

- [architecture.workspaces.00](architecture.workspaces.00.md)
- [architecture.repos.obsidian](architecture.repos.obsidian.md)
- [architecture.repo-projections](architecture.repo-projections.md)
