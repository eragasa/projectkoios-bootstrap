# Idea: Agent Windows with `on_message` Triggers

## Brainstorm

We may want each agent to run in its own window so the agents can act independently while still receiving routed messages. A message arriving in a window would fire an `on_message` event and let that agent decide whether to reply, update state, or start local work.

## Goal

Make multi-agent work easier to watch, easier to route, and less prone to prompt cross-talk.

## Current thinking

Each agent gets its own visible runtime surface. Hermes or another router can send a message into a specific agent window, and the agent reacts to the message through an event handler instead of only through one-off prompts.

## Ideas considered

- one terminal window per agent
- event-driven `on_message` handler
- message queue per agent
- shared router that posts into windows

## Objections / risks

- message ordering may matter
- restart and recovery could get messy
- windows may drift apart without shared state rules
- it is unclear whether `on_message` should be sync or async

## Open questions

- Should each agent window be isolated or share a common backing store?
- Should `on_message` be a UI event, a runtime callback, or a queue consumer?
- How should Hermes route messages when several agents are active at once?
- What happens when a window is closed, paused, or crashes?

## Preferred direction

A window-per-agent model with explicit message routing and an event-triggered local handler seems promising, especially if it keeps the role boundaries visible.

## Anything to keep out

- hidden prompt chaining
- one giant shared chat surface
- unclear ownership of incoming messages
- architecture decisions without a routing model

## Promotion target

This could become a spike if we want to prototype the runtime model, or an ADR if the routing and event semantics are already clear enough.
