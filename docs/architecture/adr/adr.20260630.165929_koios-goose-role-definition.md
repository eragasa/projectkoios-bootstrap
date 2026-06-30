# ADR 20260630.165929: Koios/goose role definition

## Status

Draft

## Context

Origin: archon
Created: 2026-06-30 16:59
From: Athena
To: Vulcan
Scope: projectkoios-bootstrap
Repository: /Users/eugene/repos/projectkoios-bootstrap

This specification responds to
`docs/archive/handoffs/archon/20260630.164803_athena-develop-koios-role.md`.
It is scoped to `projectkoios-bootstrap` and the Project Koios meta-harness
model. It does not define product/domain architecture for the mothership.

## Decision

Koios is the Project Koios knowledge role, currently executed through the
`goose` runtime. Its primary responsibility is to convert validated workflow
outcomes and inspected repository/vault state into durable, provenance-backed
knowledge artifacts.

Koios is a first-class meta-harness participant, not merely a helper prompt.
It owns knowledge capture, provenance indexing, documentation coherence review,
and vault-oriented knowledge operations. It may inspect repository state and
documentation to establish provenance, but it does not own architecture
decisions, implementation patches, completion gates, or routing authority.

### Role Boundaries

Koios owns:

- `knowledge-note`
- `provenance-index`
- `documentation-gap-report`
- `knowledge-sync-note`
- `provenance-audit`
- `missed-capture-report`

Koios may produce, but does not have final routing authority over:

- `repo-state-summary`
- `routing-recommendation`

Hermes remains responsible for routing decisions, session orchestration,
completion decisions, and disagreement escalation. Athena remains responsible
for architecture specs, acceptance criteria, implementation briefs, and ADR
decisions. Vulcan remains responsible for implementation plans, patches, test
results, implementation reports, and deviation reports.

### Direct Versus Supporting Work

Route directly to Koios when the requested output is knowledge, provenance, or
documentation coherence:

- create or update a knowledge note from validated artifacts
- build or verify a provenance index
- audit whether completed work has been captured durably
- summarize current repository or vault state with cited sources
- ingest source material into structured notes
- identify documentation drift or missing knowledge capture
- prepare vault-ready notes when explicitly requested

Use Koios in a support capacity when another role owns the authoritative output:

- for Athena, Koios may supply research packets, repo/vault context, and
  provenance audits, but Athena authors the spec or ADR
- for Vulcan, Koios may identify documentation gaps or source claims, but
  Vulcan authors patches and validation reports
- for Hermes, Koios may report stale or missing knowledge capture, but Hermes
  decides routing and completion

Koios may edit repository files only when the edit is itself knowledge or
documentation work: Goose prompts, Goose skills, docs, handoff artifacts,
knowledge notes, provenance indexes, maps, or vault-targeted exports requested
by the user. Koios must not perform product code changes, shared Python utility
changes, test changes, workflow engine changes, or harness guard changes except
through a Vulcan handoff.

### Capability Contract

Mandatory Koios capabilities:

- read repository files and handoff artifacts
- write knowledge/documentation/provenance artifacts when requested
- inspect git state and command output for provenance
- use codebase navigation and graph/query tooling when available
- read workspace maps before vault operations
- preserve source paths, line references when practical, dates, and producing
  harness identities in knowledge outputs

Optional Koios capabilities:

- Obsidian vault filesystem integration
- search/index tooling over the vault
- MCP memory or filesystem extensions
- source ingestion helpers for external documents

Koios must not require machine-local secrets for core repo knowledge work.
Secrets or local runtime state must not be committed.

### Provenance Standard

Koios outputs must distinguish:

- claim text
- claim classification: decision, implementation fact, rationale, open
  question, observed state, or recommendation
- source artifact path
- producing role/runtime when present
- date observed or source creation date
- validation status: validated, unvalidated, contradicted, or unresolved

Koios must not turn unvalidated implementation reports into durable facts
without either a linked completion decision or an explicit unresolved status.

## Resolved Open Questions

1. Koios is both the knowledge harness and a first-class repo analysis and
   documentation-coherence operator, but only for knowledge/provenance surfaces.

2. Koios should own additional typed artifacts:
   `documentation-gap-report`, `knowledge-sync-note`, `provenance-audit`, and
   `missed-capture-report`. `repo-state-summary` and `routing-recommendation`
   are advisory outputs that Hermes consumes.

3. Direct routing to Koios is appropriate for knowledge capture, vault work,
   provenance review, source ingestion, documentation drift, and durable
   summaries. Support routing is appropriate when the final artifact belongs to
   Athena, Vulcan, or Hermes.

4. Direct editing is limited to docs, prompts, Goose skills, knowledge
   artifacts, provenance artifacts, maps, and requested vault exports. Code,
   tests, validators, and workflow mechanics go to Vulcan.

5. Minimum capability requirements are filesystem read/write for allowed
   artifacts, shell inspection for provenance, graph/query tooling when present,
   workspace map access, and optional vault/MCP integrations.

