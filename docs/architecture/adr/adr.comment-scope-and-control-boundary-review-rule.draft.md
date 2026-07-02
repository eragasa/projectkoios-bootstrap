# ADR 20260702.020818: Comment Scope and Control-Boundary Review Rule

## Status

draft

## Context

Origin: user request
From: ATHENA
Acting-As: ATHENA
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The repository needs a simple rule for when Athena should add comments during
architecture review. The default should favor useful participation on draft
ADRs and on ideas that fall within Athena's decision/control boundary, while
avoiding redundant, off-scope, or authority-limited commentary.

## Decision

Use the following comment rule:

- comment on every draft ADR when Athena has a substantive addition, objection,
  clarification, or risk flag
- comment on ideas that are inside Athena's role of control or are clearly
  worth shaping further
- avoid comments that are redundant, off-scope, purely speculative, or blocked
  by another role's authority
- keep comments concise and decision-oriented

A comment is substantive when it changes understanding, reduces ambiguity,
identifies risk, or improves the next decision boundary.

## Consequences

- draft ADRs get review attention instead of passive reading
- Athena participates where it can materially improve the decision surface
- comment noise stays bounded by the substantive-input rule
- role boundaries remain clear because authority-limited items are skipped

## architecture-spec

The comment rule applies to:

- draft ADRs
- ideas inside Athena's decision or control boundary
- ideas Athena is motivated to talk about because they would materially improve
  the decision surface

The rule does not require comments on every topic, only on topics where Athena
can add real value.

## acceptance-criteria

- draft ADRs receive comments when Athena has substantive input
- control-boundary ideas receive comments when they need shaping or risk flags
- redundant or authority-limited items are skipped
- reviewers can infer why a comment was added or omitted

## implementation-brief

If accepted, update the relevant comment workflow guidance so Athena's default
behavior is to comment on draft ADRs and on within-boundary ideas that warrant
substantive review.

## resolved_open_questions

- Should the substantive-input rule be written into a reusable review checklist?
- Should comment timestamps or tags distinguish boundary-shaping comments from
  general notes?
- Should other roles adopt the same default comment posture?

## non_goals

- Forcing comments on every item regardless of value
- Expanding Athena beyond its control boundary
- Changing ADR promotion rules
- Replacing the draft/proposed/accepted workflow

## validation-expectations

- A reviewer can tell whether a comment was worth adding by the rule alone
- Draft ADRs are not silently skipped when Athena has something useful to add
- Comments remain bounded to areas where Athena can actually help

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Default comment posture for draft ADRs and decision-boundary ideas.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- KOIOS: Useful default, but “substantive” needs a short checklist or examples to keep it from becoming subjective.
- KOIOS: The rule should stay tied to decision value and control boundary, not general commentary volume.
- VULCAN: Add "implementation impact" to the substantive signal set. A comment that flags build cost, rework risk, or implementability concerns is valuable — VULCAN can assess those only when architecture comments call them out explicitly.
