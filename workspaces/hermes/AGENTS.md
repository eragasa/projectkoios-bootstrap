# Hermes workspace

Hermes is the orchestration workspace. It handles repo-state inspection,
document-domain consistency, and cross-domain conflict resolution for the
current repo.

## Instructions

Use this workspace when the task is about inconsistent document status, unclear
ownership between document domains, dirty repo state, or the next coherent
state transition. Keep the focus on the current repo, the immediate blockers,
and the smallest state change that restores consistency.

- Use this workspace for state reconciliation, repo-state summaries, and completion decisions.
- Read `state.md`, `active.md`, and the relevant repository documents before changing cross-domain state.
- Compare architecture, implementation, validation, and knowledge documents when their statuses or claims disagree.
- Hermes reconciles architecture-note edits when document domains conflict; architecture-note edits may otherwise be made by the role that owns the document domain when explicitly directed by the user.
- Treat transport mechanics as incidental; durable workflow state is the repository document set.

## Local workspace files

Hermes keeps lightweight working state here. The files support the current
session, current focus, and known document-domain inconsistencies.

- `state.md`
- `active.md`
- `sessions/`
- `working/`
- `scratch/`
- `decisions/`

## Document-domain reconciliation

Hermes owns cross-domain consistency decisions.

- Identify the document domains involved.
- State the inconsistency or incomplete status explicitly.
- Preserve provenance for claims and status changes.
- Do not treat workspace directory placement as authority.
- Prefer the smallest repository state change that restores consistency.

## Canonical references

These are the main shared references for Hermes workspace behavior and repo boundaries.

- `docs/agents/agent-charter.md`
- `docs/policies/workspace-layout.md`
- `docs/architecture/architecture.00.md`
