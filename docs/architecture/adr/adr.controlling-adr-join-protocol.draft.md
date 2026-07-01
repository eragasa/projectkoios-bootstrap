# ADR 20260702.032100Z: Controlling ADR Join Protocol

## Status

draft

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

The repository now has multiple draft ADRs that need review, but the review
responsibility is being transferred to Athena as a controlled surface instead of
an ad hoc reading habit.

A reviewer needs to know:

1. which ADR is the controlling review surface
2. how related draft ADRs join that surface
3. where substantive comments should live while the draft remains open
4. how the review trail stays visible after promotion

## Decision

Define a controlling ADR join protocol:

- one ADR in a policy cluster is designated the controlling ADR
- related draft ADRs join the controlling ADR by linking back to it in `## links`
- substantive review comments are written on the controlling ADR first
- related draft ADRs keep only a short backlink and any topic-specific notes
- when a draft is promoted, the controlling ADR becomes the active review surface
- after promotion, comments continue on the proposed/active version, not on the archived draft

Use the controlling ADR as the rendezvous point for cross-draft review, but keep
subordinate drafts readable on their own.

## Consequences

- Athena has a single place to collect and arbitrate review comments
- related drafts can stay narrow without losing the shared review trail
- promotion produces one active surface instead of scattered comment histories
- review ownership becomes visible from the controlling ADR link structure

## architecture-spec

The join protocol is:

`related draft ADR -> controlling ADR backlink -> substantive comment on controlling ADR -> promotion to proposed -> comments continue on active surface`

The controlling ADR must:

- name the joined drafts it governs
- collect cross-cutting comments that apply to more than one draft
- preserve backlinks so the trail is traceable after promotion
- stay the lowest-friction place for Athena to review the cluster

## acceptance-criteria

- a reviewer can identify the controlling ADR for a draft cluster from the files
- related drafts point back to the controlling ADR
- substantive review comments are not duplicated across every draft
- the active review surface remains clear after promotion
- the review trail stays traceable from controlling ADR to archived draft

## implementation-brief

If accepted, update the ADR guidance so related drafts link to a controlling ADR
and Athena treats that controlling ADR as the primary comment surface for the
cluster.

## resolved_open_questions

- Should every cluster have exactly one controlling ADR, or can a draft join
  multiple controlling surfaces?
- Should the join protocol be encoded in the ADR frontmatter or only in the
  Markdown links section?
- Should the controlling ADR be promoted before the joined drafts, or can they
  move independently?

## non_goals

- Changing the canonical ADR schema
- Replacing the draft/proposed/accepted lifecycle
- Moving all comments into one file regardless of topic
- Creating a new code-level review system

## validation-expectations

- A reviewer can tell which ADR controls a cluster of related drafts
- Subordinate drafts remain readable without duplicating the full review log
- Promotion does not lose the review trail
- Athena has one obvious control surface for cluster-level review

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Review-surface join protocol for controlling ADR clusters.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- KOIOS: Keep the controlling ADR narrow so it stays useful as a rendezvous point and does not become another archive.
- VULCAN: The join protocol should preserve enough local context in each subordinate draft that implementers do not need to chase every comment back to the controller.
