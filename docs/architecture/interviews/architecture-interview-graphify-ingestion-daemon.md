# Architecture Interview: Graphify ingestion daemon bootstrap

## Existing ADR Context

This interview refines
`docs/architecture/adr/adr.20260701.004713_graphify-ingestion-daemon-bootstrap.md`.

The current Draft ADR extracted the daemon-specific pieces from the superseded
Koios proposal
`docs/architecture/adr/adr.20260630.212900_graphify-backed-knowledge-daemon-proposal.md`
and the accepted consolidation ADR
`docs/architecture/adr/adr.20260630.214135_koios-evidence-intake-directive-contract.md`.

The accepted consolidation ADR remains authoritative for the broader boundary:
Graphify is a temporary evidence substrate; Koios does not own architecture;
Hermes owns routing and operations; Athena owns architecture decisions; Vulcan
implements only accepted and routed work.

The interview narrowed the daemon from a general ingestion engine to an
automatically updated Graphify service for `projectkoios-bootstrap`. Broader
ingestion, vault/PDF support, and `projectkoios.ingestion` incubation are
deferred.

## Clarifying Questions

1. What is the first implementation target?
   - Selected: Hermes CLI/background service authority, not Archon workflow,
     Koios command, or design-only artifact.

2. What source surfaces should the first slice support?
   - Selected: `projectkoios-bootstrap` only.

3. What does daemon mean in the first slice?
   - Selected: real local background service watching for changes and ingesting
     updates.

4. Where does runtime authority live?
   - Selected: Hermes-owned local service with repo-defined architecture.

5. What triggers updates?
   - Initial preference: hybrid commit-triggered and explicit transient runs.
   - Revised preference: filesystem watcher over the repo, excluding obvious
     generated/runtime/sensitive paths.

6. How should local Ollama/Goose/Koios participate?
   - Initial clarification: immediate goal is Graphify-assisted context for
     agents, especially code review.
   - Revised clarification: the daemon uses Graphify for all agents, and local
     Ollama is part of the daemon's semantic processing. Goose/Koios broader
     enrichment remains deferred.

7. What event should code-review support optimize for?
   - Revised: filesystem changes, not PR metadata or explicit review workflow
     starts.

8. What corruption guardrail matters?
   - Selected: detect unexpected source-tree changes and avoid silent
     corruption. Later clarification narrowed the daemon to Graphify output,
     but safety remains acceptance-critical.

9. What initial full build should ingest?
   - Selected: all supported `projectkoios-bootstrap` files, following
     `.gitignore`-style exclusions and obvious sensitive/runtime/generated
     exclusions.

10. What does removing the AST-only restriction mean?
    - Revised: the daemon performs a full Graphify pass first, chunks files,
      builds the graph database, and then agents may use the automatically
      updated graph as their broad-context substrate.

11. How should the future `projectkoios.ingestion` boundary be represented?
    - Revised: the daemon is just automatically updated Graphify for now.
      More complicated ingestion is deferred until `projectkoios.ingestion`
      starts incubating.

12. How should Ollama integrate?
    - Selected: daemon wraps Graphify AST/chunking and calls Ollama directly
      for semantic enrichment rather than only treating Ollama as a Graphify
      backend.

13. What semantic output should Ollama produce?
    - Selected: universal chunk cards for all agents, not review-only hints,
      role-specific overlays, or full entity/relation ontology.

14. How should chunking parameters be handled?
    - Selected: use Graphify defaults and record effective parameters/tool
      versions in run metadata. Fine tuning is deferred and needs research.

15. Where should graph database, chunk cards, and run metadata live?
    - Selected: Hermes-local runtime directory, not committed repo files.

16. Where should the portable daemon contract live?
    - Selected: YAGNI. Keep this ADR/docs-only for now; avoid per-agent
      bootstrap folders until needed.

17. How should agents discover output?
    - Selected: documented default path convention.

18. What happens when files fail processing?
    - Selected: partial publish with degraded/stale warning.

