```json
{
  "title": "HERMES acceptance: PM-0 working-engine and Console projection refinement",
  "artifact_type": "workflow-acceptance",
  "status": "accepted",
  "datetime": "20260712.143207Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-projectmanagement-pm-0-working-engine-console-projection-refinement",
  "accepted_artifact": "docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md",
  "source_architecture_acceptance": "docs/reviews/petrinet-projectmanagement.20260712.132754.pm-0.hermes-acceptance.md",
  "vulcan_review": "subagent-chat-019f527d intercom reply 20260712",
  "koios_review": "subagent-chat-019f51a8 intercom reply 20260712",
  "implementation_authorization": false,
  "console_mutation_authority": false,
  "persistent_mutation_authority": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260712.143207: PM-0 working-engine and Console projection refinement

## Decision

HERMES accepts ATHENA's PM-0 architecture refinement to:

```text
docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md
```

## Accepted refinement

The update clarifies that the first implementation direction is:

```text
petrinet-pm-working-engine-slice-0
```

The future first implementation should produce a minimal working engine implementation plus a Console projection/read-model for that engine's capability, not merely planning or skeleton artifacts.

Accepted architectural direction:

- PM-1 includes a minimal executable/inspectable engine that can load a simplified Petri-net/workflow skeleton and emit deterministic output.
- Optional non-persistent in-memory enablement/step checks may be used as engine proof.
- Console projection/read-model starts in PM-1 and should reflect each phase's backend capability.
- Phases may be decomposed into backend and frontend/projection subphases.
- Console projection remains projection/read-model only unless later separately accepted for interaction or mutation.

## Review basis

ATHENA reported `git diff --check` passed.

HERMES independently verified:

```bash
git diff --check
```

VULCAN found the refinement implementation-feasible as architecture direction with no hard blocker.

KOIOS found no provenance or authority-boundary blocker.

## Boundaries preserved

This acceptance is architecture framing only. It does not authorize implementation.

This acceptance does not create:

- Console mutation authority;
- persistent transition mutation authority;
- Gantt source/control authority;
- schema or database authority;
- product/vault/cross-repo authority;
- package move/refactor implementation authority.

Non-persistent in-memory stepping, if later scoped, must not write state files and must not be represented as controlled transition execution.

Planning Gantt and Console projections must be visibly labeled projection, non-source, and non-control.

## Watchpoints carried forward

- Future PM-0/PM-1 brief must specify exact engine API/output, skeleton file path/shape, Console projection path/fields, deterministic tests, behavior-preservation tests, compatibility import policy, and split criteria if scope grows.
- The brief should clarify any component dependency ambiguity between engine and skeleton: skeleton is input to the engine, or engine/skeleton are co-developed in PM-1.
- Console projection in PM-1 is a generated/fixture read model, not interactive UI rendering or mutation.
