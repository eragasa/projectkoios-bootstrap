# ADR 20260702.043600: Koios Adversarial Code Review Authority

## Status

draft

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap review-policy surface
Repository: projectkoios-bootstrap
Delegated-Operator: pi
Architecture-Domain: software

The repository needs a clear authority boundary for code review on Python code
that is being developed under the new workflow and architecture framework.

The immediate question is not whether review exists. Review already exists.
The question is who owns the coding standard, who may review against it, and
what Koios is allowed to do without inventing implementation style from scratch.

The current `docs/policies/code-baseline.md` already describes a review baseline
for Python code. That policy needs an authority decision behind it so the repo
can distinguish between:

1. the role that defines the coding standard
2. the role that performs basic review against that standard
3. the role that validates the architecture boundary

## Decision

Use this authority split:

- **Vulcan owns the coding standard** for implementation work.
- **Koios may perform independent, adversarial code review** against the agreed
  standard, the ADR, and the codebase.
- **Athena owns the architecture boundary** and validates that implementation
  still matches the ADR.

Koios review is intentionally independent, adversarial, and bounded. Koios may flag:

- obvious style issues that escape tooling
- missing or weak docstrings on public or architecture-sensitive code
- missing or weak type annotations on public interfaces
- missing tests or obvious validation gaps
- traceability/provenance gaps
- obvious mismatches with the accepted ADR or implementation plan

Koios should not:

- invent the coding standard
- define module layout or adapter policy from scratch
- override Vulcan's implementation-style decisions
- replace automated formatting/linting
- perform architecture ownership work

Vulcan remains the authority for package-specific coding conventions and
implementation style. Koios reviews against those conventions once they are
stated.

## Consequences

- code review becomes useful without turning Koios into a standards-authoring
  role
- Vulcan retains ownership of implementation style and package conventions
- Athena retains authority over architecture alignment
- the review baseline can be kept lightweight and explicit
- future code review comments can be interpreted against a known authority split

## architecture-spec

The code-review authority split is:

| Responsibility | Owner | Notes |
|---|---|---|
| coding standard | Vulcan | package-level implementation style and conventions |
| adversarial code review | Koios | checks code against the standard, ADR, and obvious gaps |
| architecture validation | Athena | checks implementation against the ADR |
| automated formatting/linting | tooling | handles mechanical style where possible |

Koios review is a review surface, not a standards-making surface. The point
is to provide a skeptical third-party check, not a co-authoring role.

## acceptance-criteria

- reviewers can tell from the policy who owns the coding standard
- reviewers can tell who may perform adversarial code review
- Koios review comments remain bounded to reviewable gaps rather than style
  invention
- Athena remains the authority for architecture alignment
- the policy can be mirrored into `docs/policies/code-baseline.md`

## implementation-brief

If accepted, update `docs/policies/code-baseline.md` to record the authority
split and add a short pointer from `docs/agents/agent-charter.md` if needed.

## resolved_open_questions

- Should Koios review be limited to Python only, or expanded to other languages
  once the repo has a stable baseline?
- Should the code baseline include a short review checklist for Koios?
- Should package-specific standards live in separate docs or remain implicit in
  Vulcan plans?

## non_goals

- Defining the actual coding standard content in this ADR
- Replacing Vulcan implementation plans
- Replacing Athena architecture review
- Turning Koios into the sole code reviewer
- Defining linter/formatter configuration

## validation-expectations

- a reviewer can name the standard owner without ambiguity
- Koios review comments can be scoped to basic review concerns only
- architecture validation remains separate from style review
- the policy can be used to interpret future review comments consistently

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Code-review authority boundary; Vulcan owns the standard, Koios does
  basic review, Athena validates architecture.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

## Comments

- KOIOS: Keep the review surface lightweight so it stays useful rather than becoming a second implementation plan.
- VULCAN: The coding standard still needs to be written for each package, but the ownership split above is the right boundary.
- HERMES: This is an authority decision, not an implementation plan; mirror it into the policy layer after acceptance.
