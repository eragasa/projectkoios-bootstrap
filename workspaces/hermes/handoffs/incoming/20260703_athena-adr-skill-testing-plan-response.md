# Athena response: ADR-skill testing plan

## 1) Test surfaces first
1. `agents/global/archon/skills/spec-agent-scope-review/SKILL.md`
   - Highest risk because this is the changed surface and it drives the scope/hand-off boundary.
2. `agents/global/archon/skills/spec-agent-acceptance-criteria/SKILL.md`
   - Needed to confirm the ownership split is still clean and not duplicated.
3. `docs/skills/skill-register.md`
   - Needed to confirm the register matches the skill contract and no stale path/status text remains.
4. `docs/adr/adr.adr-template-contract.md` and the two binding ADRs named by the skills
   - Needed only as reference checks for path/name consistency, not full semantic review.

## 2) Pass/fail criteria
### Success
- `spec-agent-scope-review` only owns bounded spec intake and preliminary notes.
- `spec-agent-acceptance-criteria` owns the final inspectable pass/fail criteria.
- The register rows and skill frontmatter/description agree on the same ADR bindings.
- No stale `does not exist` / wrong-path references remain for the ADR template contract.

### Regression
- Scope-review still claims final acceptance-criteria ownership.
- Acceptance-criteria skill is missing from the handoff path or is no longer the final criteria owner.
- Any register row points at the wrong ADR path or says a present file is missing.
- Any stale references appear in the tested surfaces.

## 3) Stale-reference detection at scale
### Grep strategy
- Search the repo for:
  - `adr-template-contract`
  - `does not exist as a file`
  - `acceptance-criteria`
  - `spec-agent-scope-review`
  - `spec-agent-acceptance-criteria`
- Limit first pass to `docs/`, `agents/global/`, and `workspaces/`.

### Path/naming patterns
- Check both `adr-template-contract.md` and `adr.adr-template-contract.md` variants.
- Check both skill frontmatter `adr_binding` and human-readable description text.
- Check register rows for canonical path, owning harness, and binding note consistency.

### Avoiding false positives
- Ignore archive/provenance copies unless they are active surfaces.
- Treat historical ADR text in archives as informational only.
- Require an actual nearby file/path mismatch before calling it stale.

## 4) Minimal proof of safety
### Smallest sweep
- Read the 2 skill files and the register row.
- Run targeted grep over `docs/skills/`, `agents/global/archon/skills/`, and `workspaces/*/` for the stale path phrase and the two skill names.
- Verify the referenced ADR file exists.

### Evidence to capture
- Command output showing no stale path phrase on active surfaces.
- A short note confirming the ownership split:
  - scope-review = intake/bounding
  - acceptance-criteria = final criteria
- Confirmation that the template contract file exists at `docs/adr/adr.adr-template-contract.md`.

## Recommendation
Do the bounded grep sweep first. If it comes back clean, that is enough proof to roll out the ADR-skill boundary change without a broader semantic review.
