# ADR 20260630.224106: Architecture interview skill

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

Create a repo-local Archon skill named `architecture-interview` under
`agents/global/archon/skills/architecture-interview/`.

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
before implementation. Hermes can invoke or relay this behavior when a proposed
implementation has unresolved architectural choices.

This accepts a small amount of prompt-level debt: the output is structured
Markdown, not a validated schema. If repeated use shows that downstream tools
need stable machine-readable fields, a later ADR should define a schema or
workflow contract.

The skill keeps future Petri-net compatibility open by requiring proposed
options to identify states, transitions, guards, artifacts, approvals, traces,
and repository ownership where relevant, without requiring a Petri-net engine in
this slice.

## acceptance-criteria

- `agents/global/archon/skills/architecture-interview/SKILL.md` exists.
- The skill frontmatter name is exactly `architecture-interview`.
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

Implement only the repo-local Archon skill:

- `agents/global/archon/skills/architecture-interview/SKILL.md`

Do not add scripts, schemas, workflows, CLI commands, Petri-net machinery,
status mutation commands, or mothership vault artifacts in this slice.

## validation-expectations

Run:

```bash
.venv/bin/python /Users/eugene/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  agents/global/archon/skills/architecture-interview
```

After meaningful repository changes, run:

```bash
graphify update .
```

## routing

After this Draft ADR and skill are created, route back to Hermes for review.
If Hermes accepts the skill as sufficient, no Vulcan implementation is needed
unless later work requires schema validation, workflow automation, or tests
beyond the skill validator.
