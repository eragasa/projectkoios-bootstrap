# ADR 20260702.033824Z: Skill Register and ADR Binding Policy

## Status

draft

## Context

Origin: user request
From: HERMES
Acting-As: HERMES
Scope: projectkoios-bootstrap
Repository: projectkoios-bootstrap
Architecture-Domain: software

The repository now has many reusable skills, but their authority relationship to
ADR work is still implicit. That makes it harder to answer three questions:

1. which ADR authorizes a skill's behavior
2. where that binding is recorded
3. how a reviewer can tell whether a skill still matches the ADR it serves

Without an explicit register, skills can drift away from the decisions they were
written to support.

## Decision

Add a repository skill register and require each non-exempt skill to declare its
ADR binding.

Use two linked surfaces:

- **skill register** — the canonical index of skills, skill paths, harness
  ownership, and bound ADRs
- **skill description binding** — each skill's frontmatter/description must name
  the ADR(s) it is bound to

Make the register the authoritative routing surface and the skill description
the local binding surface.

Use the following register fields at minimum:

- skill name
- skill path
- owning harness
- purpose
- bound ADR ID(s) or path(s)
- binding mode (`primary`, `supporting`, or `exempt`)
- status
- brief binding note

Use the following skill-description rule at minimum:

- the skill frontmatter includes a machine-readable ADR binding field
- the human-readable description also names the ADR binding explicitly
- the description should not rely on implication or surrounding directory
  context to establish authority

Allow only explicit exemptions for utility or bootstrap skills that genuinely do
not bind to one ADR. Those exemptions must be recorded in the register with a
reason.

## Consequences

- skill authority becomes inspectable from the register instead of inferred from
  file placement alone
- skills can be audited against the ADRs they support
- stale or drifting skills are easier to detect
- agent-facing skill descriptions become more precise and less ambiguous

## architecture-spec

The skill system should have:

- a canonical skill register file under `docs/skills/`
- one register row per committed skill
- one or more ADR bindings per skill
- a binding note that explains why the skill exists
- a corresponding binding line in the skill's own frontmatter/description

The register is the source of truth for discovery and review. The skill file is
the executable/usable surface and must echo its binding there as well.

## acceptance-criteria

- a reviewer can tell which ADR a skill belongs to by reading the register
- a reviewer can tell the same binding from the skill description itself
- skills with no ADR binding are explicitly marked exempt with a reason
- the register can represent skills with multiple ADR bindings when needed
- the binding survives path changes because it is recorded explicitly

## implementation-brief

If accepted, create the skill register under `docs/skills/` and update the skill
templates and existing skill files so each skill binds to its supporting ADR(s).

## resolved_open_questions

- Should the canonical register be Markdown, YAML, or JSON?
- Should a skill be allowed to bind to multiple ADRs by default, or only one
  primary ADR plus supporting ADRs?
- Should exemptions be limited to bootstrap/runtime glue skills?
- Should the register live in `docs/skills/` alone or also be indexed from
  `docs/architecture/architecture.00.md`?

## non_goals

- Changing how skills execute at runtime
- Replacing the ADR schema
- Forcing every utility script to become an ADR-bound skill
- Eliminating existing skill directories

## validation-expectations

- the repository can enumerate skills and their bound ADRs from the register
- a skill file can be checked for an explicit ADR binding
- exempt skills are rare and justified
- skill/ADR mismatches are easy to spot during review

## routing

- Owner: Athena
- Next phase: proposed
- Notes: Skill registry and skill-to-ADR binding policy.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None
