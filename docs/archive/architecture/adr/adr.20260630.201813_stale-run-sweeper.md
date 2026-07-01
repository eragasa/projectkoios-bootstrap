# ADR 20260630.201813: Stale-run sweeper for Archon detached workflows

## Status

historic

## Context

Archon detached workflow runs (`archon workflow run <name> --detach`) spawn a
background child process and return immediately. If the child exits prematurely
(network failure, provider error, misconfiguration), the Archon SQLite database
at `~/.archon/archon.db` never transitions the run from `running` to `failed`.
The orphan `running` row persists indefinitely, pollutes `archon workflow runs
--status running` output, and requires manual `archon workflow abandon <id>` to
clean up.

This happens every time Athena runs. The existing `archon_run_watch.py` script
monitors a single run by ID but is never invoked. No automated recovery exists.

The existing skill directory under `agents/global/roles/ATHENA/archon_run_watch/`
already contains loosely coupled scripts (`archon_run_watch.py`, `handoff_new.py`,
`session_scan.py`, `_utils.py`) that share a `sys.path.insert` import pattern
but have no shared run-utility library — each script duplicates its own
`run_archon()` and `detect_stale()` logic.

## Decision

### Architecture

1.  **Stale-run sweeper (`sweep_stale.py`)** — a standalone script that scans
    all runs currently in `running` status, checks each for staleness (child
    process gone or age exceeding threshold), and optionally abandons stale
    runs with a structured handoff artifact. Runs at session start or on demand.

2.  **Shared run library (`_run.py`)** — extract `RunStatus` (ObjectClass) and
    `ArchonClient` (ActionClass) into a common module consumed by both
    `archon_run_watch.py` and `sweep_stale.py`. Removes the prior redundant
    definitions in `archon_run_watch.py`.

3.  **ObjectClass/ActionClass factoring**:

    ```
    RunStatus (frozen dataclass)
      fields: run_id, status, pid, log_path, started_at, workflow_name, raw
      method: is_stale(max_age_minutes=60) -> str | None

    ArchonClient (class wrapping archon CLI)
      method: fetch_run(run_id)          -> RunStatus | str
      method: list_runs(status=None)     -> list[dict] | str
      method: abandon_run(run_id)        -> str | None
      private: _run(*args)               -> subprocess.CompletedProcess
    ```

4.  **Staleness detection** — two-tier:
    - PID check (`os.kill(pid, 0)`) is authoritative when the PID is present
    - Age-based fallback when PID is `null`: treat as stale if `started_at` is
      older than `max_age_minutes` (default 60)
    - Runs with neither PID nor `started_at` are inconclusive — skipped

5.  **Handoff artifact** — when `--abandon-stale` succeeds, the sweeper writes
    a structured handoff file to `docs/archive/handoffs/hermes/` with the
    abandoned run IDs, workflows, and staleness reasons. This provides
    provenance without requiring a live Hermes harness to consume it.

### What is intentionally omitted

- **Launch-path changes** — `archon workflow run --detach` is not wrapped or
  modified. The parent-exits-before-child limitation is an Archon CLI constraint
  outside this repo.
- **Daemon or background service** — no cron, LaunchAgent, or persistent monitor.
  The sweeper runs on demand and at session boundaries only.
- **Auto-retry** — stale runs are abandoned, not retried. The existing fast
  fallback rule (two failures, then write a handoff) remains the policy.
- **CLI integration** — the sweeper is a standalone script, not a
  `projectkoios bootstrap` subcommand. Neither Hermes nor Athena is alive to
  invoke CLI infrastructure, so a direct script path is simpler.

### Test strategy

- `RunStatus.is_stale()` tested as pure logic with known PID/age inputs
- `ArchonClient` tested by monkey-patching `_run()` to return synthetic
  `subprocess.CompletedProcess` values
- `sweep_stale.py` tested with mocked `ArchonClient`, including handoff artifact
  file existence assertion
- Existing `handoff_new` and `session_scan` tests unchanged

## Consequences

- Orphaned `running` rows are cleaned at session boundary rather than persisting
  indefinitely.
- `archon_run_watch.py` and `sweep_stale.py` share one run-utility library
  instead of duplicating functions.
- Handoff artifacts under `docs/archive/handoffs/hermes/` provide discoverable
  abandonment provenance even without a live Hermes.
- The sweeper catches orphans created before the session start, but not runs
  that go stale during a multi-hour session. A `--watch` mode can be added if
  that becomes a bottleneck.
- No new external dependencies, no daemon, no LaunchAgent.
