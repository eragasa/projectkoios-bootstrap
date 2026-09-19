# Project Koios repository map

Project Koios Git repositories are sibling directories beneath one operator
workspace. Resolve paths relative to this repository's parent directory; do not
encode a machine-specific absolute path. The GitHub identity column is the
trusted canonical host/owner/repository mapping. Local checkout origins are
consistency evidence and must match it; they do not redefine repository
authority.

| Repository | GitHub identity | Coordination purpose |
|---|---|---|
| `projectkoios` | `github.com/eragasa/projectkoios` | Mothership: product architecture and cross-repository decisions |
| `projectkoios-bootstrap` | `github.com/eragasa/projectkoios-bootstrap` | Multi-repository operational coordination and Project Koios-specific Pi harness incubation |
| `projectkoios-agent` | `github.com/eragasa/projectkoios-agent` | Deferred reusable agent-domain components |
| `projectkoios-api` | `github.com/eragasa/projectkoios-api` | HTTP API and runtime boundary |
| `projectkoios-courses` | `github.com/eragasa/projectkoios-courses` | Course-related functionality and content |
| `projectkoios-ingestion` | `github.com/eragasa/projectkoios-ingestion` | Source ingestion and document processing |
| `projectkoios-obsidian` | `github.com/eragasa/projectkoios-obsidian` | Obsidian integration and vault management |
| `projectkoios-references` | `github.com/eragasa/projectkoios-references` | References and citations |
| `projectkoios-research` | `github.com/eragasa/projectkoios-research` | Research-portfolio identity, discovery, and external-project relationships |
| `projectkoios-search` | `github.com/eragasa/projectkoios-search` | Search and indexing |
| `projectkoios-web` | `github.com/eragasa/projectkoios-web` | Browser interface |
| `projectkoios-workflow` | `github.com/eragasa/projectkoios-workflow` | Reusable workflow execution |

The following sibling directories may exist but are not Git repositories:

- `projectkoios-notes` — local Obsidian vault;
- `projectkoios-spec` — local specification material; and
- `projectkoios.com` — local website material.

Update this map only when repository topology changes. Runtime session status
belongs to Pi, not this file.
