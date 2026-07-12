```json
{
  "title": "HERMES acceptance: Project-management architecture framing",
  "artifact_type": "workflow-acceptance",
  "status": "accepted",
  "datetime": "20260712.122927Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "project-management-architecture-framing",
  "source_alignment": "docs/plans/petrinet-projectmanagement.20260712.project-alignment.md",
  "accepted_artifact": "docs/architecture/architecture.project-management.md",
  "index_update": "docs/architecture/architecture.00.md",
  "athena_author": "subagent-chat-019f5470 intercom reply 20260712",
  "koios_review": "subagent-chat-019f51a8 intercom reply 20260712",
  "vulcan_review": "subagent-chat-019f527d intercom reply 20260712",
  "implementation_authorization": false,
  "schema_authority_change": false,
  "product_or_vault_authority_change": false,
  "operator_console_mutation_authority": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260712.122927: Project-management architecture framing

## Decision

HERMES accepts ATHENA's project-management architecture framing and phase decomposition as an ATHENA-owned working-draft architecture surface:

```text
docs/architecture/architecture.project-management.md
```

HERMES also accepts the navigation-only index update:

```text
docs/architecture/architecture.00.md
```

## Accepted scope

This acceptance covers architecture framing only:

- long-term filesystem-backed project-management architecture;
- source/control direction using Petri-net definitions, markings/state, transition payloads, and thin operational traces;
- Gantt, Operator Console, Petri-net diagrams, and reports as projections;
- strict dependency flow `petrinet -> workflow -> pm -> projections/ui`;
- layer ownership and forbidden dependencies;
- technology-maturity phases PM-0 through PM-8;
- component dependency map suitable for later Gantt projection;
- recommended future PM-1/PM-2 implementation-brief direction.

## Review basis

ATHENA reported creation of the architecture surface and index update, with `git diff --check` passing.

HERMES independently observed the changed surfaces and verified:

```bash
git diff --check
```

KOIOS provenance/authority-boundary review found no blockers and reported the architecture framing provenance-adequate.

VULCAN implementation-reality review found the architecture implementation-feasible as PM-0 framing with watchpoints, and stated it is not yet sufficient as a coding brief.

## Boundaries preserved

This acceptance does not create:

- implementation authorization;
- schema authority;
- ADR authority or ADR-process dependency;
- product/vault/cross-repo authority;
- Operator Console mutation authority;
- database, daemon, runtime, migration, or cutover authority;
- replacement of existing `state.md`, `active.md`, workflow queue/status fixtures, ADRs, plans, reports, reviews, or AARs.

Operator Console remains projection-only until separately designed and approved for interactive input or mutation.

Gantt remains projection, not source/control.

PM-8 product/vault/cross-repo expansion remains separately gated by the relevant domains.

## Watchpoints carried forward

- ATHENA appropriately reframed USER's task-as-place mental model into a broader architecture test space: task may map to place, subnet, transition payload, or projected work package. Future briefs must not erase USER intent, but should test the mapping rather than assume it universally.
- Architecture-level choices must be answered by ATHENA-owned brief/criteria, not silently by VULCAN implementation convenience.
- Any PM-1/PM-2 cleanup must be behavior-preserving and explicitly bounded in a future implementation brief.
- Thin operational traceability should retain stable IDs, transition events, work-product refs, approvals, and source/projection markers.

## Next decision

HERMES/USER may next ask ATHENA for a bounded PM-1/PM-2 implementation brief, or pause the project-management track.

VULCAN should not implement directly from this architecture note alone.
