# ADR 20260630.121055: Build-mode default for Hermes

## Status

Draft

## Context

The plan-mode / build-mode safety rail was introduced to prevent
inadvertent changes during architecture and design sessions (Athena's
domain). When applied indiscriminately to Hermes, it creates friction:
pushing a commit, reading status, or running a validation command all
require a deliberate mode switch, adding ~3 rounds of back-and-forth
per session.

Hermes is the meta-harness operator. It does not produce architecture
specs or acceptance criteria — those belong to Athena. Its work is
predominantly execution: commands, edits, validation, orchestration.
Requiring Hermes to start in plan mode adds ceremony without protecting
any design artefact.

## Proposal

Hermes (pi) sessions default to build mode. Plan mode is only activated
when:

1. An explicit `plan` directive is issued by the user or a higher-level
   orchestrator.
2. The session is routing work to Athena — in which case plan mode
   protects the design boundary until Athena explicitly submits the
   spec.

The AGENTS.md session protocol will be updated to reflect this default.

## Consequences

- Hermes sessions start without mode friction — push, inspect,
  validate run immediately.
- Plan mode is preserved where it matters: Athena architecture
  sessions.
- The user must remember to opt into plan mode when doing design
  work through Hermes, but that's the same choice as routing to
  Athena in the first place.
- If this default is confusing, a `.opencode/` or local rule file
  can auto-switch based on the calling harness.
