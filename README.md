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

Inside the managed pane, run `pi`. Before opening or coordinating repository
panes, verify that Pi inherited `HERDR_ENV=1`; pane context cannot be added to an
already-running process.

## Operating model

1. Read the [repository map](maps/repositories.md).
2. Use `pi-intercom` to discover or contact repository sessions.
3. Distinguish local intake/tool extraction from owner-repository execution.
4. Use one visible Herdr-hosted Pi session per active repository when work spans
   repositories.
5. Keep product implementation, validation, and Git history in the owning
   repository.
6. Record cross-repository architecture in the `projectkoios` mothership.

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
