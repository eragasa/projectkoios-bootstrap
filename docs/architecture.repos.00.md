---
status: draft
date: 20260701.131500Z
---

# Repository projections overview

See `[architecture.00](architecture.00.md)`.

## Context


Project Koios wants a bootstrap-side projection layer that treats each git repo
as both:
- a version-controlled source repository
- an Obsidian-like Markdown repository of durable architecture notes

This is the place for repo state, note layout, and projection helpers that are
shared across agent workspaces.

## Decision


Use a projection package family under:

```text
src/python/projectkoios/bootstrap/
├── repos/
│   ├── __init__.py
│   ├── git.py
│   └── obsidian.py
```

## Consequences

- Repo state and note state stay close together.
- Workspace code can ask for git and note projections without pulling product
  domain packages into bootstrap.
- The design stays small enough to incubate before extraction.

## Related notes

- [architecture.workspaces.00](architecture.workspaces.00.md)
- [architecture.repos.git](architecture.repos.git.md)
- [architecture.repos.obsidian](architecture.repos.obsidian.md)
