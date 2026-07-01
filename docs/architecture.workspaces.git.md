---
status: draft
date: 20260701.131500Z
---

# Workspaces git projection

See `[architecture.00](architecture.00.md)`.

## Context


The workspace layer needs a compact representation of git state so an agent can
see which repository it is operating on and whether the tree is clean.

## Decision


A workspace git projection should capture:
- repository root
- branch
- commit or revision identifier when available
- dirty/clean status
- current repo focus
- any staged or untracked workspace-relevant files

This projection belongs in bootstrap, not in the mothership domain packages.

## Consequences

- Hermes can summarize repo state without scanning every repo manually.
- Agent workspaces can carry the minimum state needed for session resumption.
- Git details remain a projection, not the source of truth for product
  architecture.

## Related notes

- [architecture.workspaces.00](architecture.workspaces.00.md)
- [architecture.repos.git](architecture.repos.git.md)
- [architecture.repositories.00](architecture.repositories.00.md)
