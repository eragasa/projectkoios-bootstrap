# ADR 20260702.144539: Agent Production Trace and Training Capture

## Status

Draft

## Context

Origin: user request
From: VULCAN
Acting-As: VULCAN
Scope: projectkoios-bootstrap agent-training surface
Repository: projectkoios-bootstrap
Delegated-Operator: opencode
Architecture-Domain: software

The new JSON document database and ingestor under `spike/json-database-and-ingestor/`
needs a training signal to calibrate agent output to human-preferred style. Without
capturing the delta between what an agent produces and what the human accepts, each
session starts from the same generic style baseline with no memory of past corrections.

The immediate motivation is coding style: the VULCAN operator wants to review Phase P1
artifacts and extract preferred conventions from the diff. But the same pattern applies
to any agent-produced artifact — specs, ADRs, AARs, plans, reports.

Every agent session produces a sequence of turns. Each turn produces
a snapshot and a decision. The sequence itself — not just the final delta —
is the training signal. This ADR defines how to capture it durably.

## Decision

Establish an **agent production trace** that records every turn in the
agent-human iteration as an incremental step.

The snapshot set lives under the spike:

```
snapshots/<snapshot-timestamp>/
├── step-log.md     ← authoritative provenance: who, what, when, where, why
├── signals.json    ← style signals extracted after final acceptance
└── steps/
    ├── 00/plan.md
    ├── 01/plan.md
    └── ...
```

The step-log records one entry per turn:

```
## Step 00 — 2026-07-02T14:45:39
- Who: agent-VULCAN
- What: produced initial plan.md
- Where: steps/00/plan.md
- Why: first draft of JSON DB spike implementation phases

## Step 01 — 2026-07-02T15:00:00
- Who: user-eugene
- What: revised plan.md — reordered phases, tightened scope
- Where: steps/01/plan.md
- Why: phases were too granular; preferred broader boundaries

## Step 02 — 2026-07-02T15:10:00
- Who: agent-VULCAN
- What: updated plan.md — consolidated P1-P2, moved SQLite to appendix
- Where: steps/02/plan.md
- Why: applied user's preferred phase boundary width

## Step 03 — 2026-07-02T15:15:00
- Who: user-eugene
- What: accepted plan.md (no changes)
- Where: steps/03/plan.md
- Why: structure matches intent
```

Each turn materializes as a numbered step directory. Who performed the
turn is recorded in step-log.md, not in the directory name. Deltas are
not stored — `git diff --no-index steps/NN/ steps/NN+1/` can be computed
on demand when a diff is needed.

The snapshot set ends with the accepted artifact. step-log.md is the durable
record. signals.json is extracted from the full sequence after acceptance.

This is not an automated system. It is a manual capture convention that
VULCAN performs during spike implementation. The discipline of writing
the trace forces the reviewer to articulate what changed and why.

## Consequences

- Each spike phase produces a trace that encodes style preference
- Traces accumulate over time and form a training corpus for agent calibration
- The trace is stored as a JSON document, so it follows the same database path
  as other documents and can be queried, listed, and ingested
- The capture discipline is manual at first; automation is a later concern
- Reviews take slightly longer because the reviewer must write the trace summary

## Architecture spec

The production trace is a first-class document type (`DocumentType.PRODUCTION_TRACE`)
in the JSON document database. It uses the same store interface and CLI tooling
as ADRs and AARs. This ensures all agent training signals live in the same queryable
backbone as the documents they describe.

## Acceptance criteria

- A trace directory exists with `step-log.md`, `steps/`, and `signals.json`
- Each step in `step-log.md` references a valid `steps/NN/` directory
- The `Who` field distinguishes agent turns from human turns
- Style signals are a human-authored list, not machine-parsed
- A trace links to the session, agent identity, and artifact type

## Implementation brief

See `spike/json-database-and-ingestor/plan.md`. The PRODUCTION_TRACE
document type is added in Phase P1 alongside ADR and AAR.

The snapshot mechanism is first implemented by this ADR's own procedure:

- **Snapshot:** `spike/json-database-and-ingestor/snapshots/snapshot.20260702.144539/`
- **Step 00 — agent-VULCAN:** `steps/00/plan.md` (initial plan draft)
- **step-log.md:** provenance for all steps
- **signals.json:** extracted after final acceptance

This first snapshot set captures coding style and planning conventions from the JSON
database spike. Each subsequent spike phase creates a new snapshot under the same
`snapshots/` directory with an incremented timestamp identifier.

## Resolved open questions

- Should the trace use initial/final snapshots or iterative step-log? — Step-log with
  per-turn snapshots; initial/final loses the iterative process.
- Should deltas be stored or computed? — Computed on demand; deltas are compression
  of the step sequence, not the durable record.
- Should traces be auto-generated? — Not in the first slice; manual capture builds
  the habit of articulating preferences.

## Non-goals

- Automating style extraction from diffs
- Building a training pipeline or ML system
- Capturing traces for every session (opt-in, spike-only)
- Replacing human judgment in the review loop

## Validation expectations

- A reviewer can identify which trace corresponds to which phase
- The step-log.md is readable by a human and records who/what/when/where/why
- The style signals section is non-empty after a non-trivial review

## Routing

- Owner: VULCAN
- Next phase: proposed
- Notes: Training-capture decision for the spike implementation surface.

## Links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
