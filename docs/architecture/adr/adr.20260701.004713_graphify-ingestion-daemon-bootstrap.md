# ADR 20260701.004713: Hermes Graphify daemon for projectkoios-bootstrap

## Status

Accepted

## Context

Origin: user request and architecture interview
From: Codex
Acting-As: Athena
Scope: projectkoios-bootstrap only
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

This ADR replaces the broader Draft ADR
`docs/architecture/adr/adr.20260701.004713_graphify-ingestion-daemon-bootstrap.md`
with the narrower human-selected daemon architecture from
`docs/architecture/interviews/architecture-interview-graphify-ingestion-daemon.md`.

The earlier draft described a temporary Graphify ingestion daemon for bounded
evidence discovery and left room for selected vault paths, PDFs, directives,
and future knowledge-ingestion work. The architecture interview narrowed that
scope substantially. The first daemon slice is not a general Project Koios
ingestion engine. It is a Hermes-owned local background service that keeps
Graphify output automatically updated for this repository only:
`projectkoios-bootstrap`.

The accepted consolidation ADR
`docs/architecture/adr/adr.20260630.214135_koios-evidence-intake-directive-contract.md`
continues to govern the broader boundary: Graphify is a temporary evidence
substrate; Koios does not own architecture; Hermes owns routing and operations;
Athena owns architecture decisions; Vulcan implements only accepted and routed
work. This ADR adds a repo-local operational slice under that boundary.

The selected human decisions are:

- first implementation target is Hermes CLI/background service authority
- source surface is `projectkoios-bootstrap` only
- daemon means a real local background watcher
- runtime authority is Hermes-owned local service with repo-defined architecture
- updates are filesystem-triggered with `.gitignore`-style exclusions
- Graphify serves all agents as a broad-context substrate
- local Ollama participates in daemon semantic processing
- Ollama output is universal chunk cards for all agents
- chunking uses Graphify defaults and records effective parameters and versions
- generated graph database, chunk cards, and run metadata live in Hermes-local
  runtime state, not git
- agents discover output through a documented default path convention
- failed files produce partial publish with degraded or stale warnings
- changes during an update are debounced and coalesced, with one follow-up
  update scheduled when needed
- acceptance is a safety-focused functional test

## Decision

Build, when accepted and routed, a Hermes-owned local Graphify daemon for
`projectkoios-bootstrap`.

The daemon performs an initial full Graphify build over supported files in this
repository, then watches the repository filesystem for changes. It excludes
paths using `.gitignore`-style matching plus obvious generated, runtime,
sensitive, and daemon-output exclusions. When eligible changes occur, it
debounces and coalesces events, runs the smallest practical refresh, and
publishes updated local Graphify snapshots and metadata for agent use.

The daemon writes generated output only under Hermes-local runtime state. The
default path convention is:

```text
~/.pi/koios-ingestion/projectkoios-bootstrap/
```

That runtime directory may contain generated graph data, universal chunk cards,
run metadata, degraded-state reports, and freshness markers. It is local
runtime state and must not be committed to `projectkoios-bootstrap`.

Local Ollama is part of the daemon's semantic processing for this slice. The
daemon wraps Graphify AST and chunking behavior, uses Graphify default chunking
parameters, records the effective Graphify chunking metadata and tool versions,
and calls Ollama to produce universal chunk cards. A universal chunk card is a
repo-local, role-neutral summary object intended to help any agent orient to
changed or indexed content. It is not a role-specific review hint, accepted
knowledge note, entity/relation ontology, or architecture decision.

The daemon may publish a degraded snapshot when some files fail processing. A
degraded snapshot is usable discovery output only if it clearly records stale
or failed inputs, skipped paths, last successful update, and warning state.
Agents must treat degraded Graphify output as context, not as authoritative
completion evidence.

The daemon is intentionally scoped to automatically updated Graphify for this
repository. Vault ingestion, PDF ingestion, whole-workspace ingestion,
directive queues, role-specific semantic overlays, custom entity/relation
ontology work, and `projectkoios.ingestion` incubation are deferred.

## Consequences

The architecture gives all harness roles a fresher broad-context substrate for
`projectkoios-bootstrap` without turning this repository into the owner of a
general ingestion engine. Hermes owns local operation and runtime state.
Athena owns this architecture decision. Vulcan may implement only after Hermes
routes an accepted ADR. Koios may consume provenance-backed output as discovery
context but does not make architecture decisions through the daemon.

