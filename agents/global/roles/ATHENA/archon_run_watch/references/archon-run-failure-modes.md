# Archon run failure modes

## Observed failure modes

1.  **Worktree isolation hides untracked files** — Archon workflow runs in an
    isolated worktree; untracked input files are not visible unless staged or
    committed first.

2.  **`worktree.enabled: false` makes `--branch` invalid** — some workflows
    disable worktree isolation. Passing `--branch` to a non-worktree run
    causes a CLI error before the prompt node starts.

3.  **Prompt node starts but child process exits without completion** — the
    workflow shows `running` in `archon workflow list` but the child process
    (e.g. Claude Code) exits prematurely. No completion event fires.

4.  **Run remains `running` in DB after child process exits** — the Archon
    database records the run as still `running` even though the child process
    has exited. The run status does not transition to `completed` or `failed`.

5.  **`archon doctor` passes even when prompt-node path is failing** — the
    health check reports green, but the actual prompt-node provider is
    misconfigured or unreachable.

6.  **Abandoning stale runs may require write access escalation** — if the
    Archon sandbox blocks writes to `~/.archon/archon.db`, the `abandon`
    command fails with a sandbox permission error.

7.  **`toolCount: 0` in logs** — the provider config is missing or incomplete,
    causing the prompt node to start with zero tools available. Diagnostic
    signal found in
    `/Users/eugene/.archon/archon.db` and child process logs.

## Fast fallback rule

After two AI-node Archon attempts exit stale in the same way, stop retrying.
Write a handoff or deviation note. Proceed as Hermes with a direct artifact.
Report what Archon failed to do and what was done instead.
