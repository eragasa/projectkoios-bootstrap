# Session protocol

These steps execute on every session start and end to reduce manual direction.

## Session start

On first invocation, before waiting for input:

1. **Check handoffs** — scan `archon/handoffs/`, `opencode/handoffs/`, `pi/handoffs/` for any new or active artifacts targeting opencode. Report what was found.
2. **Check git state** — report current branch, dirty status, and last 5 commits.
3. **Wait for direction** — present findings and let the user choose next steps. If a handoff targeting Vulcan is found, flag it and offer to proceed.

## Session end

Before signing off, after the implementation work is done:

1. **Run validation gates** — if files were changed, run `pytest`, `ruff check .`, and `mypy src/python`.
2. **Report git state and ask to commit** — show `git status` and `git diff --stat`, then ask the user if they want to commit the changes.
3. **Write implementation-report** — create a handoff in `opencode/handoffs/` using the handoff file convention from root `AGENTS.md` (filename `YYYYMMDD.HHMMSS_<topic>.md`, header with Origin/Created/From/To/Status).
4. **Update consumed handoff status** — if work originated from a handoff artifact, update its `Status` header to `complete` (or `revision-request` if follow-up is needed).
5. **Summarize** — state what was done and what follow-ups remain.
