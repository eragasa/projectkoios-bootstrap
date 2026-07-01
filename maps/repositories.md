# Repository map

Authoritative list of Project Koios git repositories in this workspace.
Use this with `docs/agent-charter.md` for harness routing.
For vault directories, see `maps/vault_paths.md`.

| Repository | Purpose |
|---|---|
| projectkoios | mothership — shared kernel, architecture docs, ADRs, examples |
| projectkoios-bootstrap | meta-harness — routing, shared harness config, maps |
| projectkoios-agent | agent harness and workflow orchestration |
| projectkoios-api | FastAPI HTTP interface |
| projectkoios-ingestion | source ingestion and document processing pipeline |
| projectkoios-search | full-text and semantic search infrastructure |
| projectkoios-workflow | Petri-net workflow execution engine |
| projectkoios-references | reference management and citation handling |
| projectkoios-obsidian | Obsidian vault management and knowledge curation |

Note: `projectkoios-notes` is the Obsidian vault directory, not a git repo.
See `maps/vault_paths.md` for vault locations.

Update this file when repos are added, removed, or renamed.
