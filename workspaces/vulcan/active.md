```json
{
  "title": "Vulcan active work",
  "artifact_type": "workspace-active-priorities",
  "status": "template-record-roundtrip-skill-reviewed-ready-to-package",
  "datetime": "20260709.013100Z",
  "acting_as": "VULCAN",
  "repository": "projectkoios-bootstrap",
  "workspace": "workspaces/vulcan/",
  "branch": "master",
  "priority_count": 3,
  "working_directory": "working/",
  "active_working_items": [
    "agents/global/opencode/skills/template-record-roundtrip/SKILL.md",
    "docs/skills/skill-register.md",
    "docs/implementation/template-record-roundtrip-skill.20260709.012011.md",
    "docs/AAR/aar.20260709.012011_template-record-roundtrip-skill.md",
    "docs/reviews/architecture-conformance.20260709.012745_template-record-roundtrip-skill.md",
    "docs/process-capture/pc.workflow.document-trace.20260709.012953Z.md",
    "docs/process-capture/pc.workflow.document-trace.md"
  ],
  "scratch_directory": "scratch/",
  "source_brief": "docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md",
  "related_conformance_review": "docs/reviews/architecture-conformance.20260709.012745_template-record-roundtrip-skill.md"
}
```

# Vulcan active work

## Current priority stack

1. Package/commit/push the validated parser + draft skill slice per user/Hermes direction.
2. Keep KOIOS ADR-lifecycle provenance-audit workspace material out of the skill-slice commit unless explicitly requested.
3. Do not promote the skill to stable, expand to broad template migration, add CLI enforcement, or create ingestion systems without a new brief.

## Latest working material

- Skill source brief: `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md`.
- Skill: `agents/global/opencode/skills/template-record-roundtrip/SKILL.md`.
- Skill register: `docs/skills/skill-register.md`.
- Latest skill report: `docs/implementation/template-record-roundtrip-skill.20260709.012011.md`.
- Latest skill AAR: `docs/AAR/aar.20260709.012011_template-record-roundtrip-skill.md`.
- Skill conformance review: `docs/reviews/architecture-conformance.20260709.012745_template-record-roundtrip-skill.md`.
- KOIOS process trace: `docs/process-capture/pc.workflow.document-trace.20260709.012953Z.md` and aggregate `docs/process-capture/pc.workflow.document-trace.md`.
- Parser report: `docs/implementation/template-representation-roundtrip.20260708.044531.md`.
- Parser conformance review: `docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md`.

## Latest validation evidence

- VULCAN: `uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q` => `34 passed in 0.16s`.
- VULCAN: `uv run projectkoios bootstrap validate-python-policy agents/global/opencode/skills/template-record-roundtrip` => `summary: 0 finding(s), 0 file(s)`; Markdown-only skill path.
- VULCAN: frontmatter/Markdown inspection script => `frontmatter/markdown inspection: ok`.
- VULCAN: `git diff --check` => clean.
- ATHENA review reran focused pytest, skill-path Python policy, and `git diff --check` with passing/clean results.

## Implementation notes

- New skill is draft/gated and VULCAN/opencode-owned.
- Skill register row uses draft/supporting binding mode and matches skill ADR bindings.
- Skill procedure requires schema-backed records, schema validation, deterministic rendering, re-parse, re-validation, semantic equality, focused validation, and deviation reporting on boundary failures.
- ATHENA accepted the skill integration as conforming draft/gated work; no promotion to stable is authorized.

## Ignore for now

- KOIOS ADR-lifecycle provenance-audit workspace artifact unless explicitly requested.
- Graphify ingestion daemon changes.
- Vault/PDF/source/evidence ingestion.
- `src/python/ingestion/`, `projectkoios.ingestion`, or generic ingestion framework.
- Product-facing template architecture.
- Broad migration of all templates.
- Runtime CLI integration.
- ADR lifecycle/status changes.

## Next expected artifact

- Commit/push result for the coherent parser + draft skill integration slice, or user/Hermes packaging direction.
