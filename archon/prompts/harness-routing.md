# Harness routing

When producing a plan for Project Koios, assign each step to exactly one harness.

## Harness definitions

- `archon/` (spec agent) — architecture decisions, ADRs, planning, design review, workflow authoring
- `opencode/` (code agent) — implementation, tests, validation, runtime debugging, consistency review
- `goose/` (knowledge agent) — research support, source ingestion, vault curation, note organization, UI-bootstrap knowledge tasks

## Rules

- Route planning and durable design records to `archon/`.
- Route code and validation work to `opencode/`.
- Route research and note-creation work to `goose/`.
- Treat workflows named `athena_<action-in-this-mode>` as Athena-owned
  workflows. Only Athena runs them in the harness sense; if Hermes, Codex, or
  another delegated operator invokes the CLI, the output is still an
  Athena-owned artifact and must preserve delegated-operator provenance.
- If a step mixes concerns, split it into separate steps.
- Always call out handoff points explicitly.

## Output requirement

For every implementation plan, include a harness assignment section with:
- step number
- owner harness
- expected artifact passed to the next harness
