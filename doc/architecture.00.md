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
├── doc/               ← bootstrap architecture notes
├── architecture/      ← ADRs and durable decisions
├── maps/              ← authoritative workspace layout
├── agents/global/     ← committed shared harness config source
├── agents/local/      ← ignored repo-local harness overrides
├── archon/            ← Archon workflow and prompt source
├── opencode/          ← opencode rules and harness instructions
├── goose/             ← Goose agent rules and prompts
└── pi/                ← pi operator instructions
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
- `agents/global/<harness>/` for committed shared harness config
- `agents/local/<harness>/` for ignored repo-local overrides
- harness directories such as `pi/`, `opencode/`, `goose/`, and `archon/` for
  source docs, rules, prompts, and workflows owned by this bootstrap repo
- `maps/` for workspace truth

Install tooling should materialize the expected consumer locations, such as:
- `~/.pi/agent/AGENTS.md`
- `~/.pi/agent/SYSTEM.md`
- `~/.pi/agent/prompts/`
- `~/.pi/agent/skills/`

Tool-native paths in the repository root, including `.pi/`, `.opencode/`,
`.claude/`, `.agents/`, and `.archon/`, are not the long-term canonical source
model. Existing tracked files in those paths are temporary compatibility shims
until the relevant harness loaders can consume the shared source directly.

## Separation from projectkoios

Use this repo for meta-harness concerns only.
Use `projectkoios/` for product architecture, design records, and domain-level decisions.

If a document answers "how do we run the harnesses?", it belongs here.
If a document answers "how does the product work?", it belongs in `projectkoios/`.
