# AGENTS.md — Project Koios bootstrap

This repo is the shared config store for Project Koios.
It does not own domain architecture; that belongs in the `projectkoios` mothership repository.

## Contents

- [What this repo is for](#what-this-repo-is-for)
- [Harnesses](#harnesses)
- [Meta-harness](#meta-harness)
- [Directions for all harnesses](#directions-for-all-harnesses)
- [Directions for pi](#directions-for-pi)
- [Directions for archon](#directions-for-archon)
- [Directions for opencode](#directions-for-opencode)
- [Harness configs](#harness-configs)
- [Routing guide](#routing-guide)
- [Artifact handoff](#artifact-handoff)
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
| pi | pi | Meta-harness — orchestration, operations, handoff coordination |
| archon (archon.diy) | **Athena** | Architecture design, ADRs, planning |
| opencode | **Vulcan** | Code writing, tests, validation |
| goose | **Koios** | Knowledge management, vault ops |

## Meta-harness

This repo operates a role-based meta-harness that separates specification, implementation, and knowledge capture into distinct agent roles. See `doc/meta-harness.md` for the full framework detail on skill model, disagreement handling, completion gates, escalation rules, and anti-patterns.

### Role mapping

| Meta-harness role | Concrete harness | Name | Responsibility |
|---|---|---|---|
| Spec agent | archon | Athena | Architecture, scope, acceptance criteria |
| Code agent | opencode | Vulcan | Implementation, tests, validation |
| Knowledge agent | goose | Koios | Durable notes, provenance, vault ops |
| Meta-harness | pi | pi | Routing, orchestration, completion gating |

### Artifact model

Agents communicate through typed artifacts. An artifact must be explicit enough that another agent can consume it without hidden context.

| Artifact | Owner | Meaning |
|---|---|---|
| `user-request` | user | Original task or instruction |
| `architecture-spec` | spec agent (archon) | Bounded architecture decision |
| `acceptance-criteria` | spec agent (archon) | Inspectable criteria for completion |
| `implementation-brief` | spec agent (archon) | Concrete instructions for implementation |
| `implementation-plan` | code agent (opencode) | Planned file-level changes |
| `patch` | code agent (opencode) | Repository modification |
| `test-results` | code agent (opencode) | Validation output |
| `implementation-report` | code agent (opencode) | Summary of what changed |
| `deviation-report` | code agent (opencode) | Mismatch between spec and reality |
| `knowledge-note` | knowledge agent (goose) | Durable note from validated artifacts |
| `provenance-index` | knowledge agent (goose) | Mapping from claims to sources |
| `routing-decision` | meta-harness (pi) | Next agent/action selection |
| `revision-request` | meta-harness (pi) | Required correction to an artifact |
| `completion-decision` | meta-harness (pi) | Final acceptance or rejection |

Artifacts are stored in each harness's `handoffs/` directory.

### Standard workflow

```
user-request → architecture-spec → implementation → validation → knowledge capture → completion
```

1. Meta-harness (pi) routes process/completion/disagreement tasks; design ambiguity defaults to archon first.
2. Spec agent (archon) produces `architecture-spec` and `acceptance-criteria`.
3. Code agent (opencode) produces `patch`, `test-results`, and `implementation-report`. If the spec cannot be satisfied, produce a `deviation-report` which may trigger a spec revision loop.
4. Knowledge agent (goose) produces `knowledge-note` and `provenance-index`.
5. Meta-harness (pi) checks artifacts against acceptance criteria and issues `completion-decision`.

### Authority rules

When artifacts disagree, resolve using this order:

1. Explicit user instruction
2. Current repository state
3. Passing tests and executable validation
4. Approved architecture specification
5. Acceptance criteria
6. Implementation report
7. Knowledge note
8. Agent inference

A lower-authority artifact must be revised when it conflicts with a higher-authority artifact.

### Default decision rule

When in doubt:
- Route design uncertainty to archon first
- Route lightweight config changes and direct edits to the meta-harness (pi)
- Route complex implementation, tests, and validation to the code agent (opencode)
- Route durable documentation to the knowledge agent (goose)
- Route disagreement or completion checks to the meta-harness (pi)

## Directions for all harnesses

- Read only the current artifact and filesystem state; do not rely on chat history.
- For codebase, architecture, file-relationship, and impact questions, use `graphify` first.
- If `graphify-out/graph.json` exists, prefer `graphify query`, `graphify path`, or `graphify explain` before manual grepping or browsing.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review.
- Write handoff artifacts when work must continue in another harness.
- Keep local secrets out of git.
- Prefer the harness that matches the work type instead of forcing everything through one tool.

## Directions for pi

Use pi for orchestration and direct operations:
- run commands, edit files, inspect repo and filesystem state
- manage harness configs, bootstrap setup, repo maintenance
- start, inspect, approve, reject, resume, or cancel Archon workflow runs
- coordinate handoffs between harnesses
- read and write handoff artifacts
- route tasks to the appropriate specialized harness

Pi is the meta-harness operator. It is not limited to routing — it can
execute tasks directly when no specialist is required. But to respect the
separation of concerns:
- route architecture and planning ambiguity to archon
- route complex implementation, tests, and bug fixes to opencode
- route knowledge curation and vault work to goose

## Directions for archon

Use archon (Athena) for:
- architecture and planning
- ADRs and durable decisions
- workflow design
- resolving ambiguous cross-cutting project choices

Archon should:
- write implementation-ready plans
- place downstream work in `archon/handoffs/` using the [handoff file convention](#handoff-file-convention)
- keep architecture out of this config repo unless it is about bootstrap structure

## Directions for opencode

Use opencode (Vulcan) for:
- implementation
- tests and validation
- bug fixes
- code changes that follow an approved plan

Opencode should:
- read the plan or handoff artifact first
- place completion reports and questions in `opencode/handoffs/`
- escalate design ambiguity back to archon instead of inventing policy

## Harness configs

| Scope | Path | Contents |
|-------|------|----------|
| **Global (this repo)** | `agents/global/<harness>/` | Example configs, `.example` suffix, no secrets |
| **Local** | `~/.pi/` | Per-machine pi config (auth tokens, local overrides) |
| **Local** | `~/.archon/` | Per-machine archon config (worktree state, run history) |
| **Local** | `~/.opencode/` | Per-machine opencode config (accounts, sessions) |
| **Local** | `~/.local/share/goose/` | Per-machine goose runtime data |

Local configs are NEVER committed to this repo.

## Routing guide

| Task type | Route to |
|----------|----------|
| architecture, ADRs, planning | archon |
| implementation, tests, validation | opencode |
| research, vault, knowledge tasks | goose |
| run control, orchestration, handoff coordination | pi |
| unclear cross-harness decisions | archon first |

## Artifact handoff

Handoff is the standard way work moves between harnesses.
Each harness writes completion reports and artifacts to its own `handoffs/` directory for the downstream harness to consume.

| From | To | Path |
|------|----|------|
| archon (Athena) | opencode (Vulcan) | `archon/handoffs/` — `architecture-spec`, `implementation-brief` |
| opencode (Vulcan) | archon (Athena) | `opencode/handoffs/` — `implementation-report`, `deviation-report` |
| goose (Koios) | archon (Athena) | `goose/handoffs/` — `knowledge-note`, `provenance-index` |

Each harness should assume no session memory beyond its current artifact and filesystem state.

### Handoff file convention

All new handoff files use:

**Filename:** `YYYYMMDD.HHMMSS_<topic>.md`
Example: `2026-06-29.214500_graphify-out-stale-cleanup.md`

**Header:** These fields at the top of every handoff file:

```
Origin: <harness-name>
Created: <YYYY-MM-DD HH:MM>
From: <agent-name>
To: <agent-name>
Status: <draft|active|complete>
```

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
├── architecture/        ← ADRs and durable decisions (immutable archive)
├── doc/                 ← mutable docs (system overview, future ADRs)
├── maps/                ← workspace topology (repos, packages, vault)
├── src/python/          ← Python CLI package (bootstrap tooling)
├── scripts/             ← CLI wrappers
├── archon/              ← Archon workflows and prompts
├── opencode/            ← opencode rules and runtime harness
├── goose/               ← Goose agent rules and prompts
├── pi/                  ← pi-specific harness config
├── skills/              ← meta-harness skills in development
├── AGENTS.md            ← this file
└── pyproject.toml       ← Python project metadata
```

## Mothership

`~/projectkoios/` is the Obsidian vault.
Athena writes architecture docs there.
This repo is the config store only.
