```json
{
  "title": "Agent skills workflow status slice 0 implementation brief",
  "artifact_type": "implementation-brief",
  "status": "superseded-by-workflow-project-brief",
  "datetime": "20260711.120300Z",
  "acting_as": "ATHENA",
  "repository": "projectkoios-bootstrap",
  "source_intake": "docs/plans/spec-intake.20260711.115957_agent-skills-for-workflow-inspectability.md",
  "source_slicing": "docs/plans/slicing.20260711.120200_agent-skills-workflow-inspectability.md",
  "slice_name": "agent-skills-workflow-status-slice-0",
  "next_owner": "VULCAN"
}
```

# Implementation brief 20260711.120300: Agent skills workflow status slice 0

## Supersession note

This brief is superseded by `docs/plans/implementation-brief.20260711.121000_agent-skills-workflow-status-slice-0.md` after USER clarified that Slice 0 should attach to the existing workflow project/control surface, not primarily to `agents/global/pi/skills/` and `docs/skills/skill-register.md`.

## Purpose

Add the first Project Koios agent skill that connects day-to-day agent behavior to the live Petri-net inspectability command:

```bash
uv run projectkoios workflow status
```

The skill should make Pi/Hermes-style orchestration sessions inspect and report workflow state before advancing Project Koios bootstrap work.

## Scope

In scope:

- Add one skill file:

  ```text
  agents/global/pi/skills/koios-workflow-status/SKILL.md
  ```

- Update skill register:

  ```text
  docs/skills/skill-register.md
  ```

- Write an implementation report under `docs/implementation/`.
- Update VULCAN workspace state if VULCAN performs implementation.

Out of scope:

- Implementing the interactive-control skill; that is Slice 1.
- Mirroring the skill into opencode/goose/archon; that is a later propagation slice.
- Creating a new `.agents/skills/` project-level distribution mechanism.
- Changing `uv run projectkoios workflow status` behavior.
- Changing Petri-net runtime, transition firing, persistence, Operator Console, workflow-object runtime coupling, schema authority, live adapters, role/permission semantics, or product authority.

## Skill placement

Use the existing repository skill pattern:

```text
agents/global/pi/skills/koios-workflow-status/SKILL.md
```

Do not introduce a new placement convention unless implementation discovers the existing pattern cannot satisfy the slice. If that happens, pause and report the concrete placement/authority gap.

## Skill frontmatter requirements

Follow existing skill frontmatter conventions. Minimum expected frontmatter:

```yaml
---
name: koios-workflow-status
adr_binding:
  - docs/adr/adr.skill-register-and-adr-binding-policy.draft.md
  - docs/adr/adr.canonical-workspace-state-next-action-protocol.draft.md
  - docs/adr/adr.control-surfaces-and-ownership-boundaries.draft.md
description: |
  Inspect live Project Koios workflow status and report active workflow state before advancing work
  Bound to ADRs: adr.skill-register-and-adr-binding-policy.draft.md, adr.canonical-workspace-state-next-action-protocol.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md.
metadata:
  agent: meta-harness
  harness_role: operator
  consumes:
    - user-request
    - workflow-status-output
  produces:
    - workflow-status-summary
    - recommendation
---
```

VULCAN may adjust `metadata` wording to match repository style, but must preserve the ADR bindings required by `docs/skills/skill-register.md`.

## Required skill behavior

The skill must instruct agents to:

1. Use the skill when starting or resuming Project Koios workflow work, before advancing workflow state, during handoffs, or when the user asks what is active/blocked/next.
2. Run from repository root when possible:

   ```bash
   uv run projectkoios workflow status
   ```

3. Parse or summarize the command output into:
   - active workflow/net;
   - current token and place;
   - enabled transitions;
   - whether user decision is required;
   - one clear recommendation.
4. If `user decision required: yes`, stop and ask/await approval unless the user explicitly delegated the next action.
5. If the command fails or is unavailable, report the failure as an inspectability gap and do not fabricate workflow state.
6. Preserve boundaries:
   - do not fire transitions;
   - do not mutate workflow state;
   - do not treat the static fixture as canonical workflow authority;
   - do not launch subagents merely because a transition is enabled;
   - do not expand scope beyond the user's current request.

