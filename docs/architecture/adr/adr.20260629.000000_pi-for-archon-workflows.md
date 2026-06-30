# ADR 20260629.000000: Use Pi as the AI assistant for Archon workflows

## Status

Accepted

## Context

Project Koios uses `projectkoios-bootstrap` as the meta-harness for agent
operations. ADR20260628 establishes Archon as the harness for architecture,
design, ADR creation, and planning workflows.

Archon provides workflow orchestration, isolated worktrees, and structured
task execution, but the quality and consistency of those workflows still
depends on the AI assistant that performs the actual analysis and writing.
Project Koios needs a default assistant for Archon-driven work so that ADRs,
plans, and architecture outputs are produced with consistent engineering
judgment, repository awareness, and file-editing behavior.

## Decision

Use Pi as the AI assistant for Archon workflows in Project Koios.

Archon remains responsible for workflow orchestration, task routing, worktree
management, and repeatable process structure. Pi is responsible for
performing the delegated engineering work inside those workflows, including
repository inspection, ADR drafting, implementation planning, file edits, and
validation where applicable.

## Rationale

**Strong fit for repository-aware engineering tasks.** Pi is designed to
inspect a codebase, follow existing conventions, make scoped edits, and verify
the result. That fits the architecture and planning workflows assigned to
Archon.

**Clear separation of responsibilities.** Archon coordinates the workflow;
Pi performs the work. Keeping orchestration and execution separate avoids
overloading Archon with assistant-specific behavior while still giving Project
Koios a consistent default execution agent.

**Consistent ADR and planning outputs.** Pi can read the existing
`docs/architecture/adr/` directory before writing new records, which helps future ADRs
match the repository's established structure and tone.

**Works within isolated worktrees.** Archon-created worktrees provide a clean
execution boundary for delegated tasks. Pi can operate inside that boundary
without requiring Project Koios component repositories to depend on the
bootstrap harness.

## Consequences

Archon workflow definitions should assume Pi is the default assistant unless
a workflow explicitly declares another agent.

Prompts under `archon/` should be written for Pi-style execution: inspect
the repository first, preserve existing conventions, make concrete file
changes when requested, and report the resulting paths and verification.

Architecture workflows should continue to store durable decisions in
`docs/architecture/adr/`, while Pi-generated outputs should remain scoped to the
worktree and task requested by Archon.

If a workflow requires capabilities better served by another harness, such as
runtime coding sessions in opencode or knowledge-management tasks in Goose, it
should route the work to that harness instead of forcing it through Pi under
Archon.

## Alternatives considered

### Use Archon with no default assistant

Rejected. Leaving the assistant unspecified makes workflow results dependent
on ad hoc operator choices and reduces consistency across ADRs, plans, and
architecture reviews.

### Use Codex as the assistant for Archon workflows

Rejected. Codex remains a viable workflow provider, but Project Koios now
standardizes on Pi for its default Archon execution path to keep assistant
selection aligned with current repository practice.

### Use opencode as the assistant for Archon workflows

Rejected. opencode remains the preferred harness for interactive build,
runtime, test, and validation work. Using it as the default assistant inside
Archon would blur the boundary established in ADR20260628.

### Use Goose as the assistant for Archon workflows

Rejected. Goose is better suited to knowledge management, vault operations,
and MCP-centered ingestion or curation tasks. It is not the default fit for
repository-scoped architecture decisions and worktree-based planning.

### Select the assistant separately for every workflow

Rejected. Per-workflow selection may still be useful for exceptions, but using
it as the default approach creates unnecessary configuration overhead and makes
the meta-harness harder to operate consistently.
