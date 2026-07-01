# AAR 20260702.034139: Skill register and ADR binding policy

## Scope
Project Koios bootstrap repo, skill registry and skill-to-ADR binding design.

## What happened
A draft ADR was added to define a canonical skill register under `docs/skills/`, and the new `control-plane-comment-loop` skill was bound to the related draft ADRs in its description/frontmatter. A starter `docs/skills/skill-register.md` entry was also created.

## Process issues
None.

## Proposed follow-up improvements
Populate the register with the rest of the committed skills and decide whether the canonical register should remain Markdown or move to YAML/JSON.

## Candidate ADR or implementation topics
- Populate the skill register with all committed skills
- Decide the final register format
- Decide whether skill exemptions need a separate ADR

## Current status
Drafted and partially seeded.
