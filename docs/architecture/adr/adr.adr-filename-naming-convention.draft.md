# ADR 20260702.004300: ADR Filename Naming Convention

## Status

draft

## Context

Origin: user request
From: Hermes
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

Current ADR filenames are harder to scan than they need to be. The repository
needs a filename convention that makes draft vs active status obvious without
relying on timestamps in the path.

## Decision

Use `adr.<name>.md` for active ADRs and `adr.<name>.<status>.md` for non-active
ADRs.

Rules:

- `name` is a kebab-slug derived from the ADR topic
- active ADRs omit the status suffix
- draft and other non-active ADRs include their status suffix
- filename status should match the ADR `## Status` value

## Consequences

- draft ADRs are easy to recognize in the filesystem
- active ADRs get a cleaner stable filename
- filename intent matches lifecycle intent
- renames are required when an ADR changes status

## architecture-spec

This ADR defines the filesystem naming rule for ADR Markdown files on the
bootstrap architecture surface.

## acceptance-criteria

- Draft ADR filenames include `.draft`
- Active ADR filenames omit the status suffix
- The naming rule is visible in the architecture index guidance
- Existing links can be updated without ambiguity

## implementation-brief

If accepted, update the architecture index guidance and ADR creation guidance
so new ADR files follow the new filename pattern.

## resolved-open-questions

- Which statuses besides draft count as non-active for filenames?
- Should archived ADRs keep their original filenames?
- Should promotion tooling rename files automatically?

## non-goals

- Renaming every historical ADR immediately
- Changing the ADR JSON schema
- Changing ADR title conventions

## validation-expectations

- New draft ADRs can be created with a `.draft` suffix
- A promoted ADR can be renamed to the active filename form
- The naming rule is simple enough for humans and tooling

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Filesystem naming guidance for the ADR surface.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- KOIOS: Clear rule, but the migration path for existing filenames still needs a concrete policy.
- KOIOS: Decide whether historic/archive names preserve their original filenames or get normalized on promotion.
