# Package map

Authoritative mapping of package responsibility to repository.
Use this with `maps/repositories.md` and `docs/agent-charter.md`.
Package roots are under `src/python/projectkoios/` in each repo.

| Responsibility | Repository | Package path |
|---|---|---|
| Shared kernel / common abstractions | projectkoios | src/python/projectkoios/{chunking,repositories}/ |
| Ingestion & document processing | projectkoios-ingestion | src/python/projectkoios/ingestion/ |
| Search & indexing | projectkoios-search | src/python/projectkoios/{search,indexing}/ |
| HTTP API & runtime wiring | projectkoios-api | src/python/projectkoios/{api,runtime}/ |
| Obsidian vault management | projectkoios-obsidian | src/python/projectkoios/obsidian/ |
| References & citations | projectkoios-references | src/python/projectkoios/references/ |
| Workflow engine & provenance | projectkoios-workflow | src/python/projectkoios/workflow/ |
| Agent harness | projectkoios-agent | src/python/projectkoios/agent/ |
| Meta-harness config & bootstrap CLI | projectkoios-bootstrap | src/python/projectkoios/bootstrap/ |

Update this file when packages are added, renamed, or relocated.
