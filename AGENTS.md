# AGENTS.md — Project Koios bootstrap

This repo is the shared config store for Project Koios. It does not own domain
architecture — that belongs in the `projectkoios` mothership repository.

## Harnesses

| Harness | Name | Role |
|---------|------|------|
| pi | pi | Agent runtime — executes Archon workflows |
| archon (archon.diy) | **Athena** | Architecture design, ADRs, planning |
| opencode | **Vulcan** | Code writing, tests, validation |
| goose | **Koios** | Knowledge management, vault ops |

## Harness configs

| Scope | Path | Contents |
|-------|------|----------|
| **Global (this repo)** | `agents/global/<harness>/` | Example configs, `.example` suffix, no secrets |
| **Local** | `~/.pi/` | Per-machine pi config (auth tokens, local overrides) |
| **Local** | `~/.archon/` | Per-machine archon config (worktree state, run history) |
| **Local** | `~/.opencode/` | Per-machine opencode config (accounts, sessions) |
| **Local** | `~/.local/share/goose/` | Per-machine goose runtime data |

Local configs are NEVER committed to this repo.

## Agent routing

- Route architecture / planning / ADRs to **archon (Athena)**
- Route implementation / tests / validation to **opencode (Vulcan)**
- Route research / vault / knowledge tasks to **goose (Koios)**
- Route operator / orchestration tasks to **pi**

## Artifact handoff

Handoff is the only way state moves between harnesses. Each harness writes
completion reports and artifacts to its own `handoffs/` directory for the
downstream harness to consume.

| From | To | Path |
|------|----|------|
| archon (Athena) | opencode (Vulcan) | `archon/handoffs/` — implementation-ready plans |
| opencode (Vulcan) | archon (Athena) | `opencode/handoffs/` — completion reports, architecture questions |
| goose (Koios) | archon (Athena) | `goose/handoffs/` — research summaries for planning |

Each harness starts with **zero session memory** — it reads only its current
artifact and the filesystem. No conversation history carries forward.

## Layout

```
projectkoios-bootstrap/
├── agents/global/       ← example configs per harness (.example suffix)
├── architecture/        ← ADRs and durable decisions (immutable archive)
├── doc/                 ← mutable docs (system overview, future ADRs)
├── maps/                ← workspace topology (repos, packages, vault)
├── src/python/          ← Python CLI package (bootstrap tooling)
├── scripts/             ← CLI wrappers
├── archon/              ← Archon workflows and prompts
├── opencode/            ← opencode rules and runtime harness
├── goose/               ← Goose agent rules and prompts
├── pi/                  ← pi-specific harness config
├── AGENTS.md            ← this file
└── pyproject.toml       ← Python project metadata
```

## Bootstrapping

```bash
projectkoios bootstrap init     # copy agents/global/*.example → ~/.<harness>/
projectkoios bootstrap install  # symlink global configs into place
```

## Mothership

`~/projectkoios/` is the Obsidian vault. Athena writes architecture docs there.
This repo is the config store only.
