# Workspace agent instructions

Use this file for formatting and structure rules that apply to local
`workspaces/<agent_name>/AGENTS.md` files.
Controlled by: [adr.templates](../adr/adr.templates.draft.md).
Template index: [templates.00](templates.00.md).

## When to use this template

Use these instructions when:
- creating a new agent workspace
- refreshing per-agent runtime instructions
- changing the local workspace layout or file conventions
- normalizing the local AGENT file across Hermes, Athena, Vulcan, and Koios

## Required workspace format

- Keep the file local to `workspaces/<agent_name>/AGENTS.md`.
- Use a human-readable title.
- State the role and responsibility of the workspace.
- Include short instruction bullets.
- List the local workspace files the agent should expect.
- State that durable workflow state is the repository document set and each document's status.
- Link to canonical references using Markdown links.

## Required workspace files

- `AGENTS.md`
- `state.md`
- `active.md`
- `sessions/`
- `working/`
- `scratch/`
- `decisions/`
- `docs/plans/` — cross-session implementation plans owned by Vulcan

## Link rules

- Link to `docs/agents/agent-charter.md` for document-domain ownership authority.
- Link to `docs/policies/workspace-layout.md` for workspace layout.
- Link to `docs/architecture.00.md` when the workspace needs architecture context.
- Keep links filename-based and grep-friendly.
- The workspace `AGENTS.md` should describe which repository document domain the role owns.

## Plan ownership

Vulcan owns implementation plans. Plans live at `docs/plans/` and derive from an accepted ADR or implementation brief. Each plan must include Source, Scope, Verification method, Task breakdown, and an optional Escalation note. When an ADR brief is too vague to plan against, Vulcan records the inconsistency for Hermes reconciliation.

## Decision note promotion trigger

If a `decisions/` note is referenced by any authoritative repository document or ADR comment, the note must be promoted to the appropriate document domain or explicitly annotated `archived` within one session. This prevents cross-role reference drift without forcing ephemeral notes into the ADR surface.

## Editing rule

If a request is about workspace formatting or runtime instruction wording,
update this file first or alongside the workspace change so the convention stays
durable.

Only Hermes may edit `docs/architecture*.md`, and only when Zeus explicitly
requests the change.
