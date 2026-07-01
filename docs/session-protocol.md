# Pi session protocol

This document mirrors the session-start and session-stop rules for the pi meta-harness.

## Session start

At the start of a new session, keep the intake lightweight and do this in order:

1. Use Graphify first for broad repository context. If `graphify-out/graph.json`
   exists, prefer `graphify query`, `graphify path`, or `graphify explain`
   before manually reading ADRs, handoffs, docs, or source files. For a
   session-boundary refresh, prefer `graphify update .` over `graphify .`.
2. Check the live repo state: git branch, git status, and the last few commits.
3. Check active orchestration state: current ADRs, current handoff locations,
   and any running, paused, or orphaned Archon runs.
4. Treat `docs/archive/handoffs/` as provenance only. An archived
   `Status: active` header is historical evidence, not an instruction to run
   old work.
5. If an archived handoff conflicts with current filesystem state, current
   ADRs, or later implementation reports, report it as stale or superseded.
6. Report the highest-leverage next state to move toward before making changes.

## Session stop

Before ending a session:

1. If files changed, run the smallest relevant validation you can justify.
2. If meaningful repository files changed, run `graphify update .` (AST-only,
   no LLM needed) before final reporting unless unavailable or would block an
   urgent handoff. If you only need the AST/code refresh and want to skip
   clustering, use `graphify update . --no-cluster`.
3. Always write an AAR under `docs/AAR/`. Use AARs for protocol failures,
   repeated user corrections, unclear sandbox message delivery,
   workflow/tool friction, validation gaps, or improvement candidates. For
   trivial clean sessions, write a brief AAR that states no durable process
   issue was observed.
4. Report files changed and validation results.
5. Write or update the relevant handoff if work must continue in another harness.
6. Ask before commit/push unless the user already directed it.
