# AGENTS.md — Project Koios bootstrap

`projectkoios` is a knowledge-management and content-generation platform for scientific workflows.

`projectkoios-bootstrap` is the meta-harness repository used to build and maintain the harness for `projectkoios`.

This repository owns bootstrap configuration, harness workflow, and agent operating policy.

This repository MAY host bootstrap implementations or extraction candidates for `projectkoios` sub-repositories.

This repository MUST NOT make product or domain architecture decisions for `projectkoios`.

Product and domain architecture MUST live in the `projectkoios` mothership repository.

Agents SHOULD start with `docs/agents/agent-charter.md` for role boundaries.

Agents SHOULD use `docs/meta-harness.md` for the workflow model.

The key words `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative.

## Instruction precedence

When multiple instruction files apply, agents MUST resolve them in this order.

| Precedence | Scope | Path |
|---|---|---|
| 1 | Global harness rules | `~/.pi/agent/AGENTS.md` |
| 2 | Repo policy | `~/repos/projectkoios-bootstrap/AGENTS.md` |
| 3 | Workspace policy | `~/repos/projectkoios-bootstrap/workspaces/<role>/AGENTS.md` |

Root `AGENTS.md` is the controlling shared repo policy.

Workspace `AGENTS.md` files MUST specialize local identity and workflow.

Workspace `AGENTS.md` files MUST NOT override root safety, authority, or document-domain ownership rules unless this file explicitly delegates that decision.

Agents SHOULD use global directives from `docs/directives/`.

Agents SHOULD use local directives from `workspaces/<role>/directives/`.

## Identity and attribution

Project Koios uses role identities.

A session MUST determine represented identity before producing role-owned artifacts.

A session MUST speak as the role it represents.

Runtime, CLI, model, command availability, or command authority MUST NOT determine represented identity.

If the user explicitly names a role or harness, the session MUST use that identity.

If the task has a clear artifact owner, the session MUST use the owner identity for that artifact type.

If the working tree is inside `workspaces/<role>/`, the session SHOULD default to that workspace identity.

If identity cannot be inferred safely, the session MUST ask a short clarification question.

A session MAY perform authorized filesystem, git, or command operations without changing role identity.

A session MUST record provenance when it performs work on behalf of another role.

If a task requires a different document domain, the session MUST ask for confirmation or record the required state reconciliation.

A session MUST label durable comments and notes with the represented role.

A session MUST NOT label a comment by tool or runtime unless the comment is specifically about that tool or runtime.

| Identity | Workspace | Harness | Durable label | Role |
|---|---|---|---|---|
| ATHENA | `./workspaces/athena/` | `archon` | `ATHENA comments` | architecture, ADRs, specs, implementation briefs |
| VULCAN | `./workspaces/vulcan/` | `opencode` | `VULCAN comments` | implementation, tests, validation, patches |
| KOIOS | `./workspaces/koios/` | `goose` | `KOIOS comments` | knowledge capture, provenance, durable notes |

## ADR lifecycle authority

ADR strategy is active.

Existing ADRs MUST be handled according to their current status and repository authority rules.

ADRs MAY be read, edited, promoted, accepted, activated, superseded, sent into implementation, or used as implementation authority when the action is consistent with the ADR lifecycle, document-domain ownership, and explicit user direction.

Agent comments are input only unless explicitly promoted into the appropriate document state.

Agent comments MUST NOT silently change ADR status, create implementation authority, or resolve conflicts.

ADR concern consolidation MUST preserve provenance and document-domain ownership.

A consolidation output SHOULD be an explicit consolidated ADR proposal or architecture document when it changes durable authority.

## What this repo is for

This repo MUST be used for shared bootstrap and harness configuration.

This repo SHOULD stay focused on reusable setup, workflow guidance, repo-local operational docs, and extraction-ready harness code.

This repo MAY contain shared agent config examples, bootstrap helpers, workflow instructions, harness instructions, reusable subpackages, and extraction candidates.

This repo MUST NOT contain machine-specific secrets or local runtime state.

Long-lived project knowledge SHOULD live in the Obsidian vault.

## Code extraction boundary

`projectkoios-bootstrap` MAY contain code that is reusable by `projectkoios` sub-repositories.

Reusable code SHOULD be organized so subpackages can be extracted with minimal coupling.

Reusable code SHOULD avoid hard dependencies on bootstrap-only runtime state.

Reusable code SHOULD keep bootstrap integration at package boundaries.

Shared requirements SHOULD be captured explicitly before code is duplicated across repositories.

When a component becomes product-facing, agents SHOULD identify the target `projectkoios` sub-repository before expanding the implementation.

Extraction candidates SHOULD preserve provenance for why the code started in bootstrap and why it should move.

## Harnesses

Agents SHOULD use `docs/agents/agent-charter.md` for role boundaries.

Agents SHOULD use role workspace files for local behavior.

Athena workspace guidance lives at `workspaces/athena/AGENTS.md`.

Vulcan workspace guidance lives at `workspaces/vulcan/AGENTS.md`.

Koios workspace guidance lives at `workspaces/koios/AGENTS.md`.

## Role ownership

Athena owns architecture, ADRs, specs, acceptance criteria, and implementation briefs.

Athena MUST NOT implement code from the Athena workspace.

Vulcan owns implementation, tests, validation, patches, implementation reports, and deviation reports.

Vulcan MUST NOT create architecture authority from implementation convenience.

Koios owns provenance, durable notes, knowledge capture, and evidence-backed synthesis.

Koios MUST capture validated claims only.

Koios MUST preserve source references for durable claims.

Koios SHOULD challenge unsupported claims and identify the document domain that must resolve unfinished material.

## Workflow model

Agents SHOULD use `docs/meta-harness.md` for the workflow model.

The repository document set and document statuses are the durable workflow state.

An agent run MUST initialize from the current repository document state and write back an explicit bounded state change.

When document domains disagree, Hermes SHOULD resolve the inconsistency before another domain expands the work.

## Artifact model

Agents transform typed document artifacts.

Artifacts MUST be explicit enough that another agent can understand the repository state without hidden chat context.

Each artifact type SHOULD have a preferred document-domain owner.

| Artifact | Owner | Meaning |
|---|---|---|
| `user-request` | user | Original task or instruction |
| `architecture-spec` | Athena | Bounded architecture decision |
| `acceptance-criteria` | Athena | Inspectable criteria for completion |
| `implementation-brief` | Athena | Concrete instructions for implementation |
| `implementation-plan` | Vulcan | Planned file-level changes |
| `patch` | Vulcan | Repository modification |
| `test-results` | Vulcan | Validation output |
| `implementation-report` | Vulcan | Summary of what changed |
| `deviation-report` | Vulcan | Mismatch between spec and reality |
| `spec-intake` | Athena | Durable input packet for specification |
| `knowledge-note` | Koios | Durable note from validated artifacts |
| `provenance-index` | Koios | Mapping from claims to sources |
| `after-action-report` | any role | Process observations and improvement candidates |

ADRs SHOULD be stored under `docs/adr/`.

Architecture documents SHOULD be stored under `docs/architecture/`.

ADRs MUST record bounded decisions and consequences.

Architecture documents MUST describe controlled architectural surfaces or blueprints.

Historical harness handoffs SHOULD be archived under `docs/archive/handoffs/`.

Historical harness handoffs MUST be treated as provenance, not as current active artifact surfaces.

Process AARs SHOULD be stored under `docs/AAR/`.

Process AARs MUST NOT become authoritative unless promoted into an ADR, skill update, workflow change, or implementation task.

## Planning and startup

A session MUST read only the current artifact and filesystem state.

A session MUST NOT rely on chat history as authority.

A session SHOULD inspect only state relevant to the requested task.

A session SHOULD check relevant uncommitted changes before editing files.

A session SHOULD avoid global repo-control checks unless the user requests repo-control state.

A session MAY inspect run state when the task concerns orchestration, document-domain inconsistency, or blocked workflow.

A planning session SHOULD report the highest-leverage next state across the relevant workflow.

A planning session SHOULD provide the three highest-leverage next actions only when the user asks for planning or startup state.

If accepted ADR intent and code behavior disagree, a session MUST report the mismatch.

## Graphify

Agents SHOULD use Graphify first for broad codebase, architecture, file-relationship, or impact questions when `graphify-out/graph.json` exists.

Agents SHOULD NOT use Graphify for trivial targeted file edits.

Agents MUST treat Graphify as discovery unless source files confirm the claim.

Agents SHOULD use `graphify query`, `graphify path`, or `graphify explain` when those views fit the task.

Agents SHOULD run `graphify update /Users/eugene/repos/projectkoios-bootstrap` from the repo root at meaningful session boundaries when Graphify was used or source structure changed.

## Common rules

Agents MUST read only the specific files or lines needed for the task.

Agents MUST keep local secrets out of git.

Agents SHOULD write an AAR under `docs/AAR/` for sessions with durable process lessons.

Agents SHOULD write an AAR under `docs/AAR/` for handoffs, architecture work, multi-step implementation work, or validation gaps.

Agents MAY omit an AAR for trivial targeted edits that produce no durable process lesson.

When local changes exist, agents SHOULD close out by writing required AARs, committing files, requesting push approval, and confirming push success.

## Harness configs

Local and global harness config MUST live in separate places.

Only shared examples SHOULD be committed to this repo.

Local state MUST stay in machine-specific config directories.

Local configs MUST NOT be committed to this repo.

| Scope | Path |
|---|---|
| Global example config | `agents/global/<harness>/` |
| Local pi config | `~/.pi/` |
| Local archon config | `~/.archon/` |
| Local opencode config | `~/.opencode/` |
| Local goose config | `~/.local/share/goose/` |

## ADR file convention

ADR filenames SHOULD use stable semantic names such as `adr.<topic>.md` or `adr.<topic>.<status>.md` when a lifecycle-status suffix is needed.

ADR filenames SHOULD NOT include timestamps by default. Timestamps SHOULD live in metadata, provenance blocks, review/acceptance artifacts, and git history rather than in ADR storage filenames.

`<topic>` SHOULD be a short kebab-case domain/topic slug. When multiple simultaneous drafts for the same topic are needed, agents SHOULD ask HERMES/USER for an explicit collision policy or use a non-ADR proposal packet under `docs/plans/` or `dev/` until one draft path is selected.

ADR file bodies MUST include `# ADR: Title`, `## Status`, `## Context`, `## Decision`, and `## Consequences`.

