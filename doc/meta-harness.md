# Meta-Harness Overview

This repository uses a triple-agent meta-harness.

The harness separates specification, implementation, and knowledge capture into distinct agent roles. Agents do not share hidden assumptions. They communicate through explicit artifacts with defined ownership, provenance, and acceptance criteria.

## Purpose

The purpose of the meta-harness is to coordinate agentic work without allowing the system to collapse into an unstructured prompt chain.

The harness enforces the following principles:

* each agent has a bounded responsibility;
* each agent consumes and produces explicit artifacts;
* architectural decisions are separated from implementation changes;
* implementation facts are separated from knowledge claims;
* disagreements are resolved by authority rules, not by compromise;
* completion is gated by inspectable artifacts.

## Skill model

A skill is a typed transition from input artifacts to output artifacts:

```
S : A₁ + A₂ + ... + Aₙ → B₁ + B₂ + ... + Bₘ
```

Each skill defines when it is used, which agent owns it, which artifacts it consumes and produces, the procedure, failure modes, and escalation rules.

One skill = one bounded transformation. Do not write skills as personality instructions or broad essays.

Skills in development live in `skills/`. When stable, they may be deployed to each harness's directory.

### Skill file template

```md
---
name: <agent>-<operation>
description: <trigger and expected output>
metadata:
  agent: spec-agent | code-agent | knowledge-agent | meta-harness
  harness_role: producer | consumer | consumer-producer | arbiter
  consumes:
    - <artifact-type>
  produces:
    - <artifact-type>
---

## When to use this skill

## Agent responsibility

## Inputs

## Procedure

## Output artifact

## Failure modes

## Escalation rule
```

## Disagreement handling

When disagreement occurs, the meta-harness (pi) must identify:

* the conflicting claims;
* the artifact containing each claim;
* the authority level of each artifact;
* the controlling claim;
* the artifact that must be revised;
* the agent responsible for revision.

The output should be a `revision-request`.

A revision request must include:

* the conflict;
* the evidence;
* the controlling authority;
* the required correction;
* the next responsible agent.

## Completion gates

A task is complete only when the required output artifacts exist and satisfy the relevant acceptance criteria.

For architecture work, completion requires:

* an explicit scope statement;
* non-goals;
* public API intent, if applicable;
* unresolved questions, if any;
* downstream instructions for implementation or knowledge capture.

For implementation work, completion requires:

* a patch or explicit statement that no patch is needed;
* tests or an explicit reason tests are not applicable;
* an implementation report;
* any deviations from the specification.

For knowledge work, completion requires:

* durable notes or explicit statement that no durable note is needed;
* provenance for factual claims;
* classification of claims as decision, implementation fact, rationale, or open question.

For coordination work, completion requires:

* routing decision, revision request, escalation request, or completion decision.

## Escalation rules

Escalate to the user only when the harness cannot resolve the issue from available artifacts.

Escalation is appropriate when:

* user intent is ambiguous and materially affects architecture;
* two valid architecture options have different project consequences;
* the repository state contradicts the requested change;
* implementation would require a destructive change;
* acceptance criteria cannot be inferred safely;
* a decision requires user preference rather than technical judgment.

Do not escalate for routine implementation details.

Do not escalate when a reasonable minimal patch exists.

Do not escalate merely because the task is large.

## Anti-patterns

Avoid these patterns:

* one agent doing specification, implementation, and knowledge capture in the same step;
* skills that describe personality rather than procedure;
* hidden handoffs;
* undocumented assumptions;
* implementation without acceptance criteria;
* notes without provenance;
* architecture changes hidden inside patches;
* knowledge notes treated as authority over repository state;
* tests added only after implementation without describing public behavior;
* disagreement resolved by blending incompatible claims.
