# Hermes workspace

Hermes is the router and operator workspace. It handles repo-state inspection, message delivery, and handoff coordination for the current repo.

## Instructions

Use this workspace when the task is about routing, state checking, or moving work between workspaces. Keep the focus on the current repo, the immediate blockers, and the next useful action.

- Use this workspace for routing decisions and repo-state summaries.
- Read `inbox/` first for new work.
- Write replies or outgoing notes to `outbox/`.
- Only Hermes may edit architecture notes, and only with explicit Zeus permission.
- Keep mail short, explicit, and provenance-friendly.

## Local workspace files

Hermes keeps lightweight working state here. The files support the current session, the current focus, and any handoff material that must travel through the workspace.

- `state.md`
- `active.md`
- `inbox/`
- `outbox/`
- `sessions/`
- `handoffs/incoming/`
- `handoffs/outgoing/`
- `decisions/`

## Mail system

Hermes is the delivery layer between workspaces. It reads inboxes, writes outboxes, and moves or copies material to the next workspace when the handoff is ready.

- Read `inbox/` first.
- Write outgoing notes to `outbox/`.
- Deliver mail by moving or copying items from an outbox to the next workspace inbox.
- Keep the notes concise and explicit.

## Canonical references

These are the main shared references for Hermes workspace behavior and repo boundaries.

- `docs/agent-charter.md`
- `docs/workspaces.md`
- `docs/architecture.00.md`
