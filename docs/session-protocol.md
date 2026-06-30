# Pi session protocol

This document mirrors the session-start and session-stop rules for the pi meta-harness.

## Session start

Before doing other work in a new session:

1. Use Graphify first for broad repository context. If `graphify-out/graph.json`
   exists, prefer `graphify query`, `graphify path`, or `graphify explain`
   before manually reading ADRs, handoffs, docs, or source files.
2. Check current ADRs, current handoff locations, git branch, git status, and
   the last few commits.
3. Treat `docs/archive/handoffs/` as provenance only. An archived
   `Status: active` header is historical evidence, not an instruction to run
   old work.
4. If an archived handoff conflicts with current filesystem state, current
   ADRs, or later implementation reports, report it as stale or superseded.
5. Report pending current work before making changes.

## Session stop

Before ending a session:

1. If files changed, run the smallest relevant validation you can justify.
2. If meaningful repository files changed, run `graphify update .` (AST-only,
   no LLM needed) before final reporting unless unavailable or would block an
   urgent handoff.
3. Report files changed and validation results.
4. Write or update the relevant handoff if work must continue in another harness.
5. Ask before commit/push unless the user already directed it.
