# Pi session protocol

This document mirrors the session-start and session-stop rules for the pi meta-harness.

## Session start

Before doing other work in a new session:

1. Check `archon/handoffs/`, `opencode/handoffs/`, and `pi/handoffs/` for new or active artifacts.
2. Check git branch, status, and the last few commits.
3. Report pending work before making changes.

If an active artifact is stale because later evidence satisfies or supersedes
it, leave the historical header unchanged and write a pi completion-decision
handoff that names the stale artifact, controlling evidence, and closure result.

## Session stop

Before ending a session:

1. If files changed, run the smallest relevant validation you can justify.
2. Report files changed and validation results.
3. Write or update the relevant handoff if work must continue in another harness.
4. Ask before commit/push unless the user already directed it.
