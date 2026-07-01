---
status: draft
date: 20260701.131500Z
---

# Repository Obsidian projection

See `[architecture.00](architecture.00.md)`.

## Context


Architecture documents and other durable notes should be discoverable with the
same navigation style used in Obsidian: unique filenames, wiki links, and plain
Markdown.

## Decision


`repos/obsidian.py` should focus on:
- note/file naming conventions
- Markdown note discovery
- wikilink-friendly paths and aliases
- frontmatter or metadata extraction when useful
- architecture-note grouping and navigation support

## Consequences

- Repo notes can be treated as an Obsidian-like surface without leaving git.
- Graphify and grep can still discover architecture docs easily.
- The projection layer remains narrow enough to incubate in bootstrap.

## Related notes

- [architecture.repositories.00](architecture.repositories.00.md)
- [architecture.workspaces.obsidian](architecture.workspaces.obsidian.md)
- [architecture.repo-projections](architecture.repo-projections.md)
