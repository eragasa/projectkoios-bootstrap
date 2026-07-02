---
status: draft
date: 20260702.180350Z
back_to: architecture.00
---

# Implementation Plan: Adversarial Two-Plane Gate

## Purpose

This is the bootstrap implementation note for the adversarial two-plane gate.

## Scope

It defines the implementation surface for the related ADR and records the execution pattern for the gate.

## implementation-brief

If accepted, update the workflow ADR, the verification-method ADR, and the ownership-ledger ADR so they all reference the adversarial two-plane gate and use consistent completion language.

verification_method: review the workflow ADR and the verification ADR together, then confirm that the brief is the completion point and that neither gate can silently bypass the other.

## Control

This note is controlled by:

- `docs/architecture/adr/adr.adversarial-two-plane-gate.draft.md`

## Related files

- `docs/implementation/implementation.00.md`
- `docs/architecture/adr/adr.adversarial-two-plane-gate.draft.md`

## routing

- Owner: Vulcan
- Next phase: proposed
- Notes: Implementation surface; defines the execution pattern that the ADR points to.

## Comments

- HERMES: Linked from the controlling ADR so the implementation block lives on the implementation surface, not in the architecture note.
