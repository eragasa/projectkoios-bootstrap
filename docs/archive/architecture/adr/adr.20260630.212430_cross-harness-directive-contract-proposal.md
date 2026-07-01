# ADR 20260630.212430: Cross-harness directive contract proposal

## Status

historic

## Context

Origin: user decision request
From: Koios
Acting-As: goose
Scope: projectkoios-bootstrap cross-harness directive artifact contract
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

Current discussion exposed a missing artifact protocol for bounded requests that
cross harness boundaries. The immediate need is a Koios-to-Athena request
surface, but the same issue appears broad enough to warrant a general
cross-harness contract.

The discussion converged on a naming convention designed for deterministic
parsing:

`<producer>_<consumer>_<kebab-case-action>`

This allows splitting on `_` to recover producer, consumer, and action, while
keeping multi-word actions internally hyphenated.

Koios is not the architecture authority. This draft is a bounded proposal for
Athena to define the directive artifact contract rather than letting each
harness invent ad hoc request forms.

## Decision

Athena should create a bounded ADR that defines a general-purpose directive
artifact contract for requests crossing harness boundaries.

That ADR should decide at least:

- whether `directive` is the canonical general cross-harness request artifact
  class
- whether directive naming follows the pattern
  `<producer>_<consumer>_<kebab-case-action>`
- whether the convention is designed for deterministic parsing by splitting on
  `_`, leaving the action field internally hyphenated
- whether a family such as `projectkoios_<consumer>_directive` should exist for
  broad directives, with more specific intent encoded inside the document body
  rather than only in the filename
- how a directive differs from an ADR, handoff, implementation brief,
  knowledge-note, routing recommendation, or implementation report
- what mandatory fields a directive must contain, such as provenance,
  producer, consumer, action, intent, scope bounds, source set, requested
  output, constraints, and open questions
- how directive states interact with ADR status values like Draft, Accepted,
  Rejected, Completed, and Superseded

## Consequences

If Athena accepts this proposal and issues the follow-on ADR, Project Koios will
have a parseable, reusable request artifact contract rather than relying on
implicit or inconsistent handoff forms.

That would preserve role separation while improving routing clarity and machine
interpretability across harness boundaries.

This draft does not itself define the final architecture. It records the Koios
proposal surface inside the current ADR-directory convention until Athena
produces the authoritative ADR.

## acceptance-criteria

- A draft proposal exists in `docs/architecture/adr/` asking Athena to produce
  a bounded ADR about cross-harness directive artifact structure and naming.
- The proposal includes the naming pattern
  `<producer>_<consumer>_<kebab-case-action>`.
- The proposal explicitly distinguishes directive artifacts from authoritative
  architecture artifacts.
- The proposal states that Athena, not Koios, owns the final architecture
  decision.

## implementation-brief

No code implementation is requested by this proposal.

Athena should review this draft and decide whether to issue a final ADR that
standardizes the cross-harness directive artifact contract and naming
convention.

## resolved open questions

- The current discussion should result in a dedicated ADR about directive
  artifact naming and contract.
- The naming convention under consideration is
  `<producer>_<consumer>_<kebab-case-action>`.
- The proposal surface should live under `docs/architecture/adr/` for now,
  even if that is semantically awkward.
- Koios is preparing proposal context, not authoring the final architecture.

## non-goals

- This draft does not finalize the directive artifact contract.
- This draft does not define every possible harness artifact.
- This draft does not redesign the whole meta-harness.
- This draft does not implement new code, commands, or workflow behavior.
- This draft does not supersede accepted ADRs by itself.

## validation expectations

Athena should validate that any resulting ADR:

- remains scoped to projectkoios-bootstrap
- preserves role separation between Koios and Athena
- defines a parseable directive naming convention
- distinguishes directive artifacts from authoritative architecture artifacts
- specifies the minimum required fields for interoperable cross-harness
  directives