The design accepts limited local complexity: a background watcher, debounce and
coalesce logic, Graphify invocation, Ollama card generation, and degraded
snapshot handling. That complexity is constrained by repository-only scope,
Hermes-local output, default Graphify chunking, and safety-focused validation.

The daemon creates useful generated state but not accepted source-of-truth
artifacts. Accepted and completed ADRs remain architecture authority. Live
filesystem and git state remain implementation fact authority. Graphify and
Ollama outputs remain retrieval and orientation substrate.

## architecture-spec

The daemon has these components:

- **Source root:** the `projectkoios-bootstrap` repository root.
- **Watcher:** a Hermes-local filesystem watcher observing the source root.
- **Exclusion policy:** `.gitignore`-style path matching plus built-in excludes
  for `.git/`, `graphify-out/`, Hermes runtime output, generated caches,
  dependency directories, machine-local secrets, and other runtime artifacts.
- **Update scheduler:** debounce and coalesce layer that turns bursts of file
  events into a single update request and schedules one follow-up update when
  changes arrive while an update is already running.
- **Graphify runner:** initial full build plus incremental or refresh behavior
  using Graphify defaults where available.
- **Ollama card generator:** local semantic pass that produces universal chunk
  cards from Graphify chunks or chunk-equivalent inputs.
- **Publisher:** writes graph snapshots, chunk cards, run metadata, freshness
  markers, and degraded-state reports to Hermes-local runtime state.
- **Discovery convention:** agents locate output by the documented default path
  convention, not by committed per-agent bootstrap folders.

Required runtime metadata includes:

- repository path and repository identity
- daemon version or command version when available
- Graphify version and effective chunking parameters
- Ollama model name, endpoint identity, and semantic-generation settings that
  are safe to record
- start time, finish time, duration, and trigger kind
- changed paths considered, skipped paths count, and exclusion reason summary
- files processed, files failed, and files stale
- graph snapshot path and chunk-card output path
- freshness state: `fresh`, `updating`, `degraded`, `stale`, or `failed`
- previous successful snapshot reference when publishing degraded output

The daemon must preserve these authority rules:

- Graphify output is retrieval substrate, not final authority.
- Ollama chunk cards are role-neutral orientation aids, not accepted knowledge.
- Accepted and completed ADRs remain architecture intent authority.
- Live filesystem and git state remain implementation fact authority.
- Hermes owns local daemon operation and validation routing.
- Athena owns architecture changes to the daemon boundary.
- Vulcan owns implementation only after Hermes routes accepted work.
- Koios may consume output for provenance-backed discovery, not architecture
  approval.

## acceptance-criteria

- The daemon is scoped to `projectkoios-bootstrap` only.
- The daemon is Hermes-owned local runtime, not Archon, Koios, or Vulcan-owned
  runtime.
- The first supported mode is a real local background watcher with an initial
  full Graphify build.
- Filesystem events trigger updates through debounce and coalesce behavior.
- If events arrive while an update is running, the daemon schedules one
  follow-up update rather than running overlapping refreshes.
- Source inclusion follows Graphify-supported files under the repo root after
  `.gitignore`-style, generated, runtime, sensitive, and daemon-output
  exclusions.
- Graphify default chunking is used unless a later accepted ADR changes it.
- Effective chunking parameters and Graphify/Ollama tool versions are recorded
  in run metadata.
- Local Ollama produces universal chunk cards for all agents.
- Universal chunk cards are not role-specific overlays, review-only hints, or a
  durable knowledge ontology.
- Generated graph data, chunk cards, run metadata, and degraded-state reports
  live under Hermes-local runtime state such as
  `~/.pi/koios-ingestion/projectkoios-bootstrap/`.
- Generated runtime output is not committed to this repository.
- Partial processing failures publish a degraded or stale snapshot only with
  visible warnings and file-level failure metadata.
- The daemon detects unexpected source-tree changes caused by its own run and
  fails or warns rather than silently corrupting the working tree.
- Agents can discover output through the documented default path convention.
- No code is implemented from this Draft ADR until Hermes routes an accepted
  ADR to Vulcan.

## implementation-brief

Do not implement code from this Draft ADR until Hermes reviews it and Athena
accepts it.

If accepted and routed to Vulcan, implement the smallest daemon bootstrap slice:

- define a Hermes-local command or service entrypoint for the daemon
- perform an initial full Graphify build for `projectkoios-bootstrap`
- add a filesystem watcher scoped to the repository root
- implement `.gitignore`-style exclusions and built-in runtime/generated/
  sensitive exclusions
