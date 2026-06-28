## graphify

This project has a knowledge graph at `graphify-out/` with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, load and follow the `graphify` skill before doing anything else.

Rules:
- For codebase questions, if `graphify-out/graph.json` exists, run `graphify query "<question>"` first. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These usually return a smaller, more relevant subgraph than `GRAPH_REPORT.md` or raw source search.
- If `graphify-out/graph.json` does not exist, graphify is unavailable, or the task requires exact edit-level verification, inspect the source directly.
- Git-dirty files under `graphify-out/` are expected after hooks or incremental updates; this alone is not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, graphify fails, or the user explicitly says not to use it.
- If `graphify-out/wiki/index.md` exists, prefer it for broad navigation, but use source files when precise implementation details matter.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when `query`/`path`/`explain` do not surface enough context.
- After modifying code, run `graphify update .` when available to keep the graph current (AST-only, no API cost).
