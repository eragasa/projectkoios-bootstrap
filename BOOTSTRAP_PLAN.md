# Bootstrap Plan — Project Koios

## Harnesses

| Current | Future Name | Role |
|---------|-------------|------|
| pi | pi | Agent runtime — executes Archon workflows |
| archon (archon.diy) | **Athena** | Architecture design, ADRs, planning |
| opencode | **Vulcan** | Code writing, tests, validation |
| goose (→ graphifyy) | **Koios** | Knowledge management, vault ops |

## Mothership

`~/projectkoios/` is the Obsidian vault. Athena writes architecture docs there. This repo (`projectkoios-bootstrap`) is the config store — not the mothership.

## Directory Restructure

```
projectkoios-bootstrap/
├── agents/global/             ← example/template configs (committed, no secrets)
│   ├── pi/
│   │   ├── AGENTS.md.example
│   │   ├── settings.json.example
│   │   ├── models.json.example
│   │   ├── trust.json.example
│   │   └── auth.json.example
│   ├── archon/
│   │   ├── config.yaml.example
│   │   └── skills/
│   ├── opencode/
│   │   ├── opencode.json.example
│   │   ├── rules/
│   │   └── checklists/
│   └── goose/
│       ├── AGENT.md
│       ├── prompts/
│       └── .mcp.json.example
├── src/python/projectkoios/bootstrap/   ← Python CLI package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                  ← entrypoint
│   ├── commands/
│   │   ├── init.py             ← copy agents/global/ → ~/.<harness>/
│   │   ├── install.py          ← symlink global configs
│   │   └── harnesses.py        ← tmux session management
│   └── models.py
├── architecture/               ← immutable ADR archive (stays)
│   ├── adr.20260628.md
│   ├── adr.20260629.md
│   └── harness-boundaries.md
├── doc/                        ← mutable docs
│   ├── adr/                    ← future ADRs go here
│   └── architecture.00.md      ← system overview
├── maps/                       ← workspace topology (stays)
├── scripts/
│   ├── koios                   ← becomes thin wrapper: `python -m projectkoios.bootstrap "$@"`
│   └── README.md
├── AGENTS.md                   ← rewritten bootstrap manifest
├── README.md
└── pyproject.toml              ← Python project metadata
```

## Global vs Local Config

| Scope | Path | Contents |
|-------|------|----------|
| **Global** (this repo) | `agents/global/<harness>/` | Example configs, `.example` suffix, no secrets |
| **Local** | `~/.pi/` | Per-machine pi config (auth tokens, local overrides) |
| **Local** | `~/.archon/` | Per-machine archon config (worktree state, run history) |
| **Local** | `~/.opencode/` | Per-machine opencode config (accounts, sessions) |
| **Local** | `~/.local/share/goose/` | Per-machine goose runtime data |

Local configs are NEVER committed to this repo.

## CLI Commands (Python)

```bash
projectkoios bootstrap init          # copy agents/global/*.example → ~/.<harness>/
projectkoios bootstrap install       # symlink global configs into place
projectkoios harnesses start         # create tmux koios session + 4 windows
projectkoios harnesses show          # list session/window state
projectkoios harnesses connect [name] # focus a workspace window
projectkoios harnesses stop          # kill koios session
```

Scripts/koios becomes: `python -m projectkoios.bootstrap "$@"`

## AGENTS.md Outline

1. Repo purpose — config store for four harnesses
2. Harness table — pi / Athena / Vulcan / Koios
3. Global vs local — agents/global/ = examples, ~/.<name>/ = machine-local
4. Layout reference — agents/, architecture/, doc/, maps/, scripts/, src/
5. Bootstrapping — projectkoios bootstrap init/install
6. Agent routing — which harness for which task
7. Mothership — ~/projectkoios/ is the Obsidian vault

## Security

- `agents/global/*/auth.json.example` — template only, no real tokens
- Real `auth.json` lives only in `~/.pi/agent/` — never committed
- `koios install` explicitly skips auth.json (as it already does)

## Open Items

- [ ] `src/python/projectkoios/bootstrap/` — create package
- [ ] `scripts/koios` — convert to Python CLI wrapper
- [ ] `agents/global/` — create with current configs as `.example`
- [ ] Move existing configs from root dot-dirs to `agents/global/`
- [ ] `AGENTS.md` — full rewrite
- [ ] `README.md` — update
- [ ] `pyproject.toml` — add
- [ ] `doc/` — create, move docs/architecture.00.md there
- [ ] ADRs written by Athena go in `doc/adr/`
