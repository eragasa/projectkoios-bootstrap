# Multi-repository coordinator startup candidate

## Lifecycle

**Candidate.** This is the first bounded Project Koios use. It does not yet
establish independent recurrence or justify extraction as generic Pi tooling.

## Purpose and contract

The candidate performs deterministic preflight and constructs the initial Pi
invocation for the Project Koios multi-repository coordination session. It:

- requires `HERDR_ENV=1` before Pi starts;
- verifies the bootstrap repository markers;
- resolves `pi` from `PATH`;
- applies a recognizable, operator-overridable session name;
- forwards explicit Pi command-line options while preserving the launcher's
  fixed option boundary;
- supplies the Project Koios coordination startup prompt;
- directs the running coordinator to inspect Herdr session evidence and keep
  client detach distinct from pane or server termination; and
- encodes the rule that every deferred finding is fixed, routed to justified
  owner work with authority, or explicitly closed untracked.

The executable entry point is `scripts/start-coordinator`; testable behavior is
implemented in
`python/projectkoios/bootstrap/harness/coordinator_startup.py`.

Run it from a Herdr-managed pane:

```bash
./scripts/start-coordinator
```

Arguments are passed to Pi before the fixed session name and startup prompt:

```bash
./scripts/start-coordinator --model sonnet:high
```

Set `PROJECTKOIOS_COORDINATOR_NAME` to use another session display name.
Arguments are explicit operator overrides, so mode-changing Pi options may
change interactive behavior. A caller-provided `--` terminator is rejected
because the launcher supplies it after the fixed session option.

## Authority and stop conditions

The launcher starts only the coordinator. It does not open repository panes,
start workers, delegate tasks, modify repositories, create issues, install
dependencies, or infer an operator objective. The prompt requires the
coordinator to discover live sessions and obtain authority before those
operations.

Startup stops before invoking Pi when the process is not Herdr-managed, the
repository markers are absent, or `pi` cannot be resolved. Pi and Herdr retain
ownership of session and pane behavior. The separate read-only
[Herdr session-continuity candidate](herdr-session-continuity.md) checks the
running pane after Pi starts; the launcher does not pretend to prove future
pane survival or pi-intercom connectivity.

## Replay and state

Planning is side-effect free for identical repository files, environment, and
arguments. Successful execution changes to the bootstrap root and replaces the
launcher process with Pi. The candidate writes no checkpoint, transcript,
queue, status database, or other runtime state to this repository. Pi owns its
normal session persistence outside the repository.

Repeated invocations normally create separate Pi sessions. Resuming an
existing session requires an explicit Pi session option supplied by the
operator.

## Validation and limitations

Pytest coverage includes unmanaged startup, missing repository markers, missing
Pi, a rejected caller option terminator, custom and empty session-name
overrides, absolute executable resolution, exact argument construction,
working-directory selection, process replacement, executable entry-point root
resolution, deferred-finding prompt policy, and rendered failure output. Run:

```bash
python3.14 -m pytest -q tests/harness/test_coordinator_startup.py
```

The tests mock process replacement. They do not claim that Herdr is attached,
Pi authentication is ready, pi-intercom loaded successfully, or a model will
follow the prompt. Those remain visible startup and operational checks.
Detach, reattach, server restart, pane closure, and native Pi restore semantics
are sourced from Herdr's official [persistence](https://herdr.dev/docs/persistence-remote/),
[session-state](https://herdr.dev/docs/session-state/),
[CLI](https://herdr.dev/docs/cli-reference/), and
[integration](https://herdr.dev/docs/integrations/) documentation. Immutable
`v0.9.1` source links are recorded in the continuity candidate and its code.

## Owner routing and revisit criteria

This Project Koios-specific policy belongs in this bootstrap repository while
it remains a candidate. Keep product implementation in its component owner and
cross-repository architecture in `projectkoios`. Revisit extraction only after
independent reuse shows that the mechanics, without Project Koios policy, are
stable generic Pi tooling.
