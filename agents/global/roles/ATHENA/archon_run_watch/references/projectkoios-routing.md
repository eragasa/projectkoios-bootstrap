# Project Koios routing guide

## Harness roles

| Harness | Name | Role |
|---|---|---|
| pi | Hermes | Meta-harness — orchestration, operations, handoff coordination |
| archon (archon.diy) | Athena | Architecture design, ADRs, planning |
| opencode | Vulcan | Code writing, tests, validation |
| goose | Koios | Knowledge management, vault ops |

## Artifact ownership

| Artifact | Owner |
|---|---|
| user-request | user |
| architecture-spec, acceptance-criteria, implementation-brief | Athena |
| implementation-plan, patch, test-results, implementation-report, deviation-report | Vulcan |
| knowledge-note, provenance-index | Koios |
| routing-decision, revision-request, completion-decision | Hermes |

## When to bypass specialist routing

Route directly as Hermes when:
- Lightweight config changes (editing YAML, env vars)
- The specialist already failed or is unavailable
- Mechanical changes that follow an established pattern
- Handoff artifacts that the specialist would produce anyway
