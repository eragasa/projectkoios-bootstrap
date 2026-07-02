# ADR 20260629.000000: Bootstrap plan execution

## Status

historic

## Context

The bootstrap plan (BOOTSTRAP_PLAN.md) called for restructuring
`projectkoios-bootstrap` from ad-hoc per-harness configs into a standardized
layout with example templates, a Python CLI, and a rewritten root manifest.

## Decision

See the original ADR text below for the historical decision.

## Consequences

- New developers run `projectkoios bootstrap init` to bootstrap local harness
  configs from the global templates.
- `projectkoios bootstrap install` replaces direct `scripts/koios install`
  usage for Hermes config sync.
- The `scripts/koios` bash script is now a thin Python wrapper. The old bash
  implementation with inline tmux management has been replaced by the Python
  `harnesses` command.
- Future ADRs go in `docs/architecture/adr/`.
- The BOOTSTRAP_PLAN.md open items are all resolved. The file can be removed
  or kept for reference.

## architecture-spec

### agents/global/ — example config store

Created `agents/global/<harness>/` with `.example`-suffixed template configs for
all four harnesses. Each mirrors the live config structure but contains no
secrets (placeholder values only).

| Harness | Files |
|---------|-------|
| Hermes | AGENTS.md.example, settings.json.example, models.json.example, trust.json.example, auth.json.example |
| archon | config.yaml.example, skills/ |
| opencode | opencode.json.example, AGENTS.md.example, rules/, checklists/ |
| goose | AGENT.md.example, prompts/, .mcp.json.example |

### Python CLI package

Added `src/python/projectkoios/bootstrap/` with three commands:

| Command | Function |
|---------|----------|
| `bootstrap init` | Copy `agents/global/*.example` → `~/.<harness>/` |
| `bootstrap install` | Symlink Hermes config into `~/pi/agent/` → `~/.pi/agent/` |
| `harnesses {start,show,connect,stop}` | Tmux koios session management |

Entry point: `projectkoios = projectkoios.bootstrap.cli:main`
Wrapper: `scripts/koios` delegates to `python3 -m projectkoios.bootstrap`

### pyproject.toml

Standard Python project metadata with `setuptools` build backend. The
`[project.scripts]` entry point makes `projectkoios` available after
`pip install -e .`.

### doc/ — mutable docs moved from docs/

Created `doc/` (later renamed to `docs/`) with `adr/` subdirectory for future ADRs. Moved
`docs/architecture.00.md` → `doc/architecture.00.md`. Updated the deprecation
pointer in `docs/architecture/harness-boundaries.md`.

### Root AGENTS.md — rewritten as bootstrap manifest

Replaced the graphify-only `AGENTS.md` with a full bootstrap manifest
containing: harness name table, config scope table (global vs local), agent
routing rules, artifact handoff table with fresh-context contract, directory
layout, and bootstrapping commands.

### Handoff convention

Each harness writes completion reports to its own `handoffs/` directory (now
archived at `docs/archive/handoffs/`) for the downstream harness to consume.
All agents start with zero session memory — only the current artifact and
filesystem are loaded.

## acceptance-criteria

Not separately stated in the original archive ADR.

## implementation-brief

### agents/global/ — example config store

Created `agents/global/<harness>/` with `.example`-suffixed template configs for
all four harnesses. Each mirrors the live config structure but contains no
secrets (placeholder values only).

| Harness | Files |
|---------|-------|
| Hermes | AGENTS.md.example, settings.json.example, models.json.example, trust.json.example, auth.json.example |
| archon | config.yaml.example, skills/ |
| opencode | opencode.json.example, AGENTS.md.example, rules/, checklists/ |
| goose | AGENT.md.example, prompts/, .mcp.json.example |

### Python CLI package

Added `src/python/projectkoios/bootstrap/` with three commands:

| Command | Function |
|---------|----------|
| `bootstrap init` | Copy `agents/global/*.example` → `~/.<harness>/` |
| `bootstrap install` | Symlink Hermes config into `~/pi/agent/` → `~/.pi/agent/` |
| `harnesses {start,show,connect,stop}` | Tmux koios session management |

Entry point: `projectkoios = projectkoios.bootstrap.cli:main`
Wrapper: `scripts/koios` delegates to `python3 -m projectkoios.bootstrap`

### pyproject.toml

Standard Python project metadata with `setuptools` build backend. The
`[project.scripts]` entry point makes `projectkoios` available after
`pip install -e .`.

### doc/ — mutable docs moved from docs/

