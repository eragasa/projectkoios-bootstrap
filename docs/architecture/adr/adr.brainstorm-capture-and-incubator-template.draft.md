# ADR 20260702.005615: Brainstorm Capture and Incubator Note Template

## Status

draft

## Context

Origin: user request
From: Hermes
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

The repository needs a lightweight way to capture freeform brainstorming before
it becomes a spike or ADR. Users may brainstorm in a temporary chat session,
external chat tool, or a temporary agent, but the result should be summarized
into a durable repo note instead of preserved as an unstructured transcript.

## Decision

Use `docs/incubator/` as the entry surface for brainstorming summaries.

The incubator note template should capture:

- topic
- goal
- current thinking
- spike requirements
- ideas considered
- objections or risks
- open questions
- comments and replies
- preferred direction
- anything to keep out
- resolved questions
- resolved comments

Workflow rules:

- brainstorming may happen anywhere
- raw chat transcripts are not authoritative artifacts
- the durable output is a concise incubator note
- a spike is only created once minimum spike conditions are met
- the incubator note should be promoted to a spike or ADR summary when ready

## Consequences

- users can think aloud without immediately creating architectural weight
- temporary chat sessions become reusable repo input
- the repo gains a consistent handoff from freeform discussion to structured
  decision work
- spike creation stays gated by readiness rather than enthusiasm

## architecture-spec

The incubator note template is append-friendly and top-heavy: the newest idea stays at the top, while answered questions and responded-to comments move to the bottom.

```md
# Idea: <topic>

## Brainstorm

<what we are trying to figure out>

## Goal

<what outcome we want>

## Current thinking

<summary of the best current model>

## Spike requirements

- <required question 1>
- <required question 2>
- <required question 3>

## Ideas considered

- <option 1>
- <option 2>

## Objections / risks

- <risk 1>
- <risk 2>

## Open questions

- <question 1>
- <question 2>

## Comments

### ATHENA

| Idea | Action |
|---|---|
| <idea or comment> | <reply, change request, or keep> |

### VULCAN

| Idea | Action |
|---|---|
| <idea or comment> | <reply, change request, or keep> |

### KOIOS

| Idea | Action |
|---|---|
| <idea or comment> | <reply, change request, or keep> |

### HERMES

| Idea | Action |
|---|---|
| <idea or comment> | <reply, change request, or keep> |

## Preferred direction

<best current direction>

## Anything to keep out

<non-goals or exclusions>

## Resolved questions

- <answered question 1>
- <answered question 2>

## Resolved comments

- [ATHENA] <comment> → <response or change made>
- [VULCAN] <comment> → <response or change made>
- [KOIOS] <comment> → <response or change made>
- [HERMES] <comment> → <response or change made>

## Promotion target

<if this should become a spike or ADR, name the target>
```

## acceptance-criteria

- A brainstorm can be summarized into a durable incubator note
- The template makes it clear what to capture from a temporary chat
- The template distinguishes brainstorming from spike readiness
- The workflow says when to stay in incubator mode
- The workflow says when to promote into a spike

## implementation-brief

If accepted, add a reusable template file under `docs/templates/`
that presents the capture format and promotion rule.

## resolved_open_questions

- Should the template live in `docs/templates/` as a reusable file or also be mirrored in `docs/incubator/`?
- Should external-chat summaries require source attribution?
- Should the incubator note include a “promotion target” field?
- Should the template name be standardized with the other template files?
- Should responded-to comments be tracked in a dedicated bottom section?

## non_goals

- Turning brainstorming into a formal decision surface
- Replacing spikes or ADRs
- Banning freeform chat tools

## validation-expectations

- A user can chat freely and then condense the result into the template
- The template is short enough to use repeatedly
- The boundary between incubator, spike, and ADR remains obvious

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Process/documentation surface for brainstorming capture.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
