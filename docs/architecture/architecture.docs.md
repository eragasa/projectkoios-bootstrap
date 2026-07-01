---
status: draft
back_to: architecture.00
version: 0.0.0.20260701
---
# Document Architecture

## Purpose

This is the canonical architecture document for the documentation system itself.
It is the stable active Obsidian key for the docs architecture surface.

## Scope

It defines the active docs architecture key, archival replacement rule, and a portable documentation model consumable by Python 3, TypeScript, and Rust.

## Decision

The active document is `architecture.docs.md`. It is the stable key for the documentation architecture surface.
When replaced, the previous active file is archived under a timestamped filename such as `architecture.docs.20260701.182553.md`.

The documentation model is a typed tree of `DocNode` values with:

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
- Archive copies preserve the original active content.
- Unknown top-level fields are rejected by schema validation.
- Language-specific extensions belong in `metadata`.
- The model must remain portable across the supported languages.

## Consequences

- Obsidian can reference a stable filename as the current authority.
- Historical versions remain recoverable by timestamp.
- Tooling can validate the docs tree consistently across languages.
- The docs taxonomy can evolve without changing the active filename.

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

## Links

| Link | Target |
|---|---|
| `[[architecture.00]]` | Active architecture index |
| `[[architecture.repositories.00]]` | Repository architecture reference |
