# ADR 20260701.150000: Workspace-local harness instantiation

## Status

historic

## Context

Project Koios is moving agents into their own workspaces. The transition goal is that each agent’s identity comes from its own `AGENTS.md`, not from the runtime that launches it.

This repo remains the shared bootstrap/config store. That means we need a clear boundary between:
- shared bootstrap assets in `./*`
- workspace-local agent state in `./$WORKSPACE$/*`
- runtime-installed tool state

This stage must also preserve two existing policies:
- the global/local asset split for committed vs local harness assets
- the AST-only session-boundary rebuild rule (`graphify update .`)

## Decision

1. Harness identity is sourced from the target workspace’s own `AGENTS.md`, not from the runtime.
2. Harness instantiation will be treated as workspace-local inside that target workspace.
3. Bootstrap-owned source remains shared in `./*`; durable workspace state lives in `./$WORKSPACE$/*` in the target workspace.
4. Workspace materialization will be explicit and reproducible, not an implicit side effect.
5. The workspace stage will not change the current asset split model unless a later ADR says so.
6. Session-boundary graph refresh stays AST-only.

## Consequences

- Per-agent workspaces become the authoritative place for local harness state.
- Bootstrap can still materialize templates, validators, and shared examples.
- Existing docs that imply shared ownership of workspace-local state will need revision.
- We need a follow-up implementation brief before any code or file-move rollout.

## architecture-spec

Not separately stated in the original archive ADR.

## acceptance-criteria

Not separately stated in the original archive ADR.

## implementation-brief

Not separately stated in the original archive ADR.

## resolved-open-questions

1. What exact workspace directory contract should `./$WORKSPACE$/*` follow for AGENTS, configs, and handoff artifacts?
2. Which files are local workspace state vs reusable bootstrap assets?
3. Should handoffs remain workspace-local only, or be projected back into bootstrap docs as provenance?
4. What compatibility window is needed for existing paths and workflows?

## non-goals

None stated.

## validation-expectations

Not separately stated in the original archive ADR.

## routing

Collect comments on this draft, then roll it into the `proposed` lifecycle phase with the implementation-ready workspace migration brief for the target workspace.

- Notes: Historic archived ADR normalized to the template; original text preserved below.

## links

- back_to: architecture.00
- supersedes: None
- superseded_by: None

---

## original

# ADR 20260701.150000: Workspace-local harness instantiation

## Status

historic

This draft is intentionally commentable before any move to the `proposed` lifecycle phase.

## Context

Project Koios is moving agents into their own workspaces. The transition goal is that each agent’s identity comes from its own `AGENTS.md`, not from the runtime that launches it.

This repo remains the shared bootstrap/config store. That means we need a clear boundary between:
- shared bootstrap assets in `./*`
- workspace-local agent state in `./$WORKSPACE$/*`
- runtime-installed tool state

This stage must also preserve two existing policies:
- the global/local asset split for committed vs local harness assets
- the AST-only session-boundary rebuild rule (`graphify update .`)

## Decision

1. Harness identity is sourced from the target workspace’s own `AGENTS.md`, not from the runtime.
2. Harness instantiation will be treated as workspace-local inside that target workspace.
3. Bootstrap-owned source remains shared in `./*`; durable workspace state lives in `./$WORKSPACE$/*` in the target workspace.
4. Workspace materialization will be explicit and reproducible, not an implicit side effect.
5. The workspace stage will not change the current asset split model unless a later ADR says so.
6. Session-boundary graph refresh stays AST-only.

## Consequences

- Per-agent workspaces become the authoritative place for local harness state.
- Bootstrap can still materialize templates, validators, and shared examples.
- Existing docs that imply shared ownership of workspace-local state will need revision.
- We need a follow-up implementation brief before any code or file-move rollout.

## Open questions

1. What exact workspace directory contract should `./$WORKSPACE$/*` follow for AGENTS, configs, and handoff artifacts?
2. Which files are local workspace state vs reusable bootstrap assets?
3. Should handoffs remain workspace-local only, or be projected back into bootstrap docs as provenance?
4. What compatibility window is needed for existing paths and workflows?

## Next step

Collect comments on this draft, then roll it into the `proposed` lifecycle phase with the implementation-ready workspace migration brief for the target workspace.

## Phase I:

### Discussion

#### VULCAN comments
- [260701:150224]: Decision point 5 ("will not change the current asset split model unless a later ADR says so") reads as a constraint guardrail rather than an active decision. Suggest demoting it to a note in Consequences so the 6 decision points read as 5 decisions + 1 invariant.
- [260701:150224]: Open question 1 (. $WORKSPACE$  directory contract) is the critical path blocker. Without a concrete naming convention and layout spec, this draft can't graduate to proposed. Recommend resolving before promotion.
- [260701:150224]: Open question 3 (handoff projection) — I'd argue handoffs should be projected as provenance (read-only archive), but tag this post-MVP so it doesn't block workspace materialization. First version keeps handoffs workspace-local.
- [260701:150224]: The Consequences line about existing docs needing revision is underspecified. Recommend adding a lightweight inventory of which docs are affected before proposed, or at minimum reference the docs/ tree.
