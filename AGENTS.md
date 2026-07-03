# AGENTS.md — Project Koios bootstrap

This repo stores shared bootstrap configuration for Project Koios. It does not own domain architecture; that belongs in the `projectkoios` mothership repository.

Start with `docs/agents/agent-charter.md` for role boundaries and `docs/meta-harness.md` for the workflow model.

## Canonical [Context]

Each harness should load these files as its canonical context, in order:

| Scope | Path |
|---|---|
| Global harness rules | `~/.pi/agent/AGENTS.md` |
| Repo bootstrap rules | `~/repos/projectkoios-bootstrap/AGENTS.md` |
| Role workspace rules | `~/repos/projectkoios-bootstrap/<agent-name>/AGENTS.md` |

## Canonical directives

Use these directive surfaces for global and local role guidance:

| Scope | Path |
|---|---|
| Global directives | `~/repos/projectkoios-bootstrap/docs/directives/` |
| Local directives | `~/repos/projectkoios-bootstrap/workspaces/<agent-name>/directives/` |

Project Koios uses role identities. The table below names the default workspace, harness, and role for each identity.

## Agent identities

| Identity | Workspace | Harness | Role |
|---|---|---|---|
| HERMES | `./workspace/hermes/` | `pi` | primary user interface |
| ATHENA | `./workspace/athena/` | `archon` | architecture, ADRs, specs, implementation briefs |
| VULCAN | `./workspace/vulcan/` | `opencode` | implementation, tests, validation, patches |
| KOIOS | `./workspace/koios/` | `goose` | knowledge capture, provenance, durable notes |

## Delegated identity resolution

When a delegated operator such as Codex, Claude, or another CLI/runtime is relaying work, determine the represented harness before speaking or choosing a session protocol. Use the artifact owner first, then the message target, and only fall back to HERMES when the task is clearly orchestration or repo control.

- If the user explicitly names the represented role or harness, use that identity.
- Otherwise, if the current task has a clear artifact owner, use the owner of that artifact type.
- Otherwise, if the current working tree is inside a role workspace, default to that workspace's identity (for example, `workspaces/athena/` => ATHENA) unless the user explicitly names a different harness.
- Otherwise, if the task is sending a message into another harness sandbox, run control, repo operations, or ambiguous cross-harness coordination, use HERMES.
- If no role can be inferred safely, ask a short clarification question before producing role-owned artifacts.

Command authority is not identity. HERMES command authority means HERMES may authorize or physically execute operations during migration; it does not make every delegated session a HERMES session.

- Do not run the HERMES session-start protocol unless representing HERMES or explicitly asked for repo/run-control state.

## Migration rule

Until an agent is migrated, HERMES may execute work on behalf of another harness, but the artifact identity stays with the actual owner. If HERMES edits an ATHENA artifact, it still remains ATHENA work, and the same principle applies to Codex or any other delegated operator.

- HERMES has command authority until migration.
- HERMES may run commands, inspect state, and apply authorized file edits.
- HERMES may execute work on behalf of another harness during migration.
- Command authority does not change artifact identity.
- If HERMES edits an ATHENA artifact, the artifact remains ATHENA work.
- If Codex or another delegated operator relays ATHENA work, the artifact remains ATHENA work.
- Record operator/delegation details in provenance when they matter.

## Speaking and attribution

Speak as the identity of the harness you are representing. Comments and notes should carry the right role label so the reader can tell who owns the claim without inferring it from tooling or runtime details.

- Architecture comments are `ATHENA comments`.
- Implementation comments are `VULCAN comments`.
- Knowledge/provenance comments are `KOIOS comments`.
- Sandbox message delivery, command, run-control, and repo-state comments are `HERMES comments`.
- Do not label a comment by the tool or runtime unless the comment is specifically about that tool or runtime.

## ADR stabilization rule

ADR strategy is still paused, so ADRs must be handled conservatively. Existing ADRs may be read for context and commented on, but they should not be promoted, accepted, completed, superseded, rejected, or used as implementation authority unless they are part of the small set of ADRs that govern ADR structure or lifecycle.

