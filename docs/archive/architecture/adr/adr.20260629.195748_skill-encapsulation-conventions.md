# ADR 20260629.195748: Skill encapsulation conventions

## Status

historic

## Context

Skills in `.claude/skills/` and `agents/global/roles/ATHENA/archon_run_watch/`
reference harness-specific directory paths (`.archon/`, `archon/workflows/`,
`docs/archive/handoffs/pi/`) making them non-portable — a skill designed for one harness
cannot be trivially reused by another without manual path edits.

The `archon_run_watch` skill also introduced a reusable pattern: named
module-level functions (`run_archon()`) that can be swapped for testing, which
is likely to repeat across future skill scripts that interact with CLI tools
(archon, git, pi, goose).

## Decision

Skills resolve harness-specific paths through one of two mechanisms, chosen
by context:

1. **Config variables** — skills accept paths via environment variables or a
   config file, rather than hardcoding harness-specific locations.
2. **Relative path resolution** — skills derive harness identity from their
   own location in the filesystem (e.g., detecting whether they sit under
   `ATHENA/`, `HERMES/`, etc.).

For CLI-command wrappers, formalise the swappable-function pattern into a
shared utility in `projectkoios.bootstrap.harness` so that future skill
scripts that shell out to archon, git, pi, or goose can reuse it instead of
reinventing mock support.

## Consequences

- Current skills continue working during migration (no breaking changes).
- No directory renames are required.
- Future skills can import the shared CLI-runner utility instead of writing
  their own mock-injection boilerplate.
- The shared utility must remain optional — skills can still use `subprocess`
  directly for simple cases.
- This does not yet mandate the three-layer asset model (global/local/runtime)
  — that is a separate ADR (`adr.20260630.002151`).

## Source

This ADR distills content from:
- `docs/archive/handoffs/archon/20260629.195748_skill-encapsulation-recommendation.md`
- `docs/archive/handoffs/archon/20260630.150000_skill-impl-recommendations.md` (items 2-3)
