# ADR 20260701.034612: Human-in-the-loop review agent contract

## Status

Accepted

## Context

Origin: user request
From: Codex
Acting-As: Athena
Scope: projectkoios-bootstrap review-agent contract
Repository: projectkoios-bootstrap
Delegated-Operator: Codex
Source-Proposal: docs/architecture/adr/adr.20260701.034100_human-in-the-loop-code-review-agent.md
Baseline-Source-Material:
- docs/policies/architecture-baseline.md
- docs/policies/review-baseline.md
- docs/policies/review-template.md
- docs/policies/code-baseline.md

Project Koios needs a bounded review contract for an advisory human-in-the-loop
agent that reviews changes in projectkoios-bootstrap without becoming an
implementation harness, architecture authority, knowledge authority, or
autonomous router. This repository owns shared bootstrap configuration,
harness instructions, workflows, and repo-local process architecture. It does
not own product/domain architecture for Project Koios.

The baseline policy documents under `docs/policies/` are the editable policy
surface for this review contract. They provide source material for this Draft
ADR, but are not themselves accepted architecture decisions. The
architecture-baseline document is an observed-state and debt-register model,
not a decision list or refactor plan. The review-baseline, review-template, and
code-baseline documents define the review principles, output shape, and code
review checks that this ADR turns into a bounded architecture contract.

The source proposal and user constraints already resolve the review agent's
authority boundary: the agent is advisory only, must preserve human authority,
must not mutate source, must not generate ADRs automatically, must not change
ADR status, must not route work autonomously, must not perform broad rewrites,
and must not treat unrelated legacy problems as automatic blockers.

Codex must not invoke the opencode harness directly for this contract. The
first selected implementation surface is not an opencode command and not a new
Archon workflow. If this ADR is accepted, Hermes may route only the bounded
repo-local review-process surface described in the implementation brief.

The required review evidence is current repository state: Graphify output, git
diff, tests or validation output, and specific files or lines. Review output
must separate facts from interpretation so a human maintainer can distinguish
observed evidence from risk judgment and recommendation.

This ADR is an Athena specification artifact only. It does not implement a
review agent, create a workflow, create an opencode command, change an existing
ADR status, or authorize code changes.

## Decision

Adopt a Draft human-in-the-loop review agent contract for
projectkoios-bootstrap. The review agent produces a fixed Markdown review
artifact for a human maintainer. The artifact is advisory and has no direct
mutation, routing, ADR, or architecture authority.

This ADR is implementation-bearing after acceptance. The selected bounded
implementation surface is a repo-local Goose skill or harness instruction at
`agents/global/goose/skills/technical-debt-report/SKILL.md` that enables
Koios/goose to produce a repo-local technical debt report in Markdown. The
first surface is not an opencode command, new Archon workflow, autonomous
router, or source-code mutation tool. Technical debt reports use this
repo-relative path convention:

```text
docs/reviews/technical-debt/tdr.YYYYMMDD.HHMMSS_<scope>.md
```

Hermes remains the completion authority. The concrete Hermes gate is the
existing `hermes.completion_review` flow, with the Koios technical debt report
as a required input.

The review agent must use this evidence order:

1. Query Graphify first when `graphify-out/graph.json` exists. If Graphify warns
   that the graph is stale or structurally outdated, treat Graphify as
   discovery only and verify claims against source files.
2. Inspect the current git diff for the reviewed change.
3. Inspect only the files and lines needed to verify review findings.
4. Run or read the smallest relevant tests or validation available for the
   changed behavior.
5. Produce the fixed review artifact without changing repository files,
   workflow state, ADR status, or machine-local state.

Facts and interpretations must remain distinct. A fact is an observed property
from Graphify, git diff, tests, validation output, or file content. An
interpretation is a risk judgment, severity, or recommendation based on those
facts. Every `blocker`, `major`, and `minor` finding must cite evidence. `note`
and `accepted legacy` findings should cite evidence when practical.

The review contract incorporates an observed-state baseline model:

- Architecture baselines record observed modules, dependency edges, known
  problems, and debt status.
