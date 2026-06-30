# ADR 20260630.170000: Pending architecture decisions for Athena

## Status

Draft

## Context

Eight ADRs remain in Draft status and five design questions from the handoff-ledger-projection spec remain unresolved. This ADR consolidates all open decisions into a single artifact for Athena to review, resolve, or triage.

## Open decisions

### A. Handoff ledger projection — 5 design questions

From `docs/archive/handoffs/archon/20260630.141739_handoff-ledger-projection-spec.md`:

1. **message_id scheme** — Should the identifier be path-derived (e.g. `archon/20260630.141739...`), content-derived (hash of file contents), or a deterministic tuple/hash over repo-relative path plus normalized header fields?

2. **generated_at** — Should the JSON output include a `generated_at` timestamp by default, or be omitted so the output remains byte-stable across identical inputs?

3. **Command shape** — Should this ship as a new `handoff ledger` command, or extend the existing `handoff evaluate --json` with the projection vocabulary?

4. **Unparseable files** — Should skipped/unparseable handoff files appear in the projection with an error indicator, or be left out entirely with only summary counts?

5. **Status field** — Should the `Status` header field be treated as message payload only, or also as input to an inferred transition in the first slice?

### B. Draft ADRs requiring review

| ADR | Topic | Action requested |
|-----|-------|-----------------|
| `adr.20260630.141739_handoff-ledger-projection.md` | Read-only handoff ledger projection spec | Accept, modify, or reject; resolve questions above |
| `adr.20260630.042202_colored-petri-net-meta-harness.md` | Formal CPN model for the meta-harness | Accept as long-term model, or reject in favor of lighter approach |
| `adr.20260630.150000_skill-infrastructure-conventions.md` | Skill naming, header types, ledger foundation | Accept policy decisions or request revisions |
| `adr.20260630.121053_handoff-threshold.md` | When handoffs are warranted for trivial sessions | Accept, reject, or modify threshold |
| `adr.20260630.121054_session-end-gate.md` | Working tree gate at session end | Accept, reject, or modify |
| `adr.20260630.121055_hermes-build-default.md` | Build-mode default for Hermes sessions | Accept, reject, or modify |
| `adr.20260630.002151_harness-asset-layering.md` | Global vs local harness asset split | Accept or reject |
| `adr.20260629.195748_skill-encapsulation-conventions.md` | Skill encapsulation conventions | Accept or reject |

## Recommendation

Athena should:

1. Resolve the 5 handoff-ledger-projection questions first (they block Vulcan implementation).
2. Review and accept/reject the remaining draft ADRs, marking each as `accepted`, `rejected`, or `superseded` as appropriate.
3. Return a completion decision or produce follow-up implementation briefs as needed.

## Consequences

- All open architecture decisions are visible in one place.
- The 8 draft ADRs are superseded by this consolidated ADR but remain readable for context.
- After Athena resolves these items, the code agent can proceed with implementation.
