# AAR 20260701.014433: Always write session AARs

## Scope

This AAR covers the session that changed Project Koios bootstrap guidance to
require an AAR at every session end.

## What happened

After a prior session missed the AAR gate until the user asked about it, the
user requested that `AGENTS.md` and other relevant files be updated to always
do an AAR. Codex searched the repo guidance and updated the repeated
session-end policy surfaces from conditional AAR creation to mandatory AAR
creation.

## Process issues

### Conditional AAR policy caused missed closeout behavior

The previous policy required an AAR only when durable process lessons were
observed. That left room for the agent to skip the explicit AAR assessment or
forget the step entirely during closeout.

Improvement:

Require an AAR for every Project Koios session. Trivial clean sessions should
produce a short AAR stating that no durable process issue was observed.

## Proposed follow-up improvements

- Observe future sessions to confirm the mandatory AAR rule is followed.
- If any harness still skips AAR creation, update that harness's local stop
  protocol or skill guidance.

## Candidate ADR or implementation topics

- No new ADR is required unless the always-AAR policy needs formal lifecycle
  treatment beyond repo instruction updates.
- Candidate skill update if downstream harnesses carry their own copied
  session-end policy.

## Current status

This AAR is a process observation artifact. It does not change architecture
authority, ADR status, or implementation routing by itself.
