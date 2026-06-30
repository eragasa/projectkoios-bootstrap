# Pi session protocol

This document mirrors the session-start and session-stop rules for the pi meta-harness.

## Session start

Before doing other work in a new session:

1. Check `docs/archive/handoffs/` for any active artifacts not yet processed.
2. Check git branch, status, and the last few commits.
3. Report pending work before making changes.

## Session stop

Before ending a session:

1. If files changed, run the smallest relevant validation you can justify.
2. Report files changed and validation results.
3. Write or update the relevant handoff if work must continue in another harness.
4. Ask before commit/push unless the user already directed it.
