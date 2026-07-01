# AAR 20260701.120000: Repo-root AGENTS tradeoff review

## Scope
Reviewed the maintenance/isolation/discoverability tradeoffs of blanking repo-root `AGENTS.md` versus keeping shared defaults with deeper per-agent files.

## What happened
I checked the root `AGENTS.md`, `docs/agent-charter.md`, `docs/meta-harness.md`, and the progress artifact, then updated the progress note with the recommendation.

## Process issues
None observed.

## Proposed follow-up improvements
If the policy split changes later, add a short explicit convention for what must stay at repo root versus what may move to per-agent files.

## Candidate ADR or implementation topics
- Repo-root policy anchoring rules for `AGENTS.md`
- Per-harness config layering and precedence

## Current status
Complete
