# ADR 20260702.121432Z: Agent Windows with `on_message` Triggers

## Status

draft
date: 20260702.121432Z

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

The current agent interaction model is chat-centric and does not give each agent a durable visible runtime surface. Multi-agent work becomes harder to watch, harder to route, and easier to confuse when multiple roles share the same conversational channel.

A window-per-agent model with routed `on_message` handling could make each agent easier to observe and control while preserving role boundaries. A live document pane alongside chat may also be part of the same runtime surface so work can be edited in place during a process.

## Decision

Adopt an agent-window model where each agent may have its own visible runtime surface and receive routed messages through an `on_message` trigger.

The `on_message` trigger must be treated as a control boundary, not a hidden prompt chain. It may act as a callback, queue consumer, or UI event only if the routing semantics are explicit.

The architecture must define:
- how messages are routed to the agent window
- what state the window owns
- whether the handler is synchronous or asynchronous
- how recovery works if a window closes, pauses, or crashes

## Consequences

- multi-agent work can remain visible instead of dissolving into hidden prompt chains
- routing becomes a first-class architecture concern
- runtime recovery and ownership must be defined before implementation
- a shared message bus may still be needed, but it must be explicit

## architecture-spec

This ADR defines a runtime/control surface.

The core model is:
- one agent = one visible window or equivalent runtime surface
- messages enter the window through an explicit `on_message` route
- the agent reacts locally within its own boundary

The architecture must preserve independent agent ownership while allowing Hermes or another router to deliver targeted messages.

## acceptance-criteria

- an agent can receive a routed message without relying on hidden prompt chaining
- the message ownership boundary is explicit
- crash/restart behavior is defined at the architecture level
- the window model remains compatible with Hermes routing and review workflows

## implementation-brief

If accepted, define the runtime routing contract and determine whether the visible surface is implemented in pi, tmux, another terminal UI, or a separate shell process.

verification_method: review the routing contract, then confirm a prototype can receive and act on a targeted message without cross-talk.

## resolved_open_questions

- Should `on_message` be synchronous or asynchronous?
- Should the agent window own local state or share a backing store?
- Should Hermes route directly into the window or through a central router?
- Should window closure trigger archival, pause, or restart semantics?

## non_goals

- defining the full agent UI implementation
- replacing the existing chat harness with a different provider
- solving all multi-agent collaboration problems at once

## validation_expectations

- a reviewer can describe the routing flow without guessing
- the window boundary is explicit enough to support recovery
- the decision can be implemented incrementally

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Runtime/control-surface decision candidate.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
