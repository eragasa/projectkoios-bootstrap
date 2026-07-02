# ADR 20260702.030100: Decision Note Promotion Trigger

## Status

draft

## Context

Origin: implementation gap
From: VULCAN
Acting-As: VULCAN
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The `decisions/` surface in each workspace holds low-authority working notes. The control-surfaces ADR already defines it as temporary and non-authoritative. However, there is no concrete trigger that forces promotion when a decision note starts influencing work across roles.

A note that stays in `decisions/` but gets referenced in an outbox message, a handoff, or an ADR comment is no longer a scratch note — it carries cross-role weight without ADR authority. That causes silent authority drift and later rework.

## Decision

Add one concrete promotion trigger for decision notes:

> If a `decisions/` note is referenced in any outbox message, handoff artifact, or ADR comment, the note must be promoted to a draft ADR within one session.

The promotion is a lightweight action: create a draft ADR from the note content with a `supersedes` link back to the decision note. If the note is genuinely ephemeral, the promoting role should add an `archived` comment to the note instead and close the loop.

Only this single trigger is defined. No automatic expiry. No session-count rule. No scope-growth threshold.

## Consequences

- Cross-role decision notes reach the ADR surface promptly
- Scratch notes that never cross role boundaries can stay ephemeral
- The trigger is simple enough to check at session end
- Enforcement is human-readable, not tooling-dependent

## architecture-spec

The trigger fires when:

1. A write references `decisions/<filename>.md` in an outbox note, handoff artifact, or ADR comment
2. Within one session of that reference, the referenced note either becomes a draft ADR or is explicitly annotated `archived` with rationale

The promotion flow is: copy the decision note body into a new `adr.<topic>.draft.md` with `supersedes` link → remove or archive the decision note.

## acceptance-criteria

- A decision note referenced in an outbox or handoff is promoted or archived within one session
- An ephemeral note that stays within one workspace never triggers promotion
- A reviewer can tell which decision notes have been promoted by the `supersedes` trail

## implementation-brief

If accepted, add the promotion trigger rule to the workspace guidance under the `decisions/` surface description.

## resolved-open-questions

- Should Hermes enforce the trigger at delivery time? That is the natural enforcement point — Hermes sees cross-role references and can gate the delivery.
- Should the one-session window be a strict deadline or a best-effort guideline? Strict for now; relaxing later is easier than tightening.

## non-goals

- Defining automatic expiry for decision notes
- Adding session-count or scope-growth triggers
- Creating promotion tooling or CI enforcement
- Changing the ADR lifecycle or schema

## validation-expectations

- A decision note referenced in an outbox message is promoted within one session
- Notes that never cross role boundaries remain in `decisions/` without pressure
- The single trigger is easy to remember and apply

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Process surface; adds a single concrete promotion trigger to the control-surfaces model.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- VULCAN: YAGNI scope — only the cross-role-reference pattern has caused observable harm. Other accumulation triggers remain speculative until proven necessary.
