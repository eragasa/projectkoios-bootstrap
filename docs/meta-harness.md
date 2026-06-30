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

## Artifact ownership

| Artifact | Owner | Producing runtime |
|---|---|---|
| `user-request` | user | N/A |
| `architecture-spec` | Athena | archon / Codex |
| `acceptance-criteria` | Athena | archon / Codex |
| `implementation-brief` | Athena | archon / Codex |
| `implementation-plan` | Vulcan | opencode |
| `patch` | Vulcan | opencode |
| `test-results` | Vulcan | opencode |
| `implementation-report` | Vulcan | opencode |
| `deviation-report` | Vulcan | opencode |
| `knowledge-note` | Koios | goose |
| `provenance-index` | Koios | goose |
| `provenance-audit` | Koios | goose |
| `repo-state-summary` | Koios (advisory) | goose |
| `routing-recommendation` | Koios (advisory) | goose |
| `directive` | producer-specific | producer runtime |
| `routing-decision` | Hermes | pi |
| `revision-request` | Hermes | pi |
| `completion-decision` | Hermes | pi |

## Cross-surface knowledge discipline

Knowledge work often spans repository state, accepted ADRs, current handoffs,
archived artifacts, and bounded vault material. These are not interchangeable
sources.

When a knowledge agent or support flow spans multiple surfaces, it should:
- declare the bounded scope it is using
- preserve provenance per claim or summary section
- distinguish live repo truth from archived or vault memory
- flag contradictory sources instead of silently normalizing them

Graph-backed indexing systems may be used as broad-context substrate, but they
do not replace source citation or authority ordering.

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
