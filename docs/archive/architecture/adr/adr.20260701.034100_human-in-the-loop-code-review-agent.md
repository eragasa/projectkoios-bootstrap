# ADR 20260701.034100: Human-in-the-loop code review agent

## Status

historic

## Context

Origin: user request
From: Codex
Acting-As: Athena
Scope: projectkoios-bootstrap review contract
Repository: projectkoios-bootstrap
Delegated-Operator: Codex
Superseded-By: docs/architecture/adr/adr.20260701.034612_human-in-the-loop-review-agent-contract.md

Project Koios needs a repeatable review contract for an agent that reviews
existing Python code without taking over architecture authority. The requested
agent should use Graphify, git diff, tests, and project review principles as
evidence, then produce a concise review for a human maintainer.

This ADR is retained as the source proposal for the refined review-agent
contract. The current active Draft is
`docs/architecture/adr/adr.20260701.034612_human-in-the-loop-review-agent-contract.md`.

The agent must not rewrite architecture, generate ADRs automatically, or treat
all existing problems as blockers. Its job is to separate facts from
interpretation, classify risk, and surface at most three human decision points.

This ADR proposes the review contract only. It does not implement a new CLI,
workflow, opencode command, Archon workflow, or automated status transition.

## Decision

Define a human-in-the-loop code review agent contract for Project Koios Python
code review.

The review agent is advisory. It may inspect code, diffs, Graphify output, and
test results. It may classify findings and recommend one final disposition. It
must not mutate source files, create ADRs, change ADR status, route work
between harnesses, or decide that architecture has changed.

The agent reviews against these priorities:

1. YAGNI: avoid abstractions for speculative future needs.
2. Architecture boundary violations.
3. DataObject / Activity Object separation.
4. Colored Petri Net compatibility.
5. OOP no dangling Objects: ownership, lifecycle, and responsibility are clear.
6. Dry-run before mutation.
7. Provenance for state transitions.
8. No magic variables: no hidden globals, implicit state, unexplained
   constants, or stringly typed control flow.
9. Explicit typing so designs are easier to port to TypeScript or Rust.
10. PEP 8 compliance.
11. Public API documentation.
12. Tests for public behavior and invariants.

The agent must separate factual evidence from interpretation. Every major
finding must cite at least one evidence source from:

- Graphify query, path, or explain output
- git diff
- tests or validation output
- specific repository files and lines

The agent classifies findings as:

- `blocker`
- `major`
- `minor`
- `note`
- `accepted legacy`

The agent's final recommendation must be exactly one of:

- `approve`
- `approve with comments`
- `request changes`
- `defer architecture decision`
- `block`

The review output format is:

```text
# Review

## Decision

approve / approve with comments / request changes / defer architecture decision / block

## Summary

Briefly state what changed and the main risk.

## Evidence

List the key Graphify/diff/test evidence used.

## Findings

| id | severity | type | issue | recommendation |
| -- | -------- | ---- | ----- | -------------- |

## Human decision points

List at most three.

## Required changes

List only changes required before approval.

## Optional follow-up

List debt or cleanup items that should not block the current work.
```

## Consequences

The contract gives maintainers a consistent review artifact without converting
the reviewer into Athena, Hermes, or Vulcan. It preserves human authority over
architecture decisions and keeps ADR creation explicit.

The review agent may identify architectural concerns, but it must distinguish
between immediate code-review changes, accepted legacy debt, and issues that
need a separate Athena decision. This prevents broad rewrites from being
smuggled into routine review.

The contract increases review discipline by requiring evidence citations,
bounded human decision points, and a constrained recommendation vocabulary. It
also creates a stable output shape that later tooling can parse if Hermes
chooses to route implementation.

## architecture-spec

The review agent has these boundaries:

- **Input authority:** current git diff, current filesystem, Graphify output,
  and validation/test output.
- **Output authority:** advisory review only.
- **Mutation authority:** none.
- **Architecture authority:** none; architecture concerns are routed to Athena.
- **Implementation authority:** none; implementation changes are routed to
  Vulcan after Hermes decides.
- **Routing authority:** none; final review recommendations inform Hermes but
  do not route work by themselves.

The review should normally run this evidence sequence:

