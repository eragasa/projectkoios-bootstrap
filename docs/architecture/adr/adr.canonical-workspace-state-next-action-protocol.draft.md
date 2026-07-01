# ADR 20260702.020440Z: Canonical Workspace State and Next-Action Protocol

## Status

draft

## Context

Origin: user request
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

The current workspace state is spread across prose notes, inbox/outbox files,
and ad hoc session inference. That makes it hard to determine the highest-
leverage next task quickly and consistently.

The repository needs one canonical live state surface for each workspace so an
agent can answer, in order:

1. what is blocked
2. what decision is closest to completion
3. what action unlocks the most downstream work

## Decision

Define a canonical workspace state record and next-action protocol for each
workspace.

The live workspace state should be treated as the primary session control
surface. It should be short, explicit, and machine-readable enough that the
highest-leverage next action can be inferred without scanning the whole repo.

The canonical workspace state should include at minimum:

- current role
- current repository or scope
- current focus
- blockers
- last validated decision
- inbox status
- outbox status
- open decisions
- next action
- next owner
- leverage ranking or priority note
- current status summary

The next-action protocol should use a simple leverage rule:

1. prefer actions that unblock multiple downstream tasks
2. prefer actions that close the nearest decision boundary
3. prefer actions that reduce ambiguity or rework
4. prefer actions that restore workflow health over starting new work

## Consequences

- the highest-leverage task becomes easier to identify at session start
- live workspace state no longer depends on guesswork from scattered notes
- role ownership and next action are visible without rereading history
- process health can be monitored with a small, repeatable state surface

## architecture-spec

The canonical live workspace state may be rendered in Markdown, YAML, or JSON,
but it must be structurally consistent across workspaces.

Suggested shape:

```yaml
role: ATHENA
repository: projectkoios-bootstrap
current_focus: "..."
blockers:
  - "..."
last_validated_decision: "..."
inbox_status: empty
outbox_status: pending_delivery
open_decisions:
  - "..."
next_action:
  summary: "..."
  owner: HERMES
  rationale: "..."
leverage_rank:
  - "..."
status_summary: "..."
```

The protocol should also define a startup check order:

- read the canonical workspace state first
- check inbox/outbox items second
- verify the active decision surface third
- then choose the highest-leverage unblocked action

## acceptance-criteria

- a workspace can name its current role, blockers, and next action in one read
- the next owner is explicit when the current actor cannot complete the step
- the highest-leverage action is derivable from the state without inference
- the state surface is small enough to maintain regularly
- the protocol works for both quiet sessions and active review sessions

## implementation-brief

If accepted, update the workspace state files and related guidance so each
workspace keeps a canonical live state record with an explicit next-action
field and leverage rule.

## resolved_open_questions

- Should the canonical state be Markdown-only, or should YAML/JSON be the
  authoritative form with Markdown as a render?
- Should every workspace have the same field set, or may roles add optional
  fields?
- Should the leverage ranking be manual or computed from the open queue?

## non_goals

- Replacing ADRs or architectural decisions
- Replacing inbox/outbox delivery
- Defining implementation work beyond the state protocol itself
- Forcing every note into a rigid database model

## validation-expectations

- At session start, the agent can identify the highest-leverage next action in
  one pass
- The workspace state answers who owns the next step
- The protocol reduces repeated scanning of unrelated docs
- The same structure can be used across Athena, Hermes, Vulcan, and Koios

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Workflow/state surface for leverage-based session planning.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
