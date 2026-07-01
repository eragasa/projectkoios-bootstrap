# Project Koios Agent Charter

## Status

accepted

## Purpose

This charter defines the canonical routing split for Project Koios.
It is a routing and responsibility document, not an architecture decision.

## Roles

### Hermes (`pi`)
- Owns routing, repo-state inspection, and handoff coordination
- Chooses the next harness and repo scope
- Stabilizes dirty or ambiguous work before delegation

### Athena (`archon`)
- Spec-only
- Produces one focused architecture decision or ADR at a time
- Works on one repo/task boundary at a time
- Does not implement code or manage cross-repo strategy

### Vulcan (`opencode`)
- Implements approved plans
- Writes code, tests, and validation output
- Consumes one brief or plan at a time

### Koios (`goose`)
- Captures validated knowledge
- Writes durable notes, provenance, and summaries
- Does not author architecture or code

## Operating rules

1. **One active repo per task**
2. **One harness owns one artifact type**
3. **No cross-repo synthesis inside Athena**
4. **No implementation inside Athena**
5. **No knowledge capture inside implementation runs**
6. **If work spans repos, Hermes decomposes first**
7. **If the tree is dirty, stabilize before expanding scope**

## Handoff flow

```text
user request
  → Hermes routes
  → Athena defines a bounded spec (if needed)
  → Vulcan implements
  → Koios records validated knowledge (if needed)
  → Hermes closes the loop
```

## Required artifacts

- `architecture-spec` / `acceptance-criteria` / `implementation-brief` → Athena
- `implementation-plan` / `patch` / `test-results` / `implementation-report` → Vulcan
- `knowledge-note` / `provenance-index` → Koios
- `routing-decision` / `revision-request` / `completion-decision` → Hermes

## Escalation rule

If a request is ambiguous, multi-repo, or architecture-heavy:
- Hermes splits it first
- Athena receives only the bounded slice
- implementation waits for a brief

## Revision policy

Revise this charter when the split becomes unclear again.
