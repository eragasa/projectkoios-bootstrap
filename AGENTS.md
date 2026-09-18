# Project Koios coordination bootstrap

This repository is the operational coordination point for work that spans
multiple Project Koios repositories and the incubation owner for the Project
Koios-specific Pi coordination harness.

It owns bounded coordination helpers, project-specific Pi skills or prompt
templates, sanitized fixtures, tests, and experimental harness candidates. It
does not own product architecture, component or scientific-domain
implementation, knowledge, live workflow state, or a named-role system.
Durable product decisions and artifacts belong in the repository that owns
them.

## Start

1. Read `maps/repositories.md`.
2. Use `pi-intercom` to list the live Pi sessions.
3. Inspect only the repositories relevant to the operator's request.
4. Ask before opening sessions or delegating work unless the operator already
   requested multi-repository execution.

## Coordination

- Use one Pi session per active repository.
- Identify sessions by repository or task, not by fictional roles.
- Use visible Herdr project panes for long-lived work.
- Use `pi-intercom` for session discovery, messages, questions, and progress.
- Use Pi subagents with an explicit `cwd` for bounded delegated work.
- Keep one writer per repository or isolated worktree.
- State each assignment's repository, objective, constraints, expected output,
  validation, and stop conditions.
- Treat session reports as evidence. Verify repository state before reporting
  completion.

## Harness incubation

- Treat versioned harness source, sanitized fixtures, and tests as development
  artifacts, not runtime state.
- Use the lifecycle `observed → candidate → repeated → validated →
  extracted/retained`.
- One occurrence may be preserved as a candidate; it does not establish
  recurrence or authorize production promotion.
- Project Koios-specific coordination tooling may remain here after validation.
  Stable generic Pi extensions belong in the operator's Pi installation or an
  explicitly accepted extracted owner repository.
- Keep candidates bounded, deterministic, reviewable, and independent of
  hidden session context.

## Durable state

- Product and cross-repository architecture belongs in `projectkoios`.
- Component implementation and validation belongs in the component repository.
- Commit hashes, pull requests, issues, and owning-repository documents are the
  durable coordination record.
- Tracked harness source, sanitized fixtures, tests, and candidate limitations
  are allowed here.
- This repository must not store session transcripts, replicated work queues,
  generated runtime state, checkpoints, generated handoffs, telemetry, or
  status databases. Private harness observations belong in managed operational
  state and may be referenced by content identity.

## Boundaries

- Do not recreate the Hermes/Athena/Vulcan/Koios role system.
- Do not add a workflow engine, daemon, custom package manager, installer,
  schema catalog, operator console, or telemetry system here.
- Stable generic Pi extensions and credentials belong in the operator's Pi
  installation, not this repository.
- Repository-specific instructions belong in each repository's `AGENTS.md` and
  optional `.pi/` directory.
- Preserve a bounded first observation before generalizing it. Add production
  shared machinery only after independent reuse evidence or a concrete
  recurring coordination failure shows that native Pi or Git is insufficient.
