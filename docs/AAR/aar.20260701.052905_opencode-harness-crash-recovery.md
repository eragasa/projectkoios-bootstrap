# AAR 20260701.052905: Opencode harness crash recovery

## Scope

Recovery session after the prior session crashed when Codex attempted to call
the opencode harness.

## What happened

The user reported that the previous session crashed because the delegated
operator attempted to call the opencode harness. The recovery session inspected
repo-local operating guidance, Graphify state, git status, ADR status, and
Archon run state without invoking opencode.

Current observed state:

- `graphify-out/graph.json` exists, but Graphify reports it uses the pre-#1504
  node-ID scheme and should be treated as discovery until rebuilt.
- Git working tree has untracked ADR, AAR, and policy artifacts.
- Archon has no active `running` or `paused` runs.
- Recent review-agent interview runs failed or were cancelled.
- Draft ADRs remain for the human-in-the-loop review-agent contract.

## Process issues

- Codex should not call the opencode harness directly in this repo recovery
  path. Opencode/Vulcan is a harness role, not a callable dependency for Codex
  unless the user explicitly routes work there through the meta-harness.
- Recovery should begin with live state inspection rather than resuming a stale
  harness action from chat history.
- The dirty tree should be stabilized before starting new implementation or
  workflow work.

## Proposed follow-up improvements

- Add an explicit Codex recovery note to the local guidance: after a harness
  crash, inspect Graphify, git state, ADR status, and Archon run state before
  invoking any workflow.
- Treat opencode invocation as a routing decision requiring explicit user or
  Hermes direction, not as a default implementation tool.
- Review the untracked human-in-the-loop review-agent ADR and policy artifacts
  before launching another Archon interview loop.

## Candidate ADR or implementation topics

- Clarify delegated-operator boundaries for Codex when a downstream harness is
  unavailable or unstable.
- Define a recovery checklist for failed or cancelled interactive Archon
  interviews.

## Current status

No opencode command was invoked in this recovery session. The highest-leverage
next state is to stabilize the untracked ADR/AAR/policy artifacts and decide
whether the Draft review-agent ADR should be promoted, revised, or superseded.