1. Use Graphify first when `graphify-out/graph.json` exists.
2. Inspect the git diff for the reviewed change.
3. Inspect only the relevant files and lines needed to verify findings.
4. Run or read the smallest relevant tests/validation available for the change.
5. Produce the fixed-format review artifact.

Evidence handling rules:

- Facts must cite evidence.
- Interpretations must be marked by recommendation or issue framing.
- Major findings must cite Graphify, diff, tests, or file evidence.
- Legacy issues outside the diff may be recorded as `accepted legacy` or
  optional follow-up, not automatically treated as blockers.
- Missing tests may be a finding only when the changed behavior has public
  surface, invariants, or lifecycle consequences.

Decision semantics:

- `approve`: no required changes.
- `approve with comments`: only non-blocking comments or optional follow-up.
- `request changes`: required changes exist but architecture is not blocked.
- `defer architecture decision`: the review found a real architecture question
  that needs Athena before implementation proceeds.
- `block`: evidence shows unsafe mutation, boundary violation, untestable public
  behavior, broken validation, or another issue that should not proceed.

## acceptance-criteria

- The review contract is advisory and human-in-the-loop.
- The contract requires Graphify-first review when a graph exists.
- The contract requires git diff, tests or validation, and file evidence when
  available.
- The contract separates facts from interpretation.
- The contract limits human decision points to at most three.
- The contract forbids automatic ADR generation.
- The contract forbids source mutation, ADR status mutation, and autonomous
  harness routing.
- The contract includes the twelve review priorities from the user request.
- The contract defines the five finding severities.
- The contract defines the five allowed final recommendations.
- The contract preserves accepted legacy as a non-blocking classification.
- The contract includes the required Markdown review output format.

## implementation-brief

Do not implement code from this Draft ADR until Hermes reviews it and Athena
accepts it.

If accepted and routed to Vulcan, implement the smallest useful surface:

- add a reusable review prompt or command for the appropriate code-review
  harness
- ensure the prompt preserves the fixed output format
- ensure it instructs the reviewer to use Graphify first when available
- ensure it asks for git diff and validation evidence
- include tests or fixture-based checks for the output contract if implemented
  as code
- document how Hermes should consume the review recommendation

Vulcan must not implement in this slice:

- automatic ADR creation
- automatic status transitions
- source mutation during review
- autonomous routing to Athena, Hermes, Vulcan, or Koios
- broad architecture rewrites

## resolved-open-questions

- Should the review agent create ADRs automatically?
  - No. It may recommend `defer architecture decision`, but ADR creation
    remains explicit human or Hermes/Athena work.
- Should all existing problems be blockers?
  - No. Existing unrelated debt should be classified as `accepted legacy` or
    optional follow-up unless it directly affects the reviewed change.
- Should the output be free-form?
  - No. The review artifact should use the fixed Markdown sections and bounded
    recommendation vocabulary.

## non-goals

- Implementing the agent.
- Creating a new Archon workflow.
- Creating a new opencode command.
- Replacing existing code review practices.
- Rewriting Project Koios architecture.
- Turning review findings into automatic ADRs.
- Turning review recommendations into automatic harness routing decisions.

## validation-expectations

Draft validation is document-level:

- The ADR uses the repository ADR header convention.
- The ADR includes `architecture-spec`, `acceptance-criteria`,
  `implementation-brief`, `resolved-open-questions`, `non-goals`,
  `validation-expectations`, and `routing`.
- The review output format contains the exact required top-level sections.
- The severity and final recommendation vocabularies are closed sets.
- The contract preserves human decision authority.

If implemented later, validation should include:

- fixture review inputs that produce each final recommendation
- checks that major findings include evidence citations
- checks that human decision points never exceed three
- checks that no source or ADR mutation occurs during review

## routing

Route this Draft ADR to Hermes for review. If Hermes wants Athena promotion
review, run:

```bash
archon workflow run athena_review-draft-for-promotion \
  "docs/architecture/adr/adr.20260701.034100_human-in-the-loop-code-review-agent.md"
```

If accepted and implementation-bearing, Hermes may route the implementation
brief to Vulcan. If Hermes decides this should remain a policy-only contract,
record no-implementation validation before completion.
