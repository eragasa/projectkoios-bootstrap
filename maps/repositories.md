# Project Koios repository map

Project Koios Git repositories are sibling directories beneath one operator
workspace. Resolve paths relative to this repository's parent directory; do not
encode a machine-specific absolute path.

| Repository | Coordination purpose |
|---|---|
| `projectkoios` | Mothership: product architecture and cross-repository decisions |
| `projectkoios-bootstrap` | Multi-repository operational coordination |
| `projectkoios-agent` | Deferred reusable agent-domain components |
| `projectkoios-api` | HTTP API and runtime boundary |
| `projectkoios-courses` | Course-related functionality and content |
| `projectkoios-ingestion` | Source ingestion and document processing |
| `projectkoios-obsidian` | Obsidian integration and vault management |
| `projectkoios-references` | References and citations |
| `projectkoios-research` | Research-portfolio identity, discovery, and external-project relationships |
| `projectkoios-search` | Search and indexing |
| `projectkoios-web` | Browser interface |
| `projectkoios-workflow` | Reusable workflow execution |

The following sibling directories may exist but are not Git repositories:

- `projectkoios-notes` — local Obsidian vault;
- `projectkoios-spec` — local specification material; and
- `projectkoios.com` — local website material.

Update this map only when repository topology changes. Runtime session status
belongs to Pi, not this file.