- Architecture baselines are not accepted decision lists.
- Architecture baselines are not refactor plans.
- Follow-up debt may be proposed for a baseline or debt register, but it must
  not become a blocker unless it directly affects the reviewed change.
- The current target assumption is that core schema/model code should remain
  independent of runtime engines, UI, Petri-net backends, process-mining
  libraries, and external adapters.
- That target assumption can change only by explicit human decision. A review
  agent may identify evidence that the assumption is in tension with a change,
  but it must not alter the assumption.

The review priorities are:

1. YAGNI: avoid abstractions for speculative future needs.
2. Core boundary preservation where applicable to the changed code.
3. ObjectClass / ActionClass separation where applicable.
4. Petri-net compatibility where applicable.
5. Dry-run before mutation for mutating behavior.
6. Provenance for meaningful state transitions.
7. No magic variables: no hidden globals, implicit state, unexplained
   constants, or stringly typed control flow.
8. Explicit typing, especially at public APIs, schema objects, workflow
   objects, action objects, and adapter boundaries.
9. Public API behavior tested through public interfaces.
10. Thin adapter boundaries around external libraries.
11. PEP 8 style compliance for Python, preferably enforced by tooling.
12. Public documentation for modules, classes, functions, methods, CLI entry
    points, mutating behavior, I/O, exceptions, parameters, return values, and
    important invariants.
13. Examples for important public APIs, preferably as executable tests.

Finding severity is a closed set:

- `blocker`
- `major`
- `minor`
- `note`
- `accepted legacy`

Final recommendation is a closed set:

- `approve`
- `approve with comments`
- `request changes`
- `defer architecture decision`
- `block`

Decision semantics:

- `approve`: no required changes.
- `approve with comments`: only non-blocking comments or optional follow-up.
- `request changes`: required changes exist, but no Athena architecture decision
  is required before implementation can proceed.
- `defer architecture decision`: evidence shows a real architecture question
  that needs Athena before implementation proceeds.
- `block`: evidence shows a blocker such as unsafe mutation, role-boundary
  violation, broken validation, untestable public behavior, or a direct conflict
  with accepted repo-local architecture.

Unrelated legacy problems must not automatically block the reviewed change. They
may be classified as `accepted legacy` or placed in optional follow-up unless
the diff relies on them, worsens them, or makes them part of the current change.

Formatting and lint concerns should prefer tooling over manual review comments.
The reviewer may report missing or unavailable tooling as evidence, but should
not spend human attention on formatting issues that a configured formatter or
linter can enforce mechanically.

The review output must use this fixed Markdown format:

```text
# Review

## Scope

Change reviewed:
Branch / PR / commit:
Files changed:

## Graphify evidence

### Changed files

| file | observed area | change type |
|---|---|---|

### Dependency impact

| source | target | concern |
|---|---|---|

### Reverse dependencies

| changed module | modules depending on it |
|---|---|

### Tests

| changed module | related tests |
|---|---|

## Architecture check

### A1: Core boundary

Result: pass / concern / fail / unknown
Evidence:
Human decision needed: yes / no

### A2: ObjectClass / ActionClass separation

Result: pass / concern / fail / unknown
Evidence:
Human decision needed: yes / no

### A3: Petri-net compatibility

Result: pass / concern / fail / unknown
Evidence:
Human decision needed: yes / no

### A4: Dry-run and provenance

Result: pass / concern / fail / unknown
Evidence:
Human decision needed: yes / no

### A5: YAGNI

Result: pass / concern / fail / unknown
Evidence:
Human decision needed: yes / no

## Code check

### C1: Public API behavior

Result: pass / concern / fail / unknown
Evidence:

### C2: Tests

Result: pass / concern / fail / unknown
Evidence:

### C3: Mutation clarity

Result: pass / concern / fail / unknown
Evidence:

### C4: Adapter isolation

Result: pass / concern / fail / unknown
Evidence:

### C5: PEP 8 and tooling

Result: pass / concern / fail / unknown
Evidence:
Tool result:
Required change:

### C6: Public documentation

Result: pass / concern / fail / unknown
Evidence:
Missing docstrings:
Missing parameter documentation:
Missing return-value documentation:
Missing exception documentation:
Missing side-effect, mutation, or I/O documentation:
Required change:

### C7: Type annotations

Result: pass / concern / fail / unknown
Evidence:
Missing or weak annotations:
Required change:

### C8: Public examples

Result: pass / concern / fail / unknown
Evidence:
Example gap:
Required change:

## Findings

| id | type | severity | fact | interpretation | recommendation |
|---|---|---|---|---|---|

## Human decision points

Limit to at most three.

### D1:

Question:
Options:
1.
2.
3.
Agent recommendation:
Human decision:

## Final recommendation

Recommendation: approve / approve with comments / request changes / defer architecture decision / block
Reason:

## Required changes

List only changes required before approval.

## Follow-up baseline/debt register

Add to baseline/debt register:
- [ ] no
- [ ] yes

Debt items:

## ADR creation controls

Create ADR:
- [ ] no
- [ ] proposed only
- [ ] yes, after human decision

ADR rationale:

## Optional follow-up

List debt or cleanup items that should not block the current work.
```

