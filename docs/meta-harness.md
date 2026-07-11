# Meta-Harness Overview

This repository uses a triple-agent meta-harness.

The canonical document-domain ownership split lives in `docs/agents/agent-charter.md`.
The durable system state is the repository document set and each document's status.
Agents are initialized from that state, run a bounded transformation, and write
back a new state. The harness separates specification, implementation, and
knowledge capture into distinct document domains with defined ownership,
provenance, and acceptance criteria.

## Purpose

The purpose of the meta-harness is to coordinate agentic work without allowing the system to collapse into an unstructured prompt chain.

The harness enforces the following principles:

* each agent has a bounded responsibility;
* each agent consumes repository document state and produces a bounded state change;
* architecture documents set the long-term system vision and blueprint;
* implementation work is sliced from the architecture blueprint into bounded briefs and plans;
* architectural decisions are separated from implementation changes;
* implementation facts are separated from knowledge claims;
* disagreements between document domains are reconciled by authority rules, not by compromise;
* completion is gated by inspectable artifacts.

## Architecture-led workflow

Architecture documents are the primary long-term system blueprint. They describe the intended system shape, boundaries, invariants, and lifecycle expectations.

Implementation proceeds by slicing bounded pieces from that architecture blueprint:

1. Athena maintains or revises the architecture document as the vision/blueprint surface.
2. Athena or Hermes identifies a bounded implementation slice from that architecture.
3. Athena writes acceptance criteria or an implementation brief for the slice.
4. Vulcan writes an implementation plan and patch for only the approved slice.
5. Vulcan reports implementation evidence, validation results, and deviations from the architecture blueprint.
6. Athena reconciles the evidence back into the architecture document as as-built documentation or records a correction/deviation path.

The architecture document remains the durable system surface. Implementation briefs, plans, patches, and reports are supporting artifacts for slices of that surface. A patch must not silently redefine the architecture; it must either conform, request a deviation, or produce evidence that Athena uses to revise the architecture.

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

See `docs/agents/agent-charter.md` for the current document-domain ownership
rules.

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
| `state-observation` | Koios (advisory) | goose |
| `directive` | producer-specific | producer runtime |
| `state-reconciliation` | Hermes | Hermes |
| `revision-request` | Hermes | Hermes |
| `completion-decision` | Hermes | Hermes |
| `after-action-report` | any harness | any harness |

## Workflow Ownership

Archon workflow names may encode harness authority. Workflows named with the
prefix `athena_` follow this shape:

```text
athena_<action-in-this-mode>
```

The prefix means the workflow is an Athena-owned role transition. Only Athena
may run it in the harness sense, and any output from that workflow is an Athena
artifact. Hermes, Codex, or another delegated operator may physically invoke the
Archon CLI to provide access, but that does not change the artifact owner or
turn the output into a Hermes state-reconciliation decision.

The legacy artifact names `routing-recommendation` and `routing-decision` are retained
for compatibility. In prose, they mean observation/decision about document-domain
ownership, status inconsistency, and the next repository state.

An `athena_` workflow must not implement code, validate patches, complete ADRs,
or perform Koios knowledge capture unless a later accepted ADR explicitly
changes that workflow's ownership boundary.

## Cross-surface knowledge discipline

Knowledge work often spans repository state, accepted ADRs, implementation
reports, archived artifacts, and bounded vault material. These are not
interchangeable sources.

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
* treating transport artifacts as durable state;
* undocumented assumptions;
* transport mechanics treated as architecture authority;
* implementation without acceptance criteria;
* notes without provenance;
* architecture changes hidden inside patches;
* knowledge notes treated as authority over repository state;
* tests added only after implementation without describing public behavior;
* disagreement resolved by blending incompatible claims.
