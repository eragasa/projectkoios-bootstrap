# Workflow: process capture

## Status

Observation workflow, non-authoritative.

## Purpose

This document defines how Project Koios captures the software-development process between ATHENA and VULCAN as a filesystem-visible chain of artifacts.

The goal is to make forward progress inspectable without requiring a message router or delivery role.

## Core model

The repo filesystem is the coordination surface.

Process state advances by creating the next artifact and linking it backward to the prior artifact.

Each artifact SHOULD name its predecessor artifact.

Each artifact SHOULD name its current process step.

Each artifact SHOULD name its expected successor artifact.

The normal ATHENA/VULCAN loop is:

```text
ATHENA brief/spec
→ filesystem-visible work item
→ VULCAN implementation/report
→ ATHENA review
→ KOIOS process capture
→ next ATHENA brief if needed
```

A message router MAY provide optional transport or command execution.

A message router is not required by this process model.

## Role responsibilities

### ATHENA

ATHENA owns architecture/specification surfaces.

ATHENA SHOULD produce bounded briefs or specs with scope, acceptance criteria, out-of-scope items, predecessor links, and expected successors.

ATHENA SHOULD review VULCAN output for conformance.

ATHENA SHOULD record acceptance, deviations, or next-slice recommendations.

### VULCAN

VULCAN owns implementation, tests, validation, and implementation reports.

VULCAN SHOULD implement only the accepted filesystem-visible work item.

VULCAN SHOULD return changed files, validation evidence, implementation reports, known deviations, predecessor links, and expected successors.

### KOIOS

KOIOS owns process/provenance capture after an inspectable slice lands.

KOIOS SHOULD capture the observed artifact chain, not the full chat transcript.

KOIOS SHOULD identify recurring process patterns only after multiple observed examples.

KOIOS MAY propose candidate skills or policy changes after repeated patterns are visible.

## Process-capture namespace

Directory:

```text
docs/process-capture/
```

This directory stores durable repo-local records of how software-development work moves between roles.

Process-capture notes MUST NOT be treated as ADRs, implementation reports, AARs, or workflow policy.

Process-capture notes MAY recommend follow-up ADRs, policy updates, checklist changes, skills, or implementation tasks.

Process-capture notes MUST NOT create architecture, implementation, or workflow authority.

## Process-chain note schema

Process-chain notes SHOULD follow `schema.process-chain.md`.

## Skill-derivation guidance

KOIOS should capture repeated examples of:

- artifact-flow patterns
- gate conditions
- validation conventions
- review conventions
- handoff quality indicators
- recurring ambiguity or friction

ATHENA should derive candidate skills only after multiple captured process chains show a stable pattern.

Candidate skills should be proposed as observations first and promoted only through the normal docs, policy, ADR, or skill-authoring path.
