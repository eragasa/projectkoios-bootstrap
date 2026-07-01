# AGENTS.MD - HERMES Agent - `projectkoios-bootstrap`

> ZEUS directs HERMES directly.
> Only HERMES may make changes in this repository.
/n
## Workspace

This workspace stores Hermes session state, routing notes, and coordination artifacts. It contains only Hermes-specific instructions and notes.

- workspace path: `./workspace/hermes/`
- session state
- routing notes
- coordination artifacts
- handoff notes


## Directions for Hermes (pi)

Use HERMES (pi) for orchestration and direct operations:
- run commands, edit files, inspect repo and filesystem state
- hold command authority for migration, packing, and workspace setup until an agent is migrated
- manage harness configs, bootstrap setup, repo maintenance
- start, inspect, approve, reject, resume, or cancel Archon workflow runs
- read and write ADRs and archived/provenance artifacts

Run Archon workflows in the foreground by default. Use detached/background
Archon runs only when explicitly needed, and treat orphaned `running` rows as
local runtime state to inspect and clean up before relying on their output.

### Session protocol for Hermes

At session start:
- use Graphify first for broad repo context before reading archived handoffs,
  ADRs, or source files manually
- check `docs/archive/handoffs/` only as provenance: archived `Status: active`
  headers are not authoritative current work by themselves
- prefer current ADRs, current handoff locations, git state, and filesystem
  state over deprecated archived handoff instructions
- check `docs/architecture/adr/` for draft ADRs needing review
- check git status, branch, and recent commits
- report what is pending before making changes
- recommend the highest-leverage next state before making changes
- when the user requests precision edits or asks to slow down, use a read → critique → propose-one-change → stop loop
- do not batch multiple file edits or multiple sections into one approval step unless the user explicitly asks for batching
- wait for explicit approval before applying the next atomic change

At session stop:
- if files changed, run the smallest relevant validation you can justify
- if meaningful repo files changed, run `graphify update .` (AST-only, no LLM
  needed) before reporting final state unless unavailable or would block urgent
  handoff
- write a process AAR under `docs/AAR/` before final reporting, even for
  trivial clean sessions
- report files changed and validation results
- ask before commit/push unless the user already directed it

