# Herdr session-continuity integration candidate

## Lifecycle

**Candidate.** A Project Koios coordination pane was closed instead of the
Herdr client being detached, terminating its Pi process and interrupting a
read-only assignment. This first observed failure justifies preserving a
bounded diagnostic contract; it does not establish recurrence or authorize a
monitor, recovery daemon, communications layer, or replicated work queue.

## Placement and adapter boundary

The implementation is an external-application **integration** at
`projectkoios.bootstrap.integrations.herdr`. It uses the
[adapter and integration taxonomy](../architecture/adapters.md) extracted from
Project Koios Frankenstein. Herdr executable selection, read-only CLI requests,
output validation, bounded failures, and version evidence belong to the
integration boundary. There is no dependency binding because the implementation
uses the Python standard library rather than an imported Herdr client library.

The executable entry point is `scripts/inspect-herdr-session`. The tested
implementation is
`python/projectkoios/bootstrap/integrations/herdr/session.py`, and reviewed
upstream references are constants in
`python/projectkoios/bootstrap/integrations/herdr/references.py`.

## Contract

Run the inspector from a live Pi pane managed by Herdr:

```bash
./scripts/inspect-herdr-session
```

To inspect another known live pane on the same Herdr server without sending it
input:

```bash
./scripts/inspect-herdr-session --pane-id w4:p2
```

The output preserves both `inspection_target.requested_pane_id` and the
canonical `inspection_target.resolved_pane_id` returned by Herdr. They normally
match. Herdr's documented pane-move behavior retains a prior pane ID as an alias
for the same terminal, so a valid lookup can return a different canonical ID;
`resolved_via_pane_alias` makes that case explicit rather than rejecting it or
silently presenting it as an exact-ID match.

The inspector:

- requires Herdr's documented `HERDR_ENV`, `HERDR_BIN_PATH`, socket, workspace,
  tab, and pane environment values;
- uses `HERDR_BIN_PATH` rather than guessing an installation path;
- accepts exactly the reviewed Herdr `0.9.1` baseline;
- identifies the running session by the inherited socket path;
- verifies that the selected live pane appears in `herdr agent list`;
- requires a current official Pi integration new enough for documented native
  restore and a matching native Pi session reference;
- emits deterministic, schema-versioned JSON containing the exact absolute
  reattach argv, requested and canonical pane identities, and official
  reference URLs; and
- tolerates additive Herdr response fields while failing closed on missing or
  invalid fields it consumes.

The operation is read-only. It does not send pane input, detach a client, close
or create a pane, start or restore Pi, change Herdr configuration, or write
runtime state.

## Correct lifecycle semantics

Herdr is a background-server/client multiplexer. According to the official
`0.9.1` documentation:

1. `ctrl+b`, then `q` detaches the **client**. A simple terminal-window close
   also detaches. The server, pane PTYs, and original Pi processes continue.
2. `herdr` or `herdr session attach <name>` attaches a client to the running
   session.
3. Closing a pane, tab, or workspace is not detachment. It removes Herdr state
   and ends affected pane processes.
4. `herdr server stop` ends the pane processes. A later server start can restore
   layout, but live process continuity is gone.
5. Native agent restore is a distinct, weaker recovery path after server
   restart. It requires a current official integration, an integration-reported
   session reference, and enabled Herdr restore configuration. The inspector
   proves the first two facts only; it does not claim that restore is enabled or
   execute recovery.

The configured prefix or detach key may differ from the documented default.
Use `prefix+?` in Herdr to inspect active bindings. The JSON field is therefore
named `documented_client_detach_keys`, not `configured_detach_keys`.
`continuity.reattach_argv` starts with the absolute inherited
`HERDR_BIN_PATH`; it is an argv array, not shell-escaped text or a PATH lookup.

## Communication boundary

Herdr pane liveness and pi-intercom connectivity are different facts. This
integration confirms Herdr session, pane, agent, and native Pi session evidence.
It does not inspect the pi-intercom broker and must not be treated as proof that
another Pi session is reachable through pi-intercom. Coordinators still use
pi-intercom for discovery and messages, then use this read-only Herdr evidence
when pane lifecycle is in question.

A missing or closed target pane fails visibly. The integration cannot recover a
terminated process or recreate the closed assignment. Reassignment remains an
operator-authorized coordination action.

## Replay, output, and stop behavior

For unchanged Herdr CLI evidence, invocation arguments, and reviewed baseline,
the JSON content is deterministic apart from upstream live facts such as agent
status. The tool stores nothing. It stops before producing JSON when it is run
outside Herdr, required environment values are absent, the CLI fails or times
out, the Herdr version differs from the reviewed baseline, the session or pane
is absent, Pi integration evidence is missing or stale, or required response
fields are malformed.

Errors are written to stderr without a traceback. Upstream stderr is normalized
and bounded. A baseline mismatch requires reviewing the new version's official
documentation and tests before changing the pinned constant.

## Validation

The tests use a fake CLI boundary and cover unmanaged and incomplete
environments, exact command selection, current and explicit panes, baseline
mismatch, missing and stopped sessions, malformed and additive output, unknown
agent state, absent or conflicting native session identity, stale Pi
integration, bounded CLI failure, stable JSON, and executable-wrapper behavior.
Run:

```bash
python3.14 -m pytest -q tests/adapters tests/integrations/herdr
python3.14 -m ruff check python tests
python3.14 -m ruff format --check python tests
python3.14 -m mypy python
```

A successful fake test does not prove that a real Herdr server is healthy. A
successful live inspection does not prove future process survival, intercom
connectivity, or recovery after deliberate pane/server termination.

## Official Herdr references

The implementation was reviewed against installed Herdr `0.9.1`. Each stable
operator page below is paired with the immutable source at tag `v0.9.1`.

- Agent guide: [operator page](https://herdr.dev/agent-guide.md) ·
  [v0.9.1 source](https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/distribution/agent-guide.md)
- Quick start: [operator page](https://herdr.dev/docs/quick-start/) ·
  [v0.9.1 source](https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/docs/next/website/src/content/docs/quick-start.mdx)
- Persistence and remote access:
  [operator page](https://herdr.dev/docs/persistence-remote/) ·
  [v0.9.1 source](https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/docs/next/website/src/content/docs/persistence-remote.mdx)
- Session state and restore:
  [operator page](https://herdr.dev/docs/session-state/) ·
  [v0.9.1 source](https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/docs/next/website/src/content/docs/session-state.mdx)
- CLI reference: [operator page](https://herdr.dev/docs/cli-reference/) ·
  [v0.9.1 source](https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/docs/next/website/src/content/docs/cli-reference.mdx)
- Integrations: [operator page](https://herdr.dev/docs/integrations/) ·
  [v0.9.1 source](https://raw.githubusercontent.com/herdrdev/herdr/v0.9.1/docs/next/website/src/content/docs/integrations.mdx)

## Owner routing and revisit criteria

This Project Koios-specific diagnostic belongs in the bootstrap harness while it
remains a candidate. Herdr itself owns server, client, pane, and native-agent
restore semantics. Pi owns its session format, and pi-intercom owns peer
communication. Revisit promotion only after independent reuse or another
concrete coordination failure demonstrates a stable broader contract.
