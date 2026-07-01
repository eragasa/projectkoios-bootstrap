# ADR 20260702.004118: ADR Title Naming Convention

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

Some ADR titles are too vague, too process-y, or too tied to the drafting phase.
When a draft ADR is promoted, its title should become a canonical decision label
that fits the architecture index and stays stable over time.

## Decision

Use decision-oriented titles for ADRs that are intended to become active or
accepted.

Rules:

- title the decision, not the drafting process
- keep draft titles provisional when needed
- align promoted titles with the `architecture.00` naming surface
- prefer concise noun phrases over sentences
- use version suffixes only when the decision surface truly needs them

## Consequences

- draft ADRs can stay rough while work is still exploratory
- promoted ADRs get cleaner, more durable references
- the architecture index becomes easier to scan
- title churn should drop once a decision is stabilized

## architecture-spec

This ADR defines the naming surface for ADR titles, not the ADR schema.

The intended title shape for promoted ADRs is:

`<decision noun phrase> [vN]`

Examples:

- `ADR Title Naming Convention`
- `Idea to Spike Workflow`
- `Review Status Model`

## acceptance-criteria

- Draft ADR titles may remain provisional
- Promoted ADR titles read like decisions, not notes
- `architecture.00` can serve as the canonical title alignment surface
- Version suffixes are optional, not mandatory

## implementation-brief

If accepted, update the architecture guidance so promoted ADRs use the
canonical title rule and draft titles are treated as temporary working labels.

## resolved-open-questions

- Should every promoted ADR use a version suffix?
- Should `architecture.00` document canonical title examples?
- Should draft titles be mechanically rewritten on promotion?

## non-goals

- Renaming historical archived ADRs
- Forcing all draft notes to use strict canonical titles immediately
- Changing the ADR schema itself

## validation-expectations

- A reviewer can tell whether a title is draft-only or promotion-ready
- The rule is simple enough to apply consistently
- The architecture index can remain readable as ADR count grows

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Process/naming guidance for the ADR surface.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- KOIOS: Good cleanup rule; the examples should be tightened so promoted titles map cleanly to the index.
- KOIOS: Optional version suffixes are fine only if there is a real semantic reason for multiple decision surfaces.
- ATHENA: Title examples should include at least one borderline case where the decision name differs from the drafting activity, so reviewers know what gets normalized on promotion.
