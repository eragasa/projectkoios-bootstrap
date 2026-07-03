# AAR 20260703.134342: Meeting round control-boundary miss

## Scope
Story-prototype roundtable / meeting protocol behavior in Hermes intercom sessions.

## What happened
A meeting-style exchange was run with round prompts and single-word responses such as `Accepted`. The interaction drifted into a confusing control flow where a plain acceptance reply was treated as a live protocol action, and subsequent rounds appeared to open without a clearly separate moderator transition.

## Process issues
- Response text and control state were too loosely coupled.
- Acknowledgment of one round looked like it could trigger the next round implicitly.
- The protocol did not make the boundary between `reply to current round` and `open a new round` explicit enough.
- Intercom notifications were used as if they carried meeting authority.

## Proposed follow-up improvements
Introduce a hard control boundary for the story prototype:
- Every round MUST carry a meeting ID and round number.
- `Accepted` / `Rejected` / `Amend` replies MUST apply only to the current round.
- A round reply MUST NOT open the next round implicitly.
- Only the moderator MAY open a new round.
- Any new round MUST be explicitly announced as a separate action.
- Intercom remains notification-only and MUST NOT advance agenda state.

## Proposed amendment
Amend the prototype rules so that a response to a round is never interpreted as a command to continue the meeting. The moderator must publish a distinct transition message before the next round begins.

## Candidate ADR or implementation topics
- Meeting round state isolation
- Explicit round identifiers in inter-agent protocol messages
- Moderator-only round transitions
- Notification-only intercom semantics

## Current status
Problem isolated; amendment proposed.
