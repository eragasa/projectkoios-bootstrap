---
name: production-trace-capture
adr_binding:
  - docs/architecture/adr/adr.20260702.144539_agent-production-trace-and-training-capture.draft.md
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

1. Before presenting work for review, snapshot all produced files into a
   `traces/initial/` directory under the spike or phase directory.
2. After the human reviews and modifies, snapshot the final accepted files
   into `traces/final/`.
3. Run `git diff --no-index traces/initial traces/final > traces/diff.delta`.
4. Create a trace document with fields: trace_id, session_id, agent_identity,
   artifact_type, produced_at, accepted_at, paths, summary, style_signals.
5. The human supplies the `style_signals` list and `summary`.
6. Store the trace document in the spike directory.

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
