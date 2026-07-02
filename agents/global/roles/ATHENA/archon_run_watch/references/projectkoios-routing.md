# Project Koios sandbox message delivery guide

## Harness roles

| Harness | Name | Role |
|---|---|---|
| Hermes | Hermes | Meta-harness — orchestration, operations, handoff coordination |
| archon (archon.diy) | Athena | Architecture design, ADRs, planning |
| opencode | Vulcan | Code writing, tests, validation |
| goose | Koios | Knowledge management, vault ops |

## Artifact ownership

| Artifact | Owner | Notes |
|---|---|---|
| user-request | user | Original task or instruction |
| architecture-spec | Athena | Bounded architecture decision |
| acceptance-criteria | Athena | Inspectable criteria for completion |
| implementation-brief | Athena | Concrete instructions for implementation |
| implementation-plan | Vulcan | Planned file-level changes |
| patch | Vulcan | Repository modification |
| test-results | Vulcan | Validation output |
| implementation-report | Vulcan | Summary of what changed |
| deviation-report | Vulcan | Mismatch between spec and reality |
| knowledge-note | Koios | Durable note from validated artifacts |
| provenance-index | Koios | Mapping from claims to sources |
| provenance-audit | Koios | Capture-gap detection report |
| repo-state-summary | Koios (advisory) | Snapshot for Hermes |
| routing-recommendation | Koios (advisory) | Suggested recipient sandbox for Hermes |
| routing-decision | Hermes | Recipient sandbox decision |
| revision-request | Hermes | Return for revision |
| completion-decision | Hermes | Gate result |

## When to bypass specialist sandbox message delivery

Handle directly as Hermes when:
- Lightweight config changes (editing YAML, env vars)
- The specialist already failed or is unavailable
- Mechanical changes that follow an established pattern
- Handoff artifacts that the specialist would produce anyway
