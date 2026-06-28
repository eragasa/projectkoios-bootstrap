# Package map

Authoritative mapping of package to responsibility. Each row describes the
canonical location for a given concern.

| Responsibility | Repository | Package path |
|---------------|------------|-------------|
| Core/shared abstractions | projectkoios | src/python/projectkoios/core/ |
| Vault scanner & markdown | projectkoios-obsidian | src/python/projectkoios/obsidian/ |
| Search indexing & retrieval | projectkoios-search | src/python/projectkoios/search/ |
| References & citations | projectkoios-references | src/python/projectkoios/references/ |
| Workflow engine & provenance | projectkoios-workflow | src/python/projectkoios/workflow/ |
| Ingestion & chunking | projectkoios-ingestion | src/python/projectkoios/ingestion/ |
| Agent harness | projectkoios-agent | src/python/projectkoios/agent/ |
| HTTP API | projectkoios-api | src/python/projectkoios/api/ |
| Meta-harness config | projectkoios-bootstrap | (no Python code — config only) |

Update this file when packages are added, renamed, or relocated.
