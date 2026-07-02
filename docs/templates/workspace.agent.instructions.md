# Workspace agent instructions

Use this file for formatting and structure rules that apply to local
`workspaces/<agent_name>/AGENT.md` files.
Controlled by: [adr.templates](../architecture/adr/adr.templates.draft.md).
Template index: [templates.00](templates.00.md).

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
- `docs/plans/` — cross-session implementation plans owned by Vulcan

## Link rules

- Link to `docs/agent-charter.md` for sandbox message delivery authority.
- Link to `docs/workspaces.md` for workspace layout.
- Link to `docs/architecture.00.md` when the workspace needs architecture context.
- Keep links filename-based and grep-friendly.
- The workspace `AGENT.md` should describe who reads inbox, who writes outbox,
  and that Hermes delivers mail.

## Plan ownership

Vulcan owns implementation plans. Plans live at `docs/plans/` and derive from an accepted ADR or implementation brief. Each plan must include Source, Scope, Verification method, Task breakdown, and an optional Escalation note. When an ADR brief is too vague to plan against, Vulcan escalates via handoff to Hermes.

## Decision note promotion trigger

If a `decisions/` note is referenced in any outbox message, handoff artifact, or ADR comment, the note must be promoted to a draft ADR or explicitly annotated `archived` within one session. This prevents cross-role reference drift without forcing ephemeral notes into the ADR surface.

## Editing rule

If a request is about workspace formatting or runtime instruction wording,
update this file first or alongside the workspace change so the convention stays
durable.

Only Hermes may edit `docs/architecture*.md`, and only when Zeus explicitly
requests the change.
