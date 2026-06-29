# projectkoios-bootstrap

Shared harness config store for building and operating Project Koios.

## Harnesses

| Harness | Name | Tool | Domain |
|---------|------|------|--------|
| pi | pi | pi | Operator interface; runs Archon workflows |
| archon | **Athena** | [Archon](https://archon.diy) | Architecture decisions, ADRs, planning, design review |
| opencode | **Vulcan** | opencode | Code implementation, tests, validation, runtime sessions |
| goose | **Koios** | [Goose](https://goose-docs.ai) | Knowledge curation, vault ops, source ingestion, UI bootstrap |

## Current operator path

Until Archon can run under `pi` directly, use Codex as the temporary
operator/access layer for Archon workflows. In this mode, Codex is not a
replacement identity for `pi`; it is the bridge used to start, inspect,
approve, reject, resume, or cancel Archon/Athena runs and to read or write
handoff artifacts.

Target state: `pi` owns the operator interface again once it can run Archon
reliably.

## Prerequisites

```bash
brew install python uv
# opencode: https://opencode.ai
# Archon CLI:
mkdir -p ~/.local/bin
curl -fsSL https://github.com/coleam00/Archon/releases/latest/download/archon-darwin-arm64 -o ~/.local/bin/archon
chmod +x ~/.local/bin/archon
# Goose: https://goose-docs.ai/docs/quickstart
```

## Commands

### koios — tmux session and install

```bash
cd ~/repos/projectkoios-bootstrap

# Start or reuse the koios tmux session and four windows
./scripts/koios harnesses start

# Show koios workspace state
./scripts/koios harnesses show

# Focus one workspace window
./scripts/koios harnesses connect archon
./scripts/koios harnesses connect opencode
./scripts/koios harnesses connect goose
./scripts/koios harnesses connect scratch

# Sync pi harness config into ~/pi/agent/ → ~/.pi/agent/
./scripts/koios install

# Stop the koios tmux session
./scripts/koios harnesses stop
```

### projectkoios — Python CLI

```bash
# After pip install -e .
projectkoios bootstrap init      # copy agents/global/*.example → ~/.<harness>/
projectkoios bootstrap install   # symlink global configs into place
projectkoios harnesses start     # create tmux koios session
projectkoios harnesses show      # list session/window state
projectkoios harnesses connect   # focus a workspace window
projectkoios harnesses stop      # kill koios session
```

## Workspace

Read `maps/repositories.md`, `maps/packages.md`, and `maps/vault_paths.md`
before touching any code. All component repos are siblings under `~/repos/`.

## Local Generated State

`graphify-out/` is a generated local database used by Graphify and is ignored by
git. Fresh clones will not receive it. Existing clones may still have stale local
database files after a pull; if needed, clean them with:

```bash
git clean -fdX graphify-out/
```

You can also delete `graphify-out/` manually. Graphify will regenerate it when
needed.

## Architecture

- Bootstrap architecture: `doc/architecture.00.md`
- ADR archive: `architecture/adr.20260628.md`
