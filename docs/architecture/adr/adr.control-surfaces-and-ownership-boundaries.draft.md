# ADR 20260701.181956Z: Control Surfaces and Ownership Boundaries

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

The bootstrap repo now has multiple live surfaces for control, state, and
handoff, but the ownership and authority boundary between them is still spread
across separate notes.

That makes it harder to answer three questions quickly:

1. which surface is authoritative for a given kind of change
2. who owns the next move on that surface
3. when a local note should be promoted into a durable ADR

## Decision

Define the repo's control surfaces as a small, explicit matrix with distinct
owners, purposes, and authority levels.

Use the following surface set:

- **architecture surface** — ADRs and architecture indexes; owns durable
  decision authority
- **workspace state surface** — `state.md` and `active.md`; owns live session
  status, blockers, and next action
- **message delivery surface** — `inbox/` and `outbox/`; owns cross-role
  communication and routing notes
- **handoff surface** — `handoffs/`; owns durable transfer artifacts between
  sessions or roles
- **session surface** — `sessions/`; owns run-local history and execution
  traces
- **decision scratch surface** — `decisions/`; may hold temporary decision
  shaping material, but does not override ADR authority
- **process lesson surface** — `docs/AAR/`; records retrospective process
  observations only

Apply these rules:

- higher-authority surfaces override lower-authority ones when they conflict
- surfaces should stay narrow; do not store one kind of artifact on the wrong
  surface
- if a surface starts carrying recurring authority decisions, promote that
  pattern into an ADR
- if a lower surface conflicts with a higher one, fix the lower surface or
  raise a new ADR rather than normalizing the mismatch
- keep control notes concise, inspectable, and role-attributed

## Consequences

- control and ownership become easier to reason about from file location alone
- state, delivery, and decision artifacts stop competing for the same role
- recurring process patterns can be promoted instead of re-explained
- lower-surface notes stay useful without becoming accidental authority

## architecture-spec

The control-surface matrix is:

| Surface | Primary purpose | Authority level | Owner |
|---|---|---|---|
| architecture ADRs | durable decisions | highest | Athena |
| workspace state | live session control | high | Athena |
| inbox/outbox | message transfer | medium | Hermes |
| handoffs | durable transfers | medium | sending role |
| sessions | run history | low | current session owner |
| decisions/ | working notes | low | current author |
| docs/AAR/ | process lessons | lowest | session author |

The matrix should be used as a routing guide, not as a universal storage rule.
Each surface must remain small enough to scan quickly.

## acceptance-criteria

- a reviewer can tell which surface owns a given artifact by path alone
- authority conflicts resolve toward the higher surface
- recurring control rules are promoted to ADRs instead of duplicating across notes
- the workspace state surface stays separate from message delivery and
  handoff records
- process lessons remain non-authoritative

## implementation-brief

If accepted, update the workspace guidance and related architecture notes so the
surface matrix is the default reference for routing, ownership, and promotion.

## resolved_open_questions

- Should `decisions/` remain a temporary scratch surface or become a formal
  decision-log surface?
- Should the authority ordering be stated once here or repeated in each
  workspace guide?
- Should session notes inherit the owner of the current workspace role or the
  current run?

## non_goals

- Replacing the existing lifecycle workflow
- Defining implementation code
- Creating a universal database model for repo metadata
- Rewriting archived handoff or AAR history

## validation-expectations

- the repository's main control surfaces can be named without ambiguity
- a new artifact can be routed by surface type without reading the whole repo
- authority-limited notes do not masquerade as decisions
- the matrix helps decide when to promote a repeated pattern into an ADR

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Repository control-surface taxonomy and ownership boundaries.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
