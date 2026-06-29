# Package map

Authoritative mapping of package to responsibility. Each row describes the
canonical location for a given concern.

| Responsibility | Repository | Package path |
|---------------|------------|-------------|
| Shared abstractions (chunking, repos) | projectkoios | src/python/projectkoios/{chunking,repositories}/ |
| Search & indexing | projectkoios-search | src/python/projectkoios/{search,indexing}/ |
| HTTP API & runtime wiring | projectkoios-api | src/python/projectkoios/{api,runtime}/ |
| Obsidian vault management | projectkoios-obsidian | src/python/projectkoios/obsidian/ |
| References & citations | projectkoios-references | src/python/projectkoios/references/ |
| Workflow engine & provenance | projectkoios-workflow | src/python/projectkoios/workflow/ |
| Agent harness | projectkoios-agent | src/python/projectkoios/agent/ |
| Meta-harness config & bootstrap CLI | projectkoios-bootstrap | src/python/projectkoios/bootstrap/ |

Update this file when packages are added, renamed, or relocated.
