---
status: draft
date: 20260701.131500Z
---

# Repository git projection

See `[architecture.00](architecture.00.md)`.

## Context


Bootstrap needs a small git-focused projection for repository identity and
status so agent workspaces can summarize the current repo accurately.

## Decision


`repos/git.py` should focus on:
- repository root discovery
- branch and revision identification
- dirty/clean state
- staged/untracked file awareness
- lightweight repo identity metadata

It should not become a general git automation layer.

## Consequences

- Workspace summaries can report repo state consistently.
- Git state is handled as a projection, not the product architecture.
- The implementation remains easy to test and replace later.

## Related notes

- [architecture.repositories.00](architecture.repositories.00.md)
- [architecture.workspaces.git](architecture.workspaces.git.md)
- [architecture.repos.obsidian](architecture.repos.obsidian.md)
