# Handoff contract

opencode starts execution only when the incoming request is specific enough to implement and validate.

## Acceptable inputs

- an approved Archon feature plan
- a tightly scoped user request with target repo and expected outcome
- a bug report with enough reproduction detail to investigate

## Required from Archon plans

Before implementation, the handoff should identify:
- objective
- in-scope work
- non-goals
- target repository or repositories
- likely file paths or package areas
- validation expectations
- unresolved questions

## If the handoff is incomplete

Do not guess.

Switch to consultation mode and ask for the missing pieces, especially:
- which repo owns the change
- whether work is implementation vs design
- what counts as done
- what tests or checks are required

## Completion report back to Archon or user

When execution finishes, report:
- files changed
- validations run and results
- deviations from plan
- follow-up work or architecture questions

## Handoff file convention

Handoff files written by opencode follow the shared convention defined in root `AGENTS.md`:

**Filename:** `YYYYMMDD.HHMMSS_<topic>.md`
Example: `2026-06-29.214500_implementation-report.md`

**Header:**

```
Origin: opencode
Created: <YYYY-MM-DD HH:MM>
From: Vulcan
To: <Athena|pi|user>
Status: draft|active|complete
```
