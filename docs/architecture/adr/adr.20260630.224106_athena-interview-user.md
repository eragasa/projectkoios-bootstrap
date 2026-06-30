# ADR 20260630.224106: Athena interview-user skill

## Status

Draft

## Context

Origin: user request
From: Codex
Acting-As: delegated operator
Scope: projectkoios-bootstrap Archon skill surface
Repository: projectkoios-bootstrap
Delegated-Operator: Codex

Project Koios needs a reusable Athena/Archon behavior for questioning an
implementation proposal before code work begins. The behavior should produce a
decision-support document that complements an existing ADR rather than replacing
it.

The prompt supplied by the human architect defines the required interview
shape: clarify the implementation target and repository ownership, evaluate
scope discipline, model separation, workflow compatibility, and repository
boundary clarity, then present exactly four architectural options and recommend
one for human selection.

This is a bootstrap/control-plane capability. It belongs in
`projectkoios-bootstrap` as an Archon skill because it guides Athena's
architecture decision-support work. It is not a product-domain architecture
decision for the mothership vault, and it is not a Vulcan implementation task.

## Decision

Create a repo-local Archon skill named `athena-interview-user` under
`agents/global/archon/skills/athena-interview-user/`.

The skill:

- is used when Athena/Archon must produce an architecture interview or
  decision-support document before implementation begins
- treats existing ADRs as context, not as files to replace
- asks material clarifying questions before proposing solutions when required
- evaluates all options through scope discipline, model separation, workflow
  compatibility, and repository boundary clarity
- preserves separation between `ObjectClass`, `ActionClass`, `ActionInstance`,
  `Policy`, and `Trace`
- proposes exactly four courses of action
- recommends exactly one option
- states the required human decision before implementation proceeds
- produces the fixed document structure requested by the human architect
- does not implement code, mutate ADR status, create workflows, or route work to
  Vulcan by itself

The skill is intentionally a lean `SKILL.md` without scripts, references, or UI
metadata. The current behavior is prompt/procedure driven; adding deterministic
scripts or schemas now would build infrastructure before there is evidence that
the repeated output needs machine validation.

## Consequences

Athena gains a reusable decision-interview primitive for surfacing tradeoffs
before implementation begins. Hermes can invoke or relay this behavior when a proposed
implementation has unresolved architectural choices.

This accepts a small amount of prompt-level debt: the output is structured
Markdown, not a validated schema. If repeated use shows that downstream tools
need stable machine-readable fields, a later ADR should define a schema or
workflow contract.

The skill keeps future Petri-net compatibility open by requiring proposed
options to identify states, transitions, guards, artifacts, approvals, traces,
and repository ownership where relevant, without requiring a Petri-net engine in
this slice.

## architecture-spec

The skill `athena-interview-user` is a repo-local Archon skill at
`agents/global/archon/skills/athena-interview-user/SKILL.md`. It is a lean
`SKILL.md` without scripts, references, or UI metadata. The current behavior is
prompt/procedure driven; adding deterministic scripts or schemas now would build
infrastructure before there is evidence that the repeated output needs machine
validation.

The skill:

- is used when Athena/Archon must produce an architecture interview or
  decision-support document before implementation begins
- treats existing ADRs as context, not as files to replace
- asks material clarifying questions before proposing solutions when required
- evaluates all options through scope discipline, model separation, workflow
  compatibility, and repository boundary clarity
- preserves separation between `ObjectClass`, `ActionClass`, `ActionInstance`,
  `Policy`, and `Trace`
- proposes exactly four courses of action
- recommends exactly one option
- states the required human decision before implementation proceeds
- produces the fixed document structure requested by the human architect
- does not implement code, mutate ADR status, create workflows, or route work to
  Vulcan by itself

## acceptance-criteria

- `agents/global/archon/skills/athena-interview-user/SKILL.md` exists.
- The skill frontmatter name is exactly `athena-interview-user`.
- The skill description clearly triggers on architecture interviews,
  implementation-proposal reviews, and decision-support documents for
  Athena/Archon.
- The skill instructs the agent to ask material clarifying questions before
  proposing solutions when the target, owner, artifact, or boundary is unclear.
- The skill requires exactly four options and exactly one recommendation.
- The skill includes the fixed output sections requested by the human
  architect.
- The skill explicitly forbids implementation, ADR replacement, workflow
  creation, and automatic routing to Vulcan.
- The skill validates with the Codex skill validator.

## implementation-brief

The skill file already exists at
`agents/global/archon/skills/athena-interview-user/SKILL.md`. No implementation
work is required. This ADR documents the accepted skill; the implementation is
already present on disk.

## resolved-open-questions

1. Should the skill include scripts, schemas, or deterministic validation?
   - Resolved: no. The current behavior is prompt/procedure driven. Adding
     infrastructure before there is evidence of repeated output needing machine
     validation is premature.

2. Is implementation by Vulcan required?
   - Resolved: no. The skill file already exists and matches this specification.
     This is a no-implementation path; only validation evidence remains.

3. Does this skill replace existing ADRs?
   - Resolved: no. It treats existing ADRs as context and complements them with
     decision-support documents.

## non-goals

- Do not add scripts, schemas, workflows, CLI commands, or Petri-net machinery
  in this slice.
- Do not implement automatic ADR status mutation.
- Do not route work to Vulcan automatically.
- Do not create mothership vault artifacts.
- Do not define a machine-readable interview output schema until repeated use
  demonstrates the need.

## validation-expectations

Run:

```bash
.venv/bin/python /Users/eugene/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  agents/global/archon/skills/athena-interview-user
```

After meaningful repository changes, run:

```bash
graphify update .
```

## routing

After Hermes review, no Vulcan implementation is needed. The skill file already
exists at `agents/global/archon/skills/athena-interview-user/SKILL.md`. Hermes
may accept this ADR as-is. If later work requires schema validation, workflow
automation, or tests beyond the skill validator, a new ADR should define that
scope.
