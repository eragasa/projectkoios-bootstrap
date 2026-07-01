# ADR 20260630.212410: Koios ingestion scope proposal

## Status

historic

## Context

Origin: user decision request
From: Koios
Acting-As: goose
Scope: projectkoios-bootstrap Koios role refinement for multi-surface ingestion
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

Existing accepted architecture already defines Koios as the knowledge harness in
`docs/architecture/adr/adr.20260630.165929_koios-goose-role-definition.md`.
That ADR establishes broad ownership and provenance duties, but current
discussion exposed a more specific unresolved decision surface: how Koios should
operate when a task spans code repositories, repository documentation, and the
mothership Obsidian vault at the same time.

The main concern is scope control. Koios will likely need to ingest and relate
information across multiple knowledge surfaces, but it must do so without
flattening them into one authority surface, reading too broadly, or silently
turning stale or weakly sourced material into durable fact.

Koios is not the architecture authority. This draft is a bounded proposal for
Athena to refine the accepted Koios role with explicit operating rules.

## Decision

Athena should create a bounded ADR that defines Koios's operating boundary for
multi-surface knowledge ingestion.

That ADR should decide at least:

- how Koios operates across code repositories, repository documentation, and
  Obsidian vault knowledge without collapsing them into one authority surface
- what source-authority ordering Koios must apply when code, docs, archived
  handoffs, and vault knowledge disagree or differ in freshness
- what scope declaration or bounding step Koios must perform before broad
  ingestion across multiple repositories or vault regions
- what provenance, reproducibility, and claim-traceability standards Koios must
  apply for scientific-workflow-style knowledge representation
- what Koios should do when a request implicitly spans multiple repositories and
  the mothership vault at once
- what escalation path Koios must use when the source set is too broad,
  contradictory, or insufficiently authoritative
- whether Koios needs an additional first-class artifact for cross-source
  knowledge representation beyond the currently accepted `knowledge-note` and
  `provenance-index`

## Consequences

If Athena accepts this proposal and issues the follow-on ADR, Project Koios will
have an explicit scope-control doctrine for Koios rather than relying on a broad
role definition alone.

That would make Koios safer and more predictable when operating across live repo
state and durable vault memory at the same time.

This draft does not itself define the final architecture. It records the Koios
proposal surface inside the current ADR-directory convention until Athena
produces the authoritative ADR.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

- A draft proposal exists in `docs/architecture/adr/` asking Athena to produce
  a bounded ADR about Koios scope control for simultaneous repository and vault
  ingestion.
- The proposal explicitly calls out source authority ordering, scope bounding,
  provenance discipline, and escalation rules.
- The proposal states that Athena, not Koios, owns the final architecture
  decision.

## implementation-brief

No code implementation is requested by this proposal.

Athena should review this draft and decide whether to issue a final ADR that
refines the accepted Koios role with explicit operating rules for multi-surface
knowledge ingestion.

## resolved-open-questions

- The current discussion should result in a dedicated ADR about Koios scope and
  operating boundary.
- The proposal surface should live under `docs/architecture/adr/` for now,
  even if that is semantically awkward.
- Koios is preparing proposal context, not authoring the final architecture.

## non-goals

- This draft does not finalize Koios scope policy.
- This draft does not redefine the entire Koios role from scratch.
- This draft does not redesign the whole meta-harness.
- This draft does not implement new code, commands, or workflow behavior.
- This draft does not supersede accepted ADRs by itself.

## validation-expectations

Athena should validate that any resulting ADR:

- remains scoped to projectkoios-bootstrap
- preserves role separation between Koios and Athena
- gives Koios explicit scope-control rules for multi-surface ingestion
- defines authority ordering and escalation when source surfaces conflict or
  expand beyond the bounded task

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

# ADR 20260630.212410: Koios ingestion scope proposal

## Status

historic

## Context

Origin: user decision request
From: Koios
Acting-As: goose
Scope: projectkoios-bootstrap Koios role refinement for multi-surface ingestion
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

Existing accepted architecture already defines Koios as the knowledge harness in
`docs/architecture/adr/adr.20260630.165929_koios-goose-role-definition.md`.
That ADR establishes broad ownership and provenance duties, but current
discussion exposed a more specific unresolved decision surface: how Koios should
operate when a task spans code repositories, repository documentation, and the
mothership Obsidian vault at the same time.

The main concern is scope control. Koios will likely need to ingest and relate
information across multiple knowledge surfaces, but it must do so without
flattening them into one authority surface, reading too broadly, or silently
turning stale or weakly sourced material into durable fact.

Koios is not the architecture authority. This draft is a bounded proposal for
Athena to refine the accepted Koios role with explicit operating rules.

## Decision

Athena should create a bounded ADR that defines Koios's operating boundary for
multi-surface knowledge ingestion.

That ADR should decide at least:

- how Koios operates across code repositories, repository documentation, and
  Obsidian vault knowledge without collapsing them into one authority surface
- what source-authority ordering Koios must apply when code, docs, archived
  handoffs, and vault knowledge disagree or differ in freshness
- what scope declaration or bounding step Koios must perform before broad
  ingestion across multiple repositories or vault regions
- what provenance, reproducibility, and claim-traceability standards Koios must
  apply for scientific-workflow-style knowledge representation
- what Koios should do when a request implicitly spans multiple repositories and
  the mothership vault at once
- what escalation path Koios must use when the source set is too broad,
  contradictory, or insufficiently authoritative
- whether Koios needs an additional first-class artifact for cross-source
  knowledge representation beyond the currently accepted `knowledge-note` and
  `provenance-index`

## Consequences

If Athena accepts this proposal and issues the follow-on ADR, Project Koios will
have an explicit scope-control doctrine for Koios rather than relying on a broad
role definition alone.

That would make Koios safer and more predictable when operating across live repo
state and durable vault memory at the same time.

This draft does not itself define the final architecture. It records the Koios
proposal surface inside the current ADR-directory convention until Athena
produces the authoritative ADR.

## acceptance-criteria

- A draft proposal exists in `docs/architecture/adr/` asking Athena to produce
  a bounded ADR about Koios scope control for simultaneous repository and vault
  ingestion.
- The proposal explicitly calls out source authority ordering, scope bounding,
  provenance discipline, and escalation rules.
- The proposal states that Athena, not Koios, owns the final architecture
  decision.

## implementation-brief

No code implementation is requested by this proposal.

Athena should review this draft and decide whether to issue a final ADR that
refines the accepted Koios role with explicit operating rules for multi-surface
knowledge ingestion.

## resolved open questions

- The current discussion should result in a dedicated ADR about Koios scope and
  operating boundary.
- The proposal surface should live under `docs/architecture/adr/` for now,
  even if that is semantically awkward.
- Koios is preparing proposal context, not authoring the final architecture.

## non-goals

- This draft does not finalize Koios scope policy.
- This draft does not redefine the entire Koios role from scratch.
- This draft does not redesign the whole meta-harness.
- This draft does not implement new code, commands, or workflow behavior.
- This draft does not supersede accepted ADRs by itself.

## validation expectations

Athena should validate that any resulting ADR:

- remains scoped to projectkoios-bootstrap
- preserves role separation between Koios and Athena
- gives Koios explicit scope-control rules for multi-surface ingestion
- defines authority ordering and escalation when source surfaces conflict or
  expand beyond the bounded task
