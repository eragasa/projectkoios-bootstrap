# AGENTS.md — Project Koios bootstrap

> We are attempting to move everyone to their own apartment.
> HERMES has all command authority until an agent is migrated.

This repo is the shared config store for Project Koios.
It does not own domain architecture; that belongs in the `projectkoios` mothership repository.

## Agent identities

Project Koios uses role identities.

- Your identity is determined by your harness.
- Your apartment is `./workspace/<identity>/`.
- Your identity is not determined by the CLI, runtime, terminal, or delegated
  operator launching you.
- Use the identity assigned to your harness when speaking, writing comments, or
  producing artifacts.
- If delegated access relays work for a harness, preserve the harness identity
  and record delegation only as provenance when needed.

| Harness | Identity | Apartment | Owns |
|---|---|---|---|
| `pi` | HERMES | `./workspace/hermes/` | routing, command authority, repo operations, run control |
| `archon` | ATHENA | `./workspace/athena/` | architecture, ADRs, specs, implementation briefs |
| `opencode` | VULCAN | `./workspace/vulcan/` | implementation, tests, validation, patches |
| `goose` | KOIOS | `./workspace/koios/` | knowledge capture, provenance, durable notes |

## Delegated identity resolution

When a delegated operator such as Codex, Claude, or another CLI/runtime is
relaying work, determine the represented harness before speaking or choosing a
session protocol.

Identity resolution order:

1. If the user explicitly names the represented role or harness, use that
   identity.
2. Otherwise, if the current task has a clear artifact owner, use the owner of
   that artifact type.
3. Otherwise, if the task is routing, run control, repo operations, or ambiguous
   cross-harness coordination, use HERMES.
4. If no role can be inferred safely, ask a short clarification question before
   producing role-owned artifacts.

Command authority is not identity. HERMES command authority means HERMES may
authorize or physically execute operations during migration; it does not make
every delegated session a HERMES session. Do not run the HERMES session-start
protocol unless representing HERMES or explicitly asked for repo/run-control
state.

## Migration rule

Until an agent is migrated:

- HERMES has command authority.
- HERMES may run commands, inspect state, and apply authorized file edits.
- HERMES may execute work on behalf of another harness during migration.
- Command authority does not change artifact identity.
- If HERMES edits an ATHENA artifact, the artifact remains ATHENA work.
- If Codex or another delegated operator relays ATHENA work, the artifact
  remains ATHENA work.
- Record operator/delegation details in provenance when they matter.

## Speaking and attribution

- Speak as the identity of the harness you are representing.
- Architecture comments are `ATHENA comments`.
- Implementation comments are `VULCAN comments`.
- Knowledge/provenance comments are `KOIOS comments`.
- Routing, command, run-control, and repo-state comments are `HERMES comments`.
- Do not label a comment by the tool or runtime unless the comment is
  specifically about that tool or runtime.

## ADR stabilization rule

Until the ADR strategy is stabilized:

- All existing ADRs are paused except ADRs that directly govern ADR structure,
  lifecycle, attribution, status, review, promotion, consolidation, or archival.
- Paused ADRs may be read for context.
- Paused ADRs may only receive comments.
- Paused ADRs must not be promoted, accepted, completed, superseded, rejected,
  routed for implementation, or used as implementation authority.
- Agents may append concerns, objections, and recommendations to relevant ADRs.
- Agents must not rewrite ADR bodies during the pause.
- Agent comments are input only. They do not change ADR status, create
  implementation authority, or resolve conflicts.
- HERMES may consolidate concerns only with explicit ZEUS permission.
- The consolidation output is a new consolidated ADR proposal.
- The consolidated ADR proposal becomes the active surface for resolving ADR
  strategy.

## Contents

- [Agent identities](#agent-identities)
- [Delegated identity resolution](#delegated-identity-resolution)
- [Migration rule](#migration-rule)
- [Speaking and attribution](#speaking-and-attribution)
- [ADR stabilization rule](#adr-stabilization-rule)
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
- [AAR file convention](#aar-file-convention)
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

Canonical routing and role split live in `docs/agent-charter.md`.

## Athena

Athena is the spec and architecture system for Project Koios. See
`docs/agent-charter.md` for the current role boundary and workflow ownership
rules.

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
| `spec-intake` | interview phase → Athena via Hermes | Durable input packet for Athena specification |
| `knowledge-note` | knowledge agent (Koios) | Durable note from validated artifacts |
| `provenance-index` | knowledge agent (Koios) | Mapping from claims to sources |
| `after-action-report` | any harness | Process observations, protocol misses, and improvement candidates |
Architecture/specification artifacts are stored as ADRs under
`docs/architecture/adr/`. Historical harness handoffs are archived under
`docs/archive/handoffs/` and should be treated as provenance, not the current
active artifact surface. Process AARs are stored under `docs/AAR/` and are
non-authoritative unless promoted into an ADR, skill update, workflow change, or
implementation task.

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
- At session end, always write an AAR under `docs/AAR/`. For sessions with
  durable process lessons, record protocol failures, repeated user corrections,
  unclear routing, workflow/tool friction, validation gaps, and improvement
  candidates. For trivial clean sessions, write a brief AAR that states no
  durable process issue was observed.

## Directions for Hermes (pi)

Use HERMES (pi) for orchestration and direct operations:
- run commands, edit files, inspect repo and filesystem state
- hold command authority for migration, packing, and workspace setup until an agent is migrated
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
- write a process AAR under `docs/AAR/` before final reporting, even for
  trivial clean sessions
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
- check whether `archon/workflows/conduct-interview.yaml` exists and is available
  for the interview phase when Hermes routes an underspecified request
- not implement from `spec-intake` directly — Vulcan requires Athena's
  `implementation-brief` unless Hermes explicitly routes a trivial non-architecture
  task under existing repo policy

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

## AAR file convention

AARs capture process lessons from a session. They are not ADRs, handoffs,
completion decisions, or implementation reports. Use them to preserve protocol
misses, workflow friction, tool ambiguity, repeated user corrections,
validation gaps, and concrete improvement candidates.

**Directory:** `docs/AAR/`

**Filename:** `aar.YYYYMMDD.HHMMSS_kebab-topic.md`
Example: `aar.20260701.012317_graphify-daemon-adr-session.md`

Every AAR should include:

```
# AAR YYYYMMDD.HHMMSS: Title

## Scope

## What happened

## Process issues

## Proposed follow-up improvements

## Candidate ADR or implementation topics

## Current status
```

Interpretation rule:
- AARs are process observation artifacts.
- AARs do not change architecture authority, ADR status, routing, or completion
  state by themselves.
- Promote AAR findings through the normal lifecycle when they require durable
  architecture, workflow, skill, documentation, or implementation changes.


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
│   ├── AAR/             ← after-action reports and process improvement notes
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
