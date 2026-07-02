# ADR 20260702.000551: Idea → Spike → ADR → Implementation Workflow

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

The current workflow tends to push exploratory work into ADRs too early. That makes the decision log volatile and mixes brainstorming, uncertainty reduction, and durable architecture decisions.

The repository needs a lower-friction place for raw ideas, a timeboxed place for experiments, and a stable place for decisions. Iterative development should happen after the decision is stable enough to build against.

## Decision

Use a four-surface workflow:

- `docs/incubator/` for raw ideas, brainstorming, and rough notes
- `docs/spikes/` for timeboxed experiments that reduce uncertainty
- `docs/architecture/adr/` for durable decisions
- implementation briefs and tasks for iterative delivery work

ADRs are encapsulated decision records and must remain independently readable.
Hierarchy, readiness level, and promotion ordering are represented by `architecture.00`, not by nested ADR body structure.

The intended lifecycle is:

`idea -> spike -> ADR -> implementation brief -> iterative implementation`

## Consequences

- Brainstorming becomes low-friction and non-authoritative
- Spikes absorb uncertainty without churning ADRs
- ADRs become calmer, more durable decision records
- Iterative implementation can proceed without repeatedly reopening architecture decisions

## architecture-spec

This ADR introduces a process boundary, not a new runtime system.

The boundary is:

- ideas are exploratory
- spikes are investigatory
- ADRs are authoritative decisions
- implementation briefs translate decisions into build work

## acceptance-criteria

- Raw ideas can be captured without creating an ADR
- A spike can be created for a single question or uncertainty
- ADRs are only used for durable decisions
- Implementation work can proceed from an ADR-derived brief
- The workflow is understandable without additional hidden rules

## implementation-brief

If accepted, add lightweight repo guidance for:

- where incubator notes live
- what makes something a spike
- when a spike should become an ADR
- when a decision should become an implementation brief

## resolved-open-questions

- Should `docs/incubator/` and `docs/spikes/` be formal directories, or just conventions?
- Should spikes have an expiry date by default?
- Should every spike be required to name a promotion target?

## non-goals

- Replacing ADRs as the durable decision surface
- Forcing every idea into a formal process
- Making spikes as heavyweight as ADRs
- Defining the full implementation planning system

## validation-expectations

- Review the workflow for clarity and low friction
- Confirm the proposal reduces ADR volatility rather than adding more ceremony
- Confirm it still supports iterative development after decisions stabilize

## routing

- Owner: Hermes
- Next phase: proposed
- Notes: Process/workflow control surface; later ADR, policy note, or implementation guidance if stabilized.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- KOIOS: The lifecycle boundary is sensible, but it overlaps with other workflow notes; reconcile the naming before treating it as settled.
- KOIOS: Decide whether `docs/spikes/` is a real directory or only a convention so the layout matches the policy.
- VULCAN: The implementation-brief step needs a `verification_method` field so Vulcan knows how to validate against the architecture intent. Without it, "implementation brief → iterative implementation" has no defined done signal.
