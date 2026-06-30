# ADR 20260630.042202: Colored Petri net meta-harness model

## Status

Draft

## Context

The Project Koios meta-harness routing was governed by prose rules that were
not machine-checkable. Two recurring failures exposed the gap:

1. Hermes could become a passive mailbox forwarding unresolved state instead
   of producing a routing decision, revision request, or completion decision.
2. Hermes could accidentally act as implementer after work had already been
   routed to Vulcan.

A plain DAG can order steps, but cannot model ownership, artifact type,
provenance, authority, invalid transitions, concurrent active handoffs, or
revision loops.

## Decision

Model the meta-harness as a colored Petri net using OOP DataObjects and
ActionObjects.

### Core model

- **Places** — inboxes and workflow states (`hermes_inbox`, `athena_inbox`,
  `vulcan_inbox`, `koios_inbox`, `architecture_spec_ready`, etc.)
- **Colored tokens** — typed artifacts (`ArtifactToken` with `kind`, `origin`,
  `sender`, `recipient`, `acting_as`, `authority_level`, `provenance`)
- **Transitions** — harness actions (`RouteToAthena`, `ApplyImplementation`,
  `RunCompletionGate`, `RequestRevision`, etc.) with `enabled()` and `apply()`
- **Guards** — predicates that must pass before a transition fires
- **Marking** — current distribution of tokens across places
- **Violations** — first-class output when a guard fails

### Guard rules

1. **Hermes is not a passive mailbox** — Hermes may forward a token only if it
   produces a `routing-decision`, `revision-request`, `completion-decision`, or
   `blockage-report`.
2. **Vulcan owns implementation** — Once an `implementation-brief` reaches
   `vulcan_inbox`, only Vulcan may produce `patch`, `test-results`, or
   `implementation-report`.
3. **Athena owns architecture** — Only Athena may produce final
   `architecture-spec`, `acceptance-criteria`, or `implementation-brief`
   derived from design ambiguity.
4. **Codex delegation is mediation, not identity** — Codex-mediated artifacts
   must preserve `Delegated-Operator` provenance.
5. **Invalid provenance blocks authority** — Artifacts with collapsed or
   missing provenance cannot be consumed as authoritative.

### First implementation slice

A read-only handoff evaluator that:
- parses headers from handoff directories
- builds `ArtifactToken` instances
- assigns tokens to places
- runs guard checks
- prints violations without modifying files

## Consequences

- Prose-only routing rules are replaced by machine-checkable guards.
- The existing `HandoffEvaluator`, `HandoffParser`, `Marking`, and `Violation`
  types in `harness/data/` and `harness/handoffs/` implement this model.
- Archon DAG workflows are not replaced — the CPN model layers above them.
- Long-term, the model can export to other Project Koios repos.

## Source

This ADR distills content from:
- `docs/archive/handoffs/archon/20260630.042202_colored-petri-net-meta-harness.md`
- `docs/archive/handoffs/archon/20260630.044545_colored-petri-net-meta-harness-draft.md`
