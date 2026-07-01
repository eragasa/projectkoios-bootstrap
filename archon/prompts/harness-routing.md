# Harness sandbox message delivery

When producing a plan for Project Koios, assign each step to exactly one
recipient harness sandbox. Sending work means putting a message in that
recipient sandbox.

## Harness definitions

- `archon/` (spec agent) — architecture decisions, ADRs, planning, design review, workflow authoring
- `opencode/` (code agent) — implementation, tests, validation, runtime debugging, consistency review
- `goose/` (knowledge agent) — research support, source ingestion, vault curation, note organization, UI-bootstrap knowledge tasks

## Rules

- Send planning and durable design records to the `archon/` sandbox.
- Send code and validation work to the `opencode/` sandbox.
- Send research and note-creation work to the `goose/` sandbox.
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
