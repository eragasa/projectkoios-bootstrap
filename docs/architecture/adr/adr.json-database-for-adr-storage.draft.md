# ADR 20260702.121432Z: JSON ADR Storage Topology

## Status

draft
date: 20260702.121432Z

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

ADR filenames, title lookup, status, routing, and promotion behavior are all easier to query than free text. The repository needs a storage and indexing decision that balances git-friendly inspection with structured lookup.

The ADR schema already defines the canonical content model. The open question here is the storage topology: should the canonical ADR record live as JSON on disk, with Markdown as a render and SQLite as an index/cache, or should some other file shape own authority?

## Decision

Adopt JSON files on disk as the canonical ADR storage shape and treat Markdown as a render or presentation form.

The storage model should support:
- stable schema validation
- indexed lookup by title, status, and routing
- human-readable rendering for review
- promotion without losing the underlying structured record

SQLite may be used as an index/cache, but it must not become the primary authority unless explicitly promoted later.

## Consequences

- ADR content becomes easier to query and validate
- Markdown remains useful for review and diff-friendly rendering
- the repository can preserve a structured source of truth while still being legible
- index/cache behavior must be kept separate from canonical authority

## architecture-spec

This ADR defines the ADR storage authority, not just the filename convention.

The canonical record is JSON-shaped and should include the existing ADR schema fields. Markdown is derived from that record for review and navigation.

If SQLite is added, it is an index/cache layer only unless a later ADR changes its authority.

## acceptance-criteria

- ADRs can be represented as JSON without losing schema fields
- Markdown renderings remain available for review
- lookup by status/title/routing is simpler than grep-only inspection
- the authority boundary between source JSON and cache/index is explicit

## implementation-brief

If accepted, update the ADR creation and render guidance so new ADRs treat JSON as canonical and Markdown as a derived view.

verification_method: validate that a representative ADR can round-trip from JSON to Markdown and back without losing required fields.

## resolved_open_questions

- Should SQLite be cache-only or a persistent index?
- Should promoted ADRs still have Markdown-first review files?
- Should the repository migrate existing ADR drafts into JSON records later?

## non_goals

- changing the ADR schema itself
- removing Markdown from the review workflow
- forcing a database migration before the authority decision is settled

## validation_expectations

- a reviewer can identify the canonical source form
- the render stays consistent with the stored record
- lookup and promotion behavior remain explicit

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Storage-authority decision candidate for the ADR surface.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