## Consequences

The contract creates a consistent human-facing review artifact without turning
the reviewer into Athena, Hermes, Vulcan, or Koios. It preserves human authority
over architecture decisions, ADR creation, implementation routing, source
mutation, and baseline target-assumption changes.

The contract adds discipline to reviews by requiring evidence, closed severity
and recommendation vocabularies, explicit separation of fact and interpretation,
and no more than three human decision points. It prevents broad rewrites from
being smuggled into routine review by treating unrelated legacy issues as
non-blocking unless they directly affect the reviewed change.

The contract is intentionally narrow. Later tooling may parse the fixed Markdown
format, but this ADR does not require automation or implementation.

## architecture-spec

The review agent has these authority boundaries:

- Input authority: current Graphify output, current git diff, current
  filesystem content, and current tests or validation output.
- Output authority: advisory Markdown review artifact only.
- Mutation authority: none.
- Architecture authority: none.
- ADR authority: none; ADR creation and status changes remain explicit human,
  Hermes, or Athena work.
- Implementation authority: none; implementation changes remain Vulcan work
  after Hermes routing.
- Routing authority: none; recommendations inform Hermes but do not trigger
  autonomous handoff.
- Baseline authority: none; the review may propose baseline or debt-register
  updates, but a human must decide whether they are recorded.

The review artifact must be deterministic in shape even when evidence is
incomplete. Missing evidence should be reported as a fact in the evidence
sections or as a finding when it affects review confidence. The reviewer must
not fill missing evidence with assumptions.

The review may identify architecture concerns, but architecture concerns must be
framed as review observations. If the concern cannot be resolved from accepted
repo-local architecture, the final recommendation should be `defer architecture
decision` rather than inventing a decision inside the review.

The architecture checks A1-A5 are review lenses, not standalone decisions:

- A1 checks whether changed code violates an applicable core/schema boundary.
- A2 checks whether state-carrying objects and action/state-transition behavior
  remain separated where the model uses those concepts.
- A3 checks whether the change preserves future expression as places,
  transitions, markings, guards, and firing events when workflow behavior is in
  scope, without requiring a direct Petri-net library dependency.
- A4 checks whether mutating behavior has a dry-run path and produces
  provenance for meaningful state transitions.
- A5 checks whether new abstractions protect a current boundary, remove real
  duplication, isolate an unstable dependency, or represent a real domain
  concept.

The code checks C1-C8 are review lenses, not permission to rewrite code outside
the reviewed diff. They should be applied only to changed behavior, public API
surfaces touched by the change, and directly affected tests or documentation.

## acceptance-criteria

- The contract is scoped to projectkoios-bootstrap.
- The contract is advisory and human-in-the-loop.
- The contract requires Graphify-first review when `graphify-out/graph.json`
  exists.
- The contract requires git diff, tests or validation, and file evidence when
  available.
- The contract separates factual evidence from interpretation.
- The contract limits human decision points to at most three.
- The contract forbids automatic ADR generation.
- The contract forbids source mutation, ADR status mutation, machine-local state
  mutation, and autonomous harness routing.
- The contract forbids broad rewrites as part of review.
- The contract prevents unrelated legacy problems from becoming automatic
  blockers.
