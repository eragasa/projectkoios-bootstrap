# AAR 20260702.004943: ADR Filenames and JSON Storage Idea

## Scope

This session added draft ADR filename guidance and a new incubator idea note about JSON/SQLite storage.

## What happened

- Introduced a draft ADR naming rule: `adr.<name>.md` for active notes, `adr.<name>.<status>.md` for non-active notes.
- Repointed the architecture index and related guidance to the new draft filename style.
- Created an incubator note brainstorming JSON storage with SQLite as either index or source of truth.

## Process issues

- A temporary stray root-level `adr/` directory appeared during filename moves and was removed.

## Proposed follow-up improvements

- Decide which statuses count as non-active for filename suffixes.
- Clarify whether active ADRs should lose the date slug entirely or retain it in content only.
- Define where canonical JSON ADR instances would live if the schema becomes executable storage.

## Candidate ADR or implementation topics

- ADR filename promotion rules
- JSON ADR storage layout
- SQLite index/cache model for ADRs

## Current status

Draft guidance and brainstorming notes created; repository links were updated.
