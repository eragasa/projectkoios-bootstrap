# ADR 20260630.141739: Handoff ledger projection

## Status

Draft

## Context

The handoff evaluator produced violation reports but lacked a structured
projection of the full handoff state. The user reframed this as a
protocol/provenance problem: build a read-only handoff ledger projection.

The existing codebase already had:
- `HandoffParser` — parses handoff markdown into `HandoffArtifact` tokens
- `HandoffEvaluator` — runs guard rules against tokens
- `Marking` — current distribution of tokens across places
- `Violation` — structured guard failure output

## Decision

Extend the existing evaluator surface into a read-only ledger projection
pipeline:

```
handoff files → message records → inferred transitions → current marking
→ guard violations → deterministic JSON projection
```

### Key concepts

- **message** — one parsed handoff artifact derived from one markdown file
- **message_id** — deterministic stable identifier
- **transition** — process event with `source: inferred` or `source: audited`
- **marking** — mapping of places to message identifiers
- **projection** — complete read-only JSON view

### First-slice constraints

- Read-only, mutates no handoff files
- No pub/sub transport, no append-only ledger writer
- No external dependencies
- Existing markdown handoffs remain the sole source input
- Deterministic across repeated runs over the same files
- Inferred provenance explicitly labelled as `source: inferred`

### JSON contract

The projection contains: `schema_version`, `repo_root`, `messages`,
`transitions`, `marking`, `guard_violations`, `summary`. Each message
includes `message_id`, `source_path`, `place`, artifact `kind`, and header
fields. Each violation references `message_id` and `source_path`.

## Consequences

- The projection becomes the portable protocol surface for future consumers.
- The CLI output shifts from "evaluator report" lexicon to "ledger projection"
  vocabulary.
- The existing `handoff evaluate` command can be extended or wrapped for
  compatibility.
- Guard violations are now bound to stable message identifiers instead of
  raw filesystem paths.

## Source

This ADR distills content from `docs/archive/handoffs/archon/20260630.141739_handoff-ledger-projection-spec.md`.
