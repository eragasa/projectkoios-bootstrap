# Project Koios routing table

## Harness roles

| Harness | Role name | Responsibility |
|---|---|---|
| `pi` | Hermes | Operations, run control, handoff coordination, direct lightweight edits |
| `archon` | Athena | Architecture spec, ADRs, plans, acceptance criteria |
| `opencode` | Vulcan | Implementation, tests, validation, bug fixes |
| `goose` | Koios | Durable knowledge notes, provenance index, vault work |

## Artifact ownership

| Artifact | Owner |
|---|---|
| `user-request` | user |
| `architecture-spec` | spec agent (Athena) |
| `acceptance-criteria` | spec agent (Athena) |
| `implementation-brief` | spec agent (Athena) |
| `implementation-plan` | code agent (Vulcan) |
| `patch` | code agent (Vulcan) |
| `test-results` | code agent (Vulcan) |
| `implementation-report` | code agent (Vulcan) |
| `deviation-report` | code agent (Vulcan) |
| `knowledge-note` | knowledge agent (Koios) |
| `provenance-index` | knowledge agent (Koios) |
| `routing-decision` | meta-harness (Hermes) |
| `revision-request` | meta-harness (Hermes) |
| `completion-decision` | meta-harness (Hermes) |

## When to bypass specialist routing

Ceremony is justified when it reduces ambiguity, improves validation, or
preserves durable knowledge. Bypass the specialist and do the work directly
as Hermes when:

1. The task is a lightweight config change or direct edit (single file,
   clear scope, no architecture impact).
2. The specialist path has already failed (e.g. Archon prompt-node exits
   without completion twice in one session — fall back to Hermes).
3. The output is a handoff artifact that the specialist would produce anyway
   and the procedural steps add no validation value.
4. The change is purely mechanical (rename, re-indent, move file) with no
   design decision.
