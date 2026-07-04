# ADR 20260702.020440Z: Canonical Workspace State and Next-Action Protocol

## Status

draft-superseded-by-accepted-adr

## Context

Origin: user request
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The current workspace state is spread across prose notes, handoff artifacts,
and ad hoc session inference. That makes it hard to determine the highest-
leverage next task quickly and consistently.

The repository needs one canonical live state surface for each workspace so an
agent can answer, in order:

1. what is blocked
2. what decision is closest to completion
3. what action unlocks the most downstream work

## Decision

Each role workspace MUST maintain a canonical live state surface.

The canonical live state surface MUST consist of exactly two files at the
workspace root:

   - `state.md`
   - `active.md`

The two files MUST be treated as one bounded control surface. Agents MUST NOT
infer current workflow authority from scattered workspace notes, directory
placement, chat history, or transport mechanics when `state.md` and `active.md`
are present.

`state.md` MUST be the durable resume snapshot for the workspace. It MUST record,
at minimum:

   - represented role
   - repository or scope
   - current focus
   - blockers
   - validated current state or last validated document-state change
   - handoff status when relevant
   - next owner
   - open questions or open decisions
   - current status summary

`active.md` MUST be the current priority and next-action surface. It MUST record,
at minimum:

   - current priority stack
   - next action or next state transition
   - waiting-on list
   - explicitly active working material
   - ignored scope
   - exit criteria

Both `state.md` and `active.md` MUST include a stable top JSON metadata section.

Workspace-local notes MAY exist in `decisions/`, `working/`, `scratch/`, and
`sessions/`. Such notes MUST NOT become authoritative merely because of their
location. Working material MUST be treated as active only when named by
`active.md`.

Agents starting a session in a role workspace MUST read `state.md` first and
`active.md` second. Agents SHOULD inspect only the handoff, working, or decision
artifacts named by those files before selecting the next action.

The next action SHOULD be selected using this priority order:

   1. prefer actions that unblock multiple downstream tasks
   2. prefer actions that close the nearest decision boundary
   3. prefer actions that reduce ambiguity or rework
   4. prefer actions that restore workflow health before starting new work

The state pair MUST NOT replace ADRs, implementation reports, validation results,
knowledge notes, or other repository document-state artifacts.

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
handoff_status: no pending handoff
next_action_owner: HERMES
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

- read `state.md` first
- read `active.md` second
- check only relevant handoff or working artifacts named by those files third
- verify the active decision surface fourth
- then choose the highest-leverage unblocked action

## acceptance-criteria

- a workspace can name its current role, blockers, next owner, and next action from `state.md` + `active.md`
- `state.md` and `active.md` have stable top JSON metadata sections
- the next owner is explicit when the current actor cannot complete the step
- the highest-leverage action is derivable from the state pair without inference
- the state pair is small enough to maintain regularly
- the protocol works for both quiet sessions and active review sessions

## implementation-brief

If accepted, update workspace guidance so each workspace keeps the canonical
`state.md` + `active.md` pair with explicit next-owner, next-action, ignored-scope,
and leverage-priority fields.

## resolved_open_questions

- Resolved on 20260704.151957: the canonical live state surface is the pair `state.md` + `active.md`, not a single file and not scattered workspace notes.
- Resolved on 20260704.151957: Markdown files with stable top JSON metadata sections are sufficient; no separate machine-readable companion is required unless future automation proves the need.
- Should every workspace have the same field set, or may roles add optional fields?
- Should the leverage ranking be manual or computed from the open queue?

## non_goals

- Replacing ADRs or architectural decisions
- Defining transport mechanics for role coordination
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
- Next phase: accepted ADR exists at `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`
- Notes: Workflow/state surface for leverage-based session planning. Historical draft retained as context; do not use as the active authority surface.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md`
- proposal_surface: `dev/canonical-workspace-state-next-action-protocol/adr.canonical-workspace-state-next-action-protocol.proposed.md`

## Comments

- KOIOS: Strong leverage rule, but the canonical state format should be nailed down sooner so every workspace speaks the same language.
- KOIOS: Consider a smaller minimal field set; too many fields will turn the state surface into a maintenance burden.
- HERMES: This should be a single live surface, not a summary of several surfaces; otherwise the next-action protocol will still depend on scattered context.
- HERMES: Prefer one canonical workspace-state file (for example `state.md`) with any machine-readable form treated as a render or companion, so the next-action surface does not split across multiple authorities.
- HERMES: If `state.md` exists but workspace guidance does not explicitly reference it, agents may not treat it as canonical yet.
- ATHENA: Review decision on 20260704.151957 selects Option B: the canonical live state surface is the controlled pair `state.md` + `active.md`. This preserves Hermes's single-surface concern by treating the pair as one bounded control surface, not as scattered workspace context.