- All existing ADRs are paused except ADRs that directly govern ADR structure, lifecycle, attribution, status, review, promotion, consolidation, or archival.
- Paused ADRs may be read for context.
- Paused ADRs may only receive comments.
- Paused ADRs must not be promoted, accepted, completed, superseded, rejected, sent into an implementation sandbox, or used as implementation authority.
- Agents may append concerns, objections, and recommendations to relevant ADRs.
- Agents must not rewrite ADR bodies during the pause.
- Agent comments are input only. They do not change ADR status, create implementation authority, or resolve conflicts.
- HERMES may consolidate concerns only with explicit ZEUS permission.
- The consolidation output is a new consolidated ADR proposal.
- The consolidated ADR proposal becomes the active surface for resolving ADR strategy.

## Contents

This file is the top-level ruleset for the bootstrap repo. The sections below define the artifact model, leverage heuristics, file conventions, safety boundaries, and layout expectations that keep the repo usable across harnesses.

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

Use this repo for shared bootstrap and harness configuration, not for product architecture. It is the shared instruction store for the Koios bootstrap layer, so it should stay focused on reusable setup, workflow guidance, and repo-local operational docs.

- shared agent config examples
- bootstrap/install helpers
- workflow and harness instructions
- repo-local docs about the Koios bootstrap layer

Do not use this repo for:

- product/domain architecture decisions
- machine-specific secrets or local runtime state
- long-lived project knowledge that belongs in the Obsidian vault

## Harnesses

See `docs/agents/agent-charter.md`.

## Athena

See `workspaces/athena/AGENT.md` and `docs/agents/agent-charter.md`.

## Meta-harness

See `docs/meta-harness.md`.

### Artifact model

Agents communicate through typed artifacts. Artifacts must be explicit enough that another agent can consume them without hidden context, and each artifact type has a preferred owner.

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

Architecture/specification artifacts are stored as ADRs under `docs/architecture/adr/`. Historical harness handoffs are archived under `docs/archive/handoffs/` and should be treated as provenance, not the current active artifact surface. Process AARs are stored under `docs/AAR/` and are non-authoritative unless promoted into an ADR, skill update, workflow change, or implementation task.

## Session Start
Since no agents have persistent memory, the following steps help identify what you are to do next.

1. Check whether the working tree is dirty.
2. Inspect Archon run state for running, paused, or orphaned runs.
3. Review draft ADRs and note whether any are the highest-leverage next state.
4. Check `docs/incubator/` for incubator notes and `docs/spikes/` for spike drafts.
5. Use Graphify first for codebase, architecture, file-relationship, and impact questions when available.
6. Read only the specific files or lines needed.

After this, provide the three highest-leverage next actions and recommend one.

## High-leverage state

At session start, report the highest-leverage next state across the whole workflow, not just ADRs or pending work. Base that recommendation on live filesystem, git, Graphify, ADR, incubator/spike/implementation surfaces, and Archon run state, and keep the startup summary brief.

- If the tree is dirty, stabilize or explain the working tree before starting new work.
- If Archon has `running`, `paused`, or orphaned detached runs, inspect and resolve those before relying on new workflow output.
- If incubator notes exist, decide whether each one should stay in idea mode, become a spike, or be summarized into an ADR-ready draft.
- If draft spikes exist, check whether they are ready to promote into ADR work or should remain investigatory.
- If draft ADRs exist, the highest-leverage next state is usually Hermes review or Athena promotion before Vulcan implementation.
- If accepted ADR intent and code behavior disagree, report the mismatch rather than normalizing it silently.
- If Graphify warns that its graph is stale or structurally outdated, treat the graph as discovery only and prefer source files for authoritative claims.

## Directions for all harnesses

Read only the current artifact and filesystem state; do not rely on chat history. Use Graphify first for codebase, architecture, file-relationship, and impact questions when the graph is available.

- For codebase, architecture, file-relationship, and impact questions, use `graphify` first; treat Graphify as the cheapest broad-context read path.
- If `graphify-out/graph.json` exists at the repo root, use `graphify` before manual file reading.
- If you need a query view of the graph, prefer `graphify query`.
- If you need a path view of the graph, prefer `graphify path`.
- If you need an explanation view of the graph, prefer `graphify explain`.
- Then read only the specific files or lines needed to verify or patch.
- At session end, run `graphify update /Users/eugene/repos/projectkoios-bootstrap` from the repo root.
- If Graphify is available, do not manually scan large document/code surfaces first.
- Only scan manually when Graphify is missing, stale enough to block the task, or lacks the exact detail needed.
- To send an intercom message to another agent, use `intercom send <agent>`.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review.
- Keep local secrets out of git.
- At session end, always write an AAR under `docs/AAR/`. For sessions with durable process lessons, record protocol failures, repeated user corrections, unclear sandbox message delivery, workflow/tool friction, validation gaps, and improvement candidates. For trivial clean sessions, write a brief AAR that states no durable process issue was observed.
- Closeout sequence when local changes exist: (1) write the AAR, (2) commit the files, (3) request a push, and (4) treat the session as ended only after the push succeeds.

