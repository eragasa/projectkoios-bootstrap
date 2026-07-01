# Workspace agent instructions

Use this file for formatting and structure rules that apply to local
`workspaces/<agent_name>/AGENT.md` files.

## When to use this template

Use these instructions when:
- creating a new agent workspace
- refreshing per-agent runtime instructions
- changing the local workspace layout or file conventions
- normalizing the local AGENT file across Hermes, Athena, Vulcan, and Koios

## Required workspace format

- Keep the file local to `workspaces/<agent_name>/AGENT.md`.
- Use a human-readable title.
- State the role and responsibility of the workspace.
- Include short instruction bullets.
- List the local workspace files the agent should expect.
- Include mailbox instructions (`inbox/`, `outbox/`) and state that Hermes
  delivers mail.
- Link to canonical references using Markdown links.

## Required workspace files

- `AGENT.md`
- `state.md`
- `active.md`
- `inbox/`
- `outbox/`
- `sessions/`
- `handoffs/incoming/`
- `handoffs/outgoing/`
- `decisions/`

## Link rules

- Link to `docs/agent-charter.md` for routing authority.
- Link to `docs/workspaces.md` for workspace layout.
- Link to `docs/architecture.00.md` when the workspace needs architecture context.
- Keep links filename-based and grep-friendly.
- The workspace `AGENT.md` should describe who reads inbox, who writes outbox,
  and that Hermes delivers mail.

## Editing rule

If a request is about workspace formatting or runtime instruction wording,
update this file first or alongside the workspace change so the convention stays
durable.

Only Hermes may edit `docs/architecture*.md`, and only when Zeus explicitly
requests the change.
