```json
{
  "title": "HERMES acceptance: PM-0 architecture refinement for PM-1/PM-2 questions",
  "artifact_type": "workflow-acceptance",
  "status": "accepted",
  "datetime": "20260712.131949Z",
  "acting_as": "HERMES",
  "repository": "projectkoios-bootstrap",
  "scope": "petrinet-projectmanagement-pm-0-architecture-refinement-pm-1-pm-2-questions",
  "accepted_artifact": "docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md",
  "source_alignment": "docs/plans/petrinet-projectmanagement.20260712.pm-0.project-alignment.md",
  "source_architecture_acceptance": "docs/reviews/petrinet-projectmanagement.20260712.122927.pm-0.hermes-acceptance.md",
  "vulcan_review": "subagent-chat-019f527d intercom reply 20260712",
  "koios_review": "subagent-chat-019f51a8 intercom reply 20260712",
  "implementation_authorization": false,
  "schema_or_file_format_authority": false,
  "operator_console_mutation_authority": false,
  "external_engine_required_dependency": false,
  "next_owner": "HERMES_USER"
}
```

# HERMES acceptance 20260712.131949: PM-0 architecture refinement for PM-1/PM-2 questions

## Decision

HERMES accepts ATHENA's PM-0 architecture refinement incorporating USER's PM-1/PM-2 question answers and ATHENA recommendations into:

```text
docs/architecture/architecture.petrinet-projectmanagement.20260712.pm-0.architecture-framing.md
```

## Accepted refinement

The update clarifies:

- concrete package targets:
  - `src/python/projectkoios/petrinet/`
  - `src/python/projectkoios/workflow/`
  - `src/python/projectkoios/project_management/`
- strict layer flow as `projectkoios.petrinet -> projectkoios.workflow -> projectkoios.project_management`, with `pm` only as a CLI abbreviation;
- CLI target `koios pm *`, with first read-only surface preferably `koios pm status`;
- PM-2 incubation namespace `dev/project-management/self/` with `source/`, `projections/`, and `evidence/`;
- recommended minimal PM-2 pilot source/control files;
- source/control, projection/read-model, and test/evidence classification;
- YAGNI transition-payload baseline;
- concrete cleanup/refactor framing as package-boundary establishment and mechanical cleanup only, with behavior preservation;
- self-project-management pilot validator criteria;
- immediate Operator Console fixture/read-model as projection-only PM-2 scope;
- adapter/SNAKES scope as encapsulated, lazy, fail-soft, and non-blocking unless separately gated.

## Review basis

ATHENA reported `git diff --check` passed.

HERMES independently verified:

```bash
git diff --check
```

VULCAN found the refinement implementation-feasible with no hard blocker and identified watchpoints for dependency-arrow wording, compatibility wrappers/re-exports, CLI alias scope, and behavior preservation.

KOIOS found no provenance or authority-boundary blocker and confirmed the update preserves USER answers while remaining architecture guidance for a later implementation brief.

## Boundaries preserved

This acceptance does not authorize implementation.

This acceptance does not create:

- schema or reusable file-format authority;
- product/vault/cross-repo authority;
- Operator Console mutation or interactive input authority;
- required SNAKES or external-engine dependency;
- broad package extraction or behavior redesign authority;
- transition mutation, migration, or cutover authority.

Concrete filenames and package paths are architecture recommendations for a future bounded implementation brief, not immediate implementation authorization.

The split file set under `dev/project-management/self/source/` is a minimal pilot source/control recommendation, not a repository-wide PM standard or schema contract.

## Watchpoints carried forward

- The layer arrow is conceptual dependency flow: `projectkoios.workflow` may depend on `projectkoios.petrinet`, and `projectkoios.project_management` may depend on `projectkoios.workflow`; lower layers must not import higher layers.
- PM-1 package-boundary establishment must include compatibility import/wrapper policy and behavior-preservation checks.
- Future brief must resolve whether `koios pm status` requires a new CLI alias or is implemented behind existing CLI mechanics first.
- Operator Console PM-2 output remains fixture/read-model projection only.
- Adapter/SNAKES work must remain optional and non-blocking unless separately accepted as a gate.

## Next decision

HERMES/USER may now ask ATHENA for a bounded PM-1/PM-2 implementation brief using this architecture refinement and the accepted project-alignment answers.
