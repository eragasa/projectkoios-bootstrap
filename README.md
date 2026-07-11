# projectkoios-bootstrap

Shared harness config store for building and operating Project Koios.

## Document-State Orchestration

Canonical document-domain ownership lives in `docs/agents/agent-charter.md`.
The repository documents and their statuses are the durable workflow state:
agents initialize from that state, run bounded transformations, and write back a
new state.

This repo stores harness config, bootstrap helpers, and shared instructions.
The current operator path and tool-specific details belong in the charter and
repo-local harness docs.

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
projectkoios bootstrap validate-harnesses --root .
projectkoios harnesses start     # create tmux koios session
projectkoios harnesses show      # list session/window state
projectkoios harnesses connect   # focus a workspace window
projectkoios harnesses stop      # kill koios session
```

## Workspace

Read `maps/repositories.md`, `maps/packages.md`, and `maps/vault_paths.md`
before touching any code. All component repos are siblings under `~/repos/`.

Persistent per-agent workspace state is governed by the accepted ADR `docs/adr/adr.20260704.162218_canonical-workspace-state-next-action-protocol.md` and summarized in `docs/policies/workspace-layout.md`. Workspace `state.md` and `active.md` files are control surfaces, not replacements for authoritative repository documents.

## Local Generated State

`graphify-out/` is a generated local database used by Graphify and is ignored by
git. Fresh clones will not receive it. Existing clones may still have stale local
database files after a pull; if needed, clean them with:

```bash
git clean -fdX graphify-out/
```

You can also delete `graphify-out/` manually. Graphify will regenerate it when
needed.

TypeScript/Node package artifacts such as `node_modules/`, `dist/`,
`coverage/`, and `.vite/` are generated local state and are ignored by git at
both repo-root safety level and, where useful, package-local level. Do not
commit these directories. If a package install or build recreates them, clean
with targeted removal or ignored-file cleanup before staging:

```bash
rm -rf src/typescript/projectkoios/ui/operator-console/node_modules \
       src/typescript/projectkoios/ui/operator-console/dist \
       src/typescript/projectkoios/ui/operator-console/coverage
# or, from repo root, inspect ignored generated files before cleaning:
git status --ignored --short src/typescript/projectkoios/ui/operator-console
```

Package lockfiles, package manifests, source files, fixtures, and tests are not
generated local state and may be committed when the implementation report
explains the package-local lockfile decision.

`.archon/mcp/` is local Archon MCP runtime config and is ignored by git.
`.archon/mcp/*.json` files may contain machine-specific notification or server
settings and must not be committed. Repo-owned Archon assets live in
`archon/workflows/`, `archon/prompts/`, `archon/skills/`, and
`agents/global/archon/*.example`.

## Archon Health Checks

```bash
archon doctor
archon validate workflows
archon workflow runs --json --limit 5
archon isolation list
```

`archon doctor` should end with `All checks passed.` `archon validate workflows`
should report zero workflow errors; warnings from bundled marketplace workflows
are acceptable only when repo-local workflows are `ok`.

Inspect `archon workflow runs --json --limit 5` for unexpected active runs.
During this PIV loop, the current run may be `running`. Inspect
`archon isolation list` for unexpected leftover environments. During this PIV
loop, the current task worktree may appear.

Provider smoke tests are manual operator checks. Do not add them to automated
tests unless a future non-secret fixture exists.

## Architecture

- Bootstrap architecture: `docs/architecture/architecture.00.md`
- Repo projections: `docs/architecture/architecture.repo-projections.md`
- Active ADRs: `docs/adr/`
- Historic ADR archive: `docs/archive/architecture/adr/adr.20260628.000000_three-harness-meta-harness.md`
