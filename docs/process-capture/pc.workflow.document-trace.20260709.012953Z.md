# Process Petri-net trace: template record round-trip skill integration

## Metadata

- Type: process-petrinet-trace
- Status: captured
- Repository: projectkoios-bootstrap
- Scope: draft/gated `template-record-roundtrip` skill integration
- Roles: ATHENA, VULCAN, KOIOS
- Captured by: KOIOS
- Captured at: 20260709.012953Z
- Aggregate: `docs/process-capture/pc.workflow.document-trace.md`
- Non-authority: process provenance only

## Non-authority statement

This note maps observed document-state evolution to Petri-net vocabulary for
knowledge/provenance analysis only. It does not define skill policy, promote the
skill to stable, create template architecture authority, authorize broad
Markdown ingestion, or decide packaging/commit status.

Places, transitions, and tokens below describe the document process trace, not
runtime Petri-net semantics.

## Observed document trace

This slice extends the prior template representation round-trip chain. The
schema-backed parser gate now has durable VULCAN implementation evidence and
ATHENA conformance review evidence. ATHENA then produced a skill integration
brief, VULCAN implemented and validated the draft/gated skill, and ATHENA
reviewed the skill integration as conforming while keeping it draft/gated.

The trace is stronger than the earlier template representation trace because the
previous ATHENA conformance gap is now closed for both the parser gate and skill
integration. The remaining gap is not provenance but lifecycle status: the skill
is intentionally draft/gated and not stable/promoted.

## Source artifacts

| # | Artifact | Role/domain | Status | Provenance use | Authority boundary |
|---|---|---|---|---|---|
| 1 | `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md` | ATHENA revision request | implementation-revision-required | Defines schema-backed parser correction | Does not broaden beyond bootstrap template representation |
| 2 | `docs/implementation/template-representation-roundtrip.20260708.044531.md` | VULCAN implementation report | validated | Records schema-backed parser implementation and validation | First-fixture parser evidence only |
| 3 | `docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md` | ATHENA conformance review | conforms | Closes parser gate for schema-backed record round trip | Does not approve stable skill or all-template migration |
| 4 | `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md` | ATHENA implementation brief | implementation-ready draft after user approval | Defines draft/gated skill requirements and non-goals | Skill must remain draft/gated until parser report and conformance evidence exist |
| 5 | `agents/global/opencode/skills/template-record-roundtrip/SKILL.md` | VULCAN skill artifact | draft/gated | Implements reusable VULCAN procedure for schema-backed bootstrap template records | Not stable reusable practice; not generic Markdown ingestion |
| 6 | `docs/skills/skill-register.md` | shared skill index | updated | Registers skill as opencode/supporting/draft | Register row does not promote skill status |
| 7 | `docs/implementation/template-record-roundtrip-skill.20260709.012011.md` | VULCAN implementation report | validated-draft-skill | Records files changed, validation, non-goals, and residual risks | Does not claim stable reuse or packaging evidence |
| 8 | `docs/AAR/aar.20260709.012011_template-record-roundtrip-skill.md` | VULCAN AAR | current | Records process issues and follow-up candidates | Process lesson only |
| 9 | `docs/reviews/architecture-conformance.20260709.012745_template-record-roundtrip-skill.md` | ATHENA conformance review | conforms-draft-gated | Confirms skill integration conforms as draft/gated | Keeps skill bootstrap-template-specific and not stable/promoted |

## Observed process places

| Place ID | Document/process state | Evidence artifact | Token meaning |
|---|---|---|---|
| `p0.parser-revision-requested` | ATHENA required schema-backed parser output | `docs/plans/revision-request.20260708.070651_template-representation-schema-backed.md` | Parser work item has corrected schema-backed acceptance criteria |
| `p1.parser-validated-reported` | VULCAN reports schema-backed parser implementation and validation | `docs/implementation/template-representation-roundtrip.20260708.044531.md` | Parser gate has implementation evidence |
| `p2.parser-conformance-accepted` | ATHENA accepts schema-backed parser revision as conformant | `docs/reviews/architecture-conformance.20260709.011055_template-representation-schema-backed.md` | Parser gate is closed for first fixture |
| `p3.skill-brief-ready` | ATHENA skill integration brief exists | `docs/plans/implementation-brief.20260709.010343_template-record-roundtrip-skill.md` | Skill work item has bounded implementation instructions |
| `p4.skill-implemented` | VULCAN created draft skill and register row | `agents/global/opencode/skills/template-record-roundtrip/SKILL.md`, `docs/skills/skill-register.md` | Draft/gated skill artifact exists |
| `p5.skill-validated-reported` | VULCAN report records validation and non-goals | `docs/implementation/template-record-roundtrip-skill.20260709.012011.md` | Skill integration has implementation/validation evidence |
| `p6.skill-process-lessons-recorded` | VULCAN records AAR/process observations | `docs/AAR/aar.20260709.012011_template-record-roundtrip-skill.md` | Skill slice has implementation-side process lessons |
| `p7.skill-conformance-reviewed` | ATHENA confirms skill conforms as draft/gated | `docs/reviews/architecture-conformance.20260709.012745_template-record-roundtrip-skill.md` | Skill integration is architecture-conformant in draft/gated state |
| `p8.koios-trace-captured` | KOIOS captures process/Petri-net document trace | This note and aggregate index | Work item has provenance/process trace for knowledge review |
| `p9.awaiting-packaging-or-promotion-decision` | User/Hermes packaging or future promotion remains separate | ATHENA review next transition | Token remains open for repo-state/commit or later promotion criteria |

