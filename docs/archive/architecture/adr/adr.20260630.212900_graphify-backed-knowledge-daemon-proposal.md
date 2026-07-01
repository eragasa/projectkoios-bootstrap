# ADR 20260630.212900: Graphify-backed knowledge daemon proposal

## Status

historic

## Context

Origin: user decision request
From: Koios
Acting-As: goose
Scope: projectkoios-bootstrap temporary graph ingestion for repo and vault provenance
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

Project Koios needs stronger provenance-backed knowledge ingestion before a
native graph/RAG system exists. Current discussion clarified that Koios will
likely need to work across code repositories and the mothership Obsidian vault
at the same time, and that design proposals should be grounded in source
material with durable provenance.

A temporary solution is needed now. Graphify already provides a practical graph
extraction path for repository content and can serve as a bridge while the
longer-term Project Koios graph system is still undefined or unimplemented.

The immediate additional need is vault-aware ingestion, including the ability to
process PDF-backed source material through the Obsidian workflow so design and
architecture proposals can cite evidence rather than rely on untracked summary.

Koios is not the architecture authority. This draft is a bounded proposal for
Athena to decide whether Project Koios should adopt a temporary Graphify-backed
knowledge daemon and, if so, how it should operate.

## Decision

Athena should create a bounded ADR that defines whether Project Koios adopts a
temporary Graphify-backed daemon for knowledge ingestion and provenance support.

That ADR should decide at least:

- whether a temporary daemon is the right bridging architecture until a native
  Project Koios graph/RAG system exists
- what source surfaces the daemon may ingest or watch, including repository
  roots, repository docs, selected Obsidian vault paths, and PDFs
- whether the daemon should run in watch mode, polling mode, manual-trigger
  mode, or some hybrid model
- what outputs it should maintain, such as graph indexes, provenance metadata,
  extraction status, and skipped-source reporting
- what authority limits apply so the daemon remains read-oriented and does not
  silently mutate vault content, source repositories, or accepted knowledge
- how Koios should consume daemon output: as broad-context substrate,
  evidence-discovery surface, or temporary retrieval layer
- how provenance for PDF-derived and vault-derived claims must be preserved so
  design and architecture proposals remain inspectable
- how temporary status and future migration should be encoded so this daemon can
  be replaced by a first-class Project Koios graph system later without
  ambiguity

## Consequences

If Athena accepts this proposal and issues the follow-on ADR, Project Koios will
have a defined temporary ingestion substrate for provenance-backed design work
instead of relying on ad hoc repo scans and manual vault interpretation.

That would strengthen Koios's ability to support design proposals with explicit
sources while keeping the long-term graph architecture open.

This draft does not itself define the final architecture. It records the Koios
proposal surface inside the current ADR-directory convention until Athena
produces the authoritative ADR.

## acceptance-criteria

- A draft proposal exists in `docs/architecture/adr/` asking Athena to decide
  whether to adopt a temporary Graphify-backed knowledge daemon.
- The proposal explicitly includes repository ingestion, vault-aware ingestion,
  and PDF provenance requirements.
- The proposal explicitly treats the daemon as temporary infrastructure pending
  a future native graph/RAG system.
- The proposal states that Athena, not Koios, owns the final architecture
  decision.

## implementation-brief

No code implementation is requested by this proposal.

Athena should review this draft and decide whether to issue a final ADR that
standardizes the temporary graph-ingestion daemon, its source scope, its
provenance contract, and its migration boundary.

## resolved open questions

- The Graphify-backed daemon should be proposed as a separate ADR from Koios
  role definition and cross-harness directive contract.
- The daemon is intended as temporary bridging infrastructure, not the final
  Project Koios graph system.
- Vault-aware ingestion and PDF provenance are first-class requirements for this
  proposal.
- The proposal surface should live under `docs/architecture/adr/` for now,
  even if that is semantically awkward.
- Koios is preparing proposal context, not authoring the final architecture.

## non-goals

- This draft does not finalize daemon architecture.
- This draft does not define the long-term native Project Koios graph/RAG
  system.
- This draft does not implement file watching, vault parsing, or PDF extraction.
- This draft does not redesign the whole meta-harness.
- This draft does not supersede accepted ADRs by itself.

## validation expectations

Athena should validate that any resulting ADR:

- remains scoped to projectkoios-bootstrap
- preserves role separation between Koios and Athena
- defines the daemon's temporary status and migration boundary
- includes provenance handling for repo, vault, and PDF-derived claims
- constrains daemon behavior so ingestion does not become silent mutation or
  unbounded authority
