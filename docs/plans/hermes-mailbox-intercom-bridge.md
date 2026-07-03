# Implementation Plan: Hermes mailbox/intercom bridge

## Source

- `workspaces/hermes/AGENT.md`
- `docs/workspaces.md`
- `docs/session-protocol.md`
- `docs/AAR/aar.20260701.142445_workspace-mail-system.md`
- `docs/AAR/aar.20260701.154234_sandbox-message-delivery-terminology.md`

## Scope

Implement the smallest durable bridge between live coordination and workspace mail:

- intercom becomes a notifier, not the record of truth
- mailbox files remain the durable handoff surface
- Hermes can write a message envelope into a workspace inbox
- agents can read inbox messages without relying on chat history
- outbox remains the reply surface

## Repository target

- `workspaces/<agent>/inbox/`
- `workspaces/<agent>/outbox/`
- Hermes session helpers under `scripts/` if a tiny delivery helper is needed

## File-level tasks

### 1) Message envelope

- define a small markdown envelope format for inbox items
- include sender, target, timestamp, subject, body, and provenance
- keep the format append-only and human-readable

### 2) Inbox delivery

- add a minimal helper that writes one envelope into a target workspace inbox
- preserve existing content without rewriting prior messages
- keep delivery deterministic and file-based

### 3) Intercom coupling

- have intercom emit a notification after the mailbox write succeeds
- do not make intercom the source of truth
- do not move approval logic into the notifier

### 4) Inbox read path

- make the inbox the first read surface for target agents
- support a lightweight status listing for unread or newest items
- keep the read path separate from routing decisions

### 5) Hermes routing surface

- keep Hermes as the router that decides which mailbox item is delivered next
- keep routing summaries in Hermes workspace notes
- do not let Hermes treat intercom chatter as approval

## Task breakdown order

1. define the inbox envelope
2. implement write-to-inbox delivery
3. attach the intercom notification hook
4. add the simplest inbox/status read helper
5. validate a single end-to-end message

## Verification method

- write one sample envelope into a test inbox
- confirm the recipient can read it from disk
- confirm the notifier fires only after durable write succeeds
- confirm outbox remains the reply surface

## Escalation note

If the implementation needs a runtime daemon, queue semantics, or cross-session synchronization, split that work into a separate ADR or follow-up plan before expanding the slice.

## Deliverables

- durable markdown inbox envelope
- minimal inbox delivery helper
- intercom notification coupling
- basic inbox status/read behavior

## Notes

- Keep this slice smaller than a full mailbox system.
- The goal is coupling, not replacing the existing workspace mail model.
- Hermes remains the router; intercom remains the signal.
