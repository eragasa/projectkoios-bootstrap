# ADR 20260630.214135: Koios Evidence Intake and Cross-Harness Directive Contract

## Status

Draft

## Context

Origin: user decision request
From: Athena
Acting-As: archon
Scope: projectkoios-bootstrap meta-harness/bootstrap layer
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

The user explicitly corrected that this architecture product belongs to
Archon/Athena. Codex is only the delegated operator relaying and materializing
the requested artifact; Codex does not become Athena, Hermes, Vulcan, or Koios.

This ADR evaluates three draft proposal ADRs:

- `docs/architecture/adr/adr.20260630.212410_koios-ingestion-scope-proposal.md`
- `docs/architecture/adr/adr.20260630.212430_cross-harness-directive-contract-proposal.md`
- `docs/architecture/adr/adr.20260630.212900_graphify-backed-knowledge-daemon-proposal.md`

Those drafts describe one architectural boundary: how Koios turns bounded
repo/vault/PDF/source evidence into provenance-backed cross-harness requests
that Athena can safely consume without collapsing role authority, source
authority, or temporary retrieval infrastructure into final architecture.

Existing accepted or draft inputs remain relevant:

- `adr.20260630.165929_koios-goose-role-definition.md` defines Koios as the
  knowledge role and denies Koios authority over architecture, implementation,
  completion, and routing.
- `adr.20260630.173445_graphify-first-session-lifecycle.md` and
  `adr.20260630.203646_ast-only-session-boundary-rebuild.md` define Graphify as
  a broad-context read path and AST-only session-boundary update mechanism.
- `docs/meta-harness.md` defines explicit artifacts, role boundaries, and
  cross-surface knowledge discipline.

## Decision

The three proposal ADRs should be consolidated into this single authoritative
draft ADR. Keeping them separate would split one boundary contract across
ingestion scope, artifact shape, and temporary evidence substrate, causing
authority ordering and provenance rules to diverge.

This ADR resolves the three proposal ADRs as proposal inputs. If this ADR is
accepted, the proposal ADRs should be treated as superseded by this decision for
future routing and implementation.

### architecture-spec

Koios may perform bounded evidence intake across repository files, repository
documentation, selected mothership vault material, PDFs, and Graphify-derived
indexes when the requested output is a knowledge/provenance artifact or when
another harness needs research support.

Koios must turn that intake into explicit artifacts. For Athena-facing requests,
the canonical artifact class is `directive`. A directive is a bounded
cross-harness request, not an ADR, not a handoff archive, not a
knowledge-note, and not an implementation report.

Athena consumes Koios directives as proposal context only. Athena decides the
architecture. Hermes decides routing and completion. Vulcan implements accepted
work. Koios supplies evidence, provenance, and advisory routing context.

### Source Authority Ordering

When sources disagree, agents must apply this ordering unless a user gives a
more specific task constraint:

1. Explicit user instruction for the current task, including repository and
   non-goal constraints.
2. Current live filesystem and git state for implementation facts.
3. Accepted or completed ADRs for projectkoios-bootstrap architecture intent.
4. Current repo documentation and active handoff/directive artifacts for
   operating instructions.
5. Draft ADRs and proposal ADRs as non-authoritative architecture inputs.
6. Archived handoffs as provenance only; archived `Status: active` headers are
   not current authority by themselves.
7. Bounded mothership vault material as durable knowledge context, not as
   authority over this bootstrap repo unless explicitly cited by an accepted
   ADR or current user instruction.
8. PDF or external source material as cited evidence; extracted summaries remain
   unvalidated until tied to source locations.
9. Graphify graph output as retrieval and relationship substrate only. Graphify
   helps find sources; it does not replace source citation or authority
   ordering.

If code and an accepted ADR disagree, report the mismatch instead of silently
normalizing it. Code is evidence of current behavior; the accepted ADR is
evidence of intended architecture.

### Directive Artifact Contract

`directive` is the canonical general artifact class for bounded requests that
cross harness boundaries.

The canonical directive name is:

`<producer>_<consumer>_<kebab-case-action>`

The name is intentionally parseable by splitting on `_`:

- `producer`: producing harness role or project scope, such as `koios`,
  `athena`, `vulcan`, `hermes`, or `projectkoios`
- `consumer`: intended consuming role, such as `athena`, `vulcan`, `hermes`, or
  `koios`
- `action`: kebab-case request intent, such as `produce-adr`,
  `review-evidence`, or `implement-docs`

If persisted as a file, prepend the ADR-style timestamp:

`YYYYMMDD.HHMMSS_<producer>_<consumer>_<kebab-case-action>.md`

A directive must contain:

- artifact type: `directive`
- directive name
- producer
- consumer
- action
- origin
- delegated operator, if any
- scope and repository
- intent
- source set, with paths, source dates, and retrieval method where practical
- authority notes for any source-ordering conflicts
- constraints and non-goals
- requested output artifact
- acceptance or success criteria for the consumer
- open questions or blocked inputs
- routing target after the consumer reports

Directive state is independent of ADR status. A directive may use lightweight
operational states such as `proposed`, `received`, `blocked`, `fulfilled`, or
`withdrawn`, but those states do not accept, reject, complete, or supersede an
ADR.

### Temporary Graphify Evidence Substrate

Graphify may be used as a temporary evidence-discovery substrate for
projectkoios-bootstrap while the long-term Project Koios graph/RAG system is
undefined.

Allowed temporary uses:

- query existing `graphify-out/graph.json` for broad repo context
- use `graphify query`, `graphify path`, or `graphify explain` before broad
  manual reading
- run `graphify update .` as the AST-only session-boundary refresh after
  meaningful repository file changes
