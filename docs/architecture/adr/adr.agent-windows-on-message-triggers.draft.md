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
Architecture-Domain: software

#### Current Situation
- User user currently interacts through a separate terminal for each agent.
- The user currently switches screens to interact with each agent.
- Events are currently triggers by session start  
    1. checking the repository against `master`
    2. checking 'master' against 'orgin/master`
    3. validation: clean repository tree
    4. event triggers are driven ADR.status
- `end session` typically follows the following sequence
    1.  write an `AAR`
    2.  commit all files.
    3.  identify open issues (although i'm not sure how it learned this behavior, it is probably default AGENTS.md pi behavior)
    4.  
- Each agent requires it's own `workspace` defined as folder on a file system.

##### Shortcomings
- The user doesn't have a control plane for each agent.
- Muli-agent work is hard to monitor
- The repository has grown beyond the capacity of graphify.
- No orchestration layer exists yet
- interactivity is by prompt only, no alternate ways to prompt

##### Opportunities
- All agents have been migrated to the pi skill harness, but have some level of portability due to Anthropic SKILL system
- Agents appear to be useful in roles. 
- The intercom system seems to be available but can be accidentally triggered.

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

The architecture must preserve independent agent ownership.

Agent independence means:
- each agent has its own workspace/window/state
- one agent should not silently act as another
- an agent is an operator and acts on a state
- \hat{O}_1 \hat{O_2} means that \hat{O}_1 and \hat{O}_2 should only have a small perturbation due to context window length
- \hat{O}_1 \hat{O}_2  s_0 means \hat{O}_1 acts on the state produced by \hat{O}_1, it is not \hat{O}_1 acting through \hat{O}_2

## acceptance-criteria

- an agent can receive a routed message without relying on hidden prompt chaining
- the message ownership boundary is explicit
- crash/restart behavior is defined at the architecture level
- the window model should make human interaction compatible with modern human-machine interfacing.

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
