# pi — Project Koios operator harness

You are the pi-side operator harness for Project Koios.

## Scope

- Use pi to run Archon workflows and other operator-facing tasks.
- Keep shared repo rules in the repository root `AGENTS.md`.
- Use `goose/AGENT.md` and `opencode/AGENTS.md` for the other harnesses; do not duplicate their instructions here.

## Harness boundaries

- `pi` = operator interface and orchestration
- `goose` = knowledge curation and vault work
- `opencode` = implementation, tests, validation, and runtime debugging

## Local install

- `scripts/koios install` syncs this file into `~/.pi/agent/AGENTS.md` via `~/pi/agent/AGENTS.md`.
- Update this file when pi-specific operator guidance changes.

## Guardrails

- Do not manage `pi/agent/auth.json` from this repo install flow.
- Prefer repo-managed config over ad hoc home-directory edits.
