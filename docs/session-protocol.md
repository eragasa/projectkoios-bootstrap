# Pi session protocol

This document mirrors the session-start and session-stop rules for the pi meta-harness.

## Session start

Before doing other work in a new session:

1. Check current ADRs, current handoff locations, git branch, git status, and
   the last few commits.
2. Treat `docs/archive/handoffs/` as provenance only. An archived
   `Status: active` header is historical evidence, not an instruction to run
   old work.
3. If an archived handoff conflicts with current filesystem state, current
   ADRs, or later implementation reports, report it as stale or superseded.
4. Report pending current work before making changes.

## Session stop

Before ending a session:

1. If files changed, run the smallest relevant validation you can justify.
2. Report files changed and validation results.
3. Write or update the relevant handoff if work must continue in another harness.
4. Ask before commit/push unless the user already directed it.
