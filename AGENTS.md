# Project Koios coordination bootstrap

This repository is the operational coordination point for work that spans
multiple Project Koios repositories.

It does not own product architecture, implementation, knowledge, workflow
state, or a named-role system. Durable decisions and artifacts belong in the
repository that owns them.

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

## Durable state

- Product and cross-repository architecture belongs in `projectkoios`.
- Component implementation and validation belongs in the component repository.
- Commit hashes, pull requests, issues, and owning-repository documents are the
  durable coordination record.
- This repository must not store session transcripts, replicated work queues,
  generated state, checkpoints, handoffs, or status databases.

## Boundaries

- Do not recreate the Hermes/Athena/Vulcan/Koios role system.
- Do not add a workflow engine, daemon, custom package manager, installer,
  schema catalog, operator console, or telemetry system here.
- Generic Pi extensions and credentials belong in the operator's Pi
  installation, not this repository.
- Repository-specific instructions belong in each repository's `AGENTS.md` and
  optional `.pi/` directory.
- Add shared machinery only after a concrete recurring coordination failure is
  demonstrated and native Pi or Git cannot solve it.
