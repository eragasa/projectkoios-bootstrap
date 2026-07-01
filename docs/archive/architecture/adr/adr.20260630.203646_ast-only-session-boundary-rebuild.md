# ADR 20260630.203646: AST-only graphify session-boundary rebuild

## Status

historic

## Context

Every session-start and session-end graphify instruction across the Project Koios
bootstrap repository references "refresh Graphify" or "the repo-standard update
flow" without specifying which graphify mode to use.

The graphify tool has two update paths:

1. **`graphify update .`** — AST-only rebuild. Parses source files for
   code structure (classes, functions, imports, calls). No LLM credentials
   required. Completes in seconds with zero external dependencies.
2. **`graphify . --update`** — Includes semantic extraction for documentation
   files. Requires an LLM API key. Fails without one.

The ambiguous phrasing in agent instructions means different sessions may attempt
different commands, and semantic extraction attempts fail locally because no LLM
API key is configured at the machine level.

Additionally, this repository is the Project Koios bootstrap testbed. Patterns
validated here are candidates for adoption by downstream repositories. The
AST-only session-boundary rebuild policy is one such pattern: it is cheap,
reliable, and has no credential dependency.

## Decision

1. `graphify update .` (AST-only, no LLM needed) is the canonical session-boundary
   rebuild command for this repository.
2. All agent instruction files that reference session-end graphify refresh now
   specify `graphify update .` (AST-only, no LLM needed) explicitly.
3. No agent should attempt `graphify . --update` or any other semantic-extraction
   command at session boundaries. Semantic extraction may be used during a session
   when explicitly directed for documentation analysis, but never as part of the
   standard session lifecycle.
4. This policy is part of this repository's role as a Koios testbed. If validated,
   the same AST-only rebuild convention may be adopted by downstream repositories.

## Consequences

- Every agent instruction file has an exact, actionable command — no guessing.
- Session-boundary rebuild completes in seconds with no API key required.
- Semantic extraction is preserved as an in-session tool when explicitly needed,
  but is not part of the session lifecycle.
- This repository validates the pattern for downstream Koios repositories.
- If the graphify CLI command changes, all 8 instruction files plus this ADR need
  coordinated updates.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

Not separately stated in the original archive ADR.

## implementation-brief

Not separately stated in the original archive ADR.

## resolved-open-questions

None stated.

## non-goals

None stated.

## validation-expectations

Not separately stated in the original archive ADR.

## routing

- Owner: Athena
- Next phase: completed
- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260630.203646: AST-only graphify session-boundary rebuild

## Status

historic

## Context

Every session-start and session-end graphify instruction across the Project Koios
bootstrap repository references "refresh Graphify" or "the repo-standard update
flow" without specifying which graphify mode to use.

The graphify tool has two update paths:

1. **`graphify update .`** — AST-only rebuild. Parses source files for
   code structure (classes, functions, imports, calls). No LLM credentials
   required. Completes in seconds with zero external dependencies.
2. **`graphify . --update`** — Includes semantic extraction for documentation
   files. Requires an LLM API key. Fails without one.

The ambiguous phrasing in agent instructions means different sessions may attempt
different commands, and semantic extraction attempts fail locally because no LLM
API key is configured at the machine level.

Additionally, this repository is the Project Koios bootstrap testbed. Patterns
validated here are candidates for adoption by downstream repositories. The
AST-only session-boundary rebuild policy is one such pattern: it is cheap,
reliable, and has no credential dependency.

## Decision

1. `graphify update .` (AST-only, no LLM needed) is the canonical session-boundary
   rebuild command for this repository.
2. All agent instruction files that reference session-end graphify refresh now
   specify `graphify update .` (AST-only, no LLM needed) explicitly.
3. No agent should attempt `graphify . --update` or any other semantic-extraction
   command at session boundaries. Semantic extraction may be used during a session
   when explicitly directed for documentation analysis, but never as part of the
   standard session lifecycle.
4. This policy is part of this repository's role as a Koios testbed. If validated,
   the same AST-only rebuild convention may be adopted by downstream repositories.

## Consequences

- Every agent instruction file has an exact, actionable command — no guessing.
- Session-boundary rebuild completes in seconds with no API key required.
- Semantic extraction is preserved as an in-session tool when explicitly needed,
  but is not part of the session lifecycle.
- This repository validates the pattern for downstream Koios repositories.
- If the graphify CLI command changes, all 8 instruction files plus this ADR need
  coordinated updates.
