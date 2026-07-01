---
name: projectkoios
description: |
  Use when: You are in the projectkoios-bootstrap repository and need to understand
    the project structure, role model, or sandbox message delivery boundaries.
  Triggers: "what is this repo", "project koios", "projectkoios", "how do I send this",
    "who owns what", "which harness", "meta-harness".
  Capability: Codex-facing entrypoint for the Project Koios bootstrap repository.
    Explains scope, roles, sandbox message delivery, and available repo-local skills.
  NOT for: domain architecture decisions (those belong in the mothership vault at
    ~/projectkoios/), or for editing code directly (use Vulcan for that).
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md.
---
# Project Koios bootstrap

## What this repo is

This is the shared config and instruction store for Project Koios.
It manages:
- shared agent config examples
- bootstrap/install helpers
- workflow and harness instructions
- repo-local docs about the Koios bootstrap layer

It does **not** own product/domain architecture. That belongs in the
`projectkoios` mothership repository (Obsidian vault at `~/projectkoios/`).

See [`AGENTS.md`](../../AGENTS.md) and [`docs/meta-harness.md`](../../docs/meta-harness.md)
for the full framework detail.

## Role model

Project Koios separates specification, implementation, and knowledge capture
into distinct agent harness roles:

| Harness | Name | Role |
|---------|------|------|
| `pi` | **Hermes** | Meta-harness — orchestration, operations, handoff coordination |
| `archon` | **Athena** | Architecture design, ADRs, planning |
| `opencode` | **Vulcan** | Code writing, tests, validation |
| `goose` | **Koios** | Knowledge management, vault ops |

## Codex boundary

Codex is a **delegated access/operator layer** used when direct `pi` ownership
is unavailable. It may:
- invoke Archon workflows
- relay Athena artifacts into this repository
- report filesystem, git, validation, and workflow state to Hermes

Codex **does not** become `pi`, `archon`, `opencode`, or `goose`. Codex-authored
draft code or Markdown is not accepted architecture.

## Available repo-local skills

- [archon](../archon/SKILL.md) — run Archon workflows, create workflows/commands
- [manage-run](../manage-run/SKILL.md) — inspect, monitor, start, approve, or
  control Archon workflow runs
- [deep-interview](./deep-interview/SKILL.md) — recursive multi-turn interviews,
  assessment axes, and question-stack maintenance

## Koios operating notes

When acting in the Koios knowledge role:
- prefer Graphify first for broad repository context when `graphify-out/graph.json`
  exists
- treat code repositories and the mothership Obsidian vault as distinct source
  surfaces with different authority and freshness properties
- bound scope before broad ingestion; do not scan whole repos or vault areas
  without a task-level reason
- preserve provenance for design and workflow proposals, especially when a
  request is informed by archived artifacts, vault notes, or external source
  material such as PDFs
- prepare proposal context for Athena, but do not claim Athena's architecture
  authority

## Sandbox message delivery guidance

Sending work means putting a message in the recipient harness sandbox.

| Task | Send message to |
|------|----------|
| Architecture, planning, ADRs | **Athena** (archon) |
| Implementation, tests, bug fixes | **Vulcan** (opencode) |
| Orchestration, run control, operations | **Hermes** (pi) |
| Knowledge capture, vault ops | **Koios** (goose) |
| Delegated access, relaying artifacts | **Codex** (you) |

## What not to do here

- Do not commit machine-local secrets, tokens, or credentials.
- Do not make domain architecture decisions — those go in the mothership vault.
- Do not edit `Archon` workflow definitions, Python CLI behavior, or bootstrap
  install commands unless sent through an accepted ADR-backed recipient sandbox.
