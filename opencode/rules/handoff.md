# Implementation contract

opencode starts execution only when the incoming request is specific enough to implement and validate.

## Acceptable inputs

- an approved Archon feature plan
- a tightly scoped user request with target repo and expected outcome
- a bug report with enough reproduction detail to investigate

## Required from architecture plans

Before implementation, the request should identify:
- objective
- in-scope work
- non-goals
- target repository or repositories
- likely file paths or package areas
- validation expectations
- unresolved questions

## If the request is incomplete

Do not guess.

Switch to consultation mode and ask for the missing pieces, especially:
- which repo owns the change
- whether work is implementation vs design
- what counts as done
- what tests or checks are required

## Completion report

When execution finishes, report:
- files changed
- validations run and results
- deviations from plan
- follow-up work or architecture questions

## ADR convention

Durable decisions and cross-harness observations are placed in ADRs
under `docs/adr/`. See root `AGENTS.md` for the ADR file
convention.