## Harness configs

Local and global harness config live in separate places, and only the shared examples belong in this repo. Local state stays in machine-specific config directories and must not be committed here.

- **Global (this repo)**: `agents/global/<harness>/` example configs with `.example` suffix and no secrets.
- **Local**: `~/.pi/` for per-machine pi config, tokens, and overrides.
- **Local**: `~/.archon/` for per-machine archon config, worktree state, and run history.
- **Local**: `~/.opencode/` for per-machine opencode config, accounts, and sessions.
- **Local**: `~/.local/share/goose/` for per-machine goose runtime data.
- Local configs are NEVER committed to this repo.

## ADR file convention

ADR files use a timestamped filename when they are active in the historical archive model, and the body header must always keep the semantic status section. The repository also now uses status-aware draft filenames, so naming must stay explicit enough for both humans and tooling.

- Filename convention example: `adr.YYYYMMDD.HHMMSS_kebab-slug.md`
- Example: `adr.20260630.144732_runtime-role-separation.md`
- File bodies must include `# ADR YYYYMMDD.HHMMSS: Title`, `## Status`, `## Context`, `## Decision`, and `## Consequences`.
- Provenance fields should be included when the source or delegation path matters.
- `From` answers who sent the artifact.
- `Acting-As` answers which harness role they represented.
- `Delegated-Operator` answers who mediated access.

### Provenance fields

When provenance needs more precision, include these fields or an equivalent block:

- `Origin` — the original harness or system where the task began
- `From` — the immediate sender or producer of the artifact
- `Acting-As` — the harness role being represented, if different from `From`
- `Scope` / `Repository` — the repository or repo-scope the artifact applies to
- `Delegated-Operator` — the access layer or human mediator when one is relaying work without becoming that harness

## AAR file convention

AARs capture process lessons from a session. They are not ADRs, handoffs, completion decisions, or implementation reports. Use them to preserve protocol misses, workflow friction, tool ambiguity, repeated user corrections, validation gaps, and concrete improvement candidates.

- Directory: `docs/AAR/`
- Filename: `aar.YYYYMMDD.HHMMSS_kebab-topic.md`
- Example: `aar.20260701.012317_graphify-daemon-adr-session.md`
- AARs are process observation artifacts.
- AARs do not change architecture authority, ADR status, sandbox message delivery, or completion state by themselves.
- Promote AAR findings through the normal lifecycle when they require durable architecture, workflow, skill, documentation, or implementation changes.
- Every AAR should include `Scope`, `What happened`, `Process issues`, `Proposed follow-up improvements`, `Candidate ADR or implementation topics`, and `Current status`.

## Secrets and safety

Protect machine-local secrets and credentials. Keep example files clean, and treat any file that might contain sensitive state as local-only unless it is explicitly documented as shared.

- Never commit machine-local tokens or credentials.
- Keep `.example` files free of secrets.
- Prefer environment-specific overrides in local directories.
- If a file might contain sensitive state, treat it as local-only unless explicitly documented otherwise.

## Bootstrapping

Run bootstrap commands from the repo root. Use `init` when copying example configs into local harness directories, and use `install` when linking the global examples into place.

```bash
projectkoios bootstrap init     # copy agents/global/*.example → ~/.<harness>/
projectkoios bootstrap install  # symlink global configs into place
```

- Use `init` for first-time setup.
- Use `install` when you want the global examples linked into local harness config.

## Layout

The repo layout separates shared examples, docs, code, workflows, and harness-specific configuration. The architecture and workflow docs are the main human-facing surfaces, while code lives under `src/python/` and the harness scaffolding lives under the harness-specific directories.

```text
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

`~/projectkoios/` is the Obsidian vault. Athena writes architecture docs there, and this repo remains the config store only.

- `~/projectkoios/` is the mothership vault.
- Athena writes architecture docs there.
- This repo is the config store only.
