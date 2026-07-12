```json
{
  "title": "Petri-net Project Management document index",
  "artifact_type": "project-index",
  "status": "active-index",
  "datetime": "20260712",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "project_slug": "petrinet-projectmanagement",
  "index_scope": "navigation and connection map for Petri-net project-management documents",
  "source_control_runtime_state": false,
  "architecture_authority": false
}
```

# Petri-net Project Management document index

## Status

This is a navigation and connection-map index for Petri-net project-management documents.

It is not runtime source/control state, architecture authority, implementation authorization, or a project-management state machine.

## Naming convention

Dated artifacts for this project use:

```text
petrinet-projectmanagement.<datetime>.<taskphase>.<updatetype>.md
```

Current task phase:

```text
pm-0
```

## Stable index nodes

- Overall project index: `docs/plans/petrinet-projectmanagement.00.md`
- Architecture index: `docs/architecture/architecture.project-management.00.md`

## Rename trace

The PM-0 files were normalized to this convention from earlier names on 20260712:

| Earlier path | Current path |
|---|---|
| `docs/plans/petrinet-projectmanagement.20260712.project-alignment.md` | `docs/plans/petrinet-projectmanagement.20260712.pm-0.project-alignment.md` |
| `docs/architecture/architecture.project-management.md` | `docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md` |
| `docs/reviews/hermes-acceptance.20260712.122927_project-management-architecture-framing.md` | `docs/reviews/petrinet-projectmanagement.20260712.122927.pm-0.hermes-acceptance.md` |
| `docs/AAR/aar.20260712.032653_petrinet-projectmanagement-alignment.md` | `docs/AAR/petrinet-projectmanagement.20260712.032653.pm-0.aar.md` |

## PM-0 artifacts

| Artifact | Path | Role |
|---|---|---|
| Project alignment | `docs/plans/petrinet-projectmanagement.20260712.pm-0.project-alignment.md` | HERMES user-alignment handoff and source input |
| Architecture index | `docs/architecture/architecture.project-management.00.md` | Architecture navigation for PM surfaces |
| Architecture framing | `docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md` | ATHENA long-term architecture and phase decomposition |
| HERMES acceptance | `docs/reviews/petrinet-projectmanagement.20260712.122927.pm-0.hermes-acceptance.md` | HERMES acceptance of PM-0 architecture framing |
| AAR | `docs/AAR/petrinet-projectmanagement.20260712.032653.pm-0.aar.md` | Process observations from alignment session |

## Current status

PM-0 architecture framing has been accepted by HERMES as working-draft architecture framing after KOIOS and VULCAN review.

No implementation, schema, product/vault, cross-repo, Operator Console mutation, migration, or cutover authority is created by this index.

## Next routed action

HERMES/USER may next ask ATHENA for a bounded PM-1/PM-2 implementation brief based on:

```text
docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md
```
