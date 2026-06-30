# ADR 20260630.150000: Skill infrastructure conventions

## Status

Draft

## Context

During implementation of the `archon_run_watch` skill, five cross-cutting
issues emerged that affect how future skills are structured:

1. **Directory naming** — Skill directories use hyphens (`koios-handoff-operator`),
   which prevents them from being valid Python packages (imports require
   underscores).
2. **Header types** — `projectkoios.bootstrap.harness.headers` exports a regex
   and pure function returning `dict[str, str]`, with no typed header model.
   Callers cannot distinguish optional from required fields at the type level.
3. **Ledger foundation** — The shared header module is the natural foundation
   for the handoff-ledger projection, but its design feeds into the ledger
   model.

## Decision

1. **Skill directory naming** — Keep hyphens for display/convention. Scripts
   are invoked via subprocess or path manipulation, not imported as packages.
   Tests use `sys.path.insert` (accepted boilerplate). This may be revisited
   if skill scripts grow complex enough to warrant their own package.

2. **Header types** — Defer adding a typed header model to `headers.py` until
   the handoff-ledger projection defines its own message schema. The
   `headers.py` function remains the single source of header parsing, but its
   return type stays `dict[str, str]` for now. When the ledger projection
   matures, a shared typed model can be introduced alongside the existing
   function.

3. **Ledger projection model placement** — The projection model (message
   records, transitions, marking) lives as DataObjects in `harness/data/`
   alongside `HandoffArtifact`, not in a separate module. This keeps related
   types co-located and avoids premature module proliferation.

## Consequences

- Skill tests consistently use `sys.path.insert` + `# noqa: E402` — every
  skill test needs this boilerplate until the convention changes.
- `headers.py` stays simple and untyped until the ledger projection provides
  a concrete schema to type against.
- New DataObjects for the ledger projection go in `harness/data/` — the
  existing `artifact.py`, `marking.py`, and `violation.py` are the pattern.

## Source

This ADR distills content from `docs/archive/handoffs/archon/20260630.150000_skill-impl-recommendations.md`
(items 1, 4, 5).