## Observed process transitions

| Transition ID | Event | Consumes places/artifacts | Produces places/artifacts | Evidence |
|---|---|---|---|---|
| `t0.athena-issued-parser-revision` | ATHENA required schema-backed parser output | Prior template representation round-trip | `p0.parser-revision-requested` | Revision request |
| `t1.vulcan-implemented-parser-gate` | VULCAN implemented and validated schema-backed parser revision | `p0` | `p1.parser-validated-reported` | Parser implementation report |
| `t2.athena-reviewed-parser-gate` | ATHENA accepted parser revision as conformant | `p1` | `p2.parser-conformance-accepted` | Parser conformance review |
| `t3.athena-issued-skill-brief` | ATHENA produced skill integration brief | `p2` and user direction | `p3.skill-brief-ready` | Skill implementation brief |
| `t4.vulcan-integrated-skill` | VULCAN added skill and register row | `p3` | `p4.skill-implemented` | VULCAN report files changed |
| `t5.vulcan-validated-reported-skill` | VULCAN ran validation and wrote implementation report | `p4` | `p5.skill-validated-reported` | Skill implementation report |
| `t6.vulcan-recorded-aar` | VULCAN recorded process issues/follow-ups | `p5` | `p6.skill-process-lessons-recorded` | VULCAN AAR |
| `t7.athena-reviewed-skill` | ATHENA confirmed conformance as draft/gated | `p5`, `p6` | `p7.skill-conformance-reviewed`, `p9.awaiting-packaging-or-promotion-decision` | Skill conformance review |
| `t8.koios-captured-document-trace` | KOIOS mapped document trace to process Petri-net vocabulary | `p0` through `p7` | `p8.koios-trace-captured` | This note |

## Token trace

| Step | Token/state before | Transition | Token/state after | Evidence |
|---|---|---|---|---|
| 0 | Template representation parser insufficient for schema-backed contract | `t0.athena-issued-parser-revision` | Parser correction token at `p0` | Revision request |
| 1 | Parser correction token | `t1.vulcan-implemented-parser-gate` | Validated parser report token at `p1` | Parser implementation report |
| 2 | Validated parser report token | `t2.athena-reviewed-parser-gate` | Parser conformance token at `p2` | Parser conformance review |
| 3 | Parser conformance token plus user direction for skill | `t3.athena-issued-skill-brief` | Skill brief token at `p3` | Skill implementation brief |
| 4 | Skill brief token | `t4.vulcan-integrated-skill` | Draft skill artifact token at `p4` | Skill file and register row |
| 5 | Draft skill artifact token | `t5.vulcan-validated-reported-skill` | Validated draft-skill report token at `p5` | Skill implementation report |
| 6 | Validated draft-skill token | `t6.vulcan-recorded-aar` | Process-lessons token at `p6` | VULCAN AAR |
| 7 | Validated draft-skill token with process lessons | `t7.athena-reviewed-skill` | Conforms-draft-gated token at `p7` and next-decision token at `p9` | Skill conformance review |
| 8 | Conforms-draft-gated token | `t8.koios-captured-document-trace` | KOIOS process-trace token at `p8` | This note |

## Validation and evidence links

Validation recorded by VULCAN for the skill integration:

- `uv run pytest tests/projectkoios/bootstrap/template_representation tests/projectkoios/bootstrap/schema -q` passed with `34 passed in 0.16s`.
- `uv run projectkoios bootstrap validate-python-policy agents/global/opencode/skills/template-record-roundtrip` returned `summary: 0 finding(s), 0 file(s)`; this is not Markdown/frontmatter validation.
- A frontmatter/Markdown inspection script reported `frontmatter/markdown inspection: ok`.
- `git diff --check` was clean.

Validation rerun by ATHENA for skill conformance:

- focused template/schema pytest passed with `34 passed in 0.16s`.
- Python policy validator for the Markdown-only skill path returned zero Python files.
- `git diff --check` was clean.

## Provenance gaps

- No separate durable user-approval artifact for the skill implementation was inspected. The ATHENA brief records user direction, and the VULCAN AAR records user selection of the high-leverage task.
- Markdown-only skill validation currently relies on a local inspection script recorded in the VULCAN report; the repository does not yet expose a stable skill/frontmatter validation command.
- The skill register binding note still says the skill is not stable until parser report and ATHENA conformance review exist. Those prerequisites now exist, but ATHENA intentionally still classifies the skill as draft/gated rather than stable/promoted.

## Interpretation limits

This trace does not prove or authorize:

- stable skill promotion;
- all-template migration or validation;
- broad Markdown, Graphify, vault, source, PDF, or evidence ingestion;
- product-facing template architecture;
- ADR lifecycle/status changes;
- packaging, commit, or push completion;
- treating Python policy `0 file(s)` as Markdown skill validation.

## Recommendations and candidate follow-ups

- Keep `template-record-roundtrip` marked draft/gated until explicit promotion criteria are defined and reviewed.
- If Markdown skills become frequent committed surfaces, define a repository-native skill/frontmatter validation command or policy.
- If the skill is promoted later, update `docs/skills/skill-register.md` binding notes to distinguish satisfied parser prerequisites from remaining stable-promotion criteria.
- Preserve the bootstrap-template-specific boundary unless a later accepted ADR broadens template representation architecture.

## Closing non-authority statement

This note records process provenance only. It does not create architecture,
implementation, workflow, validation, enforcement, skill-promotion, packaging, or
completion authority.
