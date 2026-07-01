# ADR 20260630.121054: Session-end working tree gate

## Status

historic

## Context

Ending a session with uncommitted changes in the working tree is normal
and sometimes intended. But in this repo's current operation, 10 modified
files and 3 untracked files accumulated across multiple sessions without
validation being run or the tree being cleaned up. This drift creates
ambiguity for the next operator: are the changes intentional, work in
progress, or orphaned?

The meta-harness session protocol has no rule about working tree
discipline at session end.

## Decision

See the original ADR text below for the historical decision.

## Consequences

- Next session starts from a known state: clean tree or a named stash.
- Accumulated drift is caught early rather than compounding.
- The requirement is lightweight (1-2 commands) and doesn't interrupt
  flow.
- Stale WIP stashes may themselves accumulate; periodic stash review
  should be part of maintenance sessions.

## architecture-spec

Add a session-end gate to the Hermes session protocol:

- **If the session produced commits:** the working tree SHOULD be clean
  of both tracked and untracked modifications. Uncommitted changes MUST
  have a justification recorded in the session summary.
- **If the session did not produce commits and the tree is dirty:** the
  operator MUST either (a) commit, (b) stash, or (c) explicitly document
  why the changes are being left. A `git stash push -m "WIP: <reason>"`
  with a descriptive message is the preferred mechanism.

The gate is enforced by convention and reviewed at the next session
start — no tooling enforcement at this stage.

## acceptance-criteria

Not separately stated in the original archive ADR.

## implementation-brief

Not separately stated in the original archive ADR.

## resolved-open-questions

None stated.

## non-goals

None stated.

## validation-expectations

Not separately stated in the original archive ADR.

## routing

- Owner: Athena
- Next phase: completed
- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260630.121054: Session-end working tree gate

## Status

historic

## Context

Ending a session with uncommitted changes in the working tree is normal
and sometimes intended. But in this repo's current operation, 10 modified
files and 3 untracked files accumulated across multiple sessions without
validation being run or the tree being cleaned up. This drift creates
ambiguity for the next operator: are the changes intentional, work in
progress, or orphaned?

The meta-harness session protocol has no rule about working tree
discipline at session end.

## Proposal

Add a session-end gate to the Hermes session protocol:

- **If the session produced commits:** the working tree SHOULD be clean
  of both tracked and untracked modifications. Uncommitted changes MUST
  have a justification recorded in the session summary.
- **If the session did not produce commits and the tree is dirty:** the
  operator MUST either (a) commit, (b) stash, or (c) explicitly document
  why the changes are being left. A `git stash push -m "WIP: <reason>"`
  with a descriptive message is the preferred mechanism.

The gate is enforced by convention and reviewed at the next session
start — no tooling enforcement at this stage.

## Consequences

- Next session starts from a known state: clean tree or a named stash.
- Accumulated drift is caught early rather than compounding.
- The requirement is lightweight (1-2 commands) and doesn't interrupt
  flow.
- Stale WIP stashes may themselves accumulate; periodic stash review
  should be part of maintenance sessions.