- implement debounce and coalesce behavior, including one follow-up update when
  changes arrive during an active update
- write generated graph data, universal chunk cards, run metadata, degraded
  reports, and freshness markers under
  `~/.pi/koios-ingestion/projectkoios-bootstrap/`
- use Graphify defaults for chunking and persist effective parameters and
  Graphify tool version metadata
- call local Ollama directly for universal chunk-card generation
- document the default output path convention for agents
- include safety-focused functional validation

Vulcan must not implement in this slice:

- vault ingestion
- PDF ingestion
- whole-workspace ingestion
- directive queues or a general ingestion engine
- `projectkoios.ingestion`
- role-specific overlays
- review-specific card schemas
- a custom entity/relation ontology
- per-agent bootstrap folders or committed agent discovery config
- startup-at-login or OS-level service installation
- source repository mutation except normal reads and generated local runtime
  writes outside the repo
- committed Graphify daemon output

## resolved-open-questions

- Should the daemon remain a broad evidence-ingestion daemon?
  No. It is narrowed to automatically updated Graphify for
  `projectkoios-bootstrap`.

- Should the first slice support the mothership vault or PDFs?
  No. Vault and PDF ingestion are deferred.

- Should this begin `projectkoios.ingestion`?
  No. More complicated ingestion is deferred until that boundary is explicitly
  incubated.

- Is the daemon just a manual refresh command?
  No. The selected first slice is a real Hermes-local background watcher with
  an initial full build.

- Are updates commit-triggered?
  No. Filesystem changes are the trigger; commit metadata and review workflows
  are not required.

- Does Ollama replace Graphify?
  No. Graphify remains the graph/chunking substrate. Ollama adds local
  universal chunk cards.

- Should chunking be tuned now?
  No. Use Graphify defaults and record effective parameters and versions.

- Where does generated output live?
  Under Hermes-local runtime state, by default
  `~/.pi/koios-ingestion/projectkoios-bootstrap/`.

- How do agents discover output?
  Through the documented default path convention only.

- What happens when file processing partially fails?
  Publish the last usable or partial degraded snapshot with visible degraded or
  stale warnings and failure metadata.

## non-goals

- Do not define the long-term Project Koios ingestion system.
- Do not build or name `projectkoios.ingestion`.
- Do not ingest the mothership vault.
- Do not ingest PDFs.
- Do not watch the whole workspace.
- Do not create a native graph/RAG system.
- Do not create role-specific semantic overlays.
- Do not define a custom entity/relation ontology.
- Do not add committed per-agent bootstrap folders for daemon discovery.
- Do not make Graphify output, Ollama cards, or degraded snapshots final
  architecture or implementation authority.
- Do not commit daemon runtime state, generated graph databases, chunk cards,
  local metadata, secrets, or machine-local paths.

## validation-expectations

Hermes should require Vulcan to provide a safety-focused functional validation
report before marking implementation complete.

Validation should show:

- the daemon can perform an initial full build for `projectkoios-bootstrap`
- the watcher reacts to eligible filesystem changes
- excluded paths do not trigger ingestion
- generated/runtime/sensitive paths are excluded
- daemon output is written under Hermes-local runtime state, not the repo
- `git status --short` does not show daemon-generated output or source-tree
  mutations after a daemon run, except intentional implementation files
- event bursts are debounced into one update
- changes arriving during an update schedule one follow-up update
- partial file failures produce degraded or stale warnings
- run metadata records Graphify version, effective chunking parameters, Ollama
  model metadata, trigger kind, processed files, skipped files, failed files,
  and freshness state
- universal chunk cards are produced for at least one changed or indexed chunk
- agents can locate output by the documented default path convention

Validation may use temporary files inside the repository for the test, but the
daemon must clean up its generated runtime output outside the repo and must not
capture secrets or machine-local state in committed files.

## routing

Hermes should review this Draft ADR and route it to Athena for acceptance or
revision. If Athena accepts it, Hermes may route the implementation brief to
Vulcan.

After Vulcan reports, Hermes validates the implementation against the
acceptance criteria and validation expectations above. If Vulcan discovers that
Graphify defaults, Ollama integration, watcher behavior, or local runtime
constraints cannot satisfy this ADR without broadening scope, Vulcan should
return a deviation report to Hermes rather than expanding the implementation.

Hermes then either accepts the implementation report and test results, routes a
bounded fix back to Vulcan, or returns the architecture question to Athena.