- perform explicitly bounded, task-directed indexing or extraction when Hermes
  or Athena requests it
- use Graphify to discover candidate source files, relationships, and
  provenance leads

Limits:

- Graphify output is not accepted architecture, source truth, or completion
  evidence by itself.
- Graphify must not silently mutate repository source, vault content, accepted
  ADRs, or machine-local secrets.
- Standard session-boundary refresh remains AST-only and must not require LLM
  credentials.
- Vault and PDF ingestion must be bounded to a named task, path set, or source
  set. Whole-vault or whole-workspace ingestion requires an explicit Hermes or
  Athena directive.
- PDF-derived claims must preserve the source file, page or location when
  practical, extraction method, and validation status.
- Temporary Graphify usage must remain replaceable by a future native Project
  Koios graph/RAG system without changing role authority.

### Koios/Athena Role Separation

Koios may:

- gather bounded source evidence
- prepare provenance indexes, knowledge notes, documentation-gap reports, and
  advisory routing recommendations
- produce directives for Athena, Hermes, Vulcan, or Koios
- flag source conflicts and missing provenance

Koios must not:

- author final architecture decisions
- mark ADRs accepted, rejected, completed, or superseded
- route work as Hermes
- implement code or tests as Vulcan
- treat Graphify, vault notes, or draft proposals as final authority

Athena may consume Koios evidence and directives, but Athena must make its own
architecture decision and preserve provenance for the evidence it relies on.

### Resolved Open Questions

- The three draft proposals should be consolidated because they describe one
  Koios-to-Athena intake boundary.
- `directive` is the canonical cross-harness request artifact class.
- Directive names use `<producer>_<consumer>_<kebab-case-action>`.
- A broad project directive may use `projectkoios` as producer when the request
  is not owned by one harness role, but the body must still identify the sender
  and delegated operator.
- Graphify is a temporary evidence substrate, not a native Project Koios memory
  system and not an authority source.
- Source authority ordering is required whenever repo state, ADRs, archives,
  vault material, PDFs, and Graphify output are used together.
- Koios may prepare proposal context, but Athena owns architecture decisions.

### Non-Goals

- Do not define product/domain architecture for the mothership vault.
- Do not implement a native graph/RAG system.
- Do not implement a daemon, watcher, parser, CLI command, or validator in this
  ADR task.
- Do not move vault content, machine-local state, secrets, or generated
  Graphify output into git.
- Do not redefine the whole meta-harness.
- Do not let directive state replace ADR status or Hermes routing decisions.

### Acceptance-Criteria

This ADR is ready for Hermes review when:

1. It records the consolidation decision for the three proposal ADRs.
2. It preserves delegated-operator provenance for Codex.
3. It defines source authority ordering across live repo state, ADRs,
   documentation, archived handoffs, vault material, PDFs, and Graphify output.
4. It defines the directive artifact contract and naming convention.
5. It constrains Graphify to temporary, bounded, read-oriented evidence
   discovery.
6. It preserves Koios, Athena, Hermes, and Vulcan role separation.
7. It includes implementation guidance without implementing code.
8. It defines validation expectations and routing back to Hermes after Vulcan
   reports.

### Implementation-Brief

Do not implement code from this ADR until Hermes reviews and routes the work.

If Hermes accepts this ADR for implementation, route to Vulcan for documentation
and prompt updates only. Keep changes scoped to projectkoios-bootstrap
meta-harness surfaces, such as:

- `AGENTS.md`
- `docs/meta-harness.md`
- repo-local role instructions for Koios/goose, Athena/archon, Hermes/pi, and
  Vulcan/opencode
- any relevant skill documentation that describes directive artifacts,
  Graphify-first context gathering, or Koios provenance intake

Vulcan should not create a daemon, long-running watcher, native graph system,
vault mutator, PDF parser, or new CLI behavior unless Athena issues a later
implementation-ready ADR for that work.

Vulcan should preserve the three proposal ADRs as historical inputs unless
Hermes explicitly routes a docs cleanup to mark them superseded or to add
cross-links.

### Validation Expectations

Hermes should validate any implementation by checking:

- no machine-local secrets, tokens, runtime state, vault files, or generated
  Graphify caches are added to git
- documentation consistently treats directives as request artifacts, not ADRs
- the directive name convention appears exactly as
  `<producer>_<consumer>_<kebab-case-action>`
- Graphify session-boundary language still says `graphify update .`
  (AST-only, no LLM needed)
- Koios remains advisory for routing and non-authoritative for architecture
- Athena remains the owner of architecture specs, acceptance criteria,
  implementation briefs, and ADR decisions
- Hermes remains responsible for routing, completion decisions, and validation
- Vulcan remains responsible for implementation plans, patches, tests, and
  implementation reports

### Routing Back to Hermes After Vulcan Reports

After Vulcan completes any routed documentation implementation, Vulcan must
return to Hermes:

- implementation report
- changed files
- validation output
- any deviation report if implementation could not follow this ADR
- any recommendation for a follow-on Athena decision

Hermes then compares the report to this ADR's acceptance criteria and validation
expectations. If the evidence passes, Hermes may move the work through the
repo's ADR lifecycle. If the evidence fails or scope expands, Hermes routes the
work back to Vulcan for correction or to Athena for a revised decision.

## Consequences

Project Koios gets one inspectable boundary for evidence intake, directive
shape, and temporary Graphify-backed retrieval. Koios can prepare stronger
proposal context without gaining architecture authority. Athena receives
bounded, provenance-backed requests. Hermes retains routing and completion
authority. Vulcan receives implementation-ready documentation guidance only
after Hermes routes it.

The three proposal ADRs remain useful provenance, but future work should cite
this ADR as the consolidated decision surface once it is accepted.
