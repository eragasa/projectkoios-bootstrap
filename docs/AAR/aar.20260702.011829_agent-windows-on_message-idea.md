# AAR 20260702.011829: Agent Windows with on_message Idea

## Scope

Captured an incubator idea for running each agent in its own window with message-triggered behavior.

## What happened

Added `docs/incubator/idea.agent-windows-on_message.md` describing the goal, candidate shapes, risks, open questions, and promotion target.

## Process issues

None observed.

## Proposed follow-up improvements

If this idea stays attractive, split it into a runtime spike that defines routing, queueing, and restart behavior before turning it into an implementation plan.

## Candidate ADR or implementation topics

- Per-agent window runtime model
- `on_message` event semantics
- Hermes routing behavior for active agents

## Current status

Idea captured; no spike created yet.
