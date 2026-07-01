---
name: control-plane-comment-loop
description: |
  Use when the owner of a draft ADR needs to sit with the user, work through comment threads as a control-plane problem, and decide how the review matrix should behave.
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.controlling-adr-join-protocol.draft.md, adr.draft-adr-comment-processing-protocol.draft.md.
  Triggers: "control plane problem", "draft ADR comments", "review these comments with me", "walk the control planes", "pick a course of action".
  Capability: Classifies comments by control plane, exposes the reasoning to the user, presents exactly three candidate courses of action plus one recommendation in randomized order, records the user’s choice, and captures whether the matrix produced the result the user wanted.
  NOT for: implementation, silent ADR rewriting, or one-shot questionnaires.
metadata:
  binds_to:
    - docs/architecture/adr/adr.controlling-adr-join-protocol.draft.md
    - docs/architecture/adr/adr.draft-adr-comment-processing-protocol.draft.md
    - docs/architecture/adr/adr.skill-register-and-adr-binding-policy.draft.md
---
# Control Plane Comment Loop

## Purpose

Use this skill when a draft ADR owner needs to process comments with the user in
an explicit decision loop instead of silently “handling” review feedback.

The goal is to make the control plane visible:
- what the comment is really about
- which surface owns it
- what the matrix predicts should happen
- which of three actions the user wants
- whether that choice improves the matrix

## Operating model

This is a guided review loop, not a final decision dump.

For each comment cluster:
1. identify the control plane involved
2. explain the reasoning in plain language
3. generate exactly three plausible courses of action
4. mark one as the recommended course
5. randomize the display order of the three courses
6. ask the user to choose one
7. record the choice and the reason it was selected
8. record whether the choice produced the result the user wanted
9. revise the matrix if the result shows a mismatch

## Control planes

Classify each issue against the smallest useful set of planes:
- ownership: who may act
- surface: where the comment belongs
- lifecycle: draft / proposed / accepted / archived
- escalation: when to route to another role
- promotion: when a comment changes the ADR itself
- determinism: whether the current matrix predicts the right action

## Candidate courses of action

For each cluster, create three distinct options. They should usually map to
three different moves, such as:
- revise in place
- split or promote to a controlling ADR
- route, defer, or escalate

Do not always present them in the same order.
The recommendation may appear in any position, but it must be clearly marked.

Each option must include:
- short label
- what it does
- what it defers
- main risk
- why it might be chosen

## User-facing reasoning

Always show the user the reasoning behind the recommendation.
Do not hide the control-plane diagnosis behind a conclusion.

For each cluster, answer with:
1. current understanding
2. the control plane(s) implicated
3. the three courses of action in randomized order
4. the recommended course and why it is recommended
5. the concrete choice the user needs to make
6. what will change if the user picks each option

## Recording rule

Write the review into the active draft ADR interview note, typically under:

`docs/architecture/interviews/architecture-interview-<slug>.md`

Record:
- the comment cluster
- the control-plane diagnosis
- the three options and the recommendation
- the user’s selection
- the matrix-fit verdict: `fit`, `partial fit`, or `mismatch`
- the follow-up action required by the selection

## Determinism rule

The long-term goal is to make the matrix deterministic.
That means repeated comment patterns should eventually map to the same default
response.

If the user’s selected option differs from the recommendation, capture:
- why the recommendation missed
- what cue was missing
- whether the matrix needs a new bucket, a new escalation rule, or a new promotion rule

## Failure modes

- The issue is too broad for one cluster — split it before presenting options
- The control plane is unclear — name the ambiguity and ask for a narrower scope
- The three courses of action are not meaningfully different — reframe the cluster
- The user rejects all three options — record the failure and revise the matrix

## Deliverable shape

End with a compact decision summary:
- cluster name
- control plane diagnosis
- three courses of action
- recommendation
- user selection
- matrix-fit verdict
- next action
