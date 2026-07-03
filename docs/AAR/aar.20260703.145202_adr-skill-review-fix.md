# AAR 20260703.145202: ADR skill review fixes

## Scope
Patched the new `spec-agent-scope-review` skill and the skill register after Hermes review.

## What happened
A review identified a stale register note about the ADR template contract and a boundary overlap between scope review and acceptance-criteria derivation. I updated the docs to reflect the real ADR path and narrowed the scope-review skill to preliminary handoff notes.

## Process issues
- The skill register still carried stale “does not exist” wording after the ADR file existed.
- The scope-review skill blurred into acceptance-criteria ownership.

## Proposed follow-up improvements
- Keep the skill register synchronized with ADR file renames/moves.
- Make scope-review vs acceptance-criteria ownership explicit in future skill drafts.

## Candidate ADR or implementation topics
- None.

## Current status
Fixed in docs; no code changes were made.
