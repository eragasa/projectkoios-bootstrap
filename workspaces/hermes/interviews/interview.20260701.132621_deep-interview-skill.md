# Deep interview skill design

## Status

draft

## Problem statement

Define the control surfaces for the Project Koios meta-harness using concrete
scenario cards rather than abstract taxonomy alone:
- ADRs as explicit architecture decisions
- architectural policies as vision surfaces that define values, priorities, and target assumptions for how the system evolves
- coding implementation surfaces as executable behavior
- Markdown control-surface files as durable operational guidance
- review mechanics as system-wide evaluation and improvement loops

The interview skill must help classify these surfaces, define their boundaries,
and determine how they are reviewed, prioritized, and improved over time.

## Scenario cards

1. Policy changes agent personalities and motivations, which then shifts long-term goals and priorities
2. A debt item becomes a control-surface change
3. A control-surface change becomes an ADR candidate
4. Markdown is either a control surface or a rendered view
5. Review discovers cross-surface incoherence and improvement debt

## Question prioritization

Questions should be prioritized by domain and leverage, and questions in the same
domain should be combined unless separating them changes the answer materially.

## Status of scenario domains

### Policy / agent-motivation propagation

Resolved: policy should percolate by changing agent personalities and motivations,
which then shifts goals and priorities.

### Markdown control/render boundary

Resolved: Markdown is a hybrid control/render surface.

### Review mechanics

Resolved: review should prioritize coherence/alignment plus improvement/debt discovery.

### Debt triage and promotion

Resolved: debt items should be scored by a weighted rubric, combined/split as needed,
and promoted by human judgment into implementation tasks, control-surface work, or ADR candidates.

### Policy surface content

Resolved: policy is a vision surface consisting of values and target assumptions,
with review rules delegated to review mechanics unless needed.

## Active queue

0 active questions.

## Skill assessment

The deep-interview skill is directionally right but too verbose and too recursive.
It should be tightened before heavy reuse.

### Recommended revisions

1. Hard cap active questions per domain.
2. Require scenario cards before any abstract question.
3. Auto-merge same-domain questions aggressively.
4. Force a report/summary artifact when the queue empties.
5. Add a stop condition when answers converge.

## Next action

If this skill is reused, revise it with the five improvements above before the next session.