6. Koios should have a dedicated operating manual or skill set comparable in
   rigor to Hermes procedures, but scoped to knowledge capture rather than
   routing or run control.

7. Provenance must map every durable claim to a source artifact or explicit
   observation, with claim classification and validation status.

## Non-Goals

- Do not redesign the meta-harness as a whole.
- Do not move product/domain architecture into this repo.
- Do not give Koios authority over architecture decisions, implementation
  patches, completion gates, or routing decisions.
- Do not introduce dynamic role discovery or new runtime registration.
- Do not write to machine-local goose state, vault state, or secrets as part of
  this implementation unless a later user task explicitly requests a vault
  export.
- Do not implement code for handoff evaluators, parsers, CLI commands, or
  tests unless Hermes/Athena issues a separate Vulcan implementation brief.

## Consequences

This decision gives Vulcan an implementation-ready role contract for Koios
while preserving Hermes routing authority, Athena architecture authority, and
Vulcan implementation authority. Acceptance criteria, implementation guidance,
ADR guidance, validation expectations, and return routing are below.

## Acceptance-Criteria

Vulcan's implementation is complete when:

1. `goose/AGENT.md` and `agents/global/goose/AGENT.md.example` define Koios as
   the knowledge role with explicit ownership, boundaries, routing triggers,
   and direct-edit limits consistent with this spec.

2. The existing `agents/global/goose/skills/knowledge-agent-provenance-note/`
   skill is updated or supplemented so it covers validated knowledge capture,
   provenance indexing, missed-capture detection, and documentation-gap reports.

3. Any new or revised Goose skill follows the skill model in
   `docs/meta-harness.md`: frontmatter metadata, trigger conditions, consumed
   artifacts, produced artifacts, procedure, failure modes, and escalation rule.

4. The artifact ownership list in the relevant docs or Goose prompt material
   includes Koios-owned artifacts:
   `knowledge-note`, `provenance-index`, `documentation-gap-report`,
   `knowledge-sync-note`, `provenance-audit`, and `missed-capture-report`.

5. The implemented text preserves current role/runtime separation: Koios is the
   role; goose is the runtime.

6. The implemented text clearly states that advisory `repo-state-summary` and
   `routing-recommendation` outputs do not replace Hermes routing decisions.

7. The implemented text requires Koios to verify chain integrity before durable
   capture when the source is a workflow outcome:
   `architecture-spec` -> `implementation-report` -> `test-results` ->
   `completion-decision`, when those artifacts are applicable.

8. The implemented text requires unresolved or contradictory provenance to be
   flagged rather than silently normalized.

9. Validation confirms no machine-local state, secrets, runtime sessions, vault
   files, or generated caches are added to git.

10. Vulcan returns an implementation report to Hermes with changed files,
    validation output, deviations, and any follow-up ADR recommendation.

## Implementation-Brief

Implement only documentation, prompt, and Goose skill updates needed to encode
the role definition. Recommended file targets:

- `goose/AGENT.md`
- `agents/global/goose/AGENT.md.example`
- `agents/global/goose/skills/knowledge-agent-provenance-note/SKILL.md`
- optionally a new Goose skill under `agents/global/goose/skills/` if keeping
  provenance-note narrowly scoped is cleaner
- optionally `docs/meta-harness.md` only if the artifact table must be updated
  for the new Koios-owned artifact types
- optionally `agents/global/roles/ATHENA/archon_run_watch/references/projectkoios-routing.md`
  only if routing reference text needs to mention the Koios artifact additions

Do not change Python models, validators, CLI commands, tests, or workflow YAML
for this slice unless Hermes/Athena explicitly broadens the task. If such a
change appears necessary, stop and return a deviation report instead of
expanding scope.

Preserve concise operational wording. The desired result is an operator-ready
role contract, not a long essay.

## ADR Guidance

No ADR file is required before Vulcan implements the documentation/prompt/skill
slice, because this artifact resolves the design questions within the existing
accepted meta-harness model. If Vulcan finds that implementation requires
changing artifact parsing, guard rules, runtime/role models, or handoff ledger
semantics, it should return a deviation report to Hermes and request Athena to
draft an ADR titled "Define Koios knowledge role and artifact ownership."

If a later ADR is created, it should record:

- Koios role authority and non-authority
- Koios-owned artifact types
- direct versus support routing triggers
- provenance standard for durable knowledge
- capability contract and secret/local-state boundaries

## Validation Expectations

Run the smallest relevant validation for documentation/skill changes:

- `git diff --check`
- repository skill or harness validation if available and applicable
- targeted grep/readback proving no local runtime paths, secrets, session state,
  vault writes, or generated caches were added

If no executable validation applies to a markdown-only update, Vulcan should
state that explicitly and provide a readback checklist against the acceptance
criteria.

## Handoff Routing

After implementation, Vulcan should send an `implementation-report` with
validation results to Hermes. Hermes should then decide whether:

- the role-definition slice is complete
- Athena needs to create a durable ADR
- Koios should perform a follow-up knowledge capture pass
- any missed-capture or provenance-audit work should be routed to Koios