19. What happens when changes arrive during an update?
    - Selected: debounce and coalesce; schedule one follow-up update if needed.

20. What is the acceptance gate?
    - Selected: safety-focused functional test.

21. How should interview results become architecture?
    - Selected: write this interview artifact, then pass both this artifact and
      the Draft ADR path to Archon/Athena to produce an updated ADR.

## Architectural Decision Axes

- Scope discipline: keep the daemon to automatically updated Graphify for
  `projectkoios-bootstrap`; defer vault, PDF, directive queues, broader
  ingestion, and `projectkoios.ingestion`.
- Model separation: treat source files and graph snapshots as objects; watcher
  updates, Graphify runs, and Ollama enrichment as action instances; runtime
  metadata and degraded-state reports as traces.
- Workflow compatibility: daemon state should map to future places,
  transitions, guards, and traces without requiring a Petri-net engine now.
- Repository boundary clarity: `projectkoios-bootstrap` owns the architecture
  and docs; Hermes owns local runtime; generated graph database, chunk cards,
  and run metadata stay out of git.

## Option 1: Manual Graphify Refresh Command

Short description: Hermes exposes a manual command that runs Graphify and
updates local graph output on demand.

What it implements now: one-shot Graphify refresh for `projectkoios-bootstrap`.

What it explicitly defers: background watching, Ollama chunk cards, degraded
snapshot publishing, and coalesced update handling.

Owning repository or repositories: `projectkoios-bootstrap` for architecture;
Hermes local runtime for operation.

Affected artifacts: ADR, run metadata, graph output.

Compatibility with the existing ADR: compatible but weaker than the clarified
daemon intent.

Effect on `ObjectClass` / `ActionClass` separation: clear separation between
source objects and refresh action.

Effect on future workflow or Petri-net compatibility: easy to model as one
transition.

Main advantages: simplest, safest, quickest.

Main risks: does not satisfy the background auto-update requirement.

Reversibility: high.

Architectural grade: B.

## Option 2: Hermes Background Auto-Updated Graphify Daemon

Short description: Hermes runs a local background watcher for
`projectkoios-bootstrap`, performs an initial full Graphify build, watches
filesystem changes with `.gitignore`-style exclusions, debounces/coalesces
updates, uses local Ollama to produce universal chunk cards, and publishes local
graph/chunk metadata under Hermes runtime state.

What it implements now: automatically updated Graphify substrate for all
agents; repo-only full build; filesystem watch; Ollama-generated universal
chunk cards; degraded snapshot status; run metadata; safety-focused functional
test.

What it explicitly defers: vault ingestion, PDF ingestion, whole-workspace
ingestion, role-specific overlays, entity/relation ontology, per-agent
bootstrap folders, `projectkoios.ingestion`, startup-at-login service
management, and Graphify chunking research.

Owning repository or repositories: `projectkoios-bootstrap` owns architecture;
Hermes local runtime owns daemon operation and generated state.

Affected artifacts: Draft ADR, daemon docs, Hermes-local graph database, chunk
cards, run metadata, degraded-state reports.

Compatibility with the existing ADR: strongest match to the clarified human
decision.

Effect on `ObjectClass` / `ActionClass` separation: source files, graph
snapshots, and chunk cards are objects; watch events, Graphify runs, and Ollama
card generation are action instances; run metadata is trace.

Effect on future workflow or Petri-net compatibility: maps cleanly to places
such as `graph.stale`, `graph.updating`, `graph.fresh`, `graph.degraded`, and
guards for ignored paths and failed files.

Main advantages: useful for all agents, operationally real, bounded to one repo,
and aligned with Hermes ownership.

Main risks: local background process risk, tree-corruption concern, and
Ollama/Graphify integration complexity.

Reversibility: medium-high if runtime state remains local and generated.

Architectural grade: A-.

## Option 3: Generic Project Koios Ingestion Prototype

Short description: Begin `projectkoios.ingestion` now by defining a generic
ingestion engine around Graphify, Ollama, source manifests, and future
multi-surface support.

What it implements now: general ingestion-oriented schema and early engine
shape.

