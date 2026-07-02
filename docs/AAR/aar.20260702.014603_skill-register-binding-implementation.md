# AAR 20260702.014603: Skill register binding implementation

## Scope
Implementation of ADR skill-register-and-adr-binding-policy: skill register enrichment, machine-readable ADR bindings, skill template creation, dangling reference cleanup.

## What happened
- Enriched `docs/skills/skill-register.md` with owning harness, purpose, and binding note columns for all 20 entries
- Added `adr_binding` machine-readable YAML field to all 16 committed SKILL.md files
- Removed dangling `adr.adr-template-contract.md` references from 3 skill files (file does not exist)
- Created `docs/templates/skill.template.md` as a reusable template with binding conventions
- Updated register notes to require `adr_binding` frontmatter field
- Refreshed Graphify graph

## Process issues
- `adr.adr-template-contract.md` is referenced in `docs/architecture/architecture.00.md` and 3 skills but has no file at the expected path. Removed from skill bindings and noted in the register. The architecture index still references it — that's an Athena/HERMES concern.
- 4 skills in the register (condense, deep-interview, graphify, projectkoios) reference paths outside `agents/global/` that don't exist in this repo. The register now accurately documents those as local-only skills.

## Proposed follow-up improvements
- Create the missing `adr.adr-template-contract.md` ADR or remove it from the architecture index
- Audit local-only skills (condense, deep-interview, graphify, projectkoios) to ensure their local `SKILL.md` files also carry the `adr_binding` field

## Candidate ADR or implementation topics
- None discovered.

## Current status
Completed.
