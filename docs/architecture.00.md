# `projectkoios-bootstrap` architecture

This document is the architecturer for the `projectkois-bootstrap` 

## Boundaries
1. `projectkoios` is the mothership repository
2. `projectkoios-bootstrap` is a meta-har
It separates harness concerns from the `projectkoios` mothership repository.

## Purpose

`projectkoios-bootstrap` owns the shared agent-operation layer for Project Koios:
- harness boundaries
- install/sync behavior
- shared context and maps
- shared bootstrap guidance for pi, Goose, and opencode
- repo-local config templates for pi, Goose, and opencode
- the canonical agent charter in `docs/agent-charter.md`

It does **not** own domain architecture for Project Koios product code.
That belongs in the `projectkoios` repository and its ADRs.

## Repository layout

```text
projectkoios-bootstrap/
├── docs/              ← documentation, architecture, and ADRs
│   ├── architecture/adr/ ← ADRs and durable decisions (single source of truth)
├── maps/              ← authoritative workspace layout
├── archon/            ← Archon workflows and prompts
├── opencode/          ← opencode rules and runtime harness
├── goose/             ← Goose agent rules and prompts
└── pi/                ← pi-specific harness config
```

## Harness split

| Harness | Role |
|---|---|
| `pi` | meta-harness operator; routes, orchestrates, and executes repo-scoped work; runs Archon workflows |
| `goose` | knowledge curation, ingestion, vault/bootstrap tasks |
| `opencode` | implementation, tests, validation, runtime debugging |
| `Archon` | orchestration and planning workflows |

## Shared-source strategy

Keep shared instructions in this repo and sync them outward:
- `projectkoios-bootstrap/pi/` for pi-specific instructions
- `projectkoios-bootstrap/goose/` for Goose-specific instructions
- `projectkoios-bootstrap/opencode/` for opencode-specific instructions
- `projectkoios-bootstrap/maps/` for workspace truth

Install tooling should materialize the expected consumer locations, such as:
- `~/.pi/agent/AGENTS.md`
- `~/.pi/agent/SYSTEM.md`
- `~/.pi/agent/prompts/`
- `~/.pi/agent/skills/`

## Separation from projectkoios

Use this repo for meta-harness concerns only.
Use `projectkoios/` for product architecture, design records, and domain-level decisions.

If a document answers "how do we run the harnesses?", it belongs here.
If a document answers "how does the product work?", it belongs in `projectkoios/`.
