# AAR 20260702.173801: JSON DB Spike, Production Trace ADR, and Plan Decomposition

## Scope

VULCAN session in `projectkoios-bootstrap` covering JSON document database spike
creation, agent production trace ADR, skill registration, snapshot mechanism
design, and plan decomposition.

## What happened

- Created `spike/json-database-and-ingestor/` with `spike.md` and `plan.md`
- Wrote draft ADR `adr.20260702.144539_agent-production-trace-and-training-capture.draft.md`
  defining the production trace / snapshot mechanism
- Created and registered global skill `production-trace-capture` in the skill register
- Restructured spike path from dated `spike/20260702/json-database-and-ingestor/`
  to kebab-slug `spike/json-database-and-ingestor/` (date removed — snapshotter owns it)
- Evolved trace model from `initial/` + `final/` to iterative `steps/NN/` with
  `step-log.md` and `signals.json`
- Renamed `traces/` to `snapshots/` for descriptiveness
- Decomposed `plan.md` into 9 files: overview + 8 phase files
- Snapshotted step-00 (initial plan) and step-01 (decomposed plan) into the
  snapshot directory
- User pushed a strategic question: prompt-engineer the style filter to the
  front vs LoRA fine-tune to the back. Resolution: front-load via prompt/process
  engineering, treat residual as the signal for whether fine-tuning is needed

## Process issues

- Initial spike path used a dated directory (`spike/20260702/...`) which mixed
  spike identity with trace timestamps. User corrected: spike path is kebab-slug
  only, the snapshot owns the date.
- Initial trace model used `initial/` + `final/` which lost the iterative
  process. User corrected: step-log with numbered steps, deltas computed on
  demand as compression.
- `agent-VULCAN/` subdirectory in step paths was unnecessary — `step-log.md`
  already records who. Removed.
- `trace` as a directory name was not descriptive. Renamed to `snapshots/`.
- Agent (me) repeatedly proposed structures that needed correction. The
  correction pattern: too much ceremony in directory structure, not enough
  trust in the flat file + log combination.
- Graphify update initially refused to overwrite (node count shrink). Required
  `--force` flag.

## Proposed follow-up improvements

- Document the spike path convention (`spike/<kebab-adr-name>/`) in AGENTS.md
  or an ADR so future spikes follow the same rule
- Document the snapshot directory convention
  (`snapshots/<snapshot-timestamp>/steps/NN/`) in the ADR more explicitly
- Add a `projectkoios snapshot` CLI verb that automates the snapshot procedure
  (copy files, append step-log entry, bump counter)
- Consider whether the skill `production-trace-capture` needs updating to match
  the final snapshot model (it was partially updated but may still have
  inconsistencies)

## Candidate ADR or implementation topics

- Spike directory naming convention (kebab-slug, no date)
- Snapshot directory structure as canonical training-capture storage
- Prompt-engineering-first style calibration policy (front-load, not back-load)
- JSON document database implementation ADRs (per-phase, as user requested)

## Current status

Session complete. All work committed and pushed to `origin/master` at `0be59a8`.
Graphify updated. No running Archon runs. Working tree clean.