Created `doc/` (later renamed to `docs/`) with `adr/` subdirectory for future ADRs. Moved
`docs/architecture.00.md` → `doc/architecture.00.md`. Updated the deprecation
pointer in `docs/architecture/harness-boundaries.md`.

### Root AGENTS.md — rewritten as bootstrap manifest

Replaced the graphify-only `AGENTS.md` with a full bootstrap manifest
containing: harness name table, config scope table (global vs local), agent
routing rules, artifact handoff table with fresh-context contract, directory
layout, and bootstrapping commands.

### Handoff convention

Each harness writes completion reports to its own `handoffs/` directory (now
archived at `docs/archive/handoffs/`) for the downstream harness to consume.
All agents start with zero session memory — only the current artifact and
filesystem are loaded.

## resolved-open-questions

None stated.

## non-goals

None stated.

## validation-expectations

Not separately stated in the original archive ADR.

## routing

- Owner: Athena
- Next phase: completed
- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260629.000000: Bootstrap plan execution

## Status

historic

## Context

The bootstrap plan (BOOTSTRAP_PLAN.md) called for restructuring
`projectkoios-bootstrap` from ad-hoc per-harness configs into a standardized
layout with example templates, a Python CLI, and a rewritten root manifest.

## Completed items

### agents/global/ — example config store

Created `agents/global/<harness>/` with `.example`-suffixed template configs for
all four harnesses. Each mirrors the live config structure but contains no
secrets (placeholder values only).

| Harness | Files |
|---------|-------|
| Hermes | AGENTS.md.example, settings.json.example, models.json.example, trust.json.example, auth.json.example |
| archon | config.yaml.example, skills/ |
| opencode | opencode.json.example, AGENTS.md.example, rules/, checklists/ |
| goose | AGENT.md.example, prompts/, .mcp.json.example |

### Python CLI package

Added `src/python/projectkoios/bootstrap/` with three commands:

| Command | Function |
|---------|----------|
| `bootstrap init` | Copy `agents/global/*.example` → `~/.<harness>/` |
| `bootstrap install` | Symlink Hermes config into `~/pi/agent/` → `~/.pi/agent/` |
| `harnesses {start,show,connect,stop}` | Tmux koios session management |

Entry point: `projectkoios = projectkoios.bootstrap.cli:main`
Wrapper: `scripts/koios` delegates to `python3 -m projectkoios.bootstrap`

### pyproject.toml

Standard Python project metadata with `setuptools` build backend. The
`[project.scripts]` entry point makes `projectkoios` available after
`pip install -e .`.

### doc/ — mutable docs moved from docs/

Created `doc/` (later renamed to `docs/`) with `adr/` subdirectory for future ADRs. Moved
`docs/architecture.00.md` → `doc/architecture.00.md`. Updated the deprecation
pointer in `docs/architecture/harness-boundaries.md`.

### Root AGENTS.md — rewritten as bootstrap manifest

Replaced the graphify-only `AGENTS.md` with a full bootstrap manifest
containing: harness name table, config scope table (global vs local), agent
routing rules, artifact handoff table with fresh-context contract, directory
layout, and bootstrapping commands.

### Handoff convention

Each harness writes completion reports to its own `handoffs/` directory (now
archived at `docs/archive/handoffs/`) for the downstream harness to consume.
All agents start with zero session memory — only the current artifact and
filesystem are loaded.

## Deviations from plan

- **`agents/global/opencode/rules/` and `agents/global/opencode/checklists/`**
  created as empty directories rather than populated with `.example` files,
  since the rules live in `opencode/rules/` and are referenced by the
  `opencode/AGENTS.md` directly.
- **`agents/global/archon/skills/`** created as an empty directory. The actual
  Archon skills live in `archon/skills/` and are not example templates.
- **`agents/global/goose/prompts/`** created as an empty directory. The actual
  goose prompts live in `goose/prompts/`.
- **Python package deprecation note** from `adr.20260628.000000_three-harness-meta-harness.md` (which said the
  Python directory "becomes unused") is now outdated — the package is active.

## Consequences

- New developers run `projectkoios bootstrap init` to bootstrap local harness
  configs from the global templates.
- `projectkoios bootstrap install` replaces direct `scripts/koios install`
  usage for Hermes config sync.
- The `scripts/koios` bash script is now a thin Python wrapper. The old bash
  implementation with inline tmux management has been replaced by the Python
  `harnesses` command.
- Future ADRs go in `docs/architecture/adr/`.
- The BOOTSTRAP_PLAN.md open items are all resolved. The file can be removed
  or kept for reference.
