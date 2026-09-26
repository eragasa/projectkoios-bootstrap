# Project Koios Bootstrap

A minimal coordination and tool-extraction entry point for Project Koios.
It coordinates work spanning owner repositories and turns bounded,
operator-provided source drops into reviewable reusable-tool candidates. It
owns no product code, product architecture, live workflow state, or persistent
orchestration system.

## Start

Local static intake analysis and single-repository candidate extraction can run
in an ordinary Pi session:

```bash
cd path/to/projectkoios-bootstrap
pi
```

For multi-repository execution, follow the upstream
[Herdr quick start](https://herdr.dev/docs/quick-start/) and start Pi from a
Herdr-managed pane:

```bash
cd path/to/projectkoios-bootstrap
herdr
```

Inside the managed pane, start the named coordination session with:

```bash
./scripts/start-coordinator
```

The launcher verifies that it inherited `HERDR_ENV=1`, starts Pi from this
repository, and supplies a bounded coordination startup prompt. Its behavior
lives in the tested
[coordinator startup candidate](docs/candidates/coordinator-startup.md).
After Pi starts, inspect the live session and its native Pi session evidence
with:

```bash
./scripts/inspect-herdr-session
```

The read-only
[Herdr session-continuity candidate](docs/candidates/herdr-session-continuity.md)
is pinned to the installed and reviewed Herdr `0.9.1` behavior. Detach the
Herdr **client** with `Ctrl-b`, then `q`; reattach with `herdr` or the exact
absolute reattach argv in the inspector output. Do not use pane,
tab, workspace, or server close commands as substitutes for client detach:
they end affected pane processes. See Herdr's official
[quick start](https://herdr.dev/docs/quick-start/),
[persistence guide](https://herdr.dev/docs/persistence-remote/),
[session-state guide](https://herdr.dev/docs/session-state/),
[CLI reference](https://herdr.dev/docs/cli-reference/), and
[integration guide](https://herdr.dev/docs/integrations/).
Additional Pi arguments are forwarded as explicit operator overrides, for
example `./scripts/start-coordinator --model sonnet:high`; options that change
Pi's mode may also change the interactive startup behavior. The launcher
rejects a caller-provided `--` terminator because it supplies that boundary
after its fixed options. Set `PROJECTKOIOS_COORDINATOR_NAME` to override the
default session name. Pane context cannot be added to an already-running Pi
process.

## Operating model

1. Read the [repository map](maps/repositories.md).
2. Use `pi-intercom` to discover or contact repository sessions.
3. Distinguish local intake/tool extraction from owner-repository execution.
4. Use one visible Herdr-hosted Pi session per active repository when work spans
   repositories.
5. Keep product implementation, validation, and Git history in the owning
   repository.
6. Record cross-repository architecture in the `projectkoios` mothership.

## Repository evidence tools

The repository provides bounded command-line helpers for recurring Git and
session-evidence operations:

```bash
./scripts/inspect-herdr-session
./scripts/inspect-project-preservation \
  /absolute/path/to/repository-a \
  /absolute/path/to/repository-b
./scripts/inventory-git-worktrees /absolute/path/to/repository
./scripts/summarize-project-worktrees \
  /absolute/path/to/repository-a \
  /absolute/path/to/repository-b
./scripts/migrate-default-branch --help
./scripts/verify-staged-snapshot \
  --repository "$PWD" \
  --python "$PWD/.venv/bin/python"
```

The preservation command emits deterministic path-level status, local remote
reachability, and preservation signals across an explicit repository set. Its
[documented candidate contract](docs/candidates/project-preservation-inspection.md)
does not interpret content or authorize cleanup. The inventory command emits
complete evidence for one repository. The summary command emits deterministic
factual counts across an explicit repository set; it does not assess deletion,
GitHub, or migration safety. Mutation decisions remain with the applicable
operation-specific preflight. The staged-snapshot command validates the exact
Git index rather than unrelated working-tree changes.

## Drop-to-tool workflow

Place local source material under:

```text
python/projectkoios/bootstrap/development/<topic>/intake/
```

Raw intake directories are ignored by Git. A drop is treated as observational
source material, not as a complete patch or code to merge. Pi first performs a
bounded static inspection, identifies reusable behavior, then implements the
smallest candidate with sanitized fixtures, deterministic tests, limitations,
and an explicit future owner. Product behavior is routed to its component
repository rather than retained here.

The bounded [Python intake analysis candidate](docs/candidates/python-intake-analysis.md)
provides the first reusable helper for this workflow. It inventories dropped
Python trees, extracts dependency and test facts, plans validation, and can
compare a declared patch relationship without importing or executing intake
code.

The validated
[offline artifact archive candidate](docs/candidates/offline-artifact-archive.md)
applies a repository-owned declarative selection policy, verifies staging
against exact Git evidence, creates a deterministic external tar bundle, and
recovers it into a new identity-checked directory. Source-specific selection,
licensing decisions, uploads, and storage management remain outside that tool.

The tracked harness candidates target Python 3.14 and have no runtime package
dependencies. Pytest, Ruff, and Mypy are optional development dependencies
declared in `pyproject.toml`; installing them is an explicit local environment
operation, not part of intake analysis. Run the complete test suite with:

```bash
python3.14 -m pytest -q
```

Pytest also collects the existing `unittest.TestCase` suites, so those tests can
be migrated incrementally.

See [AGENTS.md](AGENTS.md) for operating rules and the
[harness-incubation policy](docs/harness-incubation.md) for candidate
boundaries. Git, GitHub, and owner repositories remain the durable record.
