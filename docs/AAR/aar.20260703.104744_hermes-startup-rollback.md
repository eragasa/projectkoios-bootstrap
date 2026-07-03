# AAR 20260703.104744: Hermes startup rollback

## Scope
Rolled back the Hermes startup/new-session launcher changes in `projectkoios-bootstrap`.

## What happened
Reverted the commits that added the Hermes startup launcher, the `new` session launcher behavior, and the auto-start-on-koios-start hook. The result removes the confusing script path / reload behavior so Hermes session changes stay explicit instead of being hidden behind startup automation.

## Process issues
The prior startup flow was too indirect for the user’s expectation of a simple LLM/session reload.

## Proposed follow-up improvements
If session reset support is added again, keep it explicit and minimal, and separate it from any bootstrapping or auto-start hooks.

## Candidate ADR or implementation topics
Hermes session reset ergonomics.

## Current status
Complete.
