# ADR 20260630.170000: Pending architecture decisions for Athena

## Status

historic

## Context

Eight ADRs were in Draft status and five design questions from the handoff-topics-projection spec were unresolved. This ADR consolidated all open decisions. This record documents their resolution by pi (Hermes).

## Decision

See the original ADR text below for the historical decision.

## Consequences

- All open architecture decisions from the consolidated superseded ADRs are resolved.
- The 5 handoff-topics-projection questions have concrete answers — Vulcan can proceed with implementation using the finalized spec.
- The 8 superseded ADRs are now closed as accepted. They remain readable for context.
- The Archon detached-run reliability item remains tracked but low-priority.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

### A. Handoff topics projection — 5 design questions

From `docs/archive/handoffs/archon/20260630.141739_handoff-ledger-projection-spec.md`:

| # | Question | Decision | Rationale |
|---|----------|----------|-----------|
| 1 | **message_id scheme** | **Path-derived** — repo-relative path from `docs/archive/handoffs/` | Handoff files are archived, never move. Simplest deterministic ID, human-readable, trivially portable. |
| 2 | **generated_at** | **Omitted by default; `--with-timestamp` flag** | Byte-stable output for CI/diffs/testing. Flag for operational traceability when needed. |
| 3 | **Command shape** | **New `handoff topics`** command | Clean CPN vocabulary. Coexists with existing `handoff evaluate`. Aligns with spec guidance to avoid `evaluator` as the long-term name. |
| 4 | **Unparseable files** | **Included in `skipped` array with reason** | Error states as domain DataObjects. Makes issues discoverable without breaking consumers. |
| 5 | **Status field** | **Message payload only** for first slice | YAGNI. Defer Status→transition inference to a later slice if the model needs it. |

### B. Draft ADRs — resolved

| ADR | Topic | Resolution |
|-----|-------|------------|
| `adr.20260630.141739_handoff-ledger-projection.md` | Read-only handoff topics projection spec | **Accepted**. Questions resolved above; spec is implementation-ready. |
| `adr.20260630.042202_colored-petri-net-meta-harness.md` | Formal CPN model for the meta-harness | **Accepted** as long-term model. CPN vocabulary adopted for the `handoff topics` command. |
| `adr.20260630.150000_skill-infrastructure-conventions.md` | Skill naming, header types, topics foundation | **Accepted**. Policy decisions stand. |
| `adr.20260630.121053_handoff-threshold.md` | When handoffs are warranted for trivial sessions | **Accepted**. Threshold as defined. |
| `adr.20260630.121054_session-end-gate.md` | Working tree gate at session end | **Accepted**. Gate stands. |
| `adr.20260630.121055_hermes-build-default.md` | Build-mode default for Hermes sessions | **Accepted**. Foreground builds by default. |
| `adr.20260630.002151_harness-asset-layering.md` | Global vs local harness asset split | **Accepted**. Split stands. |
| `adr.20260629.195748_skill-encapsulation-conventions.md` | Skill encapsulation conventions | **Accepted**. Encapsulation stands. |

### C. Low-priority operational follow-up

Archon detached/background workflow runs should be made reliable enough for
normal Hermes operation. Current guidance is to run Archon workflows in the
foreground by default because detached Codex-provider runs can leave orphaned
`running` rows without a completed spec, error event, or live worker process.

This is not a blocker for the Koios role definition or the handoff-topics
projection decisions, but it should be tracked as an operational hardening
item for Archon run management.

## implementation-brief

Not separately stated in the original archive ADR.

## resolved-open-questions

None stated.

## non-goals

None stated.

## validation-expectations

Not separately stated in the original archive ADR.

## routing

- Owner: Athena
- Next phase: completed
- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260630.170000: Pending architecture decisions for Athena

## Status

historic

## Context

Eight ADRs were in Draft status and five design questions from the handoff-topics-projection spec were unresolved. This ADR consolidated all open decisions. This record documents their resolution by pi (Hermes).

## Resolved decisions

### A. Handoff topics projection — 5 design questions

From `docs/archive/handoffs/archon/20260630.141739_handoff-ledger-projection-spec.md`:

| # | Question | Decision | Rationale |
|---|----------|----------|-----------|
| 1 | **message_id scheme** | **Path-derived** — repo-relative path from `docs/archive/handoffs/` | Handoff files are archived, never move. Simplest deterministic ID, human-readable, trivially portable. |
| 2 | **generated_at** | **Omitted by default; `--with-timestamp` flag** | Byte-stable output for CI/diffs/testing. Flag for operational traceability when needed. |
| 3 | **Command shape** | **New `handoff topics`** command | Clean CPN vocabulary. Coexists with existing `handoff evaluate`. Aligns with spec guidance to avoid `evaluator` as the long-term name. |
| 4 | **Unparseable files** | **Included in `skipped` array with reason** | Error states as domain DataObjects. Makes issues discoverable without breaking consumers. |
| 5 | **Status field** | **Message payload only** for first slice | YAGNI. Defer Status→transition inference to a later slice if the model needs it. |

### B. Draft ADRs — resolved

| ADR | Topic | Resolution |
|-----|-------|------------|
| `adr.20260630.141739_handoff-ledger-projection.md` | Read-only handoff topics projection spec | **Accepted**. Questions resolved above; spec is implementation-ready. |
| `adr.20260630.042202_colored-petri-net-meta-harness.md` | Formal CPN model for the meta-harness | **Accepted** as long-term model. CPN vocabulary adopted for the `handoff topics` command. |
| `adr.20260630.150000_skill-infrastructure-conventions.md` | Skill naming, header types, topics foundation | **Accepted**. Policy decisions stand. |
| `adr.20260630.121053_handoff-threshold.md` | When handoffs are warranted for trivial sessions | **Accepted**. Threshold as defined. |
| `adr.20260630.121054_session-end-gate.md` | Working tree gate at session end | **Accepted**. Gate stands. |
| `adr.20260630.121055_hermes-build-default.md` | Build-mode default for Hermes sessions | **Accepted**. Foreground builds by default. |
| `adr.20260630.002151_harness-asset-layering.md` | Global vs local harness asset split | **Accepted**. Split stands. |
| `adr.20260629.195748_skill-encapsulation-conventions.md` | Skill encapsulation conventions | **Accepted**. Encapsulation stands. |

### C. Low-priority operational follow-up

Archon detached/background workflow runs should be made reliable enough for
normal Hermes operation. Current guidance is to run Archon workflows in the
foreground by default because detached Codex-provider runs can leave orphaned
`running` rows without a completed spec, error event, or live worker process.

This is not a blocker for the Koios role definition or the handoff-topics
projection decisions, but it should be tracked as an operational hardening
item for Archon run management.

## Consequences

- All open architecture decisions from the consolidated superseded ADRs are resolved.
- The 5 handoff-topics-projection questions have concrete answers — Vulcan can proceed with implementation using the finalized spec.
- The 8 superseded ADRs are now closed as accepted. They remain readable for context.
- The Archon detached-run reliability item remains tracked but low-priority.
