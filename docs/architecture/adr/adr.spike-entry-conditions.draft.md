# ADR 20260702.121432Z: Encapsulated Spike Entry Conditions

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

The workflow needs an explicit gate for when a topic is ready to become a spike instead of remaining an idea. Without that gate, fuzzy exploration can get promoted too early and spikes lose their purpose as bounded investigations.

The incubator note surface already captures raw brainstorming. This ADR defines the minimum conditions for promoting that material into a spike.

This ADR is intentionally encapsulated and independently readable; hierarchy is supplied by `architecture.00`.

## Decision

A spike may start only when it has all of the following:

- one bounded question
- an expected decision or implementation impact
- a three-day inactivity review threshold
- a clear exit condition
- an owning ADR

If any of those are missing, the work remains in idea mode.

## Consequences

- spikes stay bounded and useful
- fuzzy exploration remains in the incubator surface
- promotion to spike becomes easier to review consistently
- downstream ADRs and implementation briefs get cleaner input

## architecture-spec

This ADR defines the entry gate for the spike surface.

The spike gate requires:
- one question
- one purpose
- a three-day inactivity review threshold
- one exit condition
- one owning ADR

The threshold is not automatic expiry. If neither the owning ADR nor the spike's downstream work has moved forward for three days, the spike must be brought to human review for archive, continuation, or conversion.

A spike attaches to an ADR. Its findings may later inform an implementation brief attached to that same ADR.

Stated negatively:
- no multiple unrelated questions
- no open-ended exploration
- no spike without an observable end state

## acceptance-criteria

- a reviewer can tell whether a topic is spike-ready
- a fuzzy topic stays in incubator mode
- a spike has a clear downstream destination
- the rule is simple enough to apply during review

## implementation-brief

If accepted, update the workflow guidance and incubator template so spike promotion explicitly checks the minimum conditions before creating a spike note. Also refine the implementation-brief language iteratively against the ADR surface.

verification_method: review a sample idea note and confirm it either stays in incubator mode or satisfies all five spike conditions before promotion.

## resolved_open_questions

- Should the timebox be a fixed default or topic-specific?
- Should the promotion target be an ADR, implementation brief, or either?
- Should the gate be hard or best-effort?
- Should the implementation brief be a forward build guide, a backward feedback transition, or both?

## non_goals

- redefining the full idea/spike/ADR workflow
- creating spike expiry automation
- turning spikes into full ADRs

## validation_expectations

- the gate distinguishes ideas from spikes
- the promotion target is explicit before work starts
- the rule reduces fuzzy or premature spikes

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Workflow gate for spike readiness.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
