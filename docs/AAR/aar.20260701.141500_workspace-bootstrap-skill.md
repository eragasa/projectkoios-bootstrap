# AAR 20260701.141500: Workspace bootstrap skill

## Scope

Created persistent per-agent workspaces in the bootstrap repo and added a Koios skill for bootstrapping them.

## What happened

- Added `workspaces/hermes`, `workspaces/athena`, `workspaces/vulcan`, and `workspaces/koios` with seed `state.md` and `active.md` files plus handoff/session/decision folders.
- Added `workspaces/` to `.gitignore` so the persistent workspace state stays local.
- Created `agents/global/goose/skills/koios-workspace-bootstrap/SKILL.md` and listed it in `goose/AGENT.md`.

## Process issues

- The workspace layout needed both a local filesystem scaffold and a reusable skill definition.
- The runtime persistence surface should remain untracked and local-only.

## Proposed follow-up improvements

- Add a small workspace bootstrap helper in `projectkoios.bootstrap` if we want automated initialization instead of manual directory creation.
- Consider adding a template note for `workspaces/<agent>/state.md` and `active.md` contents.

## Candidate ADR or implementation topics

- Bootstrap workspace initialization helper.
- Skill-driven workspace template generation.

## Current status

Complete.
