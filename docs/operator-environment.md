# Project Koios operator environment

## Purpose

This guide describes how to enter the Project Koios multi-repository
coordination environment. It configures no credentials, installs no repository
software, and stores no session state. Herdr owns terminal panes, Pi owns agent
sessions and tools, and GitHub plus the owning repositories remain the durable
record.

For generic Herdr installation and operation, use the upstream documentation:

- [Install Herdr](https://herdr.dev/docs/install/)
- [Herdr quick start](https://herdr.dev/docs/quick-start/)

## Prerequisites

- a current stable Herdr release; pane opening requires Herdr 0.7.5 or newer;
- Pi with the `pi-intercom` extension available; and
- sibling Project Koios repositories matching `../maps/repositories.md`.

The optional issue-inventory candidate additionally requires Python 3 and an
authenticated GitHub CLI with GraphQL API support. The candidate performs its
own preflight and reports authentication or API failures rather than treating
them as zero issues.

On a Homebrew system, Herdr is provided by the official `herdr` formula. This
repository does not install, update, pin, or start Herdr.

Verify the executable before entering the environment:

```bash
herdr --version
```

## Start the coordinator

From the parent workspace, enter the bootstrap repository and launch or attach
to Herdr:

```bash
cd projectkoios-bootstrap
herdr
```

Start Pi from a Herdr-managed shell pane:

```bash
pi
```

The order matters. A Pi process started outside Herdr does not inherit the pane
identity needed to open or control visible project panes. Installing or starting
Herdr later does not retrofit that process; start a new Pi session inside Herdr.

Optionally name the coordination session:

```text
/alias bootstrap
```

## Verify pane context

Before asking the coordinator to open repository sessions, verify from the
managed shell that Herdr supplied its environment:

```bash
test "${HERDR_ENV:-}" = 1
printf '%s\n' "$HERDR_WORKSPACE_ID" "$HERDR_TAB_ID" "$HERDR_PANE_ID"
```

The identifiers are ephemeral runtime values. Do not copy them into GitHub
issues, repository documents, manifests, or handoff files.

Inside Pi, ask it to list live sessions before opening new ones. Reuse a live
session in the correct repository rather than creating a duplicate writer.

## Repository panes

Use one visible Pi session per active repository for long-lived
multi-repository work. The bootstrap session coordinates; it does not become
the implementation owner for component repositories.

Each assignment must state:

1. repository and working directory;
2. objective and owning issue or decision;
3. constraints and authority boundaries;
4. expected output;
5. validation requirements; and
6. stop conditions, including commit and push authorization.

Use an isolated Git worktree when the normal owner checkout is dirty or
divergent. Keep one writer per checkout or worktree. Bounded delegated work may
use Pi subagents with an explicit `cwd` when the operator has authorized
delegation, but durable long-running repository work belongs in visible panes.

## Durable recovery

Do not depend on a pane transcript for recovery. Resume from:

- the owning GitHub issue and its decision/progress comments;
- owner-repository documents and contracts;
- Git revisions, branches, and inspected worktree state; and
- content-identified private evidence in managed `.koios` storage when the
  owning policy permits it.

Do not add transcripts, pane identifiers, persistent queues, checkpoints,
generated handoffs, credentials, or replicated task databases to this
repository.

Before resuming a dirty worktree, inspect its status and compare it with the
recorded review evidence. Never reset, stash, rebase, overwrite, or force-push
active work merely to synchronize a session.

## Failure and fallback

If pane creation reports that Herdr is missing, install a current stable release
using the upstream instructions and start a new Pi session inside Herdr.

If pane creation reports that `HERDR_PANE_ID` is missing, the current Pi process
was started outside Herdr. Stop multi-repository execution and restart it from a
managed pane.

If Herdr cannot be used, do not silently substitute a terminal launcher,
subagent, or cross-repository writer. Report the exact failure and ask the
operator either to restore Herdr or to authorize a bounded fallback. A fallback
does not relax repository ownership, one-writer, validation, commit, or push
controls.
