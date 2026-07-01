# AAR 20260701.141133: Debt triage scoring

## Scope

Refined the debt register promotion path to use scoring plus human judgment.

## What happened

Recorded the user's preference for a scoring system that identifies the highest-leverage item for reasonable effort, then promotes to a draft by human judgment. Human prioritization can override review preferences. Updated the deep-interview skill to include a human override rule.

## Process issues

No durable process issue observed.

## Proposed follow-up improvements

- Define the concrete rubric dimensions for debt triage scoring.
- Consider whether the human override should be explicit per item or per batch.

## Candidate ADR or implementation topics

- Debt triage scoring rubric.
- Human override mechanics for review/prioritization.

## Current status

Debt triage now includes human override in addition to scoring.