- The contract treats architecture baselines as observed-state and debt-register
  material, not as accepted decision lists.
- The contract preserves the core/schema independence target assumption as
  human-changeable only.
- The contract includes Graphify evidence sections for changed files,
  dependency impact, reverse dependencies, and related tests.
- The contract includes architecture checks A1-A5.
- The contract includes code checks C1-C4 from the review template.
- The contract adds code-baseline checks for PEP 8/tooling, public
  documentation, type annotations, and public examples.
- The contract defines closed finding severities.
- The contract defines closed final recommendations.
- The contract defines the fixed Markdown review output format.
- The contract includes follow-up baseline/debt register controls.
- The contract includes ADR creation controls that require human decision before
  ADR creation.
- The contract preserves routing back to Hermes after Vulcan reports.

## implementation-brief

Do not implement from this Draft ADR until Hermes reviews it and the ADR is
accepted through the normal Athena/Hermes process.

This ADR is implementation-bearing after acceptance. If accepted and routed,
implement only the smallest repo-local process surface needed for Koios/goose
to produce the required technical debt report artifact. The selected surface is
a Goose skill or harness instruction at
`agents/global/goose/skills/technical-debt-report/SKILL.md` with a fixed
Markdown technical debt report path:

```text
docs/reviews/technical-debt/tdr.YYYYMMDD.HHMMSS_<scope>.md
```

Do not implement this contract as an opencode command, new Archon workflow,
autonomous routing mechanism, source mutation tool, or automatic ADR generator.

Any implementation work must preserve:

- advisory-only behavior
- no source mutation during review
- no machine-local state mutation during review
- no automatic ADR creation
- no ADR status mutation
- no autonomous routing
- Graphify-first evidence discovery when available
- git diff, tests or validation, and file evidence in review output
- fixed Markdown output sections
- closed severity and final recommendation vocabularies
- at most three human decision points
- baseline/debt-register follow-up as human-controlled proposal only
- ADR creation as human-controlled proposal only
- no blockers for unrelated legacy issues unless the diff relies on them,
  worsens them, or makes them part of the current change

First-slice validation is template conformance only. It verifies report shape,
closed vocabularies, required fields, and required evidence slots; it does not
claim semantic correctness and must not mutate source files.

If the selected implementation surface is executable, focused contract checks
or fixtures should verify:

- output contains every required section
- final recommendation is from the closed set
- finding severity is from the closed set
- human decision points do not exceed three
- `blocker`, `major`, and `minor` findings include evidence
- source, ADR, workflow, and machine-local state are not modified by review
  execution
- ADR creation controls cannot create an ADR without human decision
- baseline/debt-register controls cannot mutate a baseline without human
  decision

The implementation report, test results, and any deviation report must be
returned to Hermes. Hermes reviews them through `hermes.completion_review`,
with the Koios technical debt report as a required input. The implementation
agent must not mark the ADR complete or route the work onward.

## resolved-open-questions

- Should the review agent create ADRs automatically?
  No. It may recommend `defer architecture decision` or propose ADR creation in
  the fixed ADR creation controls, but ADR creation remains explicit human,
  Hermes, or Athena work.

- Should review recommendations trigger automatic harness routing?
  No. Recommendations inform Hermes. Hermes remains responsible for routing.

- Should unrelated legacy problems block the reviewed change?
  No. They should be classified as `accepted legacy`, optional follow-up, or
  proposed debt-register entries unless they directly affect the diff under
  review.

- Should the review output be free-form?
  No. The output must use the fixed Markdown format and closed vocabularies.

- Should the agent mutate source files, tests, ADRs, workflow state, or
  machine-local state?
  No. It is advisory only.

- Can the core/schema independence target assumption change during review?
  No. The review may identify evidence and ask for a human decision, but the
  assumption changes only by explicit human decision.

- Should PEP 8 and formatting concerns be reviewed manually?
  Only when tooling is unavailable or the issue cannot be represented by
  tooling. Prefer `ruff`, `ruff format`, `black`, `mypy`, `pyright`, and
  `pytest` where applicable and configured by the project.

