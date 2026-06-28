# Harness boundaries

Operational routing guide for the three-harness meta-harness.

## Purpose

Use this document to decide which harness should own a task and what artifact should be handed to the next harness.

## Ownership

| Harness | Owns | Does not own |
|---|---|---|
| `archon/` | architecture decisions, ADRs, feature plans, workflow definitions, prompt assets, cross-repo planning | direct implementation in component repos, interactive test/debug loops, vault curation |
| `opencode/` | implementation, refactors, tests, validation, runtime investigation, consistency review | architecture governance, long-lived planning records, vault/note management |
| `goose/` | vault curation, source ingestion, note linking, research support, UI-bootstrap knowledge tasks | code implementation, validation gates, architectural approval |

## Routing rules

### Send work to Archon when
- the output is a plan, ADR, design review, or workflow definition
- the task spans multiple repos or requires explicit ownership/routing
- the next step should produce a durable decision in `architecture/`

### Send work to opencode when
- the task changes code, tests, configs, or validation behavior
- the user wants implementation, debugging, or runtime verification
- an Archon plan is already approved and needs execution

### Send work to Goose when
- the task is primarily research, note curation, ingestion, or vault organization
- source material must be extracted into notes before planning or implementation
- the deliverable is knowledge structure rather than executable code

## Handoff artifacts

### Archon → opencode
Archon should hand off a work order containing:
- problem statement
- scope and non-goals
- target repos and file paths
- implementation steps
- validation expectations
- open questions/blockers

Default location: issue comment, workflow output, or a markdown artifact agreed for the task.

### Archon → Goose
Archon should hand off:
- research question
- source locations or missing context
- desired note/output format
- whether results are exploratory or decision-supporting

### Goose → Archon
Goose should return:
- curated notes or summaries
- linked sources
- unresolved ambiguities
- recommendation on whether planning can proceed

### opencode → Archon
opencode should return:
- implementation status
- validation results
- deviations from plan
- new architectural questions that require a decision

## Precedence

If a task mixes planning, implementation, and knowledge work:
1. `archon/` defines the plan and routing
2. `goose/` fills missing research context if needed
3. `opencode/` executes implementation
4. `archon/` records follow-up decisions if implementation changes the design

## Guardrails

- Do not let Archon absorb normal implementation work.
- Do not let opencode create durable architecture policy without Archon review.
- Do not let Goose mutate code as a substitute for implementation.
- Keep `maps/` authoritative for workspace layout; this file governs routing, not repo locations.
