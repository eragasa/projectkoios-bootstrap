---
name: architecture-interview
description: |
  Use when Athena/Archon must question an implementation proposal before code
  begins and produce an architecture interview or decision-support document
  alongside an existing ADR. Triggers include "architecture interview",
  "decision-support document", "question this implementation proposal",
  "surface architectural options", "before implementation begins", and reviews
  that must evaluate scope discipline, model separation, workflow compatibility,
  repository ownership, ObjectClass/ActionClass/ActionInstance/Policy/Trace
  separation, or future Petri-net compatibility. Do not use for implementation,
  direct code editing, ADR replacement, workflow creation, or automatic routing
  to Vulcan.
---

# Architecture Interview

## Overview

Produce a structured architecture interview for Athena decision input. The
output complements an existing ADR by clarifying implementation choices,
surfacing viable paths, and naming the human decision required before
implementation proceeds.

## Responsibility

You are not implementing code. Do not edit product code, create workflows,
replace the existing ADR, change ADR status, or route directly to Vulcan.

You are producing an architecture decision-support document for Archon/Athena.
Treat existing ADRs, implementation briefs, workflow files, and user prompts as
context. When source material conflicts, surface the conflict instead of
normalizing it silently.

## Inputs

- `user-request` - the implementation proposal or interview request
- existing ADR path or excerpt, when provided
- related implementation brief, spec, workflow, policy, or repository context,
  when relevant

If the user names an ADR path, read it before drafting the interview. If no ADR
is provided but the task depends on prior architecture, identify that as a
blocking or open question.

## Clarifying Questions First

Before proposing solutions, ask only questions that would materially change the
architectural decision. Focus on:

- implementation target
- owning repository
- expected artifact
- boundary between bootstrap, specification, code, knowledge, agent, workflow,
  and publishing responsibilities
- whether the result is a one-time scaffold, reusable primitive, schema, policy,
  prompt, CLI command, library API, or workflow
- what must exist now versus what can be deferred
- future workflow or Petri-net compatibility that must be preserved
- risks already constrained by the existing ADR

If those answers are missing and a reasonable assumption would materially change
the recommendation, stop after the questions and wait for the user or Archon
input. If enough context exists to proceed, include the questions and assumed
answers or unresolved points in the final document.

## Decision Axes

Evaluate every option through these axes:

- Scope discipline: minimum useful capability, no speculative infrastructure,
  no framework before evidence.
- Model separation: keep persistent objects separate from actions; distinguish
  `ObjectClass`, `ActionClass`, `ActionInstance`, `Policy`, and `Trace`; avoid
  embedding opaque behavior in objects.
- Workflow compatibility: preserve later representation as states,
  transitions, guards, artifacts, approvals, and traces without requiring a
  Petri-net engine now.
- Repository boundary clarity: name which repository owns each artifact, code,
  schema, prompt, policy, workflow, or publishing responsibility; do not let
  `projectkoios-bootstrap` silently absorb long-term responsibilities for other
  repositories.

## Options

Propose exactly four plausible courses of action. For each option include:

- option name
- short description
- what it implements now
- what it explicitly defers
- owning repository or repositories
- affected artifacts
- compatibility with the existing ADR
- effect on `ObjectClass` / `ActionClass` separation
- effect on future workflow or Petri-net compatibility
- main advantages
- main risks
- reversibility
- architectural grade

Use grades sparingly. A grade summarizes judgment; it must not replace the
reasoning.

## Recommendation

Recommend exactly one of the four options.

Explain:

- why it best fits the current stage of Project Koios
- why it is preferable to the other three options
- what architectural debt it accepts
- what Archon should document
- what decision the human architect must make before implementation proceeds

## Output Format

Produce this exact top-level structure:

```markdown
# Architecture Interview: {implementation topic}

## Existing ADR Context

## Clarifying Questions

## Architectural Decision Axes

## Option 1: {name}

## Option 2: {name}

## Option 3: {name}

## Option 4: {name}

## Comparative Assessment

## Recommended Course of Action

## Required Human Decision

## Notes for Archon
```

In `Comparative Assessment`, include a compact comparison table. In `Notes for
Archon`, list follow-up ADRs, implementation briefs, specs, schemas, workflows,
or tickets that should be captured.

## Hard Rules

- Do not implement anything.
- Do not produce fewer or more than four options.
- Do not recommend more than one option.
- Do not replace the existing ADR.
- Do not hide repository ownership or future workflow compatibility.
- Do not collapse persistent objects, actions, policies, and traces into one
  model.
