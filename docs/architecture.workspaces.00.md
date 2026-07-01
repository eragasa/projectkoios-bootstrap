---
status: draft
date: 20260701.131500Z
---

# Workspaces overview

See `[architecture.00](architecture.00.md)`.

## Context


Project Koios needs persistent per-agent workspace state so sessions can resume
without re-deriving the current task, repo focus, or outstanding handoffs.

A workspace is agent-scoped, not repo-scoped:
- Hermes keeps routing and repo-state context
- Athena keeps bounded spec context
- Vulcan keeps implementation context
- Koios keeps knowledge/provenance context

## Decision


Use `workspaces/<agent_name>/` as the persistent workspace surface.
Each workspace should contain:
- `state.md`
- `active.md`
- `sessions/`
- `handoffs/incoming/`
- `handoffs/outgoing/`
- `decisions/`

## Consequences

- Sessions can resume from a small, durable, human-readable state surface.
- Each agent keeps its own context without mixing unrelated roles.
- Workspace files remain compatible with git and Obsidian-style Markdown
  navigation.

## Related notes

- [architecture.workspaces.git](architecture.workspaces.git.md)
- [architecture.workspaces.obsidian](architecture.workspaces.obsidian.md)
- [architecture.repos.00](architecture.repos.00.md)
