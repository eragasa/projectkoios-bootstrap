# ADR 20260630.002151: Harness asset three-layer model

## Status

Superseded by adr.20260630.170000_pending-athena-decisions.md

## Context

The repo layout mixed three distinct concerns in confusing ways:
- harness ownership
- tool-native runtime layout
- committed source-of-truth content

For example, `archon/skills/.agents/skills/archon` looks partly like
checked-in source, partly like installed runtime structure, and partly like
Archon-specific ownership. Similar ambiguity existed across the repo.

This made it hard to answer:
- What is canonical shared source?
- What is safe to override locally?
- What is generated/installed runtime state?
- Which directory should future harness assets live in?

## Decision

Adopt a three-layer asset model:

### 1. Committed shared source

`agents/global/<harness>/...` — canonical checked-in assets.

### 2. Optional repo-local overrides

`agents/local/<harness>/...` — developer-specific, git-ignored overrides for
local experimentation.

### 3. Installed machine/runtime state

Outside committed source (e.g., `~/.pi/`, `~/.archon/`) — tool-native
runtime layout that bootstrap commands materialise from the source layers.

### Handoffs excluded

Handoffs are operational artifacts exchanged between harnesses, not reusable
runtime config. They remain in harness-owned top-level directories (or are
archived when superseded).

## Consequences

- Source layout reflects repo semantics (harness, asset kind, shared vs local);
  runtime layout reflects tool semantics.
- Bootstrap install/sync steps translate from source layout to runtime layout.
- No immediate migration — the model is documented for future layout changes.
- The confusing pattern `archon/skills/.agents/skills/archon` is deprecated.

## Source

This ADR distills content from `docs/archive/handoffs/archon/20260630.002151_global-local-harness-assets-split.md`.
