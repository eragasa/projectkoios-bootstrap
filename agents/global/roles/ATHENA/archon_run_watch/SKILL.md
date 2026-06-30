---
name: archon_run_watch
description: |
  Use when the user asks to start a Project Koios session, inspect current
  handoffs, route work between harnesses, run or monitor Archon workflows,
  clean stale Archon runs, create handoff artifacts, or decide what to do
  next.
  Triggers: "new session", "what next?", "route this", "go archon",
  "make a handoff", "turn this interview into a spec",
  "prepare a Vulcan handoff", "check Archon runs",
  "clean stale Archon run", "inspect handoffs".
  NOT for: architecture design or product domain work.
---

# archon_run_watch

Session-start, routing, Archon run monitoring, and handoff creation for
Project Koios meta-harness operations.

## Session start protocol

1.  Inspect current ADRs, current handoff locations, git state, and recent
    commits.
2.  Treat `docs/archive/handoffs/` as provenance only. Archived
    `Status: active` headers are historical claims, not authoritative current
    work.
3.  Report stale or superseded archived claims when they explain confusing
    state, but do not ask the user to resolve questions already answered by
    later ADRs, implementation reports, or filesystem state.
4.  Report pending current active/draft artifacts before changing files.

## Routing decision table

| Task | Route to |
|---|---|
| architecture, ADRs, planning | Athena |
| implementation, tests, validation | Vulcan |
| knowledge notes, provenance, vault | Koios |
| run control, handoff coordination, operations | Hermes (self) |
| lightweight direct edits | Hermes (self, no specialist) |

## Archon preflight

1.  Run `archon workflow list --json` or validate the specific workflow.
2.  Inspect `worktree.enabled` in the workflow YAML before choosing a
    run strategy.
3.  If input files are untracked and the workflow uses worktree isolation,
    commit or stage first, or use a live-checkout workflow.
4.  Do not apply `--branch` when `worktree.enabled: false` is declared.

## Archon run monitoring

1.  Start detached with `archon workflow run <name> --detach`.
2.  Capture run ID via `archon workflow list --json`.
3.  Poll status with `archon workflow get <id> --json`.
4.  Tail detached child log if available.
5.  Detect stale-running: child process gone, no completion event, no
    artifact output.
6.  Abandon stale records with `archon workflow abandon <id> --json`.
    Escalate if sandbox blocks writes to `~/.archon/archon.db`.

## Fast fallback rule

After two AI-node Archon attempts exit stale in the same way, stop
retrying. Write a handoff or deviation note. Proceed as Hermes with a
direct artifact. Report what Archon failed to do and what was done
instead.

## Handoff creation discipline

1.  Use filename format `YYYYMMDD.HHMMSS_<topic>.md`.
2.  Include required header fields: `Origin`, `Created`, `From`, `To`,
    `Status`.
3.  Include provenance fields when mediation is involved:
    `Acting-As`, `Scope`, `Repository`, `Delegated-Operator`.
4.  Do not collapse Codex into Pi/Hermes or Athena — preserve mediation
    provenance.

## Stop conditions

1.  No active Archon runs left unintentionally.
2.  No generated runtime state committed.
3.  If files changed, report changed files and validation.
