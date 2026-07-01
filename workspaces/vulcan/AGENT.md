# Vulcan workspace

Vulcan is the implementation workspace. It owns code changes, tests, and validation output.

## Instructions

Use this workspace when the task is implementation-focused and the architecture or plan is already clear enough to build against. Keep architecture changes out of this workspace unless Hermes explicitly routes them here.

- Read the plan or ADR before making changes.
- Read `inbox/` first for new work.
- Put implementation replies in `outbox/`.
- Keep implementation and validation artifacts together.
- Do not edit architecture notes from this workspace.
- Keep changes tied to the accepted or routed work in front of you.

## Local workspace files

Vulcan keeps the working surface for implementation and validation here. Use the files to track what is active, what has been done, and what must be handed back.

- `state.md`
- `active.md`
- `inbox/`
- `outbox/`
- `sessions/`
- `handoffs/incoming/`
- `handoffs/outgoing/`
- `decisions/`

## Mail system

Vulcan receives work through inbox messages and returns results through outbox notes. Hermes delivers the mail between workspaces, so keep the notes short and easy to route.

- Read `inbox/` first.
- Write outgoing notes to `outbox/`.
- Keep implementation replies short, explicit, and provenance-friendly.
- Include validation results with the implementation reply when possible.

## Canonical references

These shared references define the repo boundary and the architecture surface Vulcan should respect.

- `docs/agent-charter.md`
- `docs/workspaces.md`
- `docs/architecture.00.md`

## Vulcan-specific bootstrap guidance

Vulcan is the implementation workspace, so it should stay focused on code changes, tests, and validation output once the plan is clear enough to build. Architecture changes stay out of this workspace unless Hermes explicitly routes them here, and every implementation reply should be short, explicit, and easy for Hermes to route back.

- Read the plan or ADR before making changes.
- Keep implementation and validation artifacts together.
- Do not edit architecture notes from this workspace.
- Keep changes tied to the accepted or routed work in front of you.
- Include validation results with the implementation reply when possible.

## Vulcan workflow emphasis

Vulcan should treat implementation as a closed loop: understand the accepted plan, make the smallest coherent change, validate it, and report back with evidence. When the work is still exploratory or under-specified, route it back to Athena or Hermes instead of widening scope inside the implementation workspace.

- Start from an accepted plan, ADR, or routed implementation brief.
- Keep changes small and coherent.
- Validate before handing work back.
- Escalate ambiguity instead of inventing architecture.
- Keep the workspace centered on implementation output, not discovery.

Vulcan is the implementation workspace, so it should stay focused on code changes, tests, and validation output once the plan is clear enough to build. Architecture changes stay out of this workspace unless Hermes explicitly routes them here, and every implementation reply should be short, explicit, and easy for Hermes to route back.

- Read the plan or ADR before making changes.
- Keep implementation and validation artifacts together.
- Do not edit architecture notes from this workspace.
- Keep changes tied to the accepted or routed work in front of you.
- Include validation results with the implementation reply when possible.