What it explicitly defers: little; it starts the broader ingestion project.

Owning repository or repositories: likely not `projectkoios-bootstrap` alone;
would need mothership or future package ownership.

Affected artifacts: new architecture surfaces, schemas, runtime output, and
possibly package boundaries.

Compatibility with the existing ADR: conflicts with the clarified desire to
defer complicated ingestion.

Effect on `ObjectClass` / `ActionClass` separation: potentially strong if
designed well, but premature.

Effect on future workflow or Petri-net compatibility: high potential, high
prematurity.

Main advantages: future-oriented and extensible.

Main risks: boundary collapse and premature ontology/schema work.

Reversibility: medium-low.

Architectural grade: C.

## Option 4: Graphify Watcher Without Ollama Chunk Cards

Short description: Run a background filesystem watcher that only keeps Graphify
structural output fresh and defers all local Ollama semantics.

What it implements now: automatic Graphify refresh, repo-only full build, and
watch/debounce behavior.

What it explicitly defers: universal chunk cards and all LLM semantics.

Owning repository or repositories: `projectkoios-bootstrap` plus Hermes local
runtime.

Affected artifacts: graph output and run metadata only.

Compatibility with the existing ADR: compatible but misses the selected Ollama
integration.

Effect on `ObjectClass` / `ActionClass` separation: simple and clean.

Effect on future workflow or Petri-net compatibility: straightforward.

Main advantages: less complex than Option 2.

Main risks: too thin for a shared all-agent context substrate.

Reversibility: high.

Architectural grade: B+.

## Comparative Assessment

| Option | Fit to clarified intent | Scope discipline | Agent usefulness | Operational risk | Recommendation |
|---|---:|---:|---:|---:|---|
| Manual Graphify Refresh Command | Medium | High | Medium | Low | No |
| Hermes Background Auto-Updated Graphify Daemon | High | High | High | Medium | Yes |
| Generic Project Koios Ingestion Prototype | Low | Low | High later | High | No |
| Graphify Watcher Without Ollama Chunk Cards | Medium | High | Medium | Low-Medium | No |

## Recommended Course of Action

Recommend Option 2: Hermes Background Auto-Updated Graphify Daemon.

This best matches the clarified human direction:

- real background service
- repository-only first slice
- automatically updated Graphify
- local Ollama universal chunk cards
- all-agent broad-context substrate
- Hermes-local runtime output
- `.gitignore`-style exclusions
- degraded snapshot status
- debounce/coalesce update behavior
- safety-focused functional acceptance gate

The accepted architectural debt is that chunking parameters are not tuned yet
and local Ollama card generation is a narrow custom semantic layer before the
larger `projectkoios.ingestion` effort exists. The ADR should constrain that
debt by forbidding broader ingestion semantics, role-specific overlays, and
entity/relation ontology work in this slice.

## Required Human Decision

The human architect selected the daemon shape above and asked to pass this
interview plus the Draft ADR to Archon/Athena to produce an updated ADR.

## Notes for Archon

- Update the existing Draft ADR in place rather than creating a duplicate ADR
  unless Archon determines the repo lifecycle requires a replacement.
- Preserve Status: Draft unless explicitly instructed otherwise.
- Narrow the ADR from broad Graphify ingestion daemon to automatically updated
  Graphify for `projectkoios-bootstrap`.
- Include local Ollama universal chunk cards, but keep broader
  `projectkoios.ingestion` out of scope.
- Keep runtime output under Hermes-local state such as
  `~/.pi/koios-ingestion/projectkoios-bootstrap/`.
- Document discovery by default path convention only; do not introduce
  per-agent bootstrap folders or config surfaces yet.
- Use Graphify defaults for chunking and record effective parameters/tool
  versions in run metadata.
- Require `.gitignore`-style exclusions and obvious runtime/generated/sensitive
  exclusions.
- Require partial publish with degraded/stale warning when some files fail.
- Require debounce/coalesce behavior for update events.
- Require safety-focused functional validation before completion.
