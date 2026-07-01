# ADR 20260630.173445: Graphify-first session lifecycle

## Status

historic

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

At session end, after meaningful repository file changes, agents should run
`graphify update .` (AST-only, no LLM needed). This AST-only rebuild requires
no LLM credentials and is the canonical session-boundary update command for this
repository.

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
- Session-boundary rebuild uses AST-only `graphify update .`, which requires no
   LLM credentials and runs entirely locally.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

Not separately stated in the original archive ADR.

## implementation-brief

Not separately stated in the original archive ADR.

## resolved-open-questions

None stated.

## non-goals

None stated.

## validation-expectations

Not separately stated in the original archive ADR.

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

# ADR 20260630.173445: Graphify-first session lifecycle

## Status

historic

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

At session end, after meaningful repository file changes, agents should run
`graphify update .` (AST-only, no LLM needed). This AST-only rebuild requires
no LLM credentials and is the canonical session-boundary update command for this
repository.

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
- Session-boundary rebuild uses AST-only `graphify update .`, which requires no
   LLM credentials and runs entirely locally.