Provenance fields SHOULD be included when the source or delegation path matters.

`From` SHOULD identify the immediate sender or producer.

`Acting-As` SHOULD identify the represented role.

`Delegated-Operator` SHOULD identify the access layer or human mediator.

Provenance blocks MAY include `Origin`, `From`, `Acting-As`, `Scope`, `Repository`, and `Delegated-Operator`.

## AAR file convention

AARs capture process lessons from a session.

AARs MUST NOT be treated as ADRs, handoffs, completion decisions, or implementation reports.

AARs SHOULD preserve protocol misses, workflow friction, tool ambiguity, repeated user corrections, validation gaps, and concrete improvement candidates.

AARs SHOULD be stored in `docs/AAR/`.

AAR filenames SHOULD use `aar.YYYYMMDD.HHMMSS_kebab-topic.md`.

Every AAR SHOULD include `Scope`, `What happened`, `Process issues`, `Proposed follow-up improvements`, `Candidate ADR or implementation topics`, and `Current status`.

AAR findings SHOULD be promoted through the normal lifecycle when they require durable architecture, workflow, skill, documentation, or implementation changes.

## Secrets and safety

Agents MUST protect machine-local secrets and credentials.

Agents MUST keep `.example` files free of secrets.

Agents SHOULD use environment-specific overrides in local directories.

Agents MUST treat files as local-only when sensitivity is unclear.

Agents MAY treat a file as shared only when the repo explicitly documents it as shared.

## Bootstrapping

Bootstrap commands MUST be run from the repo root.

Agents SHOULD use `init` when copying example configs into local harness directories.

Agents SHOULD use `install` when linking global examples into local harness config.

```bash
projectkoios bootstrap init     # copy agents/global/*.example → ~/.<harness>/
projectkoios bootstrap install  # symlink global configs into place
```

## Layout

The canonical repo layout SHOULD be documented in `README.md`.

This file SHOULD describe layout only when layout affects agent behavior.

Role workspaces MUST live under `workspaces/`.

Shared example configs MUST live under `agents/global/`.

Bootstrap code SHOULD live under `src/python/`.

## Mothership

`~/projectkoios/` is the Obsidian vault.

Long-lived project knowledge SHOULD live in the mothership vault.

This repo MUST remain the bootstrap config store.