- Which concrete surface should carry this contract if accepted?
  A repo-local Goose skill or harness instruction at
  `agents/global/goose/skills/technical-debt-report/SKILL.md` that produces a
  repo-local Markdown technical debt report under
  `docs/reviews/technical-debt/tdr.YYYYMMDD.HHMMSS_<scope>.md`. It is not an
  opencode command or new Archon workflow in the first slice.

- Should the first implementation include executable contract validation?
  First-slice validation is template conformance only. Executable checks may be
  added when the selected surface is executable, but semantic correctness and
  source mutation are out of scope for the first slice.

- Which Hermes review gate decides whether implementation evidence satisfies
  this ADR?
  The existing `hermes.completion_review` flow, with the Koios technical debt
  report as a required input.

## unresolved human decisions

None remain for promotion. Any later request to change the selected surface,
expand validation beyond template conformance, or replace the
`hermes.completion_review` gate requires a new human decision and Athena
revision.

## non-goals

- Implementing the review agent in this ADR.
- Creating a new Archon workflow in this ADR.
- Creating a new opencode command in this ADR.
- Creating a repo-local skill in this ADR.
- Replacing all existing review practices.
- Rewriting project architecture.
- Generating ADRs automatically.
- Mutating source files during review.
- Mutating machine-local state during review.
- Changing ADR status automatically.
- Changing baseline target assumptions automatically.
- Routing work autonomously between Hermes, Athena, Vulcan, or Koios.
- Blocking current work for unrelated legacy problems.
- Treating editable policy baseline documents as accepted architecture
  decisions by themselves.

## validation-expectations

Draft validation is document-level:

- Confirm the ADR filename and header follow the repository ADR convention.
- Confirm all required sections are present:
  `architecture-spec`, `acceptance-criteria`, `implementation-brief`,
  `resolved-open-questions`, `unresolved human decisions`, `non-goals`,
  `validation-expectations`, and `routing`.
- Confirm the review output format contains Graphify evidence, architecture
  checks A1-A5, code checks C1-C8, findings, human decision points, final
  recommendation, required changes, follow-up baseline/debt register, ADR
  creation controls, and optional follow-up.
- Confirm severity and final recommendation vocabularies are closed sets.
- Confirm the contract remains advisory only and forbids source mutation,
  machine-local state mutation, automatic ADR generation, ADR status mutation,
  and autonomous routing.
- Confirm no unresolved human decisions remain for promotion.
- Confirm the implementation classification is implementation-bearing after
  acceptance.
- Confirm the selected first implementation surface is
  `agents/global/goose/skills/technical-debt-report/SKILL.md`, not an opencode
  command or new Archon workflow.
- Confirm first-slice validation is template conformance only.
- Confirm `hermes.completion_review` is the Hermes gate and the Koios technical
  debt report is a required input.
- Confirm architecture baselines are represented as observed state and debt
  register material, not decisions.
- Confirm code-baseline checks are represented in `docs/policies/code-baseline.md`
  and reflected in the review contract.

If implemented later, validation should include:

- Review fixtures or contract tests for each final recommendation.
- Checks that `blocker`, `major`, and `minor` findings cite evidence.
- Checks that human decision points never exceed three.
- Checks that the technical debt report path follows
  `docs/reviews/technical-debt/tdr.YYYYMMDD.HHMMSS_<scope>.md`.
- Checks that no source, ADR, workflow, or machine-local state mutation occurs
  during review.
- Checks that baseline/debt-register and ADR creation controls require human
  decision before mutation or creation.
- A minimal validation command or documented manual validation path that Hermes
  can inspect.

## routing

Route this Draft ADR to Hermes for review. Hermes may request Athena promotion
review, keep the ADR as Draft, reject it, or route the accepted
implementation-bearing brief to the appropriate implementation harness for the
selected Goose technical debt report skill or harness-instruction surface.

After implementation reports, Hermes must review the `implementation-report`,
`test-results`, any `deviation-report`, and the required Koios technical debt
report through `hermes.completion_review`. Hermes then routes back to Athena
only if the implementation exposed an unresolved architecture decision, a
deviation from this contract, or a requested change to the baseline target
assumption. Otherwise Hermes may record completion according to the accepted ADR
lifecycle.
