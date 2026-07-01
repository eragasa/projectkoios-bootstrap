# Skill Register

This register is the canonical index of committed skills and the ADRs they bind to.

## Register

| Skill | Canonical path | Bound ADRs | Binding mode | Status |
|---|---|---|---|---|
| archon | `agents/global/archon/skills/archon/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.idea-spike-adr-implementation-workflow.draft.md` | supporting | draft |
| archon_run_watch | `agents/global/roles/ATHENA/archon_run_watch/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.canonical-workspace-state-next-action-protocol.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md` | supporting | draft |
| athena-interview-user | `agents/global/archon/skills/athena-interview-user/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.controlling-adr-join-protocol.draft.md, adr.draft-adr-comment-processing-protocol.draft.md` | supporting | draft |
| code-agent-implementation-from-spec | `agents/global/opencode/skills/code-agent-implementation-from-spec/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.implementation-plan-ownership.draft.md, adr.implementation-brief-verification-method.draft.md` | supporting | draft |
| code-agent-validation | `agents/global/opencode/skills/code-agent-validation/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.implementation-plan-ownership.draft.md, adr.implementation-brief-verification-method.draft.md` | supporting | draft |
| condense | `workspaces/hermes/.agents/skills/condense/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md` | supporting | draft |
| control-plane-comment-loop | `agents/global/pi/skills/control-plane-comment-loop/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.controlling-adr-join-protocol.draft.md, adr.draft-adr-comment-processing-protocol.draft.md` | supporting | draft |
| deep-interview | `workspaces/hermes/.agents/skills/projectkoios/deep-interview/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.canonical-workspace-state-next-action-protocol.draft.md, adr.comment-scope-and-control-boundary-review-rule.draft.md` | supporting | draft |
| graphify | `pi/agent/skills/graphify/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md, adr.canonical-workspace-state-next-action-protocol.draft.md` | supporting | draft |
| knowledge-agent-provenance-note | `agents/global/goose/skills/knowledge-agent-provenance-note/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md` | supporting | draft |
| knowledge-provenance-audit | `agents/global/goose/skills/knowledge-provenance-audit/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md` | supporting | draft |
| koios-workspace-bootstrap | `agents/global/goose/skills/koios-workspace-bootstrap/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.canonical-workspace-state-next-action-protocol.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md` | supporting | draft |
| manage-run | `agents/global/archon/skills/manage-run/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.canonical-workspace-state-next-action-protocol.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md` | supporting | draft |
| meta-harness-completion-gate | `agents/global/pi/skills/meta-harness-completion-gate/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md, adr.adr-template-contract.md` | supporting | draft |
| meta-harness-disagreement-resolution | `agents/global/pi/skills/meta-harness-disagreement-resolution/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md, adr.comment-scope-and-control-boundary-review-rule.draft.md` | supporting | draft |
| meta-harness-task-routing | `agents/global/pi/skills/meta-harness-task-routing/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md` | supporting | draft |
| projectkoios | `workspaces/hermes/.agents/skills/projectkoios/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md` | supporting | draft |
| session-aar | `agents/global/archon/skills/session-aar/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.control-surfaces-and-ownership-boundaries.draft.md, adr.comment-scope-and-control-boundary-review-rule.draft.md` | supporting | draft |
| spec-agent-acceptance-criteria | `agents/global/archon/skills/spec-agent-acceptance-criteria/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.adr-template-contract.md, adr.implementation-brief-verification-method.draft.md` | supporting | draft |
| spec-agent-scope-review | `agents/global/archon/skills/spec-agent-scope-review/SKILL.md` | `adr.skill-register-and-adr-binding-policy.draft.md, adr.adr-template-contract.md, adr.idea-spike-adr-implementation-workflow.draft.md` | supporting | draft |

## Notes

- Skill descriptions must name their bound ADRs.
- Workspace/runtime copies should mirror the canonical binding.
- Exemptions must be explicit and justified in this register.
