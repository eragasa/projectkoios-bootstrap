---
status: draft
"back_to:": architecture.00
version: " 0.0.0.20260701"
---

# architecture.docs

## Status

draft


## Docs Tree

```text
   docs/
   ├── README.md
   ├── index.md
   ├── architecture/
   │   ├── adr/
   │   ├── specs/
   │   └── briefs/
   ├── workflows/
   │   ├── process/
   │   ├── runbooks/
   │   └── templates/
   ├── skills/
   │   ├── specs/
   │   └── design/
   ├── governance/
   │   ├── policies/
   │   ├── roles/
   │   └── decisions/
   ├── handoffs/
   ├── archive/
   │   ├── handoffs/
   │   └── superseded/
   ├── AAR/
   └── notes/
```

## Context

We need a canonical architecture document for the documentation system itself.
The document must be stable enough to serve as the active Obsidian database key,
while replacement versions are archived under timestamped filenames.

This repo also needs a docs representation that can be consumed by Python 3,
TypeScript, and Rust.

## Decision

The active document is `architecture.docs.md`.
When replaced, the prior active file is archived as a timestamped copy using its
creation time, for example `architecture.docs.20260701.182553.md`.

The documentation system is modeled as a typed tree of `DocNode` values with:

- `name`
- `path`
- `kind`
- `lifecycle`
- `authority`
- `description`
- `metadata`
- `children`

The canonical schema is JSON Schema.
YAML and JSON are allowed instance formats.
Language bindings may be generated or mirrored for:

- Python 3
- TypeScript
- Rust

## Constraints

- One active file per stable name.
- Archive copies must preserve the original active content.
- Unknown top-level fields are rejected by schema validation.
- Language-specific extensions belong in `metadata`.
- The model must remain portable across the supported languages.

## Consequences

- Obsidian can reference a stable filename as the current authority.
- Historical versions remain recoverable by timestamp.
- Tooling can validate the docs tree consistently across languages.
- The docs taxonomy can evolve without changing the active filename.

## Links

| Link | Target |
|---|---|
| `[[architecture.docs]]` | Active docs architecture doc |
| `[[architecture.repositories.00]]` | Repository architecture reference |