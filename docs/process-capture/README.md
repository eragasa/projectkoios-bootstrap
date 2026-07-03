# Process capture

This directory stores durable repo-local records of how software-development work moves between roles.

The repo filesystem is the coordination surface.

Process state advances by creating the next artifact and linking it backward to the prior artifact.

Process-capture records MUST NOT require a message router or delivery role.

Process-capture records MUST NOT be treated as ADRs, implementation reports, AARs, or workflow policy.

Process-capture records MAY recommend follow-up ADRs, policy updates, checklist changes, skills, or implementation tasks.

## Files

- `workflow.process-capture.md` defines the filesystem-sequential process-capture workflow.
- `schema.process-chain.md` defines the reusable process-chain note schema.
- `20260704_graphrag-first-slice-athena-vulcan-process-chain.md` captures the GraphRAG first-slice ATHENA/VULCAN process chain.

## Naming

Workflow documents SHOULD use `workflow.<topic>.md`.

Schema documents SHOULD use `schema.<artifact-type>.md`.

Process-chain notes SHOULD use `YYYYMMDD_<slice>-<roles>-process-chain.md`.

## Promotion path

Repeated process observations MAY become workflow policy, checklist updates, skills, or ADR candidates.

Promotion MUST happen through the appropriate authority surface.
