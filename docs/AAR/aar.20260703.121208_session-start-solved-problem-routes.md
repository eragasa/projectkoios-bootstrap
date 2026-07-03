# AAR 20260703.121208: Session-start solved-problem routing

## Scope
HERMES / pi session in `projectkoios-bootstrap`.

## What happened
The user asked where a solved problem should go, then clarified that the question referred to the issues just handled in this session. I identified the durable home as `docs/AAR/` and drafted this report.

The session also validated startup state before proceeding:
- working tree clean
- no active workspace state in `state.md` or `active.md`
- no running or paused Archon workflow runs
- no draft ADRs, incubator notes, or spikes found

## Process issues
The initial answer path was too abstract and required user clarification before landing on the concrete session-specific lesson.

## Proposed follow-up improvements
- Treat “what did we just solve?” as an AAR candidate by default when no code, ADR, or knowledge artifact is involved.
- Keep the session-start check explicit: git status, Archon runs, then draft/incubator surfaces.
- When the user asks for a durable home for a solved problem, answer with the artifact type first, then offer to draft it immediately.

## Candidate ADR or implementation topics
- None from this session.
- Possible workflow note: default routing rules for solved-session lessons.

## Current status
Captured as an AAR only. No repo behavior or architecture changed.
