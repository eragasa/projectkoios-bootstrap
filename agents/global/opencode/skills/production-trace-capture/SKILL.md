---
name: production-trace-capture
adr_binding:
  - docs/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md
description: |
  Capture the delta between agent-produced artifacts and human-accepted versions for style training.
  Bound to ADR: adr.20260702.144539_agent-production-trace-and-training-capture.draft.md.
metadata:
  agent: opencode
  harness_role: producer
  consumes:
    - agent-artifact
    - human-feedback
  produces:
    - production-trace
    - style-signal
---
## When to use this skill

During spike or implementation work when the human will review VULCAN-produced
artifacts and modify them. Before and after the review cycle, capture the initial
agent output and the final accepted version, then diff them to extract style signals.

## Agent responsibility

VULCAN (opencode) snapshots its own output before submitting for review and
captures the final accepted version after human modification. The diff between
them is the training signal. Do not guess which changes are style preferences;
the human writes the style-signal list during review.

## Inputs

- `agent-artifact` — files produced by VULCAN before human review
- `human-feedback` — the human's modifications or acceptance

## Procedure

1. Before presenting work for review, snapshot all produced files into a new
   step directory under `snapshots/<snapshot-timestamp>/steps/NN/`.
2. Record the turn in `step-log.md`: Who, What, Where, Why.
3. After the human reviews and produces their version, snapshot into the next
   step directory and log.
4. Repeat for each agent-human turn until the artifact is accepted.
5. After the final step, extract style signals from the full sequence and
   write `signals.json`.
6. Deltas are never stored — compute `git diff --no-index steps/NN/ steps/NN+1/`
   on demand when needed.

## Output artifact

- `production-trace` — JSON document capturing the trace metadata
- `style-signal` — the style-signals list from the trace, available for future
  orientation

## Failure modes

- No snapshot taken before review — cannot reconstruct the initial state; skip
  trace and start fresh next phase
- Diff is empty — no training signal; note zero-change in trace and move on
- Style signals list is empty after non-trivial changes — prompt the human to
  articulate at least one preference
