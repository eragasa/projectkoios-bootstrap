# Archon run failure modes

## Observed failures

### 1. Worktree isolation hides untracked files

If a workflow declares `worktree.enabled: true`, Archon creates an isolated
git worktree. Untracked source files (new handoffs, new spec files) are not
visible inside the worktree because they have not been committed.

**Symptom:** The prompt node starts, reads an empty directory, and produces
no output or an incorrect output.

**Fix:** Either commit or stage the source files first, or use a workflow
with `worktree.enabled: false` when working with untracked inputs.

### 2. worktree.enabled: false makes --branch invalid

Some workflows (e.g. `athena-handoff-spec`) set `worktree.enabled: false`
because they need live access to the current checkout. Passing `--branch`
to `archon workflow run` is meaningless for these workflows — there is no
worktree to branch.

**Symptom:** Archon accepts the flag silently but produces unexpected
runtime behavior.

**Fix:** Check `worktree.enabled` in the workflow YAML before adding
`--branch`. Use `--branch` only for workflows that explicitly enable
worktree isolation.

### 3. Prompt node starts but child process exits without completion

The prompt node is created and a detached child process starts. The child
process exits (success or failure) but no completion event is recorded in
`~/.archon/archon.db`.

**Symptom:** `archon workflow get <id> --json` shows `status: running` even
though the child process is gone. No artifact was written.

**Possible cause:** The node's completion handler did not fire, or the
provider's response stream terminated abnormally before a terminal state
was recorded.

**Fix:** Detect the stale-running condition and abandon the run with
`archon workflow abandon <id>`.

### 4. Run remains running in DB after child process exits

The `archon.db` record never transitions from `running` to
`completed`/`failed`/`abandoned`.

**Symptom:** `archon workflow list --json` shows stale `running` runs.
The `archon workflow get <id> --json` response has `status: running` but
no active OS process can be found for the associated PID.

**Fix:** Use `archon workflow abandon <id> --json` to clear the stale
record.

### 5. archon doctor passes even when prompt-node path is failing

`archon doctor` checks global configuration, provider connectivity, and
workflow validity. It does not verify that prompt-node execution completes
successfully for a specific workflow.

**Symptom:** `archon doctor` reports all green, but running a workflow
produces stale exits as described above.

**Interpretation:** The problem is in the runtime execution path for a
specific provider/workflow combination, not in Archon's global health.

### 6. Abandoning stale runs may require write access escalation

`archon workflow abandon` writes to `~/.archon/archon.db`. If the sandbox
or runtime environment blocks writes to that path, the command will fail.

**Symptom:** `archon workflow abandon <id>` exits with a permission error.

**Fix:** Report the sandbox restriction clearly. If escalation is available,
request it. Otherwise note the stale run and move on.

### 7. toolCount: 0 in logs

When a Pi-provider prompt-node route is used, `toolCount: 0` in the Archon
log indicates the node was created without tool bindings. This is a useful
diagnostic clue that the provider configuration may be incomplete.

## Fast fallback rule

After two AI-node Archon attempts in one session exit stale in the same
way, stop retrying. Write or update a handoff/deviation note. Proceed as
Hermes with a direct artifact if that is within Hermes scope. Report
exactly what Archon failed to do and what was done instead.
