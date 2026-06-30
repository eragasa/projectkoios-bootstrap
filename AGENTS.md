# AGENTS.md — Project Koios bootstrap

This repo is the shared config store for Project Koios.
It does not own domain architecture; that belongs in the `projectkoios` mothership repository.

## Contents

- [What this repo is for](#what-this-repo-is-for)
- [Harnesses](#harnesses)
- [Athena](#athena)
- [Meta-harness](#meta-harness)
- [High-leverage state](#high-leverage-state)
- [Directions for all harnesses](#directions-for-all-harnesses)
- [Directions for Hermes (pi)](#directions-for-hermes-pi)
- [Directions for Athena (archon)](#directions-for-athena-archon)
- [Directions for Vulcan (opencode)](#directions-for-vulcan-opencode)
- [Harness configs](#harness-configs)
- [ADR file convention](#adr-file-convention)
- [Secrets and safety](#secrets-and-safety)
- [Bootstrapping](#bootstrapping)
- [Layout](#layout)
- [Mothership](#mothership)

## What this repo is for

Use this repo to manage:
- shared agent config examples
- bootstrap/install helpers
- workflow and harness instructions
- repo-local docs about the Koios bootstrap layer

Do not use this repo for:
- product/domain architecture decisions
- machine-specific secrets or local runtime state
- long-lived project knowledge that belongs in the Obsidian vault

## Harnesses

| Harness | Name | Role |
|---------|------|------|
| pi | **Hermes** | Meta-harness — orchestration, operations, handoff coordination |
| archon (archon.diy) | **Athena** | Architecture design, ADRs, planning |
| opencode | **Vulcan** | Code writing, tests, validation |
| goose | **Koios** | Knowledge management, vault ops |

## Athena

Athena is the spec and architecture system for Project Koios. It comprises
two layers that operate as one role:
- **Codex** is a delegated access/operator layer used when direct pi
  ownership is unavailable; it may invoke Archon workflows and relay
  artifacts, but it is not `pi`.
- **Archon** runs the workflow — producing architecture specs, acceptance
  criteria, and implementation briefs.

Athena operates as a single spec agent with a unified handoff boundary.

### Athena workflow naming

Archon workflows named with the prefix `athena_` are Athena-owned role
transitions. The name shape is:

```text
athena_<action-in-this-mode>
```

Only Athena may run these workflows in the harness sense: their outputs are
Athena artifacts, and they must not be treated as Hermes routing decisions,
Vulcan implementation, or Koios knowledge capture. A delegated operator such as
Codex or Hermes may invoke the CLI when relaying access, but the artifact must
preserve that it was produced by Athena and mediated by the delegated operator.

## Meta-harness

This repo operates a role-based meta-harness that separates specification, implementation, and knowledge capture into distinct agent roles. See `docs/meta-harness.md` for the full framework detail on skill model, disagreement handling, completion gates, escalation rules, and anti-patterns.

### Artifact model

Agents communicate through typed artifacts. An artifact must be explicit enough that another agent can consume it without hidden context.

| Artifact | Owner | Meaning |
|---|---|---|
| `user-request` | user | Original task or instruction |
| `architecture-spec` | spec agent (Athena) | Bounded architecture decision |
| `acceptance-criteria` | spec agent (Athena) | Inspectable criteria for completion |
| `implementation-brief` | spec agent (Athena) | Concrete instructions for implementation |
| `implementation-plan` | code agent (Vulcan) | Planned file-level changes |
| `patch` | code agent (Vulcan) | Repository modification |
| `test-results` | code agent (Vulcan) | Validation output |
| `implementation-report` | code agent (Vulcan) | Summary of what changed |
| `deviation-report` | code agent (Vulcan) | Mismatch between spec and reality |
| `knowledge-note` | knowledge agent (Koios) | Durable note from validated artifacts |
| `provenance-index` | knowledge agent (Koios) | Mapping from claims to sources |
Architecture/specification artifacts are stored as ADRs under
`docs/architecture/adr/`. Historical harness handoffs are archived under
`docs/archive/handoffs/` and should be treated as provenance, not the current
active artifact surface.

## High-leverage state

At session start, agents should report not only pending work, but the
highest-leverage next state to move toward. Base this recommendation on live
filesystem, git, Graphify, ADR, and Archon run state.

Default recommendations:
- If the tree is dirty, stabilize or explain the working tree before starting
  new work.
- If Archon has `running`, `paused`, or orphaned detached runs, inspect and
  resolve those before relying on new workflow output.
- If the tree is clean, Archon has no active runs, and Draft ADRs exist, the
  highest-leverage next state is usually Hermes review or Athena promotion of
  those Draft ADRs before Vulcan implementation.
- If accepted ADR intent and code behavior disagree, report the mismatch rather
  than normalizing it silently.
- If Graphify warns that its graph is stale or structurally outdated, treat the
  graph as discovery only and prefer source files for authoritative claims.

## Directions for all harnesses

- Read only the current artifact and filesystem state; do not rely on chat history.
- For codebase, architecture, file-relationship, and impact questions, use
  `graphify` first.
- At new session start, all harnesses should use `graphify` before manual file
  reading when `graphify-out/graph.json` exists. Prefer `graphify query`,
  `graphify path`, or `graphify explain` to establish context, then read only
  the specific files or lines needed to verify or patch.
 - At session end, after meaningful repository file changes, run
   `graphify update .` (AST-only, no LLM needed) so the next session starts from
   current indexed state.
- Treat Graphify as the cheapest broad-context read path. Do not manually scan
  large document/code surfaces before trying Graphify, unless Graphify is
  missing, stale in a way that blocks the task, or lacks the exact detail needed.
- If `graphify-out/graph.json` exists, prefer `graphify query`,
  `graphify path`, or `graphify explain` before manual grepping or browsing.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review.
- Keep local secrets out of git.

## Directions for Hermes (pi)

Use Hermes (pi) for orchestration and direct operations:
- run commands, edit files, inspect repo and filesystem state
- manage harness configs, bootstrap setup, repo maintenance
- start, inspect, approve, reject, resume, or cancel Archon workflow runs
- read and write ADRs and archived/provenance artifacts

Run Archon workflows in the foreground by default. Use detached/background
Archon runs only when explicitly needed, and treat orphaned `running` rows as
local runtime state to inspect and clean up before relying on their output.

### Session protocol for Hermes

At session start:
- use Graphify first for broad repo context before reading archived handoffs,
  ADRs, or source files manually
- check `docs/archive/handoffs/` only as provenance: archived `Status: active`
  headers are not authoritative current work by themselves
- prefer current ADRs, current handoff locations, git state, and filesystem
  state over deprecated archived handoff instructions
- check `docs/architecture/adr/` for draft ADRs needing review
- check git status, branch, and recent commits
- report what is pending before making changes
- recommend the highest-leverage next state before making changes

At session stop:
- if files changed, run the smallest relevant validation you can justify
 - if meaningful repo files changed, run `graphify update .` (AST-only, no LLM
   needed) before reporting final state unless unavailable or would block urgent
   handoff
- report files changed and validation results
- ask before commit/push unless the user already directed it

## Directions for Athena (archon)

Use Athena (archon) for:
- architecture and planning
- ADRs and durable decisions
- workflow design
- resolving ambiguous cross-cutting project choices
- `athena_<action-in-this-mode>` Archon workflows

Athena should:
- write implementation-ready plans
- place downstream work in ADRs under `docs/architecture/adr/`
- keep architecture out of this config repo unless it is about bootstrap structure
- treat `athena_` workflow outputs as Athena-owned artifacts even when a
  delegated operator invokes the Archon CLI

## Directions for Vulcan (opencode)

Use Vulcan (opencode) for:
- implementation
- tests and validation
- bug fixes
- code changes that follow an approved plan

Vulcan should:
- read the plan or ADR first
- place observations and recommendations in ADRs under `docs/architecture/adr/`

## Harness configs

| Scope | Path | Contents |
|-------|------|----------|
| **Global (this repo)** | `agents/global/<harness>/` | Example configs, `.example` suffix, no secrets |
| **Local** | `~/.pi/` | Per-machine pi config (auth tokens, local overrides) |
| **Local** | `~/.archon/` | Per-machine archon config (worktree state, run history) |
| **Local** | `~/.opencode/` | Per-machine opencode config (accounts, sessions) |
| **Local** | `~/.local/share/goose/` | Per-machine goose runtime data |

Local configs are NEVER committed to this repo.

## ADR file convention

ADR files use the following convention:

**Filename:** `adr.YYYYMMDD.HHMMSS_kebab-slug.md`
Example: `adr.20260630.144732_runtime-role-separation.md`

**Header:** Every ADR contains these sections:

```
# ADR YYYYMMDD.HHMMSS: Title

## Status

draft | accepted | completed | superseded | rejected

## Context

...

## Decision

...

## Consequences

...
```

### Provenance fields

When provenance needs more precision, include these fields or an equivalent
block:

- `Origin` — the original harness or system where the task began
- `From` — the immediate sender or producer of the artifact
- `Acting-As` — the harness role being represented, if different from `From`
- `Scope` / `Repository` — the repository or repo-scope the artifact applies to
- `Delegated-Operator` — the access layer or human mediator when one is
  relaying work without becoming that harness

Interpretation rule:
- `From` answers who sent the artifact
- `Acting-As` answers which harness role they represented
- `Delegated-Operator` answers who mediated access


## Secrets and safety

- Never commit machine-local tokens or credentials.
- Keep `.example` files free of secrets.
- Prefer environment-specific overrides in local directories.
- If a file might contain sensitive state, treat it as local-only unless explicitly documented otherwise.

## Bootstrapping

Prerequisite: run commands from the repo root.

```bash
projectkoios bootstrap init     # copy agents/global/*.example → ~/.<harness>/
projectkoios bootstrap install  # symlink global configs into place
```

Use `init` for first-time setup and `install` when you want the global examples linked into local harness config.

## Layout

```
projectkoios-bootstrap/
├── agents/global/       ← example configs per harness (.example suffix)
├── docs/                ← documentation, architecture, and ADRs
│   ├── architecture/adr/ ← ADRs and durable decisions (single source of truth)
├── maps/                ← workspace topology (repos, packages, vault)
├── src/python/          ← Python CLI package (bootstrap tooling)
├── scripts/             ← CLI wrappers
├── archon/              ← Athena (archon) workflows and prompts
├── opencode/            ← opencode rules and runtime harness
├── goose/               ← Goose agent rules and prompts
├── pi/                  ← Hermes (pi) harness config
├── skills/              ← meta-harness skills in development
├── AGENTS.md            ← this file
└── pyproject.toml       ← Python project metadata
```

## Mothership

`~/projectkoios/` is the Obsidian vault.
Athena writes architecture docs there.
This repo is the config store only.
