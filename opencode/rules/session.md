# Session protocol

These steps execute on every session start and end to reduce manual direction.

## Session start

On first invocation, before waiting for input:

1. **Check handoffs** — scan `docs/archive/handoffs/` for any active artifacts not yet processed. Report what was found.
2. **Check git state** — report current branch, dirty status, and last 5 commits.
3. **Wait for direction** — present findings and let the user choose next steps. If a handoff targeting Vulcan is found, flag it and offer to proceed.

## Session end

Before signing off, after the implementation work is done:

1. **Run validation gates** — if files were changed, run `pytest`, `ruff check .`, and `mypy src/python`.
2. **Report git state and ask to commit** — show `git status` and `git diff --stat`, then ask the user if they want to commit the changes.
3. **Document decisions in ADRs** — if the session produced durable architectural decisions, update or create an ADR in `docs/architecture/adr/`.
5. **Summarize** — state what was done and what follow-ups remain.