## Suggested skill structure

Recommended headings:

- `When to use this skill`
- `Agent responsibility`
- `Procedure`
- `Output format`
- `Stop conditions`
- `Failure modes`
- `Escalation rule`

Recommended output format:

```text
Workflow status:
- workflow: <workflow id>
- current token/place: <token> at <place>
- enabled transitions: <transition list>
- user decision required: yes/no
- recommendation: <one sentence>
```

## Skill register update

Add a row to `docs/skills/skill-register.md` for `koios-workflow-status`.

Expected values:

- Skill: `koios-workflow-status`
- Canonical path: `agents/global/pi/skills/koios-workflow-status/SKILL.md`
- Owning harness: `pi`
- Purpose: inspect live workflow status before advancing Project Koios bootstrap work
- Bound ADRs:
  - `adr.skill-register-and-adr-binding-policy.draft.md`
  - `adr.canonical-workspace-state-next-action-protocol.draft.md`
  - `adr.control-surfaces-and-ownership-boundaries.draft.md`
- Binding mode: `supporting`
- Status: `draft`
- Binding note: should mention `uv run projectkoios workflow status` and read-only inspectability.

## Acceptance criteria

1. `agents/global/pi/skills/koios-workflow-status/SKILL.md` exists.
2. The skill frontmatter includes `name: koios-workflow-status`.
3. The skill frontmatter includes `adr_binding` entries aligned with `docs/skills/skill-register.md`.
4. The skill instructs agents to run/consult `uv run projectkoios workflow status`.
5. The skill requires reporting workflow id, current token/place, enabled transitions, user-decision requirement, and one recommendation.
6. The skill requires stopping/asking when user decision is required unless the user explicitly delegated action.
7. The skill explicitly forbids firing transitions, mutating workflow state, treating the fixture as canonical authority, launching subagents just because a transition is enabled, or expanding scope beyond the request.
8. `docs/skills/skill-register.md` includes a matching row for the skill.
9. Validation confirms the skill file and register row are present and consistent enough for repository review.
10. No Petri-net runtime, workflow status command, Operator Console, workflow-object, schema, live adapter, role/permission, or product authority behavior is changed.

## Suggested validation

From repository root:

```bash
test -f agents/global/pi/skills/koios-workflow-status/SKILL.md
grep -n "name: koios-workflow-status" agents/global/pi/skills/koios-workflow-status/SKILL.md
grep -n "uv run projectkoios workflow status" agents/global/pi/skills/koios-workflow-status/SKILL.md
grep -n "koios-workflow-status" docs/skills/skill-register.md
git diff --check
```

Optional lightweight structured check:

```bash
python - <<'PY'
from pathlib import Path
skill = Path('agents/global/pi/skills/koios-workflow-status/SKILL.md').read_text()
assert skill.startswith('---\n')
assert 'name: koios-workflow-status' in skill
assert 'adr_binding:' in skill
for required in [
    'docs/adr/adr.skill-register-and-adr-binding-policy.draft.md',
    'docs/adr/adr.canonical-workspace-state-next-action-protocol.draft.md',
    'docs/adr/adr.control-surfaces-and-ownership-boundaries.draft.md',
    'uv run projectkoios workflow status',
    'user decision required',
    'recommendation',
]:
    assert required in skill
register = Path('docs/skills/skill-register.md').read_text()
assert 'koios-workflow-status' in register
assert 'agents/global/pi/skills/koios-workflow-status/SKILL.md' in register
PY
```

## Pause triggers

Pause and ask USER/HERMES if implementation would require:

- defining a new shared skill distribution mechanism;
- changing local harness install behavior;
- adding skills to multiple harnesses in the same slice;
- changing Petri-net runtime or workflow CLI behavior;
- adding interactive-control behavior into Slice 0;
- creating new ADR or schema authority.

## Handoff

VULCAN should produce a concise implementation plan and pause for USER/HERMES approval before coding unless USER/HERMES explicitly approves direct implementation from this brief.
