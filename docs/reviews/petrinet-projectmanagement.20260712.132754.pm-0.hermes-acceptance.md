```json
{
  "title": "HERMES acceptance: PM-0 hybrid Gantt architecture refinement",
  "artifact_type": "workflow-acceptance",
  "status": "accepted",
  "datetime": "20260712.132754Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-projectmanagement-pm-0-hybrid-gantt-refinement",
  "accepted_artifact": "docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md",
  "source_architecture_acceptance": "docs/reviews/petrinet-projectmanagement.20260712.131949.pm-0.hermes-acceptance.md",
  "koios_review": "subagent-chat-019f51a8 intercom reply 20260712",
  "vulcan_review": "subagent-chat-019f527d intercom reply 20260712",
  "implementation_authorization": false,
  "gantt_source_control_authority": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260712.132754: PM-0 hybrid Gantt architecture refinement

## Decision

HERMES accepts ATHENA's hybrid Gantt architecture refinement to:

```text
docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md
```

## Accepted refinement

The update distinguishes two Gantt roles:

- `PROJ-GANTT-PLAN`: early PM-0/PM-1 planning/design projection derived from the architecture phase table and component dependency map;
- `PROJ-GANTT-OPS`: later PM-5 operational/live projection generated from PM/workflow source-control read models.

The early planning Gantt may be used to reveal sequencing, critical-path hints, missing dependencies, and required work products before PM-1/PM-2 implementation planning.

Findings from early planning Gantt must be back-propagated into architecture or later source/control design before becoming implementation requirements.

## Review basis

ATHENA reported `git diff --check` passed.

HERMES independently verified:

```bash
git diff --check
```

KOIOS found no provenance/authority blocker and confirmed projection boundaries are preserved.

VULCAN found no implementation blocker and confirmed the split reduces the risk of pulling PM-5 operational Gantt semantics into PM-0/PM-1.

## Boundaries preserved

This acceptance does not authorize implementation.

This acceptance does not make Gantt source/control authority, workflow truth, runtime state, implementation authorization, or a replacement for Petri-net/workflow/project-management files.

A planning Gantt artifact, if produced later, must be visibly labeled as planning/design projection only.

Operational/live Gantt remains deferred to PM-5 or a separately accepted scope.

Duration, calendar, resource, and critical-path semantics remain hints only unless separately scoped and accepted.
