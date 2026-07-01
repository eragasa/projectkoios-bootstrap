# ADR 20260702.030000: Implementation Brief Verification Method

## Status

draft

## Context

Origin: implementation gap
From: VULCAN
Acting-As: VULCAN
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Delegated-Operator: opencode
Architecture-Domain: software

Implementation briefs in the current lifecycle reach Vulcan with no defined done signal. Vulcan builds against intent, but cannot validate whether the result matches the architecture expectation. That forces rework when the implementation brief and the delivery drift apart.

The established workflow is `idea → spike → ADR → implementation brief → iterative implementation`, but the brief-to-implementation boundary has no verification gate.

## Decision

Add one required field to every implementation brief: `verification_method`.

The field must name how Vulcan validates the implementation against the architecture intent. Examples:

- "Run `pytest tests/foo.py` — all 3 cases must pass"
- "AST-based: verify `class Foo` implements interface `Bar` without adding unused imports"
- "Manual inspection: reviewer confirms outputs match the table in ADR N"
- "Graphify update + compare: run `/graphify update .` and check `graphify-out/graph.json` contains the expected nodes"

No other fields are added. No schema change. The verification method is prose, not a structured constraint.

## Consequences

- Vulcan has an explicit done signal before building
- The architect writes one extra line per brief — minimum viable overhead
- Verification failures become inspectable: they show a mismatch between intent and output, not just a vague completion gap
- Rework drops because both sides agree on the gate before implementation starts

## architecture-spec

The implementation brief is currently a prose section in the ADR draft. The `verification_method` field is an additional prose subsection, appended at the end of the existing `implementation-brief` section.

No new schema fields, no new files, no validation tooling. The verification method is a human-readable note until actual rework costs justify formal enforcement.

## acceptance-criteria

- Every implementation brief in the repo includes a `verification_method` subsection
- A reviewer can tell from the brief alone whether the implementation can be validated
- The field is short enough that adding it does not discourage writing briefs
- The field reduces rework by making the done signal explicit

## implementation-brief

Update the ADR template guidance to include a `verification_method` subsection in the implementation-brief section. Existing briefs are grandfathered; only new briefs require it.

## resolved-open-questions

- Should `verification_method` be optional? No — if it is optional it will be omitted and the gap remains.
- Should the field be structured (checkbox, test path, etc.)? No — YAGNI; prose handles all current cases.

## non-goals

- Defining every possible implementation brief section
- Changing the ADR JSON schema
- Creating verification tooling or CI gates
- Replacing the ADR lifecycle

## validation-expectations

- A new implementation brief with a clear verification method lets Vulcan start building with a known done signal
- The field reduces the number of briefs that reach implementation without a completion definition

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Process/implementation surface; adds verification gate to the existing ADR lifecycle.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- VULCAN: Proposed from implementation experience — the missing done signal is the only concrete gap observed so far. No other brief fields fail YAGNI.
- ATHENA: The field should stay short enough to read at a glance; if the verification note grows into a mini-plan, it belongs in `docs/plans/` instead.
