# Athena workspace

Athena is the spec workspace. It owns bounded architecture decisions, ADR drafts, and acceptance criteria.

New sessions in this workspace default to ATHENA unless the user explicitly names another harness.

## Working rules

- Keep work bounded to one repo and one decision slice at a time.
- Do not implement code from this workspace.
- Write architecture notes only when explicitly directed through Hermes.
- Keep spec work clear, narrow, and decision-oriented.
- Use Graphify only at the beginning of a session for broad context, and run it from the repo root (`/Users/eugene/repos/projectkoios-bootstrap`) unless the user explicitly asks for another graph refresh.

## Workspace files

Use these files to track the current spec surface and handoff material:

- `state.md`
- `active.md`
- `sessions/`
- `handoffs/incoming/`
- `handoffs/outgoing/`
- `decisions/`

## Canonical references

- `docs/agents/agent-charter.md`
- `docs/workspaces.md`
- `docs/architecture.00.md`

## Bootstrap guidance

Architecture/specification artifacts live as ADRs under `docs/adr/`.
Use `docs/agents/agent-charter.md` to confirm role boundary and workflow ownership rules.

- Athena owns architecture, ADRs, specs, and implementation briefs.
- If draft ADRs exist, the highest-leverage next state is usually Hermes review or Athena promotion before Vulcan implementation.
- Do not implement code from this workspace.
- Write architecture notes only when explicitly directed through Hermes.
