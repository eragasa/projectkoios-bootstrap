# ADR 20260630.173445: Graphify-first session lifecycle

## Status

Accepted

## Context

Project Koios agents need fresh repository context at session start and a
current semantic/code graph at session end. Previous guidance required Graphify
for codebase, architecture, file-relationship, and impact questions, but did
not make Graphify part of the standard session lifecycle.

Manual broad reading is more expensive and more error-prone than querying the
existing graph first. The repository already keeps `graphify-out/graph.json`
locally, and session-start behavior now depends on distinguishing current
filesystem state and ADRs from deprecated archived handoffs.

## Decision

All Project Koios harnesses should use Graphify as the first broad-context read
path at session start when `graphify-out/graph.json` exists.

Agents should prefer:

- `graphify query` for broad context questions
- `graphify path` for relationship tracing
- `graphify explain` for focused node explanation

Manual file reads remain appropriate after Graphify identifies the relevant
files or lines, or when exact verification, patching, validation, or citation is
needed.

At session end, after meaningful repository file changes, agents should refresh
Graphify with the repository-standard update flow when available. If a full
semantic refresh needs credentials or a backend that is unavailable, agents
should run the available no-LLM/code update path and report the limitation.

This policy is documented in:

- `AGENTS.md`
- `docs/session-protocol.md`
- `pi/AGENTS.md`
- `opencode/AGENTS.md`
- `opencode/rules/session.md`
- `goose/AGENT.md`
- `agents/global/roles/ATHENA/archon_run_watch/SKILL.md`

## Consequences

- New sessions start from the indexed repository model before broad manual
  reading.
- Session-end work keeps local graph state closer to current filesystem state.
- Agents spend less context on exploratory reads and more on verification and
  targeted edits.
- Graphify output remains local generated state unless a future ADR decides to
  commit it.
- Semantic graph refresh can be limited by available backend credentials; this
  must be reported rather than silently ignored.
