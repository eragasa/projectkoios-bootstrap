# Docs model design

## Purpose

Define a single language-neutral representation for the `docs/` tree that can be consumed from Python 3, TypeScript, and Rust.

## Canonical rule

- **Canonical source**: JSON Schema
- **Readable instance format**: YAML or JSON
- **Language bindings**: generated or hand-mirrored from the schema

## Invariants

- Every node has one name, one path, one kind, one lifecycle, and one authority.
- Children are recursive `DocNode` values.
- Language-specific extras must live in `metadata`, not in the core shape.
- The schema must reject unknown top-level fields.

## File set

- `schema/docs-node.schema.json` — canonical schema
- `python/docs_model.py` — Python 3 types
- `typescript/docs-model.ts` — TypeScript types
- `rust/docs_model.rs` — Rust types
- `examples/docs-tree.yaml` — example tree instance

## Intended use

1. Validate a docs manifest.
2. Load it in any supported language.
3. Use it as the source for docs taxonomy, tooling, and skill governance.
