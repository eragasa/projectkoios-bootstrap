---
name: koios-workspace-bootstrap
description: Initialize persistent per-agent workspaces, mail folders, and local AGENT.md files
metadata:
  agent: knowledge-agent
  harness_role: consumer-producer
  consumes:
    - user-request
    - repo-state-summary
    - routing-recommendation
  produces:
    - knowledge-note
    - provenance-index
---

## When to use this skill

Use this skill when Koios needs to create or refresh the persistent
`workspaces/<agent_name>/` layout for Hermes, Athena, Vulcan, or Koios.
Use the bootstrap command `projectkoios bootstrap workspaces init` when you need
to materialize the files. It is for bootstraping workspace persistence, not for
product architecture.

## Agent responsibility

Create and maintain the agent-scoped workspace folders and seed files used to
resume sessions across runs. Keep the layout small, human-readable, and easy to
inspect with git, grep, and Obsidian. Seed each workspace with its own local
`AGENT.md` file and mailbox folders (`inbox/`, `outbox/`).

## Inputs

- `user-request` — the request to create or refresh agent workspaces
- `repo-state-summary` — current repo context when available
- `routing-recommendation` — the requested or inferred target agent scope

## Procedure

1. Identify the requested agent scopes. Default to the four canonical workspaces:
   Hermes, Athena, Vulcan, and Koios.
2. Create `workspaces/<agent_name>/` for each requested scope.
3. Seed each workspace with:
   - `AGENT.md`
   - `state.md`
   - `active.md`
   - `inbox/`
   - `outbox/`
   - `sessions/`
   - `handoffs/incoming/`
   - `handoffs/outgoing/`
   - `decisions/`
4. Populate the seed files with short placeholders for current state,
   active focus, blockers, and last validated decision.
5. Keep the files plain Markdown and filesystem-oriented.
6. Record what was created, where it lives, and the provenance of the request.
7. Produce a durable knowledge note and provenance index so Hermes can audit
   the workspace bootstrap later.

## Output artifact

- `knowledge-note` — durable note describing the workspace layout and the
  created seed state
- `provenance-index` — mapping from the workspace bootstrap note to the source
  request and any cited repo state

## Failure modes

- Workspace layout is ambiguous — ask Hermes for the canonical scope before
  creating files.
- Mail system direction is ambiguous — ask Hermes before routing inbox/outbox
  conventions.
- Existing files contain conflicting state — report the conflict rather than
  overwriting without permission.
- Request tries to repurpose the workspace layout as product architecture —
  refuse and route back to Hermes/Athena.

## Escalation rule

If the request implies a new workspace schema, a new agent role, or a change to
routing authority, escalate to Hermes before making any file changes.
