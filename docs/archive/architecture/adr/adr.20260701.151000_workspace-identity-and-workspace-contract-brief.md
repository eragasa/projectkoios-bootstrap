# ADR 20260701.151000: Workspace identity and workspace contract brief

## Status

historic

This draft is intentionally commentable before any move to the `proposed` lifecycle phase.

## Context

Project Koios is transitioning agents into their own workspaces.

The target model is:
- identity comes from the workspace’s own `AGENTS.md`
- runtime is only the launcher/executor
- shared bootstrap config lives in `./*`
- workspace-local state lives in `./$WORKSPACE$/*`

This means the workspace itself must be the source of truth for agent identity, while `projectkoios-bootstrap` remains the shared configuration and materialization layer.

This brief is for the next implementation slice. It does not change architecture beyond the workspace identity boundary.

## Decision

1. Agent identity is defined by the `AGENTS.md` file in the target workspace.
2. Runtime names do not define identity; they only identify how the workspace is launched.
3. Shared bootstrap assets remain in the bootstrap repo root (`./*`).
4. Workspace-local configuration and state live under the target workspace root (`./$WORKSPACE$/*`).
5. Workspace-local identity and state must be independent from runtime-installed tool state.
6. The AST-only session refresh policy remains unchanged.

## Acceptance criteria

- Each target workspace has its own `AGENTS.md` that defines the agent identity.
- The identity in that `AGENTS.md` does not depend on the runtime name.
- Bootstrap-owned files remain shared and reusable; workspace-local files remain workspace-local.
- `./$WORKSPACE$/*` is the documented home for workspace-local config/state.
- Any runtime install/mirror step is a materialization step, not the source of identity.
- Existing docs that imply runtime-derived identity are updated or flagged for migration.
- Session-boundary rebuilds still use `graphify update .`.

## implementation-brief

Implement the workspace identity transition in the smallest safe slice:

1. **Inventory current identity coupling**
   - Find files and docs that currently imply runtime-derived identity.
   - Classify them as shared bootstrap content, workspace-local state, or runtime install state.

2. **Define the workspace contract**
   - Specify what belongs in `./*` versus `./$WORKSPACE$/*`.
   - Define precedence: workspace `AGENTS.md` wins for identity; runtime metadata does not.

3. **Materialize workspace-local identity**
   - Ensure the target workspace contains its own `AGENTS.md`.
   - Keep that file independent from runtime configuration.

4. **Update bootstrap/install flow**
   - Materialize shared templates into the target workspace.
   - Do not let runtime config author the workspace identity.
   - Keep bootstrap behavior reproducible and explicit.

5. **Update validation and docs**
   - Validate that workspace identity exists and is local.
   - Update bootstrap docs, role docs, and handoff guidance that still describe runtime-derived identity.

6. **Preserve compatibility during rollout**
   - Keep temporary shims only as needed for transition.
   - Remove runtime-identity assumptions after the workspace model is verified.

## resolved-open-questions

- What is the identity source of truth?
  The workspace’s own `AGENTS.md`.

- Does runtime still matter?
  Yes, but only as execution context.

- Is `./$WORKSPACE$/*` bootstrap-owned?
  No. It is workspace-owned and target-local.

- Does this change the AST-only session rule?
  No.

## non-goals

- Changing product/domain architecture.
- Making runtime files the source of identity.
- Introducing a new semantic session-refresh policy.
- Moving every historical artifact in this phase.
- Reworking unrelated harness contracts.

## validation-expectations

- Workspace identity can be read from the target workspace `AGENTS.md` without consulting runtime metadata.
- Shared bootstrap files remain in the repo root model.
- Workspace-local files are isolated under `./$WORKSPACE$/*`.
- No session-boundary command changes from `graphify update .`.
- Rollout instructions are explicit enough for follow-up implementation without guesswork.

## routing

This brief is ready for comment collection in draft form, then promotion into the `proposed` lifecycle phase for implementation planning in the target workspace.

## Phase I:

### Discussion

#### VULCAN comments
- [260701:150224]: Artifact boundary concern — the implementation-brief section mixes ADR decision with execution planning. Per ADR convention (Context/Decision/Consequences), the implementation brief should be a separate downstream artifact. Keeping them together makes architecture review harder and creates ambiguity about what's being accepted.
- [260701:150224]: Step 1 (inventory current identity coupling) is the highest-risk step and needs explicit deliverables: categorized file list with runtime-derived, shared-bootstrap, or workspace-local classification. Without this inventory, steps 2-5 lack ground truth.
- [260701:150224]: Step 6 (preserve compatibility during rollout) — "temporary shims only as needed" is too vague. Recommend a defined compatibility window (X days or Y releases) or flag-gated rollover so old and new paths coexist during migration.
- [260701:150224]: Strongly agree with the core decision (workspace AGENTS.md as identity source). The runtime vs identity decoupling is architecturally correct.
- [260701:150224]: The resolved-open-questions section is well-structured and increases confidence in the proposal. Good practice.
