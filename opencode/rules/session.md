# Session protocol

These steps execute on every session start and end to reduce manual direction.

## Session start

On first invocation, before waiting for input:

1. **Use Graphify first** — if `graphify-out/graph.json` exists, query the graph
   for current repo context before broad manual reading.
2. **Check current work** — inspect only ADRs actionable for Vulcan (Accepted
   status with implementation briefs, or handoffs/directives addressed to
   Vulcan/opencode), current handoff locations targeting Vulcan, branch, dirty
   status, and last 5 commits. Do not scan all draft ADRs — those are
   Hermes/Athena scope unless routed to you.
3. **Treat archives as provenance** — do not treat archived `Status: active`
   headers as current work unless later current artifacts confirm them.
4. **Wait for direction** — present findings and let the user choose next steps.
   If a current handoff targeting Vulcan is found, flag it and offer to proceed.

> **Actionable for Vulcan** means: Accepted ADRs with an `implementation-brief`
> section that Hermes has routed, or a directive/handoff with consumer/recipient
> matching opencode/Vulcan. Draft ADRs (even those specifying Vulcan work) need
> Hermes routing before implementation begins.

## Session end

Before signing off, after the implementation work is done:

1. **Run validation gates** — if files were changed, run `pytest`, `ruff check .`, and `mypy src/python`.
2. **Refresh Graphify** — after meaningful repository changes, run
   `graphify update .` (AST-only, no LLM needed) when available.
3. **Report git state and ask to commit** — show `git status` and `git diff --stat`, then ask the user if they want to commit the changes.
4. **Document decisions in ADRs** — if the session produced durable architectural decisions, update or create an ADR in `docs/architecture/adr/`.
5. **Summarize** — state what was done and what follow-ups remain.
