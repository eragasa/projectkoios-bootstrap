# ADR 20260630.121053: Handoff threshold for trivial sessions

## Status

historic

## Context

The meta-harness session protocol requires a handoff file at session end
when work must continue. In practice, many sessions perform trivial or
same-harness work — push, status inspection, minor edits — that generate
no cross-harness artifact boundary crossing. Writing a handoff file for
every session, even same-harness continuation, adds ceremony without
corresponding value.

Current convention also fans out handoffs to every other harness (e.g.
a pi→pi session-end note also copied to Athena), multiplying overhead.

## Proposal

Require a handoff file only when at least one of these conditions is met:

1. Artifacts crossed a harness boundary (a new architecture-spec,
   implementation-brief, patch, test-results, or knowledge-note was produced
   for a different harness to consume).
2. The session produced durable work that changes the system state
   (committed files, new ADRs, new handoff artifacts).
3. Explicit blocking or escalation must be recorded.

If none of these conditions are met — the session was read-only, pushed
existing commits, or inspected state — the session is documented by
terminal output only (git log, git status, a brief verbal summary).
No handoff file is written.

Additionally, remove the convention of broadcasting session-end
notifications to other harnesses that have no stake in the work.

## Consequences

- Handoff files are archived at `docs/archive/handoffs/` rather than cluttering harness root directories.
- Sessions that need handoffs are clearly distinguished from sessions
  that don't.
- New operators have fewer files to scan at session start.
- Risk of losing state between same-harness sessions is mitigated by
  relying on git (commits = durable state) rather than handoff files.
