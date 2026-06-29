# Project Koios bootstrap architecture

This document is the bootstrap-specific architecture for `projectkoios-bootstrap`.
It separates harness concerns from the `projectkoios` mothership repository.

## Purpose

`projectkoios-bootstrap` owns the shared agent-operation layer for Project Koios:
- harness boundaries
- install/sync behavior
- shared context and maps
- repo-local config for pi, Goose, and opencode

It does **not** own domain architecture for Project Koios product code.
That belongs in the `projectkoios` repository and its ADRs.

## Repository layout

```text
projectkoios-bootstrap/
├── docs/              ← bootstrap architecture notes
├── architecture/      ← ADRs and durable decisions
├── maps/              ← authoritative workspace layout
├── archon/            ← Archon workflows and prompts
├── opencode/          ← opencode rules and runtime harness
├── goose/             ← Goose agent rules and prompts
└── pi/                ← pi-specific harness config
```

## Harness split

| Harness | Role |
|---|---|
| `pi` | operator interface; runs Archon workflows |
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
