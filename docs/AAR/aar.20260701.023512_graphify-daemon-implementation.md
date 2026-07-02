# AAR 20260701.023512: Graphify ingestion daemon implementation

## Scope

This AAR covers the Vulcan session that implemented the Graphify ingestion
daemon first slice per ADR adr.20260701.004713, routed by Hermes via the
handoff brief at docs/archive/handoffs/opencode/20260701.020850.

## What happened

- The session began with Hermes routing the accepted Graphify daemon
  ADR to Vulcan via a handoff brief. The brief embedded three user
  constraints: YAGNI, DataObject+ActivityObject modeling, and Colored Petri
  net compatibility.
- The user switched the harness role to Vulcan (build mode) to implement.
- Vulcan studied the existing CPN types (Marking, HandoffArtifact, Violation,
  guards, topics projection) and the Graphify CLI interface.
- Vulcan identified that the existing Marking type was hardcoded to
  HandoffArtifact, preventing daemon token reuse. A minimal refactor
  generalized Marking to Marking[T] (Generic) with a HandoffMarking alias,
  enabling CPN type reuse without a parallel type hierarchy.
- Vulcan implemented the daemon across 8 modules (data, activities,
  exclusions, watcher, scheduler, graphify_runner, ollama, publisher, daemon)
  plus the CLI subcommand (ingestion.py).
- 47 new tests were written covering exclusions, watcher, scheduler,
  activities, publisher, ollama degradation, daemon run cycle, and the
  source-tree safety gate.
- All validation passed: 150 tests (103 existing + 47 new), ruff clean,
  mypy clean, graphify rebuilt.

## Process issues

- **Test collection pattern required three underscore groups.** The
  `pyproject.toml` pattern `__*__*__*.py` requires three double-underscore
  groups. Initial test files named with only two groups (e.g.
  `__Watcher__tests.py`) were not collected. Renaming to
  `__Watcher__scan_mtimes__tests.py` fixed collection. This is a minor
  convention friction that could be documented in skill infrastructure
  conventions.
- **Ollama is running on the development machine.** The test
  `test__generate_chunk_cards__degrades_when_ollama_unreachable` initially
  failed because Ollama was actually reachable on localhost:11434, causing
  the degradation path not to fire. The test was fixed by mocking
  `_check_ollama` to return False. This is correct test isolation practice
  but worth noting: tests that assume external services are absent should
  always mock, not rely on environmental state.
- **Safety warnings needed metadata propagation.** The source-tree safety
  gate added warnings to the context after the publisher had already
  finalized the metadata. The fix was to propagate post-publish safety
  warnings into the metadata object. This was a minor control-flow issue
  caught by tests.

## Proposed follow-up improvements

- Document the three-group test naming convention (`__Class__method__case.py`)
  more explicitly in skill infrastructure conventions or AGENTS.md, so future
  Vulcan sessions don't hit the collection gap.
- Consider adding a daemon guard (CPN guard function) that fires when the
  daemon's own run mutates the source tree — currently this is a warning,
  not a violation. A future ADR could promote it to a guard rule in
  harness/daemon/ if the daemon proves to be a recurring source-tree risk.
- The Marking generic refactor is a clean minimal change but should be
  validated by Athena for CPN model consistency. No ADR change is required
  yet, but if daemon tokens evolve, the CPN model ADR
  (adr.20260630.042202) may need an annotation.

## Candidate ADR or implementation topics

- No new architecture ADR is required for this implementation slice.
- Candidate follow-up: a daemon guard module (harness/daemon/guards.py) if
  the daemon's safety behavior needs to be machine-checkable through the CPN
  evaluator, not just warning-level.

## Current status

This AAR is a process observation artifact. The implementation is complete
and validated. Hermes should review the implementation report at
docs/archive/handoffs/opencode/20260701.023420 against the ADR acceptance
criteria and validation expectations before marking the daemon ADR as
Completed.
