---
status: draft
date: 20260701.131500Z
---

# Workspaces overview

See `[architecture.00](architecture.00.md)`.

## Context


Project Koios needs persistent per-agent workspace state so sessions can resume
without re-deriving the current task, repo focus, blockers, or next action.
The controlling protocol is the accepted ADR
`docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`.

A workspace is agent-scoped, not repo-scoped:
- Athena keeps bounded spec context
- Vulcan keeps implementation context
- Koios keeps knowledge/provenance context

## Decision


Use `workspaces/<agent_name>/` as the persistent workspace surface.
Each workspace should contain:
- `state.md` with stable top JSON metadata and durable resume state
- `active.md` with stable top JSON metadata, priority stack, waiting-on items, active working material, ignored scope, and exit criteria
- `sessions/`
- `working/`
- `scratch/`
- `decisions/`

Workspace-local notes in `decisions/`, `working/`, `scratch/`, and `sessions/` are control surfaces only. Files in `working/` are active only when named in `active.md`; directory placement does not create authority.

## Consequences

- Sessions can resume from a small, durable, human-readable state surface.
- Each agent keeps its own context without mixing unrelated roles.
- Workspace files remain compatible with git and Obsidian-style Markdown
  navigation.

## Related notes

- [architecture.workspaces.git](architecture.workspaces.git.md)
- [architecture.workspaces.obsidian](architecture.workspaces.obsidian.md)
- [architecture.repositories.00](architecture.repositories.00.md)
