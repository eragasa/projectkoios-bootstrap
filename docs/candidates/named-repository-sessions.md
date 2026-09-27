# Named repository sessions

## Lifecycle

**Candidate.** This is the first bounded Project Koios use. It remains local to
this bootstrap harness until independent reuse establishes a stable generic
contract.

## Purpose

Cross-repository messages need an unambiguous live destination. An unnamed Pi
process receives a runtime fallback alias that does not express either its
repository or task. This candidate makes identity explicit at tab creation
without adding a session registry or durable orchestration state.

`scripts/open-repository-session` accepts one absolute Git worktree root and one
lowercase kebab-case task slug. From a Herdr-managed coordinator pane, it asks
Herdr to create a labeled tab in the current workspace and then runs the
resolved Pi executable in its root pane as:

```text
pi --name <repository-directory-name>:<task-slug>
```

Example:

```bash
./scripts/open-repository-session \
  --repository-root /absolute/path/to/projectkoios-ingestion \
  --task domain-packages
```

The command emits deterministic JSON containing the canonical repository root,
task, session name, tab and root-pane IDs, and exact Herdr and Pi executables.
It does not send
a message. After the named session registers, coordination uses pi-intercom with
both its exact name and canonical cwd.

## Guard

The project extension `.pi/extensions/coordination-guard.js` blocks intercom
`send` and `ask` calls unless `cwd` is absolute, `to` has the exact
`<repository>:<task>` form, and the repository name agrees with the cwd's final
component. This also excludes unnamed runtime fallback aliases. The guard
blocks `openProjectPaneIfMissing`; that external path currently launches bare
Pi and would bypass deterministic naming. Other intercom actions are unchanged.

The guard is deliberately small. It is not an authorization service, task
tracker, repository registry, message filter, or replacement for pi-intercom.

## Safety and stop behavior

The launcher fails before tab creation when:

- it is not running under Herdr;
- required Herdr binary, pane, tab, workspace, or socket environment evidence
  is missing, or `HERDR_BIN_PATH` is relative;
- Pi cannot be resolved;
- the repository root is relative, missing, not a Git worktree, or lacks
  `AGENTS.md`; or
- the task slug or repository directory name cannot form the bounded session
  name.

It validates the tab and root-pane IDs returned by Herdr before invoking
`pane run`. Commands are passed as argument vectors without a shell. If
`pane run` fails after successful tab creation, the command reports the exact
new tab and pane and leaves them intact; it does not silently close or
repurpose them.

The launcher does not inspect other repositories, list sessions, send messages,
close panes, install dependencies, write runtime state, or contact a remote.

## Validation and limits

Python tests cover exact Herdr tab-create/pane-run arguments, deterministic
naming, focus behavior, environment and repository preflight, invalid tasks,
malformed tab evidence, bounded failures, and preservation of a tab after run
failure.
A Node test exercises the actual Pi extension policy and registration handler.
The pytest suite invokes that test when Node is available.

The command establishes the name passed to Pi; it does not prove that Pi loaded
successfully or that pi-intercom registered. The first scoped `list-cwd` and
subsequent `send` or `ask` provide that live evidence. Automatic spawning can be
reconsidered only after the installed integration supports and verifies an
explicit session name.
