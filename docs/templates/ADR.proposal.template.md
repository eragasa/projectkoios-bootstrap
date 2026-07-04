# ADR YYYYMMDD.HHMMSS: <Title>

> Legacy Markdown render example. Canonical ADRs are JSON in `docs/schemas/adr.schema.json`.
> Controlled by: [adr.adr-template-contract](../adr/adr.adr-template-contract.md).
> Template index: [templates.00](templates.00.md).

---
## Status

draft

## Context

Origin: <origin>
From: <sender>
Acting-As: <harness-role>
Scope: <repository-or-scope>
Repository: <repository-name>

<Describe the problem, why it matters, and the current state.>

<Use exactly one architecture domain. This is a proposal, not an implementation plan.>
---

## Decision

<State the proposal being made to the relevant architecture owner.>

## Consequences

<Describe the trade-offs, follow-on work, and validation impact if accepted.>

## architecture-spec

<Bounded architecture decision for one domain.>

## acceptance-criteria

- <Criterion 1>
- <Criterion 2>
- <Criterion 3>

## implementation-brief

<Describe downstream follow-up expected, or state that no implementation is requested.>

### Verification method

<How Vulcan validates completion — e.g., `pytest tests/foo.py`, AST check, manual inspection, Graphify diff. Required for any implementation-bearing ADR.>

## Comments

Comments remain open while this ADR is in draft status. When the ADR is promoted to proposed, the proposed ADR becomes the active review surface and the draft is archived or marked superseded.

- ATHENA: <comment or concern>
- VULCAN: <comment or concern>
- KOIOS: <comment or concern>
- HERMES: <comment or concern>

## resolved-open-questions

- <Question or decision point 1>
- <Question or decision point 2>

## non-goals

- <Non-goal 1>
- <Non-goal 2>

## validation-expectations

- <How the resulting ADR, workflow, or artifact should be validated>

## document-state

- Owner: <Hermes | Athena | Vulcan | Koios>
- Current phase: <draft | proposed | review | accepted | validated | completed>
- Notes: <optional document-domain consistency guidance>
