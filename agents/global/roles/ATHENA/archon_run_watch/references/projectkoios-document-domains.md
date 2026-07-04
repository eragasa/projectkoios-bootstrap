# Project Koios document-domain guide

## Harness roles

| Harness | Name | Document domain |
|---|---|---|
| Hermes | Hermes | Cross-domain orchestration, repository state reconciliation, completion decisions |
| archon (archon.diy) | Athena | Architecture design, ADRs, specifications, acceptance criteria |
| opencode | Vulcan | Code changes, implementation plans, tests, validation evidence |
| goose | Koios | Knowledge notes, provenance indexes, vault-oriented capture |

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
| state-observation | Koios (advisory) | Observation about document-domain consistency |
| state-reconciliation | Hermes | Cross-domain consistency decision |
| revision-request | Hermes | Request to revise a document-domain state |
| completion-decision | Hermes | Gate result |

## When Hermes handles the state change directly

Handle directly as Hermes when:
- Lightweight config or status changes follow an established pattern
- The specialist already failed or is unavailable
- Mechanical changes are required to make document domains consistent
- The work is a cross-domain inconsistency rather than a domain-owned transformation
